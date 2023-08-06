#import os 
#os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
#import dgl.function as fn
import torch
import numpy as np 
import dgl
import math

            
class Prediction_Module(nn.Module):

    def __init__(self, final_hidden_layers, num_nodes_types, num_bases, in_feat , out_feat , is_bias = True, activation = F.relu, dropout = False, noisy= False):
        super(Prediction_Module, self).__init__() 
        self.dropout = dropout
        self.noisy = noisy
        self.in_feat = in_feat
        self.out_feat = out_feat   
        self.num_nodes_types = num_nodes_types
        self.num_bases = num_bases
        self.is_bias = is_bias
        self.activation = activation
        self.prediction_weights = nn.ParameterList()  
        self.prediction_w_comps = nn.ParameterList()   
        self.prediction_biases = nn.ParameterList()  
        if self.noisy:
            self.prediction_weights_sigma = nn.ParameterList()    
            self.prediction_biases_sigma = nn.ParameterList()              
        
        if self.num_bases <= 0 or self.num_bases > self.num_nodes_types:
            self.num_bases = self.num_nodes_types
            
        self.dims = [self.in_feat] + final_hidden_layers + [self.out_feat]
        
        for in_feat, out_feat in zip(self.dims[:-1],self.dims[1:]):
            weight_prediction = nn.Parameter(torch.Tensor(self.num_bases, in_feat,
                                                    out_feat), )
            nn.init.xavier_uniform_(weight_prediction,
                                    gain=nn.init.calculate_gain('relu'))
            self.prediction_weights.append(weight_prediction)
            if self.num_bases < self.num_nodes_types:
                w_comp = nn.Parameter(torch.Tensor(self.num_nodes_types, self.num_bases))
                nn.init.xavier_uniform_(w_comp,
                                        gain=nn.init.calculate_gain('relu')) 
                self.prediction_w_comps.append(weight_prediction)
                
            if self.is_bias:
                bias_prediction = nn.Parameter(torch.Tensor(self.num_nodes_types, out_feat))               
                nn.init.uniform_(bias_prediction) 
                self.prediction_biases.append(bias_prediction)
                
                
            if self.noisy:
                weight_sigma = nn.Parameter(torch.Tensor(self.num_nodes_types, in_feat,
                                                                               out_feat).fill_(0.017))
                #self.register_buffer("actor_epsilon_weight_prediction_output", torch.zeros(self.num_nodes_types, self.hidden_layers_size,
                                                                                 #self.actor_out_feat))
                std = math.sqrt(3 / in_feat)
                nn.init.uniform(weight_sigma, -std, std)
                self.prediction_weights_sigma.append(weight_sigma)
                if self.is_bias:
                    bias_sigma = nn.Parameter(torch.Tensor(self.num_nodes_types, 
                                                                                 out_feat).fill_(0.017))
                    #self.register_buffer("actor_epsilon_bias_prediction_output", torch.zeros(self.num_nodes_types, self.actor_out_feat))

                    nn.init.uniform(bias_sigma, -std, std)
                    self.prediction_biases_sigma.append(bias_sigma)
                    
                    
    def predict(self, nodes):
        #print('START PRED ')
        value = nodes.data['hid']
        for idx, (in_feat, out_feat) in enumerate(zip(self.dims[:-1],self.dims[1:])):
            if self.num_bases < self.num_nodes_types:
                weight_prediction = self.prediction_weights[idx].view(in_feat, self.num_bases, out_feat)#.to("cuda")     
                weight_prediction = torch.matmul(self.prediction_w_comps[idx], weight_prediction).view(self.num_nodes_types,
                                                            in_feat, out_feat)#.to("cuda")     
            else:
                weight_prediction = self.prediction_weights[idx]#.to("cuda")    

                
            #print('weight_prediction', weight_prediction.size())
            #print('node_type', nodes.data['node_type'])
            w_prediction = weight_prediction[nodes.data['node_type']].to(self.device)#.to("cuda")   
            bias_prediction = self.prediction_biases[idx][nodes.data['node_type']].to(self.device)
            

            #print("DEVICE", self.device)
            if self.noisy:
                #print('PREDICTION NOISY')
                if 'cuda' in self.device:
                    e_w = torch.cuda.FloatTensor(self.prediction_weights_sigma[idx][nodes.data['node_type']].size()).normal_()
                else:
                    e_w = torch.FloatTensor(self.prediction_weights_sigma[idx][nodes.data['node_type']].size()).normal_()
                w_prediction += self.prediction_weights_sigma[idx][nodes.data['node_type']] * Variable(e_w).to(self.device)
                if self.is_bias:
                    if 'cuda' in self.device:
                        e_b = torch.cuda.FloatTensor(self.prediction_biases_sigma[idx][nodes.data['node_type']].size()).normal_()
                    else:
                        e_b = torch.FloatTensor(self.prediction_biases_sigma[idx][nodes.data['node_type']].size()).normal_()
                    #e_b = torch.randn(self.actor_epsilon_bias_prediction_output[nodes.data['node_type']].size())
                    bias_prediction += self.prediction_biases_sigma[idx][nodes.data['node_type']] * Variable(e_b).to(self.device)            
            
            value = torch.bmm(value.unsqueeze(1), w_prediction).view(-1, out_feat)
            if self.is_bias:
                value = value + bias_prediction
            if self.dropout:
                value = torch.nn.functional.dropout(value, p=0.5, training=True, inplace=False)       

        return {'predictions' : value}
        #pred = pred.view(-1,self.out_feat)
        #return pred
    
    
    
    
    
    
