'''
	Example script showing how coding is used with spad timestamps as done in the compressive histograms paper.
'''
## Standard Library Imports
import math

## Library Imports
import numpy as np
from IPython.core import debugger
breakpoint = debugger.set_trace

## Local Imports
from gray_coding import uint_to_zero_mean_gray_code, uint_to_gray_code
from truncated_fourier_coding import uint_to_trunc_fourier_code

if __name__=='__main__':
	import matplotlib.pyplot as plt

	## Set parameters
	# number of time bins in the max-resolution histogram we are building
	# if repetition period is 10ns, and TDC resolution is 0.1ns, the number below would be 100 
	# We keep it as a power of two because fully-binary gray codes only work with powers of 2
	n_tbins = 256

	## generate possible timestamp values to test with
	test_tstamps = np.random.randint(0, n_tbins, size=(3,)).astype(int)

	## Gray Coding Example: generate corresponding gray codes for each timestamp
	gray_code_len = int(math.ceil(math.log2(n_tbins)))
	n_codes = gray_code_len
	if(gray_code_len == math.floor(math.log2(n_tbins))):
		for tstamp in test_tstamps:
			zero_mean_gray_code = uint_to_zero_mean_gray_code(tstamp, gray_code_len=gray_code_len)
			gray_code = uint_to_gray_code(tstamp, gray_code_len=gray_code_len)
			print("Testing {}-bit gray code for = {}".format(gray_code_len, tstamp))
			print("    gray code = {}".format(gray_code))
			print("    zero-mean gray code = {}".format(zero_mean_gray_code))
	else:
		## We should neve go in here
		print("WARNING: Gray codes can only be generated for n_tbins that are powers of 2 (e.g., 256, 512, 1024, etc)")

	## Fourier Coding Example: generate corresponding fourier code for each timestamp
	n_fourier_codes = gray_code_len
	assert((n_fourier_codes % 2) == 0), "Number of fourier codes should be even"
	n_freqs = int(n_fourier_codes / 2)
	for tstamp in test_tstamps:  
		fourier_code = uint_to_trunc_fourier_code(tstamp, n_tbins, n_freqs, include_zeroth_harmonic=False)
		print("Testing {} frequency fourier code for = {}".format(n_freqs, tstamp))
		print("    fourier code = {}".format(np.around(fourier_code,decimals=2)))
