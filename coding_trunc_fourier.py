'''
	The functions in this file generate fourier codes. You can generate the codes in two ways:
	* Generate a fourier coding matrix with k sinusoids  
	* Given a non-negativbe integer you can generate the tuple for k sinusoids

	Look at the main script here to see how these functions are used
'''
## Standard Library Imports

## Library Imports
import numpy as np

## Local Imports

def uint_to_trunc_fourier_code(nonneg_int: int, domain_len: int, n_freqs: int, include_zeroth_harmonic: bool=False) -> np.array:
	## Validate inputs
	assert(nonneg_int >= 0), "input should be non-negative"
	assert(np.issubdtype(type(nonneg_int), np.integer)), "input should be an integer"
	assert(nonneg_int < domain_len), "input should be smaller than the domain length"
	## Bound input between 0-2*np.pi
	bounded_int = 2*np.pi*float(nonneg_int)/float(domain_len)
	## allocate fourier code
	fourier_code_len = 2*n_freqs 
	fourier_code = np.zeros((fourier_code_len,))
	if(include_zeroth_harmonic): freqs = np.arange(0, n_freqs)
	else: freqs = np.arange(1, n_freqs+1)
	## Query sinusoid for each frequency
	fourier_code[0::2] = np.cos(freqs*bounded_int)
	fourier_code[1::2] = -1*np.sin(freqs*bounded_int)
	return fourier_code

def generate_trunc_fourier_coding_matrix(domain_len: int, n_freqs: int, include_zeroth_harmonic: bool=False) -> np.array:
	'''
		Generates a truncated fourier matrix of size domain_len x n_freqs*2 
	'''
	## Allocate matrix for codes
	fourier_code_len = 2*n_freqs
	fourier_codes = np.zeros((domain_len, fourier_code_len))
	## generate a gray code for each possible code
	for i in range(domain_len):
		fourier_codes[i,:] = uint_to_trunc_fourier_code(i, domain_len, n_freqs, include_zeroth_harmonic)
	return fourier_codes


if __name__=='__main__':
	import matplotlib.pyplot as plt

	## Generate a Gray Coding Matrix
	n_bins = 1024 
	n_fourier_freqs = 4 
	n_fourier_codes = 2*n_fourier_freqs


	trunc_fourier_C = generate_trunc_fourier_coding_matrix(1024, n_fourier_freqs, include_zeroth_harmonic=False)

	## Visualize coding matrix
	from utils import get_pretty_C
	plt.clf()
	plt.imshow(get_pretty_C(trunc_fourier_C), vmin=-1, vmax=1)
	plt.title("Truncated Fourier Coding Matrix with {} frequencies and domain length = {}".format(n_fourier_freqs, n_bins), fontsize=12)
	plt.colorbar()
	plt.show()
