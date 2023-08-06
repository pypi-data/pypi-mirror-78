## RawPrassLib

RawPrassLib provides Finnigan .raw file format decoder intended for loading Thermo/Finnigan spectra into python code.

The project is in experimental state so please verify that it gives meaningful outputs in your case before reyling on it. The number of supported machines is very low at this time. If you would like to get your machine supported, please send me some sample spectrum/spectra. I do not guarantee that I will have free time to look at it, but it is worth trying.

## Usage
RawPrassLib is designed to enable fast advanced data processing by python, which is not easily acessible with original software.

>!#/usr/bin/env python3

>from rawparse import load_raw

>import numpy as np

>import logging

>...

>...

>chromatogram, masses, ion_scans = load_raw(filename)

The chromatogram is np.array of times of acquisition and total ion current during these acquisitions. (np.array ([times[],intensities[]]))

masses is np.array of the scanned masses from the lowest to the highest. As it should stay the same during whole acquisition only one masses array is provided. (np.array [mass])

matrix is np.array of acquired intensities during each acquisition. It is two-dimensional np.array where the first dimension count should correlate with number of acquisition and the second dimension with the number of masses which were scanned during each acquisition.

## Tested instruments
We've tested and optimized the code against TSQ-7000, LCQ Deca, LCQ Max and LTQ machines .raw output files.

## Known drawbacks
Projet is still very experimental so not all formats and acquisition supported

## Known benefits
The only file which has some real code has just 300 lines of codes.

## Installation
>pip install rawprasslib
