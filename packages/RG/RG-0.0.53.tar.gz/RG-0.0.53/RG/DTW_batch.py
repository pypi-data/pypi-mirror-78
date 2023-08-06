# DTW_batch: Dynamic time warping (DTW) for a 3D datacube - batch process

import numpy as np
import RG as rg
import cv2

def DTW_batch(X):
    '''
    
    DTW_batch: Dynamic time warping (DTW) for a 3D datacube - batch process
    [X_align] = DTW_batch(X)
    
    Important: the first variable is used to align all the others
    
    INPUT
    X [a x b x c] <numpy.ndarray>
        3D datacube, typical of a batch process
        a times
        b batches
        c variables
    
    OUTPUT
    X_align [a x b x c] 
        aligned data
       
    '''
    
    # Alignment is based on the first variable
    for i in range(1,X.shape[1]): # for each batch (column of X, excluding x0, the reference)
        x0 = X[:,0,0]
        xi = X[:,i,0]
        distance, path = rg.DTW(x0, xi)
        path = np.array(path) # Path suggested by DWT to align xi and x0
        
        # Align x0 (ref batch)
        x0 = x0[path[:,0]]
        x0 = cv2.resize(x0, (1,X.shape[0]), interpolation = cv2.INTER_AREA)
        X[:,0,0] = np.squeeze(x0)
    
        # Align other variables linked to x0
        for k in range(1,X.shape[2]):
            xk = X[:,0,k]
            xk = xk[path[:,0]]
            xk = cv2.resize(xk, (1,X.shape[0]), interpolation = cv2.INTER_AREA)
            X[:,0,k] = np.squeeze(xk)
    
        # Align xi
        xi = xi[path[:,1]]
        xi = cv2.resize(xi, (1,X.shape[0]), interpolation = cv2.INTER_AREA)
        X[:,i,0] = np.squeeze(xi)     
        
        # Align other variables linked to xi
        for k in range(1,X.shape[2]):
            xk = X[:,i,k]
            xk = xk[path[:,1]]
            xk = cv2.resize(xk, (1,X.shape[0]), interpolation = cv2.INTER_AREA)
            X[:,i,k] = np.squeeze(xk)
        
        # Align all other batches between 0 and i
        # These have already been aligned with x0, just apply the alignment for x0
        if i>1:
            for j in range(1,i):
                xj = X[:,j,0]
                xj = xj[path[:,0]]
                xj = cv2.resize(xj, (1,X.shape[0]), interpolation = cv2.INTER_AREA)
                X[:,j,0] = np.squeeze(xj)
                
                # Align other variables linked to x0
                for k in range(1,X.shape[2]):
                    xk = X[:,j,k]
                    xk = xk[path[:,0]]
                    xk = cv2.resize(xk, (1,X.shape[0]), interpolation = cv2.INTER_AREA)
                    X[:,j,k] = np.squeeze(xk)  

    return X