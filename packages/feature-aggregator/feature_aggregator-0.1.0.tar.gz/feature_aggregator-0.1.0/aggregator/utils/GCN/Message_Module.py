import torch.nn as nn
import torch.nn.functional as F
import torch
import numpy as np 
import dgl
from torch.autograd import Variable
import sys
import math
import collections

torch.autograd.set_detect_anomaly(True)

class Message_Module(nn.Module):
    def __init__(self, num_attention_heads, data, use_attention, attention_type, std_attention, residual, num_rels, num_bases, inp_node_state_dim, outp_node_state_dim, in_feat , node_embedding_dim, out_feat , message_hidden_layers = [], request_hidden_layers = [], attention_hidden_layers = [], query_hidden_layers = [], key_hidden_layers = [], q_size = 32, is_bias = True, activation = F.relu, norm = True, dropout = False, noisy = False):
        super(Message_Module, self).__init__()    
        self.q_size = q_size
        self.num_attention_heads = num_attention_heads
        self.data = data
        self.inp_node_state_dim = inp_node_state_dim
        self.outp_node_state_dim = outp_node_state_dim
        self.node_embedding_dim = node_embedding_dim
        self.use_attention = use_attention
        self.std_attention = std_attention
        self.residual = residual
        self.dropout = dropout
        self.noisy = noisy
        self.norm = norm
        self.in_feat = in_feat
        self.out_feat = out_feat
        self.num_rels = num_rels
        self.num_bases = num_bases
        self.is_bias = is_bias
        self.activation = activation
        self.module_elems = collections.OrderedDict()
        self.attention_type = attention_type
        self.message_weights = nn.ParameterList()
        self.message_w_comps = nn.ParameterList()
        self.message_biases = nn.ParameterList()
        self.message_weights_sigma = nn.ParameterList()
        self.message_biases_sigma = nn.ParameterList()
        self.module_elems['message'] = [self.message_weights, self.message_w_comps, self.message_biases, self.message_weights_sigma, self.message_biases_sigma, [self.in_feat] + message_hidden_layers + [self.out_feat]]
        att_size = 0
        if 'src' in self.attention_type.lower():
            att_size +=1
        if self.use_attention:
            if 'dst' in self.attention_type.lower():
                att_size +=1
                self.request_weights = nn.ParameterList()
                self.request_w_comps = nn.ParameterList()
                self.request_biases = nn.ParameterList()
                self.request_weights_sigma = nn.ParameterList()
                self.request_biases_sigma = nn.ParameterList()
                self.module_elems['request'] = [self.request_weights, self.request_w_comps, self.request_biases, self.request_weights_sigma, self.request_biases_sigma, [self.in_feat] + request_hidden_layers + [self.out_feat]]
            if 'dot_product' in self.attention_type.lower():
                self.query_weights = nn.ParameterList()
                self.query_w_comps = nn.ParameterList()
                self.query_biases = nn.ParameterList()
                self.query_weights_sigma = nn.ParameterList()
                self.query_biases_sigma = nn.ParameterList()
                self.module_elems['query'] = [self.query_weights, self.query_w_comps, self.query_biases, self.query_weights_sigma, self.query_biases_sigma, [self.out_feat] + query_hidden_layers + [self.num_attention_heads*self.q_size]]
                self.key_weights = nn.ParameterList()
                self.key_w_comps = nn.ParameterList()
                self.key_biases = nn.ParameterList()
                self.key_weights_sigma = nn.ParameterList()
                self.key_biases_sigma = nn.ParameterList()
                self.module_elems['key'] = [self.key_weights, self.key_w_comps, self.key_biases, self.key_weights_sigma, self.key_biases_sigma, [self.out_feat] + key_hidden_layers + [self.num_attention_heads*self.q_size]]                
                
            else:
                self.attention_weights = nn.ParameterList()
                self.attention_w_comps = nn.ParameterList()
                self.attention_biases = nn.ParameterList()
                self.attention_weights_sigma = nn.ParameterList()
                self.attention_biases_sigma = nn.ParameterList()
                self.module_elems['attention'] = [self.attention_weights, self.attention_w_comps, self.attention_biases, self.attention_weights_sigma, self.attention_biases_sigma, [att_size*self.out_feat] + attention_hidden_layers + [self.num_attention_heads*1]]
            
        if self.num_bases <= 0 or self.num_bases > self.num_rels:
            self.num_bases = self.num_rels    

        for module_elems in self.module_elems.values():
            w_list, w_comp_list, b_list, w_list_sigma, b_list_sigma, dims = module_elems
            for in_feat, out_feat in zip(dims[:-1],dims[1:]):
                weight = nn.Parameter(torch.Tensor(self.num_bases, in_feat, out_feat))
                nn.init.xavier_uniform_(weight,
                                        gain=nn.init.calculate_gain('relu'))
                w_list.append(weight)
                if self.num_bases < self.num_rels:
                    w_comp = nn.Parameter(torch.Tensor(self.num_rels, self.num_bases))
                    nn.init.xavier_uniform_(w_comp,
                                            gain=nn.init.calculate_gain('relu'))  
                    w_comp_list.append(w_comp)
                if self.is_bias:
                    bias = nn.Parameter(torch.Tensor(self.num_rels, out_feat))                
                    nn.init.uniform_(bias)  
                    b_list.append(bias)
                    


                if self.noisy:
                    weight_sigma = nn.Parameter(torch.Tensor(self.num_rels, in_feat,
                                                                                   out_feat).fill_(0.017))
                    #self.register_buffer("actor_epsilon_weight_prediction_output", torch.zeros(self.num_nodes_types, self.hidden_layers_size,
                                                                                     #self.actor_out_feat))
                    std = math.sqrt(3 / in_feat)
                    nn.init.uniform(weight_sigma, -std, std)
                    w_list_sigma.append(weight_sigma)
                    if self.is_bias:
                        bias_sigma = nn.Parameter(torch.Tensor(self.num_rels, 
                                                                                     out_feat).fill_(0.017))
                        #self.register_buffer("actor_epsilon_bias_prediction_output", torch.zeros(self.num_nodes_types, self.actor_out_feat))

                        nn.init.uniform(bias_sigma, -std, std)
                        b_list_sigma.append(bias_sigma)

                    
    def compute(self, value, w_list, w_comp_list, b_list, w_list_sigma, b_list_sigma, dims, edges):

        for idx, (in_feat, out_feat) in enumerate(zip(dims[:-1],dims[1:])):
            
            
            
            #print('w edges', w_list[idx].size())
            #print('max edge index', edges.data['edge_type'].max())
            
            
            if self.num_bases < self.num_rels:
                weight = w_list[idx].view(in_feat, self.num_bases, out_feat)   
                weight = torch.matmul(w_comp_list[idx], weight).view(self.num_rels,
                                                            in_feat, out_feat)
                
                

            else:
                weight = w_list[idx]
            w = weight[edges.data['edge_type']].to(self.device)  
            bias = b_list[idx][edges.data['edge_type']].to(self.device)

            
            if self.noisy:
                #print('MESSAGE NOISY')
                #print('w_list_sigma', w_list_sigma.size(), 'edge_type', w_list_sigma[edges.data['edge_type']])
                if 'cuda' in self.device:
                    e_w = torch.cuda.FloatTensor(w_list_sigma[idx][edges.data['edge_type']].size()).normal_()     
                else:
                    e_w = torch.FloatTensor(w_list_sigma[idx][edges.data['edge_type']].size()).normal_()                     
                w += w_list_sigma[idx][edges.data['edge_type']] * Variable(e_w).to(self.device)
                if self.is_bias:
                    if 'cuda' in self.device:
                        e_b = torch.cuda.FloatTensor(b_list_sigma[idx][edges.data['edge_type']].size()).normal_() 
                    else:
                        e_b = torch.FloatTensor(b_list_sigma[idx][edges.data['edge_type']].size()).normal_()                         
                    #e_b = torch.randn(self.actor_epsilon_bias_prediction_output[nodes.data['node_type']].size())
                    bias += b_list_sigma[idx][edges.data['edge_type']] * Variable(e_b).to(self.device)            
            
            
            
            
            value = torch.bmm((torch.cat(value,1) if type(value)==tuple else value).unsqueeze(1), w).view(-1,out_feat)
            if self.is_bias:
                value = value + bias
            if self.dropout :
                value = torch.nn.functional.dropout(value, p=0.5, training=True, inplace=False) 
            if idx < (len(w_list) - 1) :
                value = self.activation(value)
        
        return value

    def message_func(self, edges):
        for module, module_elems in self.module_elems.items():
            w_list, w_comp_list, b_list, w_list_sigma, b_list_sigma, dims = module_elems
            
            if module == 'message':
                #print('message')
                msg = self.compute(tuple(edges.src[var][:,:(self.inp_node_state_dim if var =='state' else self.node_embedding_dim)].to(self.device) for var in self.data), w_list, w_comp_list, b_list, w_list_sigma, b_list_sigma, dims, edges)
            elif module == 'request':
                #print('request')
                rqst = self.compute(tuple(edges.dst[var][:,:(self.outp_node_state_dim if var =='state' else self.node_embedding_dim)].to(self.device) for var in self.data), w_list, w_comp_list, b_list, w_list_sigma, b_list_sigma, dims, edges)
            elif module == 'attention':
                #print('attention')
                if 'src' in self.attention_type.lower() and 'dst' in self.attention_type.lower():
                    #print('att_src_dst')
                    att = self.compute(tuple((msg,rqst)), w_list, w_comp_list, b_list, w_list_sigma, b_list_sigma, dims, edges)
                elif 'src' in self.attention_type.lower():
                    #print('att_src')
                    att = self.compute(msg, w_list, w_comp_list, b_list, w_list_sigma, b_list_sigma, dims, edges)
                elif 'dst' in self.attention_type.lower():
                    #print('att_dst')
                    att = self.compute(rqst, w_list, w_comp_list, b_list, w_list_sigma, b_list_sigma, dims, edges)
            elif module == 'query':
                if 'dst' in self.attention_type.lower():
                    qry = self.compute(rqst, w_list, w_comp_list, b_list, w_list_sigma, b_list_sigma, dims, edges).view(-1, 1, self.q_size)                
                else:
                    qry = self.compute(msg, w_list, w_comp_list, b_list, w_list_sigma, b_list_sigma, dims, edges).view(-1, 1, self.q_size)
            elif module == 'key':
                #print('key')
                key = self.compute(msg, w_list, w_comp_list, b_list, w_list_sigma, b_list_sigma, dims, edges).view(-1, 1, self.q_size)

                
        if self.norm:
            print("NORM NOT YET IMPLEMENTED")
            #msg = msg / edges.dst['norm'].to(self.device).gather(dim = 1, index = edges.data['edge_type'].to(self.device).view(-1,1)).detach()
        if self.use_attention:
            if 'dot_product' in self.attention_type.lower():
                att = (torch.bmm(qry,key.transpose(1,2))/math.sqrt(self.q_size)).view(-1,self.num_attention_heads)
            return {'msg': msg, 'att' :att}   
        else:
            return {'msg' : msg}

    def reduce_func(self, nodes):
        # AGGREGATION OF ATTENTION 
        # REDUCE FUNCTION BATCHES NODES OF SAME IN-DEGREES TOGETHER 
        if self.use_attention : 
            if self.std_attention:
                att_w = F.softmax(nodes.mailbox['att'],dim=1).transpose(1,2)
            else:
                att_w = nodes.mailbox['att'].transpose(1,2)
            mailbox = nodes.mailbox['msg']
            agg_msg = torch.bmm(att_w, mailbox)
        else:
            agg_msg = torch.sum(nodes.mailbox['msg'], dim = 1)
        return {'agg_msg' : agg_msg}

    def apply_func(self, nodes):
        pass

    def propagate(self, graph, device):
        self.device = device
        graph.update_all(message_func = self.message_func, reduce_func = self.reduce_func, apply_node_func = self.apply_func)     


        
        
