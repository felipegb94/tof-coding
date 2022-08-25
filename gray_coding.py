'''
	The functions in this file generate binary gray codes. You can generate the codes in two ways:
	* Generate a k-bit coding matrix containing all possible gray codes 
	* Given a non-negativbe integer you can generate the k-bit binary gray code

	Look at the main script here to see how these functions are used
'''
## Standard Library Imports

## Library Imports
import numpy as np
from IPython.core import debugger
breakpoint = debugger.set_trace

## Local Imports

def make_zero_mean(gray_code: np.array) -> np.array: 
	return (2*gray_code) - 1  

def int2binstr(integer: int) -> str: 
	'''
		Convert an integer into its binary form stored as a string
	'''
	return bin(integer).lstrip('-0b')

def uint_to_gray(nonneg_int: int) -> int:
	'''
		convert a python integer into a gray code. Assumes that the input integer is positive
		Arguments:
			* nonneg_int: non-negative integer to generate the gray code for
	'''
	## Validate inputs
	assert(nonneg_int >= 0), "input should be non-negative"
	assert(np.issubdtype(type(nonneg_int), np.integer)), "input should be an integer"
	# Right shift the number by 1-bit and then take the XOR with the original number
	gray_uint = nonneg_int ^ (nonneg_int >> 1)
	return gray_uint

def uint_to_gray_code(nonneg_int: int, gray_code_len: int) -> np.array:
	'''
		convert a python integer into a gray code and return the gray code as a numpy array of binary numbers.
		Arguments:
			* nonneg_int: non-negative integer to generate the gray code for
			* gray_code_len: Max length of the gray code we want
	'''
	## Validate inputs
	assert(nonneg_int < 2**gray_code_len), "can't represent {} with a {}-bit gray code".format(nonneg_int, gray_code_len)
	## get gray code as an integer
	gray_uint = uint_to_gray(nonneg_int)
	# convert binary representation to a gray code of a pre-specified length
	gray_bin_arr = np.zeros((gray_code_len,), dtype=int)
	# just return zeros for 0
	if(nonneg_int > 0):  
		# get binary representation of gray code as a string and then convert to array
		gray_bin_str = int2binstr(gray_uint)
		gray_bin_arr[-len(gray_bin_str):] = [int(bin_char) for bin_char in gray_bin_str] 
	return gray_bin_arr

def uint_to_zero_mean_gray_code(nonneg_int: int, gray_code_len: int) -> np.array:
	'''
		convert a python integer into a zero-mean gray code (i.e., 0's are replaced by -1)
	'''
	return make_zero_mean(uint_to_gray_code(nonneg_int, gray_code_len))

def generate_gray_coding_matrix(k_bits: int) -> np.array:
	'''
		Generates all possible k_bits gray codes (binary reflected mode)
	'''
	assert(k_bits >= 1), "invalid k_bits"
	assert(np.issubdtype(type(k_bits), np.integer)), "k_bits shoudl be an integer"
	## Number of possible binary values for gray a gray code with k_bits
	n_binary_codes = int(np.power(2, k_bits))
	## Allocate matrix for codes
	codes = np.zeros((n_binary_codes, k_bits))
	## generate a gray code for each possible code
	for i in range(n_binary_codes):
		codes[i, :] = uint_to_gray_code(i, gray_code_len=k_bits)
	return codes

def generate_zero_mean_gray_coding_matrix(k_bits: int) -> np.array:
	'''
		Generate all poissble k_bits gray codes, but 0's are replaced by -1
	'''
	return make_zero_mean(generate_gray_coding_matrix(k_bits))

if __name__=='__main__':
	import matplotlib.pyplot as plt

	## Generate a Gray Coding Matrix
	k = 4 # number of bits based on the gray code
	gray_C = generate_gray_coding_matrix(k)
	zero_mean_gray_C = generate_zero_mean_gray_coding_matrix(k)
	
	## test 
	test_nums = np.random.randint(0, 2**k, size=(5,)).astype(int)
	for num in test_nums:
		gray_code1 = gray_C[num, :].astype(int)
		gray_code2 = uint_to_gray_code(num, k)
		print("Testing {}-bit gray code for = {}".format(k, num))
		print("    gray_C[:, {}] = {}".format(num, gray_C[num, :]))
		print("    uint_to_gray_code({}) = {}".format(num, uint_to_gray_code(num, k)))
		print("    uint_to_zero_mean_gray_code({}) = {}".format(num, uint_to_zero_mean_gray_code(num, k)))

	## Visualize coding matrix
	from utils import get_pretty_C
	plt.clf()
	plt.subplot(2,1,1)
	plt.imshow(get_pretty_C(gray_C), vmin=-1, vmax=1)
	plt.title("{}-bit Gray Coding Matrix - {} possible binary codes (columns)".format(k, gray_C.shape[0]), fontsize=14)
	plt.colorbar()
	plt.subplot(2,1,2)
	plt.imshow(get_pretty_C(zero_mean_gray_C), vmin=-1, vmax=1)
	plt.title("Zero Mean {}-bit Gray Coding Matrix - {} possible binary codes (columns)".format(k, gray_C.shape[0]), fontsize=14)
	plt.colorbar()
