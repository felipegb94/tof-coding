# tof-coding

This repository contains functions to generate coding matrices often used in time-of-flight imaging. 

Currently, this repository includes code to generate the following coding matrices

1. **Fourier-based Coding:** Coding matrix based on the Fourier codes (i.e., rows from the DFT matrix)
2. **Gray Coding:** Binary coding matrix based on gray codes

## Setup Python Env

The code in this repository has been tested on `Python 3.8` and mainly depends: `numpy`, `scipy`, `matplotlib`, and `ipython` (for debugging). 

You can setup a python virtual environment using `conda` and the `environment.yml` file in this repository by running: `conda env create -f environment.yml`

## How to use?

The script `tof_coding_spad_example.py` shows how we can use the functions in all `coding_*.py` to convert a timestamp into its corresponding coded values. 

We assume that timestamps are unsigned integers between 0 and some maximum number of time bins (usually computed as repetition period divided by time resolution).

