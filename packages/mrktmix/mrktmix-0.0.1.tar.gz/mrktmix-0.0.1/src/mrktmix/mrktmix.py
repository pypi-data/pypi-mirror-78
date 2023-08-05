import numpy as np
from scipy.ndimage.interpolation import shift
from scipy.signal import lfilter

def apply_apl(df_apl,adstock,power,lag):
    '''(array,integer,integer,integer) -> array
    
    APL transformation and standardization
    '''    
    
    return(shift(np.nan_to_num(np.power(lfilter([1], [1, -float(adstock)], df_apl,axis=0),power)), lag, cval=0,order=1))