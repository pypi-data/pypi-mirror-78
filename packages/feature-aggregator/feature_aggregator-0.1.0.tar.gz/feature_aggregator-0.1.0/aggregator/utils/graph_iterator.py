import torch
import dgl
import os 
import copy 
import random
import pickle
import glob
import collections

import sys
import psutil



class graph_iterator():
    def __init__(self, foldername, batch_size, expansion_factor = None, test = False):
        self.test = test
        self.expansion_factor = expansion_factor
        self.batch_size = batch_size
        self.foldername = foldername
        self.files_idxs = list(range(0,len(glob.glob(foldername + '/*'))))        
        self.shuf_files_idxs = [] 
        self.file_epochs = 0
        self.dataset_epochs = 0
        self.values = []
        self.main_ids = []
        
        
    def get_values_from_file(self):
        rf = open(self.foldername + str(self.file_idx),'rb')
        rf1 = pickle.load(rf)
        rf.close()
        self.main_ids = list(rf1.keys()) 
        random.shuffle(self.main_ids)         
        self.values = [rf1[main_id] for main_id in self.main_ids] # list of list [values:....,target:1]

    def sample(self):
        i = []
        v = []
        while True:
            difference = self.batch_size - len(v)
            for idx in range(min(difference, len(self.main_ids))):
                i.append(self.main_ids.pop())
                v.append(self.values.pop())
                                
            if len(v) == self.batch_size:
                break
             
            else:
                if self.shuf_files_idxs :   
                    pass
                else:
                    if self.test and self.dataset_epochs > 0: # if test
                        if v:
                            input_graphs, target = map(list,zip(*v))
                            source_nodes = []
                            counter = 0
                            for g in input_graphs:
                                source_nodes.append(counter)
                                counter+=g.number_of_nodes()
                            input_graphs = dgl.batch(input_graphs)
                            targets_dict = collections.OrderedDict()
                            for t in target[0].keys():
                                targets_dict[t] = []
                                for v in target:
                                    targets_dict[t].append([v[t]])
                            return i, input_graphs, targets_dict, source_nodes                          
                        else:
                            return 'done', 'done', 'done'
                    else:
                        self.shuf_files_idxs = copy.deepcopy(self.files_idxs)
                        random.shuffle(self.shuf_files_idxs) 
                        self.dataset_epochs +=1   
                
                self.file_idx = self.shuf_files_idxs.pop()
                self.get_values_from_file()
                self.file_epochs+=1                        
                
        input_graphs, target = map(list,zip(*v))
        source_nodes = []
        counter = 0
        for g in input_graphs:
            source_nodes.append(counter)
            counter+=g.number_of_nodes()
        input_graphs = dgl.batch(input_graphs)
        targets_dict = collections.OrderedDict()
        for t in target[0].keys():
            targets_dict[t] = []
            for v in target:
                targets_dict[t].append([v[t]])
 
        return i, input_graphs, targets_dict, source_nodes
            
        
    def sample_score(self):
        i = []
        v = []
        
        while True:
            difference = self.batch_size - len(v)
            for idx in range(min(difference, len(self.main_ids))):
                i.append(self.main_ids.pop())
                v.append(self.values.pop())
                                
            if len(v) == self.batch_size:
                break
                
            else:
                if self.shuf_files_idxs :   
                    pass
                else:
                    if self.test and self.dataset_epochs > 0:
                        if v:
                            input_graphs, target = map(list,zip(*v))
                            source_nodes = []
                            counter = 0
                            for g in input_graphs:
                                source_nodes.append(counter)
                                counter+=g.number_of_nodes()
                            input_graphs = dgl.batch(input_graphs)
                            return i, input_graphs, source_nodes                 
                        else:
                            return 'done', 'done'
                    else:
                        self.shuf_files_idxs = copy.deepcopy(self.files_idxs)
                        self.dataset_epochs +=1                        
                        
                self.file_idx = self.shuf_files_idxs.pop()
                rf = open(self.foldername + str(self.file_idx),'rb')
                rf1 = pickle.load(rf)
                rf.close()
                self.main_ids = list(rf1.keys())
                self.values = [rf1[main_id] for main_id in self.main_ids]
                self.file_epochs+=1                        
                       

        input_graphs, target = map(list,zip(*v))
        source_nodes = []
        counter = 0
        for g in input_graphs:
            source_nodes.append(counter)
            counter+=g.number_of_nodes()
        input_graphs = dgl.batch(input_graphs)
        return i, input_graphs, source_nodes
    
    def mem(self):
        my_mem = psutil.virtual_memory()
        return 'Memory used: {:.2f} %, {:.2f} MB | free: {:.2f} MB'.format(my_mem.percent,my_mem.used/1024/1024,my_mem.free/1024/1024)


