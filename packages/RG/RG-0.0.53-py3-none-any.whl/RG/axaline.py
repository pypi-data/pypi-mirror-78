# axaline: Arbitrary line with intercept and slope

import matplotlib.pyplot as plt 
import numpy as np    

def axaline(slope, intercept,style=':r',label='name'):
   
    """
    axaline: plot a line from slope and intercept
    # Acts like axhline or axvline
    # Works for 2D plots
    
    axaline(slope, intercept,style=':r',label='name')
    
    INPUT
    slope [1 x 1] <numpy.ndarray> 
    intercept [1 x 1] <numpy.ndarray>   
    stype <text>
        optional input
    label <text>
        optional input    
    
    """
    
    
    
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, style, label=label)
