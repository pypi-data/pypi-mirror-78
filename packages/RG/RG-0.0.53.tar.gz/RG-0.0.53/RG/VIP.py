# VIP: PLS VIP (variable importance in the projection)

import numpy as np

def VIP(X,W,SSY):

    '''
    
    VIP: PLS variable importance in the projection
    [VIP] = VIP(X,nb)
    
    INPUT
    X [n x k] <numpy.ndarray>
        X data used in PLS
        n samples
        k variables
    W [k x nbPC] <numpy.ndarray>
        PLS weights
        k variables
        nbPC PLS components
    SSY [nbPC x 1] <numpy.ndarray>
        PLS sum of squares of Y
        nbPC PLS components      
    
    
    OUTPUT
    VIP [k x 1] 
        PLS VIP values
   
    
    '''
    
    
    VIP = []
    
    for i in range(X.shape[1]):
        wi = W[i,:]
        NUM = 0
         
        for j in range(W.shape[1]):
            wij = wi[j]
            num = wij**2 * SSY[j]
            NUM = NUM + num
    
        vip = X.shape[1]*NUM/np.sum(SSY)
        VIP.append(vip)
        
    VIP = np.array(VIP)



    return VIP