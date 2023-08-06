# MCR: Multivariate Curve Resolution (by ALS: alternating least squares)

import numpy as np

def MCR(X,nbPC):

    # Normalize spectra (each spectrum has a sum=1)
    for i in range(X.shape[0]):
        X[i,:] = X[i,:]/np.sum(X[i,:])
    
    x0, x1 = X.shape
    
    # Initialize C
    np.random.seed()
    C = np.random.rand(x0, nbPC)/nbPC
    C_temp = np.random.rand(x0, nbPC)/nbPC
    error = 1e10
    
    while error > 1E-7:
    
        # Compute S
        S = np.linalg.inv(C.T@C)@C.T@X

        # Correct negative spectra
        S[S < 0] = 0
        
        # Normalize spectra (each spectrum has a sum=1)
        for i in range(nbPC):
            S[i,:] = S[i,:]/np.sum(S[i,:])
        
        # Compute C
        C = X@S.T@np.linalg.inv(S@S.T)
        
        # Correct impossible compositions
        C[C < 0] = 0 
        C[C > 1] = 1                  
                    
        # Normalize composition (each timepoint has a sum=1)
        for i in range(C.shape[0]):
            C[i,:] = C[i,:]/np.sum(C[i,:])
        
        # Check c convergence --------------------
        error = np.sum(np.power((C-C_temp),2)) # Squared error
        C_temp = C
        # ----------------------------------------     
    
    return C,S