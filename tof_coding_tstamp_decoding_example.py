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
from coding_gray import uint_to_zero_mean_gray_code, uint_to_gray_code, generate_gray_coding_matrix
from coding_trunc_fourier import uint_to_trunc_fourier_code, generate_trunc_fourier_coding_matrix
from depth_decoding import zncc, zncc_decoding

if __name__=='__main__':
	import matplotlib.pyplot as plt

	## Set parameters
	# number of time bins in the max-resolution histogram we are building
	# if repetition period is 10ns, and TDC resolution is 0.1ns, the number below would be 100 
	# We keep it as a power of two because fully-binary gray codes only work with powers of 2
	n_tbins = 256

	## generate a histogram with a single timestamp
	test_tstamp = np.random.randint(0, n_tbins) 
	print("Ground Truth Timestamp: {}".format(test_tstamp))

	## Estimate depths with gray coding
	gray_code_len = int(math.ceil(math.log2(n_tbins)))
	# Encode
	encoded_tstamp = uint_to_zero_mean_gray_code(test_tstamp, gray_code_len)
	# Decode with gray coding matrix
	gray_Cmat = generate_gray_coding_matrix(gray_code_len)
	gray_decoded_tstamp = zncc_decoding(encoded_tstamp, gray_Cmat)
	print("Gray Decoded Timestamp: {}".format(gray_decoded_tstamp))

	## Estimate depths with fourier coding
	n_fourier_codes = 8
	assert((n_fourier_codes % 2) == 0), "Number of fourier codes should be even"
	n_freqs = int(n_fourier_codes / 2)
	# Encode
	encoded_tstamp = uint_to_trunc_fourier_code(test_tstamp, n_tbins, n_freqs, include_zeroth_harmonic=False)
	# Decode with fourier coding matrix
	fourier_Cmat = generate_trunc_fourier_coding_matrix(n_tbins, n_freqs, include_zeroth_harmonic=False)
	fourier_decoded_tstamp = zncc_decoding(encoded_tstamp, fourier_Cmat)
	print("fourier Decoded Timestamp: {}".format(fourier_decoded_tstamp))

