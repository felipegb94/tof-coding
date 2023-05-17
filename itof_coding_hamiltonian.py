'''
	This script generates the coding matrices for hamiltonian coding that can be used in iToF. 
	- The modulation functions are variable duty cycle square pulses
	- The demodulation functions are binary functions
	- The correlation functions are the correlation between modulation and demodulation 

	The script also generate "complementary hamiltonian codes" which are the same codes but for each hamiltonian code there is a complemetary one that is 180 degrees shifted
'''
import os
import math
import numpy as np
import matplotlib.pyplot as plt

import coding_gray
from utils import get_pretty_C
from tof_utils import circular_corr

def variable_duty_cycle_functions(n, k, duty_cycle):
	assert(duty_cycle <= 1.), "duty cycle should be smaller than 1"
	X = np.zeros((n,k))
	X[0:math.floor(duty_cycle*n), :] = 1. / duty_cycle
	return X


def GetHamK3(N = 1000):
	"""GetHamK3: Get modulation and demodulation functions for the coding scheme
		HamK3 - Sq16Sq50.	
	Args:
		N (int): N
	Returns:
		modfs: NxK matrix
		demodfs: NxK matrix
	"""
	#### Set some parameters
	K = 3
	modulationDutyCycle = 1. / 6.
	#### Allocate modulation and demodulation vectors
	modfs = variable_duty_cycle_functions(n=N, k=K, duty_cycle=modulationDutyCycle)
	#### Prepare demodulation functions
	demodfs = np.zeros((N,K))
	## Make shape of function
	demodDuty = 1./2.
	for i in range(0,K):
		demodfs[0:math.floor(demodDuty*N),i] = 1.
	## Apply necessary phase shift
	shifts = [0, (1./3.)*N, (2./3.)*N]
	for i in range(0,K): demodfs[:,i] = np.roll(demodfs[:,i], int(round(shifts[i])))
	return (modfs, demodfs)


def GetHamK4(N=1000):
	"""GetHamK4: Get modulation and demodulation functions for the coding scheme HamK4	
	Args:
		N (int): N
	Returns:
		modfs: NxK matrix
		demodfs: NxK matrix
	"""
	#### Set some parameters
	K = 4
	modulationDutyCycle = 1. / 12.
	#### Allocate modulation and demodulation vectors
	modfs = variable_duty_cycle_functions(n=N, k=K, duty_cycle=modulationDutyCycle)
	#### Prepare demodulation functions
	demodfs = np.zeros((N,K))
	## Make shape of function
	demodDuty1 = np.array([6./12.,6./12.])
	shift1 = 5./12.
	demodDuty2 = np.array([6./12.,6./12.])
	shift2 = 2./12.
	demodDuty3 = np.array([3./12.,4./12.,3./12.,2./12.])
	shift3 = 0./12.
	demodDuty4 = np.array([2./12.,3./12,4./12.,3./12.])
	shift4 = 4./12.
	shifts = [shift1*N, shift2*N, shift3*N, shift4*N]
	demodDutys = [demodDuty1, demodDuty2, demodDuty3, demodDuty4]
	for i in range(0,K):
		demodDuty = demodDutys[i]
		startIndeces = np.floor((np.cumsum(demodDuty) - demodDuty)*N)
		endIndeces = startIndeces + np.floor(demodDuty*N) - 1
		for j in range(len(demodDuty)):
			if((j%2) == 0):
				demodfs[int(startIndeces[j]):int(endIndeces[j]),i] = 1.
	## Apply necessary phase shift
	for i in range(0,K): demodfs[:,i] = np.roll(demodfs[:,i], int(round(shifts[i])))

	return (modfs, demodfs)


def GetHamK5(N=1000):
	"""GetHamK5: Get modulation and demodulation functions for the coding scheme HamK5.	
	Args:
		N (int): N
	Returns:
		modfs: NxK matrix
		demodfs: NxK matrix
	"""
	#### Set some parameters
	K = 5
	modulationDutyCycle = 1. / 30.
	#### Allocate modulation and demodulation vectors
	modfs = variable_duty_cycle_functions(n=N, k=K, duty_cycle=modulationDutyCycle)
	#### Prepare demodulation functions
	demodfs = np.zeros((N,K))
	## Make shape of function
	demodDuty1 = np.array([15./30.,15./30.])
	shift1 = 15./30.
	demodDuty2 = np.array([15./30.,15./30.])
	shift2 = 7./30.
	demodDuty3 = np.array([8./30.,8./30.,7./30.,7./30.])
	shift3 = 3./30.
	demodDuty4 = np.array([4./30.,4./30.,4./30.,4./30.,3./30.,4./30.,4./30.,3./30.])
	shift4 = 1./30.
	demodDuty5 = np.array([2./30.,2./30.,2./30.,2./30.,2./30.,2./30.,2./30.,
							3./30.,2./30.,2./30.,2./30.,2./30.,3./30.,2./30])
	shift5 = 4./30.
	shifts = [shift1*N, shift2*N, shift3*N, shift4*N, shift5*N]
	demodDutys = [demodDuty1, demodDuty2, demodDuty3, demodDuty4, demodDuty5]
	for i in range(0,K):
		demodDuty = demodDutys[i]
		startIndeces = np.floor((np.cumsum(demodDuty) - demodDuty)*N)
		endIndeces = startIndeces + np.floor(demodDuty*N) - 1
		for j in range(len(demodDuty)):
			if((j%2) == 0):
				demodfs[int(startIndeces[j]):int(endIndeces[j]),i] = 1.

	## Apply necessary phase shift
	for i in range(0,K): demodfs[:,i] = np.roll(demodfs[:,i], int(round(shifts[i])))

	return (modfs, demodfs)

## Number of gray codes
k = 4 # number of bits based on the gray code

## Number of time samples
n = 128

## Create output directory
out_dir = './itof_coding_functions'
hamilt_codes_fname = 'k-{}_n-{}_hamilt'.format(k,n)
complementary_hamilt_codes_fname = 'k-{}-{}_n-{}_hamilt-complementary'.format(k, 2*k,n)

## Generate Gray Demodulation Functions
if(k==3): (hamilt_modfs, hamilt_demodfs) = GetHamK3(N=n)
elif(k==4): (hamilt_modfs, hamilt_demodfs) = GetHamK4(N=n)
elif(k==5): (hamilt_modfs, hamilt_demodfs) = GetHamK5(N=n)
else:  assert(False), "Hamiltonian codes are only defined for K=3,4,5 in this script."
## Generate complementary gray demodulation functions
negated_hamilt_demodfs = (hamilt_demodfs*-1) + 1
complementary_hamilt_demodfs = np.concatenate((hamilt_demodfs, negated_hamilt_demodfs), axis=1)
## Generate complementary gray modulation functions
complementary_hamilt_modfs = np.concatenate((hamilt_modfs, hamilt_modfs), axis=1)

## apply correlation
hamilt_corrfs = circular_corr(hamilt_modfs, hamilt_demodfs, axis=0) / n
complementary_hamilt_corrfs = circular_corr(complementary_hamilt_modfs, complementary_hamilt_demodfs, axis=0) / n

print("mean of light modulation functions = {}".format(hamilt_modfs.mean(axis=0)))

## Save the 
os.makedirs(out_dir, exist_ok=True)
np.savez(os.path.join(out_dir, hamilt_codes_fname) 
		 , modfs=hamilt_modfs
		 , demodfs=hamilt_demodfs
		 , corrfs=hamilt_corrfs
		 )
np.savez(os.path.join(out_dir, complementary_hamilt_codes_fname) 
		 , modfs=complementary_hamilt_modfs
		 , demodfs=complementary_hamilt_demodfs
		 , corrfs=complementary_hamilt_corrfs
		 )

## Plot a subset of functions to not make the plot too crowded
indeces_to_plot = [2, 2+k]

plt.close('all')
fig, ax = plt.subplots(3,1)
for i in range(len(indeces_to_plot)):
	ax[0].plot(complementary_hamilt_modfs[:,indeces_to_plot[i]], label="ModFs {}".format(indeces_to_plot[i]))
	ax[1].plot(complementary_hamilt_demodfs[:,indeces_to_plot[i]], label="DemodFs {}".format(indeces_to_plot[i]))
	ax[2].plot(complementary_hamilt_corrfs[:,indeces_to_plot[i]], label="CorrFs {}".format(indeces_to_plot[i]))
ax[0].legend()
ax[1].legend()
ax[2].legend()
## Visualize coding matrix
plt.figure()
# plt.imshow(get_pretty_C(hamilt_demodfs), vmin=0, vmax=1, cmap='gray')
plt.imshow(get_pretty_C(complementary_hamilt_demodfs), vmin=0, vmax=1, cmap='gray')
