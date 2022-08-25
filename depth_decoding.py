'''
	Functions to estimate depths given coded ToF values
'''
## Standard Library Imports

## Library Imports
import numpy as np
from IPython.core import debugger
breakpoint = debugger.set_trace

## Local Imports


def norm_t(C, axis=-1):
	'''
		Divide by standard deviation across given axis
	'''
	return C / (np.linalg.norm(C, ord=2, axis=axis, keepdims=True) + 1e-6)

def zero_norm_t(C, axis=-1):
	'''
		Apply zero norm transform to give axis
		This performs exactly the same as the old zero_norm_t_old, but in the old version denominator is scale by a factor of (1/sqrt(K)) which is part of the standard deviation formula
	'''
	return norm_t(C - C.mean(axis=axis, keepdims=True), axis=axis)

def zncc(x, C):
    '''
        Zero-mean normalized cross correlation between vector x and matrix C
        * x is a Kx1 vector or a KxM matrix
        * C is a NxK matrix
    '''
    assert(x.ndim <= 2), "x should be a vector or a matrix"
    assert(C.ndim == 2), "C should be a a matrix"
    assert(x.shape[0] == C.shape[-1])
    ## Compute zero norm
    zero_norm_x = zero_norm_t(x, axis=0)
    zero_norm_C = zero_norm_t(C, axis=1)
    ## Compute cross correlation
    return np.matmul(zero_norm_C, zero_norm_x).squeeze()

def ncc(x, C):
    '''
        Zero-mean normalized cross correlation between vector x and matrix C
        * x is a Kx1 vector or a KxM matrix
        * C is a NxK matrix
    '''
    assert(x.ndim <= 2), "x should be a vector or a matrix"
    assert(C.ndim == 2), "C should be a a matrix"
    assert(x.shape[0] == C.shape[-1])
    ## Compute zero norm
    norm_x = norm_t(x, axis=0)
    norm_C = norm_t(C, axis=1)
    ## Compute cross correlation
    return np.matmul(norm_C, norm_x).squeeze()
    
def zncc_decoding(x, C):
    '''
        Use this method if any of the codes in C is not zero-mean
    '''
    ## Build lookup table
    zncc_lookup = zncc(x,C)
    ## Find maximum
    return np.argmax(zncc_lookup, axis=0)

def ncc_decoding(x, C):
    '''
        Use this method if all codes/columns in C are zero-mean
    '''
    ## Build lookup table
    ncc_lookup = ncc(x,C)
    ## Find maximum
    return np.argmax(ncc_lookup, axis=0)