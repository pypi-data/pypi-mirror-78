
import torch
import dgl
from sklearn.metrics import roc_curve, auc

def collate(samples):
    input_graphs, target_1, target_2 =  map(list, zip(*samples)) 
    input_graphs = dgl.batch(input_graphs)
    return input_graphs, torch.FloatTensor(target_1), torch.FloatTensor(target_2)
  
def filt(nodes, identifier): 
    return(nodes.data['node_type'] == identifier)    
        
def func_compute_AUC(labels, scores):
    '''
    Computes AUC of ROC curve.
    '''
    assert len(labels) == len(scores)
    # Compute ROC curve and area the curve
    fpr, tpr, thresholds = roc_curve(labels, scores)
    roc_auc = auc(fpr, tpr)


    return(roc_auc)




