# lags: add lag times to a data matrix

import numpy as np
import matplotlib.pyplot as plt

def lags(A,nb):

    '''
    
    Lags: add lag times to a data matrix
    [X_lags_1, X_lags_2] = lags(X,nb)
    
    INPUT
    X [n x k] <numpy.ndarray>
        n samples
        k variables  
    nb [1 x 1] <int>
        number of time lags
    
    OUTPUT
    X_lags_1 [n x k] 
        data with time lags
        X matrix is tiled as a whole 
    X_lags_2 [n x k] 
        data with time lags
        X matrix is laggee one variable at a time    
    
    '''

    
    s1,s2 = A.shape

    B = np.copy(A) # Copy of A that will be lagged
    C = np.copy(A) # A containing lags
    
    for i in range(nb):
        zeros = np.zeros((1,s2))
        B = np.concatenate((zeros,B),axis=0)
        B = B[:-1,:]
        C = np.concatenate((C,B),axis=1)
    
    D = []
    for i in range(s2):
        for j in range(i,C.shape[1],s2):
            c = C[:,j]
            D.append(c)
    D = np.array(D)
    D = D.T
    
    # Crop first times to only keep full lines
    C = C[nb:,:]
    D = D[nb:,:]
    
    # Matrix C: data is tiled, each tile is a time lag
    # Matrix D: C reordered by variable
    
    plt.figure()
    plt.imshow(C,aspect='auto')
    
    plt.figure()
    plt.imshow(D,aspect='auto')
    
    return C,D