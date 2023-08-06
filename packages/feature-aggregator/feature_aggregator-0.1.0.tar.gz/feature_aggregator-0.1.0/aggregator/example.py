import os
import sys
from utils.Aggregator import Aggregator
import torch

# DEFINE RELATIONSHIPS (LINKS) BETWEEN TABLES 
population = [('train.csv','offers.csv','offer'),
              ('train.csv','transactions.csv','id')]

# INSTANCIATE THE MAIN RELATIONAL-TREE STRUCTURE
aggregator = Aggregator(parent = 'train.csv', 
                        links = population, 
                        parent_id = 'id', 
                        target_variables = ['repeater'],
                        no_link_symbol = 0,
                        bidirectional = True,
                        self_loop = True)



# DEFINING FINAL MLP(s) TO BE USED ON THE EMBEDDING OF THE FINAL 'SOURCE/AGGREGATION' NODE REPRESENTATION/EMBEDDING
prediction_modules = []
prediction_modules.append(['repeater', [32,32,32], 2])


# DEFINING THE GCN/GGREGATION ARCHITECTURE
aggregator.create_model(prediction_modules = prediction_modules,
                        message_hidden_layers = [], 
                        request_hidden_layers = [], 
                        attention_hidden_layers = [],
                        query_hidden_layers = [], 
                        key_hidden_layers = [], 
                        q_size = None,
                        use_attention = True,
                        attention_type = 'normal_src_dst',                    
                        std_attention = True, 
                        node_embedding_size = 2, 
                        attention_heads = 2,
                        norm = False,
                        bidir = False,
                        self_loop = False,
                        full_graph_computation=False)
                

# TRAINING THE AGGREGATOR (END TO END LEARNING WITH THE FINAL MLP(s))
aggregator.train(predicted_variables = [['repeater', 'classification',1]],
                 n_epochs = 1e9, 
                 graphs_folder = 'no_bidir/graph/', 
                 results_folder = 'exp2', 
                 alias = '12_normal_no_agg_corrected_new_fx_1e-3',
                 lr = 1e-3, 
                 weighted = 0.27,
                 batch_size = 64,
                 expand_factor = 500,
                 accumulation_steps = 1,
                 save_frequency = 100, 
                 test_frequency = 10, 
                 nb_batch_test = 10,
                 device = 'cuda:0' if torch.cuda.is_available() else 'cpu',
                 tensorboard_port = 6006)

