# tof-coding

This repository contains functions to generate coding matrices often used in time-of-flight imaging. 

Currently, this repository includes code to generate the following coding matrices

1. **Fourier-based Coding:** Coding matrix based on the Fourier codes (i.e., rows from the DFT matrix)
2. **Gray Coding:** Binary coding matrix based on gray codes
3. **Hamiltonian Coding:** This is a continuous gray coding matrix where the values on the transitions between 0 to 1 or -1 to 1 are linearly interpolated.

## Setup Python Env

The code in this repository has been tested on `Python 3.8` and mainly depends: `numpy`, `scipy`, `matplotlib`, and `ipython` (for debugging). 

You can setup a python virtual environment using `conda` and the `environment.yml` file in this repository by running: `conda env create -f environment.yml`