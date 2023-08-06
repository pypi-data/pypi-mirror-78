#import os 
#os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
import torch.nn as nn
import torch.nn.functional as F
import dgl.function as fn
from torch.autograd import Variable
import torch
import numpy as np 
import dgl
import math
  
class Aggregation_Module(nn.Module):

    def __init__(self, use_gating, use_attention, num_attention_heads, residual, num_nodes_types, num_bases, in_feat , out_feat , is_bias = True, activation = F.relu, norm = False, dropout = False, noisy = False):

        super(Aggregation_Module, self).__init__()   
        self.num_attention_heads = num_attention_heads
        self.residual = residual
        self.dropout = dropout
        self.noisy = noisy
        self.norm = norm
        self.use_gating = use_gating
        # HIDDEN
        self.in_feat = in_feat
        self.out_feat = out_feat
        self.num_nodes_types = num_nodes_types
        self.num_bases = num_bases
        self.is_bias = is_bias
        self.activation = activation
        self.use_attention = use_attention
        if self.num_bases <= 0 or self.num_bases > self.num_nodes_types:
            self.num_bases = self.num_nodes_types    


        if self.use_attention:
            
            # MAPPING FROM CONCATENATED MULTI-HEAD ATTENTION MECHANISMS RESULTS TO THE ORIGINAL EMBEDDING SIZE 
            self.weight_att_head_aggregation = nn.Parameter(torch.Tensor(self.num_bases, self.num_attention_heads*self.in_feat, self.in_feat))  
            nn.init.xavier_uniform_(self.weight_att_head_aggregation, gain=nn.init.calculate_gain('relu')) 
            if self.num_bases < self.num_nodes_types:
                self.w_comp_att_head_aggregation = nn.Parameter(torch.Tensor(self.num_nodes_types, self.num_bases))   
                nn.init.xavier_uniform_(self.w_comp_att_head_aggregation, gain=nn.init.calculate_gain('relu'))       
            if self.is_bias:
                self.bias_att_head_aggregation = nn.Parameter(torch.Tensor(self.num_nodes_types, self.out_feat))
                nn.init.uniform_(self.bias_att_head_aggregation)   
                # CREATE AND INIT WEIGHTS
                
            if self.noisy:
                self.weight_att_head_aggregation_sigma = nn.Parameter(torch.Tensor(self.num_nodes_types, self.num_attention_heads*self.in_feat,
                                                                               self.in_feat).fill_(0.017))
                #self.register_buffer("actor_epsilon_weight_prediction_output", torch.zeros(self.num_nodes_types, self.hidden_layers_size,
                                                                                 #self.actor_out_feat))
                std = math.sqrt(3 / self.num_attention_heads*self.in_feat)
                nn.init.uniform(self.weight_att_head_aggregation_sigma, -std, std)
                if self.is_bias:
                    self.bias_att_head_aggregation_sigma = nn.Parameter(torch.Tensor(self.num_nodes_types, 
                                                                                 self.in_feat).fill_(0.017))
                    #self.register_buffer("actor_epsilon_bias_prediction_output", torch.zeros(self.num_nodes_types, self.actor_out_feat))

                    nn.init.uniform(self.bias_att_head_aggregation_sigma, -std, std)
                    
        
        # RNN _ HIDDEN        
        if self.use_gating:
            # RNN - GRU
            """
            r=Ïƒ(Wirâ€‹x+bir+Whrâ€‹h+bhr)
            z=Ïƒ(Wizâ€‹x+biz+Whzâ€‹h+bhz)
            n=tanh(Winâ€‹x+bin+râˆ—(Whnâ€‹h+bhn))
            hâ€²=(1âˆ’z)âˆ—n+zâˆ—h
            """
            self.weight_input_aggregation = nn.Parameter(torch.Tensor(self.num_bases, self.in_feat, 3*self.out_feat))
            self.weight_hidden_aggregation = nn.Parameter(torch.Tensor(self.num_bases, self.out_feat, 3*self.out_feat))            
            nn.init.xavier_uniform_(self.weight_input_aggregation, gain=nn.init.calculate_gain('relu'))            
            nn.init.xavier_uniform_(self.weight_hidden_aggregation, gain=nn.init.calculate_gain('relu'))            


            if self.num_bases < self.num_nodes_types:            
                self.w_comp_input_aggregation = nn.Parameter(torch.Tensor(self.num_nodes_types, self.num_bases))
                self.w_comp_hidden_aggregation = nn.Parameter(torch.Tensor(self.num_nodes_types, self.num_bases))
                nn.init.xavier_uniform_(self.self.w_comp_input_aggregation, gain=nn.init.calculate_gain('relu'))            
                nn.init.xavier_uniform_(self.self.w_comp_hidden_aggregation, gain=nn.init.calculate_gain('relu'))                

            if self.is_bias:
                self.bias_input_aggregation = nn.Parameter(torch.Tensor(self.num_nodes_types, 3*self.out_feat))
                self.bias_hidden_aggregation = nn.Parameter(torch.Tensor(self.num_nodes_types, 3*self.out_feat))
                nn.init.uniform_(self.bias_input_aggregation)   
                nn.init.uniform_(self.bias_hidden_aggregation)   
                
                
            if self.noisy:
                self.weight_input_aggregation_sigma = nn.Parameter(torch.Tensor(self.num_nodes_types, self.in_feat, 3*self.out_feat).fill_(0.017))
                std = math.sqrt(3 / self.in_feat)
                nn.init.uniform(self.weight_input_aggregation_sigma, -std, std)
                if self.is_bias:
                    self.bias_input_aggregation_sigma = nn.Parameter(torch.Tensor(self.num_nodes_types, 
                                                                                 3*self.out_feat).fill_(0.017))
                    nn.init.uniform(self.bias_input_aggregation, -std, std)
                    
                    
                self.weight_hidden_aggregation_sigma = nn.Parameter(torch.Tensor(self.num_nodes_types, self.out_feat, 3*self.out_feat).fill_(0.017))
                #self.register_buffer("actor_epsilon_weight_prediction_output", torch.zeros(self.num_nodes_types, self.hidden_layers_size,
                                                                                 #self.actor_out_feat))
                std = math.sqrt(3 / self.out_feat)
                nn.init.uniform(self.weight_hidden_aggregation_sigma, -std, std)
                if self.is_bias:
                    self.bias_hidden_aggregation_sigma = nn.Parameter(torch.Tensor(self.num_nodes_types, 
                                                                                 3*self.out_feat).fill_(0.017))
                    #self.register_buffer("actor_epsilon_bias_prediction_output", torch.zeros(self.num_nodes_types, self.actor_out_feat))

                    nn.init.uniform(self.bias_hidden_aggregation, -std, std)
                    
                    

    def message_func(self, edges):
        pass
    def reduce_func(self, nodes):
        pass
    def apply_func(self, nodes):
        #return {'agg_msg': self.activation(nodes.data['agg_msg'])}
        agg_msg = self.activation(nodes.data['agg_msg'])

        if self.use_attention:

            # MAPPING FROM CONCATENATED RESULTS OF MULTIPLE ATTENTION HEAD MECHANISMS TO ORIGINAL EMBEDDING DIM
            if self.num_bases < self.num_nodes_types:
                weight_att_head_aggregation = self.weight_att_head_aggregation.view(self.num_attention_heads * self.in_feat, self.num_bases, self.in_feat) 
                weight_att_head_aggregation = torch.matmul(self.w_comp_att_head_aggregation, weight_att_head_aggregation).view(self.num_nodes_types, self.num_attention_heads * self.in_feat, self.in_feat)  
            else:
                weight_att_head_aggregation = self.weight_att_head_aggregation 

                
            #print('w node', weight_att_head_aggregation.size())
            #print('max node index', nodes.data['node_type'].max())
            weight_att_head_aggregation = weight_att_head_aggregation[nodes.data['node_type']].to(self.device)
            bias_att_head_aggregation = self.bias_att_head_aggregation[nodes.data['node_type']].to(self.device)
            
            if self.noisy:
                e_w = torch.cuda.FloatTensor(self.weight_att_head_aggregation_sigma[nodes.data['node_type']].size()).normal_()                        
                weight_att_head_aggregation += self.weight_att_head_aggregation_sigma[nodes.data['node_type']] * Variable(e_w).to(self.device)
                if self.is_bias:
                    e_b = torch.cuda.FloatTensor(self.bias_att_head_aggregation_sigma[nodes.data['node_type']].size()).normal_()                            
                    #e_b = torch.randn(self.actor_epsilon_bias_prediction_output[nodes.data['node_type']].size())
                    bias_att_head_aggregation += self.bias_att_head_aggregation_sigma[nodes.data['node_type']] * Variable(e_b).to(self.device)            
            
            
            agg_msg = agg_msg.view(-1,self.num_attention_heads*self.in_feat)
            agg_msg = torch.bmm(agg_msg.unsqueeze(1), weight_att_head_aggregation).squeeze()
            if self.is_bias:
                agg_msg = agg_msg + bias_att_head_aggregation
            agg_msg = self.activation(agg_msg)            
            if self.dropout :
                agg_msg = torch.nn.functional.dropout(agg_msg, p=0.5, training=True, inplace=False) 


        if self.use_gating:


            # FORWARD UNIQUE
            if self.num_bases < self.num_nodes_types:

                weight_input_aggregation = self.weight_input_aggregation.view(self.in_feat, self.num_bases, self.out_feat)#.to("cuda")     
                weight_input_aggregation = torch.matmul(self.w_comp_input_aggregation, weight_input_aggregation_).view(self.num_nodes_types,
                                                            self.in_feat, 3*self.out_feat)#.to("cuda")     

                weight_hidden_aggregation = self.weight_hidden_aggregation.view(self.out_feat, self.num_bases, self.out_feat)#.to("cuda")     
                weight_hidden_aggregation = torch.matmul(self.w_comp_hidden_aggregation, weight_hidden_aggregation_).view(self.num_nodes_types,
                                                            self.out_feat, 3*self.out_feat)#.to("cuda")

            else:
                weight_input_aggregation = self.weight_input_aggregation     
                weight_hidden_aggregation = self.weight_hidden_aggregation



            w_input_aggregation = weight_input_aggregation[nodes.data['node_type']].to(self.device)#.to("cuda")   
            w_hidden_aggregation = weight_hidden_aggregation[nodes.data['node_type']].to(self.device)

            if self.is_bias:
                bias_input_aggregation = self.bias_input_aggregation[nodes.data['node_type']].to(self.device)
                bias_hidden_aggregation = self.bias_hidden_aggregation[nodes.data['node_type']].to(self.device)
                
                
                
                
            if self.noisy:
                #print('AGGREGATION NOISY')
                
                #print('weight_base', self.weight_input_aggregation_sigma.size())
                #print('weight',  w_input_aggregation.size())
                #print('node_type',nodes.data['node_type'])
                if 'cuda' in self.device:
                    e_w = torch.cuda.FloatTensor(self.weight_input_aggregation_sigma[nodes.data['node_type']].size()).normal_()
                else:
                    e_w = torch.FloatTensor(self.weight_input_aggregation_sigma[nodes.data['node_type']].size()).normal_() 
                    
                #print('ew', e_w.size())
                #print('used weight', self.weight_input_aggregation_sigma[nodes.data['node_type']].size())
                w_input_aggregation += self.weight_input_aggregation_sigma[nodes.data['node_type']] * Variable(e_w).to(self.device)
                if 'cuda' in self.device:
                    e_w = torch.cuda.FloatTensor(self.weight_hidden_aggregation_sigma[nodes.data['node_type']].size()).normal_()
                else:
                    e_w = torch.FloatTensor(self.weight_hidden_aggregation_sigma[nodes.data['node_type']].size()).normal_()                   
                w_hidden_aggregation += self.weight_hidden_aggregation_sigma[nodes.data['node_type']] * Variable(e_w).to(self.device)
                
                if self.is_bias:
                    if 'cuda' in self.device:
                        e_b = torch.cuda.FloatTensor(self.bias_input_aggregation_sigma[nodes.data['node_type']].size()).normal_()
                    else:
                        e_b = torch.FloatTensor(self.bias_input_aggregation_sigma[nodes.data['node_type']].size()).normal_()                   
                    bias_input_aggregation += self.bias_input_aggregation_sigma[nodes.data['node_type']] * Variable(e_b).to(self.device)            
                    if 'cuda' in self.device:
                        e_b = torch.cuda.FloatTensor(self.bias_hidden_aggregation_sigma[nodes.data['node_type']].size()).normal_()
                    else:
                        e_b = torch.FloatTensor(self.bias_hidden_aggregation_sigma[nodes.data['node_type']].size()).normal_()                   
                    bias_hidden_aggregation += self.bias_hidden_aggregation_sigma[nodes.data['node_type']] * Variable(e_b).to(self.device)                
                
                

            gate_x = torch.bmm(agg_msg.to(self.device).unsqueeze(1), w_input_aggregation).squeeze()
            gate_h = torch.bmm(nodes.data['hid'].to(self.device).unsqueeze(1), w_hidden_aggregation).squeeze()

            if self.is_bias:
                gate_x += bias_input_aggregation
                gate_h += bias_hidden_aggregation

            i_r, i_i, i_n = gate_x.chunk(3, 1)
            h_r, h_i, h_n = gate_h.chunk(3, 1)                

            resetgate = torch.sigmoid(i_r + h_r)
            inputgate = torch.sigmoid(i_i + h_i)
            newgate = torch.tanh(i_n + (resetgate * h_n))

            if self.residual:
                hy = nodes.data['hid'].to(self.device) + (newgate + inputgate * (nodes.data['hid'].to(self.device) - newgate))    
            else:
                hy = newgate + inputgate * (nodes.data['hid'].to(self.device) - newgate)    

        else:
            hy = agg_msg

            
            
        #print('END AGG')
        #print('hy.size()', hy.size())
        return {'hid' : hy}      


    def aggregate(self, graph, device):
        self.device = device
        graph.update_all(message_func = self.message_func, reduce_func = self.reduce_func, apply_node_func = self.apply_func)             



    
