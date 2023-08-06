# pcorrcoef: Partial correlation matrix  

import numpy as np

def pcorrcoef(X):

    # Center X
    X = X - np.mean(X,axis=0)
    
    #%% Correalation matrix
    
    dataset_corr = np.corrcoef(X.T)

    
    #%% Partial correlation matrix
    
    #inverse of the correlation matrix
    corr_inv = np.linalg.inv(dataset_corr)
    nrow_inv_corr, ncol_inv_corr = dataset_corr.shape
    
    #partial correlation matrix
    A = np.ones((nrow_inv_corr,ncol_inv_corr))
    for i in range(0,nrow_inv_corr,1):
        for j in range(i,ncol_inv_corr,1):
            if i !=j:
                #above the diagonal
                A[i,j] = - (corr_inv[i,j]) / (np.sqrt(corr_inv[i,i] * corr_inv[j,j]))
                #below the diagonal
                A[j,i] = A[i,j]
            
            
    return A