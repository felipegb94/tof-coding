## Standard Library Imports

## Library Imports
import numpy as np
import scipy
from scipy import signal
from IPython.core import debugger
breakpoint = debugger.set_trace

## Local Imports


def get_pretty_C(C, col2row_ratio=1.35):
	'''
		Create a matrix based on C that can be displayed as an image to visualize the matrix
	'''
	assert(C.ndim == 2), "C should be a 2D matrix"
	(n, k) = C.shape
	if((n // 2) < k): col2row_ratio=1
	n_row_per_code = int(np.floor(n / k) / col2row_ratio)
	n_rows = n_row_per_code*k
	n_cols = n
	pretty_C = np.zeros((n_rows, n_cols))
	for i in range(k):
		start_row = i*n_row_per_code
		end_row = start_row + n_row_per_code
		pretty_C[start_row:end_row, :] = C[:, i] 
	return pretty_C	

def tstamp2hist(tstamp, hist_len):
	hist = np.zeros((hist_len,))
	hist[tstamp] = 1
	return hist

