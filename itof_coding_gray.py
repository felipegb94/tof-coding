'''
    This script generates the coding matrices for gray coding that can be used in iToF. 
    - The modulation function is assumed to be a perfect pulse
    - The demodulation functions are the gray codes
    - The correlation functions are the correlation between 

    The script also generate "complementary gray codes" which are the same gray codes but for each gray code there is a complemetary one that is 180 degrees shifted
'''
import os
import numpy as np
import matplotlib.pyplot as plt

import coding_gray
from utils import get_pretty_C
from tof_utils import circular_corr

## Number of gray codes
k = 8 # number of bits based on the gray code

## Number of gray codes determines the number of samples
n = 2**k

## Create output directory
out_dir = './itof_coding_functions'
gray_codes_fname = 'k-{}_n-{}_gray'.format(k,n)
complementary_gray_codes_fname = 'k-{}-{}_n-{}_gray-complementary'.format(k, 2*k, n)

## Generate Gray Demodulation Functions
gray_demodfs = coding_gray.generate_gray_coding_matrix(k)
## Generate Gray Modulation
gray_modfs = np.zeros_like(gray_demodfs)
# scale the modulation functions such that their area under the curve is 1
gray_modfs[0,:] = 1.*n 

## Generate complementary gray demodulation functions
negated_gray_demodfs = np.logical_not(np.array(gray_demodfs, dtype=bool)).astype(gray_demodfs.dtype)
complementary_gray_demodfs = np.concatenate((gray_demodfs, negated_gray_demodfs), axis=1)
## Generate complementary gray modulation functions
complementary_gray_modfs = np.concatenate((gray_modfs, gray_modfs), axis=1)

## apply correlation
gray_corrfs = circular_corr(gray_modfs, gray_demodfs, axis=0) / n
complementary_gray_corrfs = circular_corr(complementary_gray_modfs, complementary_gray_demodfs, axis=0) / n

print("mean of light modulation functions = {}".format(gray_modfs.mean(axis=0)))

## Save the 
os.makedirs(out_dir, exist_ok=True)
np.savez(os.path.join(out_dir, gray_codes_fname) 
         , modfs=gray_modfs
         , demodfs=gray_demodfs
         , corrfs=gray_corrfs
         )
np.savez(os.path.join(out_dir, complementary_gray_codes_fname) 
         , modfs=complementary_gray_modfs
         , demodfs=complementary_gray_demodfs
         , corrfs=complementary_gray_corrfs
         )

## Plot a subset of functions to not make the plot too crowded
indeces_to_plot = [0, 2, k+2]

plt.clf()
plt.subplot(3,1,1)
plt.plot(complementary_gray_modfs[:,indeces_to_plot], label="Modulation Functions")
plt.legend()
plt.subplot(3,1,2)
plt.plot(complementary_gray_demodfs[:,indeces_to_plot], label="Demodulation Functions")
plt.legend()
plt.subplot(3,1,3)
plt.plot(complementary_gray_corrfs[:,indeces_to_plot], label="Correlation Functions")
plt.legend()

## Visualize coding matrix
plt.figure()
# plt.imshow(get_pretty_C(gray_demodfs), vmin=0, vmax=1, cmap='gray')
plt.imshow(get_pretty_C(complementary_gray_demodfs), vmin=0, vmax=1, cmap='gray')
