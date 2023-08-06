# correlated_matrix : Create (normal) random matrix with correlated columns

import numpy as np
import matplotlib.pyplot as plt

def correlated_matrix(obs,C):

    # C is a variance-covariance matrix
    # Examples:
    # C = np.array([[3, 0.9],[0.9, 1]])
    # C = 0.5*np.ones((40,40)) + np.eye(40)
    
    X = np.random.randn(obs,C.shape[0])
    
    #C = np.array([[3, 0.9],[0.9, 1]])
    
    Y = X@C

    return Y