## Standard Library Imports

## Library Imports
import numpy as np

## Local Imports

TWOPI = 2*np.pi
SPEED_OF_LIGHT = 3e8
EPSILON = 1e-7

def linearize_phase(phase):
	# If phase  < 0 then we need to add 2pi.
	corrected_phase = phase + (TWOPI*(phase < 0))
	return corrected_phase
	
def phase2depth(phase, repetition_tau):
	return time2depth(phase2time(phase, repetition_tau))

def phase2time(phase, repetition_tau):
	'''
		Assume phase is computed with np.atan2
	'''
	# If phase  < 0 then we need to add 2pi.
	corrected_phase = linearize_phase(phase)
	return (corrected_phase*repetition_tau / TWOPI )

def time2depth(time):
	return (SPEED_OF_LIGHT * time) / 2.

def depth2time(depth):
	return (2*depth /  SPEED_OF_LIGHT)

def phasor2time(phasor, repetition_tau):
	phase = np.angle(phasor)
	return phase2time(phase, repetition_tau)

def zero_norm_t(C, axis=-1):
	'''
		Apply zero norm transform to give axis
	'''
	return (C - C.mean(axis=axis, keepdims=True)) / (C.std(axis=axis, keepdims=True) + EPSILON)

def circular_conv( v1, v2, axis=-1 ):
	"""Circular convolution: Calculate the circular convolution for vectors v1 and v2. v1 and v2 are the same size
	
	Args:
		v1 (numpy.ndarray): ...xN vector	
		v2 (numpy.ndarray): ...xN vector	
	Returns:
		v1convv2 (numpy.ndarray): convolution result. N x 1 vector.
	"""
	v1convv2 = np.fft.irfft( np.fft.rfft( v1, axis=axis ) * np.fft.rfft( v2, axis=axis ), axis=axis, n=v1.shape[-1] )
	return v1convv2

def circular_corr( v1, v2, axis=-1 ):
	"""Circular correlation: Calculate the circular correlation for vectors v1 and v2. v1 and v2 are the same size
	
	Args:
		v1 (numpy.ndarray): Nx1 vector	
		v2 (numpy.ndarray): Nx1 vector	
	Returns:
		v1corrv2 (numpy.ndarray): correlation result. N x 1 vector.
	"""
	v1corrv2 = np.fft.ifft( np.fft.fft( v1, axis=axis ).conj() * np.fft.fft( v2, axis=axis ), axis=axis ).real
	return v1corrv2