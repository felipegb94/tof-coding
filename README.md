# tof-coding

This repository contains functions to generate coding matrices often used in time-of-flight imaging. 

It also shows how we can use these coding matrices to encode timestamp values (without generating the coding matrix).

Currently, this repository includes code to generate the following coding matrices

1. **Fourier-based Coding:** Coding matrix based on the Fourier codes (i.e., rows from the DFT matrix)
2. **Gray Coding:** Binary coding matrix based on gray codes

It also includes scripts that generate the coding functions for Hamiltonian and Gray coding for indirect ToF (see `itof_coding_gray.py` and `itof_coding_hamiltonian.py`)

## Setup Python Env

The code in this repository has been tested on `Python 3.8` and mainly depends: `numpy`, `scipy`, `matplotlib`, and `ipython` (for debugging). 

You can setup a python virtual environment using `conda` and the `environment.yml` file in this repository by running: `conda env create -f environment.yml`

## How to use?

The script `tof_coding_spad_example.py` shows how we can use the functions in all `coding_*.py` to convert a timestamp into its corresponding coded values. 

We assume that timestamps are unsigned integers between 0 and some maximum number of time bins (usually computed as repetition period divided by time resolution).

## Visualizing the coding matrices

Simply run `python coding_gray.py` or `python coding_trunc_fourier.py`. This will display a visualization of each coding matrix with K codes (rows).


