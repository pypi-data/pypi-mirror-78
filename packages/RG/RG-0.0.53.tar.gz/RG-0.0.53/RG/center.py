#%% Center 

import numpy as np

def center(X, *args):
    '''
    
    Center: center data
    [X_auto, mX] = center(X)
    
    INPUT
    X [n x k] <numpy.ndarray>
        spectra
        n samples
        k variables
    *args
        optional inputs
        mX [1 x k] 
            mean of all variables - computed beforehand
    
    OUTPUT
    X_auto [n x k] 
        preprocessed spectra
    mX [1 x k] 
        mean of all variables     
    
    '''
    
    varargin = args
    n_params = len(varargin)

    if n_params == 1:
        mx = varargin[0]
        mx = np.squeeze(mx)
        
    else:
        mx = np.nanmean(X, axis=0)
    
    
    m,n = X.shape

    ax = (X - mx)
    
    mx = mx[np.newaxis]
    
    return ax, mx