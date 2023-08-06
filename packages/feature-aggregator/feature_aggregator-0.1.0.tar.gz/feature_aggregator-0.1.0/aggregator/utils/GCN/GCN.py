import os 
#os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
import torch.nn as nn
import torch.nn.functional as F
import dgl.function as fn
import torch
import numpy as np 
import dgl
from functools import partial
from utils.functions import *
from torch.autograd import Variable
import copy
from IPython.display import clear_output
import glob
import atexit
import time
import traceback
from utils.GCN.Message_Module import Message_Module
from utils.GCN.Aggregation_Module import Aggregation_Module
from utils.GCN.Prediction_Module import Prediction_Module

	
class Convolutional_Message_Passing_Framework(nn.Module):
    def __init__(self, num_attention_heads, state_first_dim_only, use_gating, use_attention, attention_type, std_attention, n_convolutional_layers, num_nodes_types, nodes_types_num_bases, node_state_dim, node_embedding_dim, num_rels, prediction_modules, message_hidden_layers = [], request_hidden_layers = [], attention_hidden_layers = [], query_hidden_layers = [], key_hidden_layers = [], q_size = 32, num_propagations = 1, rel_num_bases = -1, norm = True, is_bias = True, activation = F.elu, dropout = False, residual = False, noisy = False, bidir = False, self_loop = False, full_graph_computation = False, layer_modifier = 0):
        """
        use_attention : if True, attention element-wise attention mechanisms are used to weight messages4
        std_attention : if True, attention coefficients corresponding to messages of the same type leading to the same node will be normalized to sum up to one
        n_convolutional_layers : number of layers with different parameters we want to use.
        prediction_modules : a list of final neural networks to use for predictions. Every element needs to be a list including : the name of the corresponding prediction, the architecture of the corresponding NN (a list of hidden layers), and the size of the prediction (output_dim)
        final_hidden_layers : a list defining the size of every hidden layers to be included in the final mapping (neural network) linking the final embedding of the target node to the prediction  (for instance, [64 ,128] would lead to the creation of a 1st hidden layer of 64 neurons and a second hidden layer of 128 neurons)
        num_nodes_types : number of different types of nodes which exist in the studied graphs 
        nodes_types_num_bases : if < 0 no basis decomposition is used for the nodes parameters (Gating/GRU). If > 0 there will be as many bases for node parameters as indicated (up to a maximum of 'num_nodes_types')
        node_state_dim : the size of the complete node representation (state_size + embedding_size)
        node_embedding_dim : the size of the node embedding (computed representation)
        num_rels : number of different types of edges which exist in the studied graphs
        rel_num_bases : if < 0 no basis decomposition is used for the edges parameters (message/request/attention). If > 0 there will be as many bases for edges parameters as indicated (up to a maximum of 'num_rels')
        num_propagations : default number of propagations which are performed ON EVERY DIFFERENT LAYER during a forward pass if no 'num_propagations' argument is passed to the forward function.
        norm : if True and attention is not used, messages are averaged 
        is_bias : if True, a bias will be included with every layer (message/request/attention/GRU/prediction...)
        activation: The activation function which will be used to add non linearity in the architecture
        dropout : if True, dropout will be used with the specified probability ( not yet properly implemented )
        residual : if True, a residual connection is added between the previous embedding of a node and its new embedding (ie. the aggregation module only has to learn to output the relevant difference between the previous and new embedding)
        """        
        super(Convolutional_Message_Passing_Framework, self).__init__() 
        self.bidir = bidir
        self.full_graph_computation = full_graph_computation
        self.noisy = noisy
        self.num_attention_heads = num_attention_heads
        self.state_first_dim_only = state_first_dim_only
        self.use_gating = use_gating
        self.use_attention = use_attention
        self.std_attention = std_attention
        self.n_convolutional_layers = n_convolutional_layers
        self.num_nodes_types = num_nodes_types 
        #self.num_node_embedding_types = num_node_embedding_types
        self.nodes_types_num_bases = nodes_types_num_bases
        self.node_state_dim = node_state_dim
        self.node_embedding_dim = node_embedding_dim
        self.num_rels = num_rels
        self.num_propagations = num_propagations
        self.rel_num_bases = rel_num_bases
        self.norm = norm 
        self.is_bias = is_bias 
        self.layer_modifier = layer_modifier
        self.activation = activation
        self.dropout = dropout
        self.residual = residual 
        self.conv_layers = nn.ModuleList()
        self.pred_mods = prediction_modules
        self.prediction_modules = nn.ModuleDict()
        
        self.layer_filter = '(graph.edata["layer"] == layer_idx)'
        self.to_parent_filter = '(graph.edata["edge_meta_type"] == 0)'
        self.to_child_filter = '(graph.edata["edge_meta_type"] == 1)'
        self.loop_filter = '(graph.edata["edge_meta_type"] == 2)'
        
        self.final_filter = '(' + self.to_parent_filter + ((' | ' + self.to_child_filter) if bidir else '') + ((' | ' + self.loop_filter) if self_loop else '') + ')' + ((' & ' + self.layer_filter) if not full_graph_computation else '')
        
        #blocks_state_dims.reverse()
        #print(blocks_state_dims)
        #self.blocks_state_dims = blocks_state_dims
        
        #self.node_embeddings = nn.Parameter(torch.Tensor(self.num_node_embedding_types, self.node_embedding_dim))

        for i in range(self.n_convolutional_layers):
            #conv = Relational_Message_Passing_Framework(num_attention_heads, self.state_first_dim_only, self.n_convolutional_layers, True if i == 0 else False, use_gating, use_attention, attention_type, std_attention, num_nodes_types, nodes_types_num_bases, blocks_state_dims[i], blocks_state_dims[i+1], node_embedding_dim, num_rels, message_hidden_layers = message_hidden_layers, request_hidden_layers = request_hidden_layers, attention_hidden_layers = attention_hidden_layers, query_hidden_layers = query_hidden_layers, key_hidden_layers = key_hidden_layers, q_size = q_size, num_propagations = num_propagations, rel_num_bases = rel_num_bases, norm = norm, is_bias = is_bias, activation = activation, dropout = dropout, residual = residual, noisy = noisy)
            
            conv = Relational_Message_Passing_Framework(num_attention_heads, self.state_first_dim_only, self.n_convolutional_layers, True if i == 0 else False, use_gating, use_attention, attention_type, std_attention, num_nodes_types, nodes_types_num_bases, inp_node_state_dim = self.node_state_dim, outp_node_state_dim = self.node_state_dim, node_embedding_dim = node_embedding_dim, num_rels = num_rels, message_hidden_layers = message_hidden_layers, request_hidden_layers = request_hidden_layers, attention_hidden_layers = attention_hidden_layers, query_hidden_layers = query_hidden_layers, key_hidden_layers = key_hidden_layers, q_size = q_size, num_propagations = num_propagations, rel_num_bases = rel_num_bases, norm = norm, is_bias = is_bias, activation = activation, dropout = dropout, residual = residual, noisy = noisy)
            self.conv_layers.append(conv)
            
        for module_name, hidden_layers, output_size in prediction_modules :
            prediction_module = Prediction_Module(hidden_layers , self.num_nodes_types, self.nodes_types_num_bases, in_feat = self.node_embedding_dim, out_feat = output_size, is_bias = is_bias, activation = activation, dropout = dropout, noisy = noisy)
            self.prediction_modules[module_name] = prediction_module
            
            
       
    def forward(self, graph, source_nodes, device, identifier, noise = False): 

        self.to(device)
        for layer in self.conv_layers:
            for module in layer.mods.values():
                module.device = device
                module.to(device)
        for p_module in self.prediction_modules.values():
            p_module.device = device
            p_module.to(device)
            
        #for data in graph.ndata.values():
            #data = data.to(device)
        #print('self.node_embeddings', self.node_embeddings.size())
        #print('max embedding_type', graph.ndata['embedding_type'].max())
        #try:
            #self.node_embeddings.to(device)[graph.ndata['embedding_type'].to(device)]
        #except:
            #print('embedding weight sizes', self.node_embeddings.size())
            #print('embedding types', graph.ndata['embedding_type'])
            
        
        #graph.ndata['state'] = torch.cat((graph.ndata['state'].to(device), self.node_embeddings.to(device)[graph.ndata['embedding_type'].to(device)]),1)
        if self.use_gating:
            graph.ndata['hid'] = torch.zeros((graph.number_of_nodes(), self.node_embedding_dim )).to(device)
        #graph.ndata['hid'] = self.node_embeddings[graph.ndata['embedding_type'].to(device)]
        if self.layer_modifier !=0:
            graph.edata['layer'] -= self.layer_modifier
        
        for layer_idx, layer in enumerate(self.conv_layers):
            #print('layer_idx', layer_idx)
            #print('graph.edata["edge_meta_type"]', graph.edata['edge_meta_type'].max(), graph.edata['edge_meta_type'])
            # GET RIGHT EDGES (for current layer)
            #print('edata layer',  graph.edata['layer'].max(), graph.edata['layer'])
            #print('self.final_filter', self.final_filter)
            eids = torch.nonzero(eval(self.final_filter)).squeeze().tolist()
            #print('eids', eids)
            #print('eids', eids)
            #if not eids:
                #print('no edge of valid type found in layer :', layer_idx)
                #continue
            for prop_idx in range(self.num_propagations):
            # PROPAGATE ALONG THE GIVEN LAYER
                graph.send_and_recv(eids, 
                                     message_func=layer.mods['message_module'].message_func, 
                                     reduce_func=layer.mods['message_module'].reduce_func, 
                                     apply_node_func=layer.mods['aggregation_module'].apply_func, 
                                     inplace=True)
                
       
        # GET FINAL SOURCE NODES EMBEDDINGS
        #print('pre filt')
        
        new_filt = partial(filt, identifier = identifier)
        final_subgraph = graph.subgraph(list(graph.filter_nodes(new_filt)))
        #final_subgraph = graph.subgraph(source_nodes)
        final_subgraph.copy_from_parent()

        
        # PROPAGATE THROUGH PREDICTION MODULE(S)
        results = {}
        #results['hid'] = final_subgraph.ndata['hid']
        #print('nb_final_nodes', final_subgraph.number_of_nodes())
        #print('hid size', final_subgraph.ndata['hid'].size())
        for module_name, prediction_module in self.prediction_modules.items():
            final_subgraph.apply_nodes(func=prediction_module.predict, v='__ALL__', inplace=True)
            results[module_name] = final_subgraph.ndata['predictions']
            
        #RETURN
        return results
 
    
class Relational_Message_Passing_Framework(nn.Module):
    def __init__(self, num_attention_heads, state_first_dim_only, n_convolutional_layers, is_first_layer, use_gating, use_attention, attention_type, std_attention, num_nodes_types, nodes_types_num_bases, inp_node_state_dim, outp_node_state_dim, node_embedding_dim, num_rels, message_hidden_layers = [], request_hidden_layers = [], attention_hidden_layers = [], query_hidden_layers = [], key_hidden_layers = [], q_size = 32, num_propagations = 1, rel_num_bases = -1, norm = True, is_bias = True, activation = F.elu, dropout = False, residual = False, noisy = False):
        
        
        super(Relational_Message_Passing_Framework, self).__init__()
        self.is_first_layer = is_first_layer
        self.state_first_dim_only = state_first_dim_only
        self.n_convolutional_layers = n_convolutional_layers
        self.num_nodes_types = num_nodes_types
        self.nodes_types_num_bases = nodes_types_num_bases
        self.inp_node_state_dim = inp_node_state_dim        
        self.outp_node_state_dim = outp_node_state_dim
        self.node_embedding_dim = node_embedding_dim
        self.norm = norm
        self.num_propagations = num_propagations 
        self.mods = nn.ModuleDict()
        self.num_rels = num_rels
        self.rel_num_bases = rel_num_bases
        self.is_bias = is_bias
        self.activation = activation
        

        data = [] 
        in_feat=0
        if self.is_first_layer :
            in_feat += self.inp_node_state_dim
            data.append('state')
        else:
            if not self.state_first_dim_only:
                in_feat += self.inp_node_state_dim
                data.append('state')
                
            in_feat += self.node_embedding_dim
            data.append('hid')            
                

        self.mods['message_module'] = Message_Module(num_attention_heads, data, use_attention, attention_type, std_attention, residual, self.num_rels, self.rel_num_bases, inp_node_state_dim = self.inp_node_state_dim, outp_node_state_dim = self.outp_node_state_dim, in_feat = in_feat, node_embedding_dim = self.node_embedding_dim,  out_feat = self.node_embedding_dim, message_hidden_layers = message_hidden_layers, request_hidden_layers = request_hidden_layers, attention_hidden_layers = attention_hidden_layers, query_hidden_layers = query_hidden_layers, key_hidden_layers = key_hidden_layers, q_size = q_size, is_bias = is_bias, activation = F.elu, norm = norm, dropout = dropout, noisy = noisy)
        self.mods['aggregation_module'] = Aggregation_Module(use_gating, use_attention, num_attention_heads, residual, self.num_nodes_types, self.nodes_types_num_bases, in_feat = self.node_embedding_dim, out_feat = self.node_embedding_dim, is_bias = is_bias, activation = F.elu, norm = False, dropout = dropout, noisy = noisy)
