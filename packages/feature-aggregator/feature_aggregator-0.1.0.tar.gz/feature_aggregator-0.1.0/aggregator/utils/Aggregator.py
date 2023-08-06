import time 
import collections
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import psutil
import sys
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import glob
import dgl
import collections
import networkx as nx
from pathos.helpers import mp as multiprocessing
from datetime import datetime, date
import pickle
import re
from tensorboardX import SummaryWriter
from utils.GCN.GCN import Convolutional_Message_Passing_Framework
from utils.graph_iterator import graph_iterator
import csv
import statistics
import copy
import math
from utils.functions import *


def Merge(dict1, dict2): 
    dict2.update(dict1)
    return dict2


class Aggregator():
    def __init__(self, parent, links, parent_id, target_variables = None, no_link_symbol = 'N/A', bidirectional = False, self_loop = False):
        self.self_loop = self_loop
        self.no_link_symbol = no_link_symbol
        self.links = copy.deepcopy(links)
        self.bidirectional = bidirectional
        self.nodes = []
        for l in links:
            self.nodes.extend(list(l[:2]))
        self.nodes = set(self.nodes)
        self.tables = self.nodes
        #self.nodes = None
        self.main_id = parent_id
        self.main = parent
        self.target_variables = target_variables
        self.n_nodes = len(self.nodes)
        self.n_rels = (2 if bidirectional else 1)*len(links)+(len(self.nodes) if self_loop else 0)
        self.tree_dict = collections.OrderedDict()
        self.tree_dict[parent] = collections.OrderedDict()
        self.dataframes = collections.OrderedDict()
        self.nodes_types = collections.OrderedDict()
        self.nodes_types[parent] = 0
        # edge type of self_loop
        self.rel_type_self = collections.OrderedDict()
        # initiate tree dictionary for root node
        self.tree_dict[parent]['key'] = parent_id
        self.tree_dict[parent]['node_type'] = 0
        self.rel_counter=0
        self.rel_depth = {}
        if self.self_loop:
            self.tree_dict[parent]['rel_type_self'] = self.rel_counter
            self.rel_type_self[parent] = self.rel_counter
            self.rel_depth[self.rel_counter] = 0
            self.rel_counter+=1 
        if self.bidirectional:
            self.tree_dict[parent]['rel_type_from_parent'] = None
        self.tree_dict[parent]['rel_type_to_parent'] = None
        self.tree_dict[parent]['parent'] = None
        self.tree_dict[parent]['depth'] = 0
        # read columns names for root node table
        self.tree_dict[parent]['col'] = list(pd.read_csv(parent,index_col=0,nrows=1).columns)
        self.node_counter = 1
        
        # recrusively build tree dictionary for all nodes
        self.tree_dict[parent]['children'] = self.tree_dict_creation(parent, links)
        
        # relation depths from the root node
        self.rel_depth = {k: (max(self.rel_depth.values()) - v) for (k,v) in self.rel_depth.items()}
        # list of max dimensions in each level of the tree
        self.max_dims = []
        self.tree_dict = self.max_dimension()  
        # maximum dimensions among all the tables
        self.max_dim = max(self.max_dims)
        print('max dimension for each layer:',self.max_dims)
        self.print_tree_dict()
 
        
    def tree_dict_creation(self, parent_name, links, depth = 0):
        """Create a dictionaries in a tree structure for all nodes
        Start from the root node table,the node name is the key of the
        dictionary, value is also a dictionary of the items for all 
        necessary structual information. Leaf nodes are saved in the
        value of the key: ['child']. Tree dictionary is built 
        recursively until reach the leaf nodes.

        Parameters
        ----------
        parent_name : string
            The name of the root table
        links: list of tuples
            list of the tuples indicating the linked tables
        depth : int
            Initial depth of the root node.

        Returns
        -------
        dic: ordered dictionary
            The tree structured dictionary that contains all the tables
        """         
        depth +=1
        dic = collections.OrderedDict()
        childrens = []
        for link in links.copy():
            # find parent node name
            if link[0] == parent_name:
                link_idx = links.index(link)
                childrens.append((link[1], link[2]))
                links.pop(link_idx)
        if childrens:
            # create dictionary for each child node
            for child_name, key in childrens:
                dic[child_name] = collections.OrderedDict()
                dic[child_name]['depth'] = depth
                dic[child_name]['parent']=parent_name
                dic[child_name]['key'] = key
                dic[child_name]['rel_type_to_parent'] = self.rel_counter
                self.rel_depth[self.rel_counter]=depth-1
                self.rel_counter+=1
                if self.bidirectional:
                    dic[child_name]['rel_type_from_parent'] = self.rel_counter
                    self.rel_depth[self.rel_counter] = depth
                    self.rel_counter+=1
                if child_name not in self.rel_type_self:
                    self.rel_type_self[child_name] = self.rel_counter
                    if self.self_loop:
                        dic[child_name]['rel_type_self'] = self.rel_counter
                        self.rel_depth[self.rel_counter] = depth
                        self.rel_counter+=1
                    dic[child_name]['node_type'] = self.node_counter                    
                    self.nodes_types[child_name] = self.node_counter
                    self.node_counter+=1   
                else:
                    if self.self_loop:
                        dic[child_name]['rel_type_self'] = self.rel_type_self[child_name]
                    dic[child_name]['node_type'] = self.nodes_types[child_name]
                dic[child_name]['col']=list(pd.read_csv(child_name,index_col=0,nrows=1).columns)
                # child node becomes the parent so that to continue 
                # search for their childres to build dictionary
                dic[child_name]['children'] = self.tree_dict_creation(child_name,links, depth)
        return dic    
    
    
    def print_tree_dict(self, parent = None, children_dic = None, depth = -1):
        """Print the tree dictionary structure to check the structure 
        of the tree with printing the information in different depths.
        """  
        if children_dic == None:
            children_dic = self.tree_dict
        depth+=1 
        print(' '*5*depth,"DEPTH : ", depth)
        print("PARENT", parent)
        for child, values in children_dic.items():
            for grandchild in values['children'].values():
                print("key", grandchild['key'])
            print(' '*5*values['depth'],'CHILD :', child,' | ' ,'DEPTH :', values['depth'],' | ' ,  'CHILD-CHILDRENS :', [child for child in values['children']],' | ' , 
                  'NODE TYPE :', values['node_type'],' | ' ,
                  'rel_type_to parent :', values['rel_type_to_parent'],' | ',
                  'KEY_TO_PARENT :', values['key'])
            if self.bidirectional:
                print(' '*5*values['depth'], 'rel_type_from_parent :', values['rel_type_from_parent'])
            if self.self_loop:
                print(' '*5*values['depth'], 'rel_type_self :', values['rel_type_self'])
            self.print_tree_dict(child, values['children'], depth)
            
      
    def max_dimension(self, parent=None, children_dic=None, max_dim=0): 
        """ Remove id columns in the 'col' of the dictionaries.
        Get the maximum dimensions in each depth of the tree
        to decide the initial embedding demension for the graph
        """
        if children_dic == None:
            children_dic = self.tree_dict
            if self.target_variables is not None:
                for var in self.target_variables:
                    children_dic[self.main]['col'].remove(var)
                for link in self.links:
                    # remove id/key column to its children
                    if self.main in link and link[2] in children_dic[self.main]['col']:
                        # remove id column from 'col'
                        children_dic[self.main]['col'].remove(link[2])
                # dimension of the main table / root node
                dim = len(children_dic[self.main]['col'])
                # append to the list
                self.max_dims.append(dim) 
                
        # FIND MAX DIMENSIONS FOR EACH LEVEL OF THE TREE            
        for child, values in children_dic.items():
            for link in self.links:
                # if dataframe in links and id column in 'col'
                if child in link and link[2] in values['col']:
                    # remove id column from 'col'
                    values['col'].remove(link[2])  
            dim = len(values['col'])
            if len(self.max_dims)<(values['depth']+1):
                self.max_dims.append(dim)
            elif dim > self.max_dims[values['depth']]:
                self.max_dims[values['depth']] = dim
            _ = self.max_dimension(child, values['children'],max_dim)
            
        # RETURN
        return children_dic     
    
            
    def create_linkage(self,children_dic = None): 
        """ Find the linkage for each observations among all
        tables and save the linkage chain of the each id in an
        ordered-dictionary.
        """  
        if children_dic == None:
            print('\n')
            print('creating linkage idx among tables...')
            print('\n')            
            my_dic = self.tree_dict
            children_dic = my_dic[self.main]['children'] 
        # create dictionary for each table
        for child, values in children_dic.items(): 
            # save ach id value of its parent id column as a key with 
            # empty list as the value 
            values['link_dict'] = collections.OrderedDict({key:[] for key in self.dataframes[values['parent']][values['key']].values.tolist()})
            # iterate the series through id column in the child 
            # table, append each row idx to the dictionary values with its 
            # corresponding key value 
            for idx, k in self.dataframes[child][values['key']].iteritems():        
                if k not in values['link_dict']:
                    values['link_dict'][k] = [ ]
                values['link_dict'][k].append(idx)
            # recursively until reach the leave nodes
            self.create_linkage(values['children'])
            
            
    def read_tables(self):
        self.dataframes = collections.OrderedDict()
        # read all tables
        print('Reading files....')
        s = time.time()
        for table in self.tables:
            self.dataframes[table] = pd.read_csv(table)
            print(table,'Done! | ',self.mem())
        print ('Reading Files Done!, used time: ',time.time()-s)

        
    def create_graph(self, main_id, main_idx):
        """ Create a graph for the observation 
        
        Parameters
        ----------
        main_id : string
            The element provided by the queue to the worker 
            so it can create the graph based on the ID (main 
            table) of the current observation.
        main_idx: row index of the given main id in main table

        Returns 
        -------
        [graph, labels]: list
            a list where first element is the created graph, 
            second element is the label of the observation
        """
        # initiate the graph
        graph = dgl.DGLGraph()
        graph.adresses_in_graph = collections.OrderedDict()
        graph.adresses_in_db = collections.OrderedDict()
        graph.counter = 0
        graph.src = []
        graph.dst = []
        graph.data = []
        graph.tp = []
        graph.edge_meta_type = []
        graph.norm = []
        graph.node_type = []
        graph.nb_ch_types = []
        graph.edge_layers = []
        
        # create node for the main id
        # unique id for main node, id is the string that consists
        # of the main table name and the row index
        graph.adresses_in_graph[str(self.main)+str(main_idx)] = graph.counter
        graph.adresses_in_db[graph.counter]= str(self.main)+str(main_idx)
        graph.node_type.append(self.tree_dict[self.main]['node_type'])
        

        cols = self.tree_dict[self.main]['col']
        main = self.dataframes[self.main]
        parent_id = self.tree_dict[self.main]['key']
        
        # add initial embedding for root node
        node_data = main.loc[main[parent_id]==main_id][cols].iloc[0].to_list()       
        node_data += [0]*(self.max_dim-len(node_data))
        graph.data.append(node_data)
        graph.counter += 1
        graph.norm.append([0]*self.n_rels)

        # Add self loop and edge type
        if self.self_loop:
            graph.src.append(graph.adresses_in_graph[str(self.main)+str(main_idx)])
            graph.dst.append(graph.adresses_in_graph[str(self.main)+str(main_idx)])
            graph.tp.append(self.tree_dict[self.main]['rel_type_self'])
            graph.edge_meta_type.append(2)
            graph.edge_layers.append(self.rel_depth[self.tree_dict[self.main]['rel_type_self']])
            graph.norm[graph.adresses_in_graph[str(self.main)+str(main_idx)]][self.tree_dict[self.main]['rel_type_self']] +=1
        
        graph.nb_ch_types.append(len(self.tree_dict[self.main]['children'].keys()) + (1 if self.self_loop else 0))
        # recursively create node for the all children nodes
        # until reach the leaf node   
        self.iterate_graph(main_idx,graph) 

        num_nodes = graph.counter
        graph.add_nodes(num_nodes)  
        # convert to tensor
        node_type = torch.LongTensor(graph.node_type).squeeze()        
        src = torch.LongTensor(graph.src)
        dst = torch.LongTensor(graph.dst)
        edge_type = torch.LongTensor(graph.tp)
        edge_meta_type = torch.LongTensor(graph.edge_meta_type)
        nb_ch_types = torch.LongTensor(graph.nb_ch_types).squeeze()
        edge_norm = torch.FloatTensor(graph.norm).squeeze()
        embeddings = torch.FloatTensor(graph.data)  
        edge_layers = torch.LongTensor(graph.edge_layers)
        #print(len(src),len(dst))
        graph.add_edges(src,dst)

        # update graph data
        graph.edata.update({'edge_type': edge_type, 'layer': edge_layers, 'edge_meta_type':edge_meta_type})        
        graph.ndata.update({'state': embeddings, 'nb_ch_types' : nb_ch_types, 'node_type' : node_type, 'norm' : torch.LongTensor(graph.norm)}) 
        
        # add labels as dictionary
        if self.target_variables is not None:
            labels = {}
            for var in self.target_variables:
                labels[var] = self.dataframes[self.main][var][main_idx]
        else:
            labels = None
            
        def message_func(edges):
            edges.data['norm'] = ( edges.dst['norm'].gather(1, edges.data['edge_type'].view(-1,1)) ).squeeze()
            edges.data['weight'] = 1/(edges.data['norm']*edges.dst['nb_ch_types'].type(torch.float))

        def reduce_func(nodes):
            pass
        def apply_func(nodes):
            pass

        graph.update_all(message_func = message_func, reduce_func = reduce_func, apply_node_func = apply_func)     
        
        return [graph, labels]


    def iterate_graph(self,parent_idx,graph,children_dic = None):
        """ Add nodes and edges to the given root node/parent id, 
        recursively until add all the linked nodes.
        """
        # At first children dictionary is the 'children' for the
        # main table /root node.
        if children_dic == None:
            my_dic = self.tree_dict
            children_dic = my_dic[self.main]['children'] 

        for child, values in children_dic.items(): 
            # find the value of the key column in parent table
            key_value = self.dataframes[values['parent']][values['key']][parent_idx]

            # unique name for the node
            parent_node_name = str(values['parent']) +str(parent_idx)
            
            # only search for child node if the value in the key column is valid
            if str(key_value) != str(self.no_link_symbol):
                for child_idx in values['link_dict'][key_value]:
                    node_name = str(child)+str(child_idx)
                    if node_name not in graph.adresses_in_graph:
                        # add new node 
                        graph.adresses_in_graph[node_name] = graph.counter
                        graph.adresses_in_db[graph.counter]= node_name
                        graph.node_type.append(values['node_type'])
                        graph.nb_ch_types.append(len(values['children'].keys())+ (1 if self.self_loop else 0))
                        graph.norm.append([0]*self.n_rels)

                        #add embedding
                        node_data = self.dataframes[child][child_idx:child_idx+1][values['col']].values.tolist()[0]
                        node_data += [0]*(self.max_dim-len(node_data))
                        graph.data.append(node_data)
                        graph.counter += 1

                        # Add self loop             
                        if self.self_loop:
                            graph.src.append(graph.adresses_in_graph[node_name])
                            graph.dst.append(graph.adresses_in_graph[node_name])
                            graph.tp.append(values['rel_type_self'])
                            graph.edge_meta_type.append(2)
                            graph.edge_layers.append(self.rel_depth[values['rel_type_self']])
                            graph.norm[graph.adresses_in_graph[node_name]][values['rel_type_self']] +=1

                    if self.bidirectional:
                        # Add edge from parent
                        graph.src.append(graph.adresses_in_graph[parent_node_name]) ## main ID
                        graph.dst.append(graph.adresses_in_graph[node_name])
                        graph.tp.append(values['rel_type_from_parent']) 
                        graph.edge_meta_type.append(1)
                        graph.edge_layers.append(self.rel_depth[values['rel_type_from_parent']])
                        graph.norm[graph.adresses_in_graph[node_name]][values['rel_type_from_parent']] +=1

                    # Add edge to parent
                    graph.src.append(graph.adresses_in_graph[node_name])
                    graph.dst.append(graph.adresses_in_graph[parent_node_name])
                    graph.tp.append(values['rel_type_to_parent']) 
                    graph.edge_meta_type.append(0)
                    graph.edge_layers.append(self.rel_depth[values['rel_type_to_parent']])
                    graph.norm[graph.adresses_in_graph[parent_node_name]][values['rel_type_to_parent']] +=1

                    # recursively add children node for the current child node
                    self.iterate_graph(child_idx,graph,values['children'])                         
        return graph
        
    
    def print_graph(self,graph):
        nx_G = graph.to_networkx()
        pos = nx.kamada_kawai_layout(nx_G)
        #print(graph.ndata)
        print(self.nodes_types)
        #print(self.nodes_types.values())
        f = plt.figure()
        nx.draw(nx_G, pos, with_labels=False, node_color=list(graph.ndata['node_type']))
        f.savefig("graph.png")
        #nx.draw(nx_G, pos, with_labels=False, node_color=list(graph.ndata['node_type']))

        
    def create_all_graphs(self, folder = os.getcwd(), n_workers = 1, nb_graphs_per_file = 10, train_percentage = 0.8, predict = False):
        """ Create graphs for all observations using multiple processes. 
        Split and save graphs into `train` and `test` folders.

        Parameters
        ----------
        folder : string
            The path want to save the graphs
        n_workers: int
            number of the processes want to use
        nb_graphs_per_file : int
            number of the garphs we want to save per file
        train_percentage: float
            the percetage of the observations want to use for train, the 
            rest will be used for validation       
        predict: bool
            if we use the model only to make prediction. When it equals 
            to `True`, it will override the argument `nu_graphs_per_file` 
            to become 1. All graphs will be saved into `prediction` folder.
        """  
        self.predict = predict
        self.train_percentage = train_percentage  
        if self.predict:
            self.train_percentage = 1
        self.setup_folders(folder)
        self.read_tables() # read all tables
        # find linkage among tables for all observations
        self.create_linkage() 
        self.n_workers = n_workers 
        self.manager = multiprocessing.Manager()
        #Create queue for id, train_counter, test_counter
        self.queues = []
        self.id_queue = self.manager.Queue()
        self.train_queue = self.manager.Queue()
        self.test_queue = self.manager.Queue()
        self.predict_queue = self.manager.Queue()
        self.nb_graphs_per_file = nb_graphs_per_file
        # put IDs and counters into the queue
        self.get_Queue(self.main_id,self.main,self.train_percentage,self.nb_graphs_per_file,shuffle=True)  

        # CREATE PROCESSES (TASKS)
        process_list=[]
        for worker_idx in range(self.n_workers):
            process_list.append(multiprocessing.Process(target = self.worker, 
                                    args =(worker_idx,)))

        # LAUNCH / INITIATE THE TASKS
        for worker_process in process_list:
            worker_process.start()

        for worker_process in process_list:
            worker_process.join()
                                  
        # RESTRUCTURE FILES TO INSURE SIZES ARE CORRECT 
        if self.predict:
            # RESTRUCTURE FOR PREDICTION FILES
            dic = collections.OrderedDict()
            counter = 0
            for idx, filename in enumerate(glob.glob(self.path_predict + '/*')):
                with open(filename,'rb') as  f:
                    new_dic = pickle.load(f)
                os.system('rm '+ filename + ' > /dev/null 2>&1')
                l = len(new_dic)
                difference = self.nb_graphs_per_file - len(dic)
                dic.update(list(new_dic.items())[:min(difference,l)])
                if l>=difference:
                    p=open(self.path_predict+"/" + str(counter),'wb')
                    pickle.dump(dic,p)
                    print('predict file counter :', counter, ' | number of graphs : ', len(dic))
                    p.close()       
                    counter+=1
                    dic = collections.OrderedDict()
                    if l>difference:
                        dic.update(list(new_dic.items())[difference:])
                else:
                    dic.update(list(new_dic.items())[:])    

            if dic:
                p=open(self.path_predict+"/" + str(counter),'wb')
                pickle.dump(dic,p)
                print('predict file counter :', counter, ' | number of graphs : ', len(dic))
                p.close()     

        else:
            # RESTRUCTURE FOR TRAIN FILES
            dic = collections.OrderedDict()
            counter = 0            
            for idx, filename in enumerate(glob.glob(self.path_train + '/*')) :
                with open(filename,'rb') as  f:
                    new_dic = pickle.load(f)
                os.system('rm '+ filename + ' > /dev/null 2>&1')
                l = len(new_dic)
                difference = self.nb_graphs_per_file - len(dic)
                dic.update(list(new_dic.items())[:min(difference,l)])
                if l >= difference:
                    p = open(self.path_train + "/" + str(counter),'wb')
                    pickle.dump(dic,p)
                    print('train file counter :', counter, ' | number of graphs : ', len(dic))
                    p.close()       
                    counter += 1
                    dic = collections.OrderedDict()
                    if l > difference:
                        dic.update(list(new_dic.items())[difference:])
                else:
                    dic.update(list(new_dic.items())[:])

            if dic:
                p = open(self.path_train + "/" + str(counter),'wb')
                pickle.dump(dic,p)
                print('train file counter :', counter, ' | number of graphs : ', len(dic))
                p.close()  
                
            # RESTRUCTURE FOR TEST FILES
            dic = collections.OrderedDict()
            counter = 0
            for idx, filename in enumerate(glob.glob(self.path_test + '/*')):
                with open(filename,'rb') as  f:
                    new_dic = pickle.load(f)
                os.system('rm '+ filename + ' > /dev/null 2>&1')
                l = len(new_dic)
                difference = self.nb_graphs_per_file - len(dic)
                dic.update(list(new_dic.items())[:min(difference,l)])
                if l>=difference:
                    p=open(self.path_test+"/" + str(counter),'wb')
                    pickle.dump(dic,p)
                    print('test file counter :', counter, ' | number of graphs : ', len(dic))
                    p.close()       
                    counter+=1
                    dic = collections.OrderedDict()
                    if l>difference:
                        dic.update(list(new_dic.items())[difference:])
                else:
                    dic.update(list(new_dic.items())[:])    

            if dic:
                p=open(self.path_test+"/" + str(counter),'wb')
                pickle.dump(dic,p)
                print('test file counter :', counter, ' | number of graphs : ', len(dic))
                p.close()   
        print("\n")
        print("Finished")
            
        
    def worker(self, worker_idx):
        start = datetime.now()
        # create dictionary for adding graphs later
        graphs = collections.OrderedDict()  
        train_graphs = collections.OrderedDict()
        test_graphs = collections.OrderedDict()
        train_counter = 0
        test_counter = 0
        while True:
            # get index and id from the TRAIN queue until it's empty
            main_idx, main_id = self.train_queue.get()
            if main_idx == 'done':
                break
            if main_idx % 400 == 0:
                print('idx:',main_idx, datetime.now() - start)
                
            # *** CREATE GRAPH FOR TRAIN OBSERVATIONS ***
            train_graphs[main_id]  = self.create_graph(main_id, main_idx)   
            if len(train_graphs)>= self.nb_graphs_per_file:  
                # save the dictionary of graphs
                print('dumping graphs...|',self.mem())
                
                if self.predict:
                    # save the graphs to `predict` folder 
                    p=open(self.path+"graph/predict/predict_graph_%s"%(train_counter*self.n_workers+worker_idx) + '_' + str(len(train_graphs)),'wb')
                else:
                    p=open(self.path+"graph/train/train_graph_%s"%(train_counter*self.n_workers+worker_idx) + '_' + str(len(train_graphs)),'wb')
                pickle.dump(train_graphs,p)
                p.close()         
                train_graphs=collections.OrderedDict()   
                train_counter+=1
                                           
        # save grpahs when there is no more observations in the queue 
        if train_graphs: 
            if self.predict:   
                p=open(self.path+"graph/predict/predict_graph_%s"%(train_counter*self.n_workers+worker_idx) + '_' + str(len(train_graphs)),'wb') 
            else: 
                p=open(self.path+"graph/train/train_graph_%s"%(train_counter*self.n_workers+worker_idx) + '_' + str(len(train_graphs)),'wb')
            print('dumping graphs...| number of the graphs:', len(train_graphs),'idx:',main_idx)
            pickle.dump(train_graphs,p)
            p.close()         
            train_graphs=collections.OrderedDict()   
            train_counter+=1             
                
        while True:
            # get index and id from the TEST queue until it's empty
            main_idx, main_id = self.test_queue.get()
            if main_idx == 'done':
                break
            if main_idx % 400 == 0:
                print('idx:',main_idx, datetime.now() - start)   
            # *** CREATE GRAPHS FOR FOR TEST OBSERVATIONS ***
            test_graphs[main_id]  = self.create_graph(main_id, main_idx)  

            if len(test_graphs)>= self.nb_graphs_per_file:  
                # SAVE FILE AS PICKLE OBJECT
                print('dumping graphs..|',self.mem())
                p=open(self.path+"graph/test/test_graph_%s"%(test_counter*self.n_workers+worker_idx) + '_' + str(len(test_graphs)),'wb')
                pickle.dump(test_graphs,p)
                p.close()         
                test_graphs=collections.OrderedDict()   
                test_counter+=1

        if test_graphs: #checks if not empty 
                p=open(self.path+"graph/test/test_graph_%s"%(test_counter*self.n_workers+worker_idx) + '_' + str(len(test_graphs)),'wb')
                print('dumping graphs... | number of the graphs:', len(test_graphs))
                pickle.dump(test_graphs,p)
                p.close()         
                test_graphs=collections.OrderedDict()   
                test_counter+=1            

 
    def get_Queue(self,ID,main,train_percentage,number_id_per_file,shuffle=True): 
        ID_list = pd.read_csv(main,usecols = [ID])[ID] #get the series
        print('number of ids:', len(set(ID_list)))
        if shuffle == True:
            self.ID_list = ID_list.sample(frac=1, random_state=2020)
        self.n_obs = len(self.ID_list)
        self.n_workers = min(self.n_workers, self.n_obs, multiprocessing.cpu_count()-1)

        # PUT ELEMENTS INTO THE QUEUES
        for i, (idx,main_id) in enumerate(ID_list.items()):
            if i <= int(len(ID_list)*self.train_percentage)-1 or self.predict:
                self.train_queue.put([idx,main_id]) 
            else:
                self.test_queue.put([idx,main_id])
                
        # PUT ENDING SIGNAL INTO THE QUEUES                        
        for _ in range(self.n_workers):
            self.train_queue.put(['done', 'done'])
            self.test_queue.put(['done', 'done'])
            
    
    def setup_folders(self, path=os.getcwd()): 
        #create folder under the path to save train and test graphs
        self.path = path + '/'       
        if self.predict:
            self.path_predict = path+'/'+'graph/predict'  
            os.system('rm -r ' +str(self.path_predict))    
            if not os.path.exists(self.path_predict):
                # create predict folder
                os.system('mkdir -p '+ self.path_predict)
        else:
            # create train and test path
            self.path_train = path+'/'+'graph/train' 
            self.path_test = path+'/'+'graph/test'
            os.system('rm -r ' +str(self.path_train))
            os.system('rm -r '  +str(self.path_test))          
            if not os.path.exists(self.path_train):
                # create train folder
                os.system('mkdir -p '+ self.path_train)
            if not os.path.exists(self.path_test):
                # create test folder
                os.system('mkdir -p '+ self.path_test)           
           
        
    def create_model(self, prediction_modules, message_hidden_layers = [], request_hidden_layers = [], attention_hidden_layers = [], query_hidden_layers = [], key_hidden_layers = [], q_size = 32, use_attention = True, use_gating = False, attention_type = 'normal', std_attention = True, node_embedding_size = 32, attention_heads = 5, norm = True, bidir = False, self_loop = False, full_graph_computation = False, residual = False, created_bidir = True, created_self_loop = True):
        self.node_embedding_size = node_embedding_size
        self.initial_embedding_dim = self.max_dim
        self.node_embedding_size = node_embedding_size
        self.n_rels = (2 if created_bidir else 1)*len(self.links)+(len(self.nodes) if created_self_loop else 0)
        self.n_used_rels = (2 if bidir else 1)*len(self.links)+(len(self.nodes) if self_loop else 0)
        self.use_attention = use_attention
        self.norm = norm 
        self.q_size = q_size
        self.std_attention = std_attention 
        self.attention_heads = attention_heads
        adjustment = 1 if (bidir or self_loop) else 0
        n_convolutional_layers = (len(self.max_dims)-1) + adjustment
        print('n_layers', n_convolutional_layers)
        self.model = Convolutional_Message_Passing_Framework(
                         num_attention_heads = attention_heads, 
                         state_first_dim_only = False, 
                         use_gating = use_gating,
                         use_attention = use_attention,  
                         attention_type = attention_type,
                         std_attention = std_attention, 
                         n_convolutional_layers = n_convolutional_layers, 
                         prediction_modules = prediction_modules,
                         num_nodes_types = self.n_nodes, 
                         nodes_types_num_bases = -1, 
                         node_state_dim = self.initial_embedding_dim, 
                         node_embedding_dim = self.node_embedding_size, 
                         num_rels = self.n_rels, 
                         message_hidden_layers = message_hidden_layers, 
                         request_hidden_layers = request_hidden_layers, 
                         attention_hidden_layers = attention_hidden_layers, 
                         query_hidden_layers = query_hidden_layers,
                         key_hidden_layers = key_hidden_layers, 
                         q_size = q_size,
                         rel_num_bases = -1, 
                         norm = norm, 
                         is_bias = True, 
                         activation = F.elu, 
                         dropout = False, 
                         residual = residual,
                         bidir = bidir,
                         self_loop = self_loop,
                         full_graph_computation = full_graph_computation,
                         layer_modifier = 0 if (bidir or self_loop) else 1
                         )
        
        


    def train(self, predicted_variables, n_epochs, graphs_folder, results_folder, alias, lr = 1e-3, weighted = None, batch_size = 32, expand_factor = None, accumulation_steps = 1, save_frequency = 100, test_frequency = 10, nb_batch_test = 1, device = 'cuda' if torch.cuda.is_available() else 'cpu', tensorboard_port = 6006):
        self.expand_factor = expand_factor
        # CREATE FOLDERS TO SAVE THE RESULTS
        os.system('mkdir -p ' + results_folder)
        self.path_results = results_folder + '/results/'
        os.system('mkdir -p ' + results_folder + '/results/' + alias + '/')
        self.path_saved_model = results_folder + '/saved_model'
        os.system('mkdir -p ' + results_folder + '/saved_model/' + alias + '/')
        self.device = device
        self.batch_size = batch_size
        self.model.train()
        self.model.to(device)
        os.system('rm -r ' + str(self.path_results) + alias + '/')
        self.predicted_variables = predicted_variables
        self.n_epochs = n_epochs
        self.results_folder = results_folder 
        self.graph_folder = graphs_folder
        self.alias = alias
        os.system('mkdir ' + str(self.path_results))
        self.lr = lr
        self.accumulation_steps = accumulation_steps
        # weighted loss
        self.weighted = weighted
        self.save_frequency = save_frequency 
        self.test_frequency = test_frequency 
        self.nb_batch_test = nb_batch_test
        self.device = device 
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)
        for layer in self.model.conv_layers:
            for module in layer.mods.values():
                module.device = device
        for p_module in self.model.prediction_modules.values():
            p_module.device = device
        self.counter = 0
        self.train_counter = 0
        self.test_counter = 0
        self.val_losses = []
        self.train_losses = []
        self.test_losses = []
        # create summary writer for tensorboard X
        self.writer = SummaryWriter(self.path_results + '/' + alias + '/')
        for k,v in {**vars(self) , **vars(self.model)}.items():
            if type(v) in [str, float, int, list, dict]:
                self.writer.add_text(str(k),str(v))
        # create iterator for all the graphs files
        self.train_iterator = graph_iterator(graphs_folder + "/train/", batch_size, test = False)
        self.test_iterator = graph_iterator(graphs_folder + "/test/", batch_size, test = False)       
        if tensorboard_port is not None:
            multiprocessing.Process(target = self.visualize, args =(tensorboard_port,)).start()
        # create logs for visulization of the events
        self.logs = {}
        for target_var, pred_type , _ in self.predicted_variables:
            if pred_type.lower()== 'regression':
                self.logs[target_var] = {'train_losses':[], 'test_losses':[], 'train_RMSEs' : [], 'test_RMSEs' : []}
            elif pred_type.lower()=='classification':
                self.logs[target_var] = {'train_losses':[], 'test_losses':[], 'train_AUCs' : [], 'test_AUCs' : []}
        counter = 0
        
        for n in range(int(n_epochs)): # HERE AN EPOCH IS SIMPLY A BATCH
            self.train_()
         
        
    def train_(self):
            s = time.time()  
            Loss=0
            if self.counter!=0 and self.counter % self.test_frequency == 0:
                train = False
                # sampling batch of the graphs from `test` folder
                main_ids, input_graphs, targets_dict, source_nodes = self.test_iterator.sample()
            else:
                train = True
                # sampling batch of the graphs from `train` folder
                main_ids, input_graphs, targets_dict, source_nodes = self.train_iterator.sample()
            
            if self.expand_factor is not None:
                # GRAPH NEIGHBOR SAMPLING FOR THE NODES
                Batched_Graph_Sampler = NeighborSampler(expand_factors = [self.expand_factor for i in range(len(self.max_dims))], prob= 'weight')
                sample = Batched_Graph_Sampler.sample(input_graphs, source_nodes)
            else: 
                sample = input_graphs
            # pass the graphs through the encoder layers of the model
            results = self.model.forward(sample, source_nodes, self.device, self.nodes_types[self.main])  
            
            # COMPUTE THE LOSS AND EVALUATE BY RMSE OR AUC
            for target_var, pred_type, coeff in self.predicted_variables:
                if pred_type.lower() == 'regression':
                    criterion = nn.MSELoss(reduction = 'mean')     
                    predictions = results[target_var]                    
                    target = torch.FloatTensor(targets_dict[target_var])
                    loss = criterion(predictions.view(-1), target.to(self.device).view(-1))
                    
                    # log loss and RMSE for regression visualization
                    if train:
                        self.logs[target_var]['train_losses'].append(loss.item())
                        self.logs[target_var]['train_RMSEs'].append(loss.item())
                        if (self.train_counter+1) % self.accumulation_steps == 0 :
                            self.writer.add_scalar(target_var + ' Train RMSE', math.sqrt(statistics.mean(self.logs[target_var]['train_RMSEs'])), self.train_counter/self.accumulation_steps)
                            self.logs[target_var]['train_RMSEs'] = []
                            self.writer.add_scalar(target_var + ' Train loss', statistics.mean(self.logs[target_var]['train_losses']), self.train_counter/self.accumulation_steps)
                            self.logs[target_var]['train_losses'] = []
                    else:
                        self.logs[target_var]['test_losses'].append(loss.item())  
                        self.logs[target_var]['test_RMSEs'].append(loss.item())   
                        if (self.test_counter+1) % self.nb_batch_test == 0:
                            self.writer.add_scalar(target_var + ' Test RMSE', math.sqrt(statistics.mean(self.logs[target_var]['test_RMSEs'])), self.test_counter/self.nb_batch_test) 
                            self.logs[target_var]['test_RMSEs'] = []
                            writer.add_scalar(target_var + ' Test loss', statistics.mean(self.logs[target_var]['test_losses']), self.test_counter/self.nb_batch_test) 
                            self.logs[target_var]['test_losses'] = []
                            
                            
                elif pred_type.lower() == 'classification':                   
                    criterion = nn.NLLLoss(reduction = 'mean' if self.weighted is None else 'none')
                    target = torch.LongTensor(targets_dict[target_var])
                    predictions = results[target_var] 
                    logits = torch.nn.functional.log_softmax(predictions,dim=-1)
                    probabilities = torch.nn.functional.softmax(predictions.detach(),dim=-1)
                    loss = criterion(logits, target.to(self.device).view(-1))
                    
                    # weighted loss to take unbalanced samples into consideration
                    if self.weighted is not None: 
                        w = torch.FloatTensor([self.weighted,1-self.weighted])
                        adjustment = (target.to(self.device)*w[1]) + ((1-target.to(self.device))*w[0])
                        loss *= adjustment.squeeze()
                        loss = loss.mean() 
                    # compute ACU
                    auc = func_compute_AUC(target.to("cpu").detach().numpy().ravel(), probabilities[:,1].to("cpu").detach().numpy().ravel())
                    
                    # log loss and AUC for classification visualization
                    if train:
                        self.logs[target_var]['train_losses'].append(auc)
                        self.logs[target_var]['train_AUCs'].append(auc)                        
                        if (self.train_counter+1) % self.accumulation_steps == 0 :
                            self.writer.add_scalar(target_var + ' Train AUC', statistics.mean(self.logs[target_var]['train_AUCs']), self.train_counter/self.accumulation_steps)
                            self.logs[target_var]['train_AUCs'] = []
                            self.writer.add_scalar(target_var + ' Train loss', statistics.mean(self.logs[target_var]['train_losses']), self.train_counter/self.accumulation_steps)
                            self.logs[target_var]['train_losses'] = []
                    else:
                        self.logs[target_var]['test_losses'].append(auc)    
                        self.logs[target_var]['test_AUCs'].append(auc)

                        print("epoch :", self.counter,'train:',train , 'AUC :', auc)
                        
                        # compute average loss and AUC for every  the number of test batch 
                        if (self.test_counter+1) % self.nb_batch_test == 0:
                            batch_test_auc = statistics.mean(self.logs[target_var]['test_AUCs'])
                            self.writer.add_scalar(target_var + ' Test AUC', batch_test_auc, self.test_counter/self.nb_batch_test) 
                            self.logs[target_var]['test_AUCs'] = []
                            self.writer.add_scalar(target_var + ' Test loss', statistics.mean(self.logs[target_var]['test_losses']), self.test_counter/self.nb_batch_test) 
                            self.logs[target_var]['test_losses'] = []
                            
                            # SAVE PARAMETERS ONLY IF THE VALIDATION RESULT IS THE BEST SO FAR 
                            try:
                                self.max_val_auc
                            except:
                                self.max_val_auc = batch_test_auc
                            if batch_test_auc >=  self.max_val_auc:
                                # save and update best model
                                print("update, best auc:",batch_test_auc)
                                self.max_val_auc = batch_test_auc
                                torch.save(self.model.state_dict(), self.path_saved_model + '/' + self.alias + '/params_best.pt') 
                                torch.save(self.model, self.path_saved_model + '/' + self.alias + '/model_best.pt')
                                               
                self.writer.add_scalar(target_var + ' ' + ('train_loss' if train else 'test_loss'), loss.item(), self.train_counter if train else self.test_counter)        
                Loss += loss*coeff
                           
            del results
            Loss_ = Loss.item()
            # average the accumlated loss
            Loss /= self.accumulation_steps
            
            if train:
                Loss.backward()
                self.train_losses.append(Loss_)
                if (self.train_counter+1) % self.accumulation_steps == 0 :
                    self.optimizer.step()
                    self.optimizer.zero_grad()
                    self.writer.add_scalar('Global' + ' ' + 'train_loss', statistics.mean(self.train_losses), self.train_counter/self.accumulation_steps)
                    self.train_losses = []
                if (self.train_counter+1) % self.save_frequency == 0:
                    torch.save(self.model.state_dict(), self.path_saved_model + '/' + self.alias + '/params_checkpoint.pt')  
                    torch.save(self.model, self.path_saved_model + '/' + self.alias + '/model_checkpoint.pt') 
                self.train_counter+=1
            else:
                if pred_type.lower() == 'regression':
                    try: 
                        self.min_val_loss
                    except:
                        self.min_val_loss = Loss_
                    # SAVE PARAMETERS ONLY IF THE VALIDATION RESULT IS THE BEST SO FAR 
                    if Loss_ <= self.min_val_loss:
                        self.min_val_loss = Loss.item()               
                    self.test_losses.append(Loss_)
                    if (self.test_counter+1) % self.nb_batch_test == 0:
                        self.writer.add_scalar('Global' + ' ' + 'test_loss', statistics.mean(self.test_losses), self.test_counter/self.nb_batch_test)     
                        self.test_losses = []
                self.test_counter+=1                    
            self.counter += 1
            
        
                
    def load_model(self, path):
        # LOAD PRETRAINED MODEL AND PARAMETERS
        self.model = torch.load(path)
        
        
    def visualize(self, tensorboard_port = 6006):
        os.system('tensorboard --logdir=' + self.path_results)
        #os.system('open https://localhost:' + str(tensorboard_port))

             
    def create_embeddings(self, input_folders, write_path, batch_size, device = 'cuda' if torch.cuda.is_available() else 'cpu'): 
        self.model.eval()
        self.model.to(device)
        c = 0
        # WRITE A COLUMN WITH ALL ID KEYS OF THE ORIGINAL MAIN TABLE ('exemple: person_id')
        with open(write_path, 'w+', newline='') as file:
            writer = csv.writer(file)
            print('input files:',input_folders)
            for file in input_folders:
                print('Creating embedings from:',file)
                iterator = graph_iterator(file, batch_size, test = True)
                while True :
                    main_ids, input_graphs, source_nodes = iterator.sample_score() 
                    if main_ids == 'done':
                        break
                    results = self.model.forward(input_graphs, source_nodes,device, self.nodes_types[self.main])
                    for main_id, hid in zip(main_ids, results['hid']):
                        if c == 0:
                            # write header 
                            writer.writerow(['id'] + [str('embedding_dim_' + str(idx)) for idx in range(len(hid))])
                        # write embeddings
                        writer.writerow([str(main_id)] + [h.item() for h in hid])
                        c+=1
                    if len(main_ids) < batch_size:
                        break
        return('Finished')

             
        
    def score(self, input_folders, predicted_variables,write_path, batch_size, expand_factor = None, device = 'cuda' if torch.cuda.is_available() else 'cpu'): 
        ''' Make predictions for the unseen observations'''
        self.expand_factor = expand_factor 
        self.model.eval()
        self.model.to(device)
        
        # WRITE A COLUMN WITH ALL ID KEYS OF THE ORIGINAL MAIN TABLE ('exemple: person_id')
        with open(write_path, 'w+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id'] + [variable[0] for variable in predicted_variables])
            
            for file in input_folders:
                score_iterator = graph_iterator(file, batch_size, test = True)
                while True :
                    main_ids, input_graphs, source_nodes = score_iterator.sample_score()     
                    if main_ids == 'done':
                        break  
                    if self.expand_factor is not None:                
                        Batched_Graph_Sampler = NeighborSampler(expand_factors = [self.expand_factor for i in range(len(self.max_dims))], prob= 'weight')   
                        sample = Batched_Graph_Sampler.sample(input_graphs, source_nodes)
                    else: 
                        sample = input_graphs       
                    results = self.model.forward(sample, source_nodes, device, self.nodes_types[self.main])
                    
                    for var, pred_type in predicted_variables:
                        if pred_type.lower() == 'classification':
                            results[var] = torch.nn.functional.softmax(results[var].detach(),dim=-1)
                            # probability for the positive class
                            results[var] = results[var][:,1].to("cpu").numpy()  

                    for idx, main_id in enumerate(main_ids):
                        script = []
                        for var, _ in predicted_variables:
                            script.extend([results[var][idx]])
                        writer.writerow([str(main_id)] + script) 
                    if len(main_ids) < batch_size:
                        break

        return('Finished')
    
    
    def mem(self):
        my_mem = psutil.virtual_memory()
        return 'Memory used: {:.2f} %, {:.2f} GB | free: {:.2f} GB'.format(my_mem.percent,my_mem.used/1024/1024/1024,my_mem.free/1024/1024/1024)

    
            
class NeighborSampler():
    ''' Neighbor sampling on mini batch of the large graph'''
    def __init__(self, expand_factors = [], prob = None):
        self.expand_factors = expand_factors
        self.prob = prob

    def sample_block(self, source_nodes=[], depth = -1):
        depth+=1
        if depth<len(self.expand_factors):
            for idx, n in enumerate(source_nodes):
                    preds, _, eids = list(self.g.in_edges([n], form = 'all'))
                    #print('preds before', preds)
                    valid_sampling_locs = (self.g.edata['edge_meta_type'][eids]==0).nonzero().squeeze()
                    preds = preds[valid_sampling_locs].unique()
                    eids = eids[valid_sampling_locs].unique()
                    #print('preds after', preds)
                    #print('eids', eids)
                    idxs = list(range(len(preds)))
                    if preds.tolist():
                        if self.prob is not None:
                            weights = self.g.edata[self.prob][eids].cpu().numpy()
                            norm_weights = weights/weights.sum()
                        else:
                            norm_weights = None
                        idxs = np.random.choice(idxs, size = min(self.expand_factors[depth], len(preds)), replace = False, p = norm_weights )
                        ns = preds[idxs].tolist()
                        if ns :
                            self.nodes.append(n)
                        self.nodes.extend(ns)
                        self.sample_block(ns, depth)

        
    def sample(self, g, source_nodes = []):
        self.g = g
        self.nodes = []
        self.nodes.extend(source_nodes)
        # sampling the graph
        self.sample_block(source_nodes)
        self.nodes = list(set(self.nodes))  
        #print('self nodes', len(self.nodes), self.nodes)
        subgraph = g.subgraph(self.nodes)
        # copy the data from the original graph
        subgraph.copy_from_parent()
        
        return subgraph
