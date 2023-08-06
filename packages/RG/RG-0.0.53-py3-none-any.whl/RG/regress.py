# regress: MLR regression

import numpy as np
import statsmodels.api as sm
import pandas as pd

def regress(y, X):
    ''' 
    
    regress: MLR regress
    [b, b_int, model, R2, F, p] = regress(y,X)
    
    INPUT
    X [n x k] <numpy.ndarray>
        independent variable
        n samples
        k variables
    y [n x 1] <numpy.ndarray>
        dependent variable
    
    OUTPUT
    b [k x 1]
        regression coefficients
    b_int [k x 2]
        95% confidence interval on regression coefficients  
    model < wrapper>
        MLR regression model
    R2 [1 x 1]
        Coefficient of determination
    F [1 x 1]
        Fisher test: F value for the MLR model
    p [1 x 1]
        Fisher test: p value for the MLR model
    
    ''' 
    
    model = sm.OLS(y, X).fit()
    b = model.params
    b_int = model.conf_int(0.05)
    b = (b[np.newaxis]).T # Vector format for output
    
    R2 = model.rsquared
    F = model.fvalue
    p = model.f_pvalue
    
    return b, b_int, model, R2, F, p