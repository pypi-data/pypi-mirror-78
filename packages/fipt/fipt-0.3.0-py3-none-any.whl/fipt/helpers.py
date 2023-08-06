import logging
from math import log10, floor

import numpy as np
import scipy as sp
# import pandas as pd

import lmfit

__all__ = ['round_to_n', 'make_log_likelihood_function', 'make_complex_model_wrapper']

# create logger
module_logger = logging.getLogger(__name__)
module_logger.setLevel(logging.DEBUG)


#############################################
# general tools
#############################################

def round_to_n(x, n=1):    
    try:
        x_abs = x.m # compatibility with ufloats
    except (NameError, AttributeError) as e:
        x_abs = abs(x)
    
    try:
        prec = n-1-int(floor(log10(x_abs)))
        return round(x, prec)    
    except ValueError as e:
        return x




#############################################
# fitting code
#############################################
def make_log_likelihood_function(name='normal', scale=1, **kwds):
    ''' Creates common log likelihood functions.
    name can be:
    'normal': Normal distribution. Results in least sqr optimization
    't': Student T distribution. Requires shape parameter df as additional keyword.
    
    Examples:
    >>> llf = make_log_likelihood_function('normal', scale=1)
    >>> llf(0)
    ... -0.91893853320467267
    
    >>> llf = make_log_likelihood_function('t', scale=1, df=2)
    >>> llf(0)
    ... -1.0397207708399179
    
    Plot likelihood:
    
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 1)

        llf_configs = [    
            dict(name='norm', scale=1),
            dict(name='t', scale=1, df=0.3),
            dict(name='t', scale=1, df=1),
            dict(name='t', scale=1, df=3),
        ]

        rng = 5.0
        x = np.linspace(-rng, rng, 100)

        for llf_c in llf_configs:
            llf = make_log_likelihood_function(**llf_c)
            ax.plot(x, llf(x), lw=5, alpha=0.6)

        ax.set_ylim(-10, 0)    
    
    '''
    
    student_t = sp.stats.t
    norm_dist = sp.stats.norm
    
    if name in ['normal', 'norm']:
        llf = norm_dist.logpdf
    elif name == 't':
        shape_df = kwds['df']
        llf = lambda x: student_t.logpdf(x, shape_df)
    else:
        raise ValueError(f'Invalid name for loglikelihood function: {name}')

    return llf


def make_complex_model_wrapper(func, likelihood_func=None):
    ''' This generates a wrapper for a complex values model function. 
    The returned wrapper function takes model parameters and can return 
    two different things:
    If no data is provided, it returns the complex valued model output
    If data is provided it returns the real valued residuals.
    '''
    
    if likelihood_func is None:
        likelihood_func = make_log_likelihood_function('normal', scale=1)
    
    def complex_model_wrapper(params, x=None, data=None, eps=None):
        if x is None:
            raise ValueError('x cannot be None!')

        # unpack parameters: extract .value attribute for each parameter
        if isinstance(params, lmfit.Parameters):
            parvals = params.valuesdict()
        elif isinstance(params, dict):
            parvals = params

        model = func(x, **parvals)

        if data is None:
            return model

        # residuals have to be real numbers!        
        # return -1.0 * likelihood_func(np.absolute((model-data)).sum())
        return -1.0 * likelihood_func(np.absolute((model-data)))

    return complex_model_wrapper, likelihood_func



