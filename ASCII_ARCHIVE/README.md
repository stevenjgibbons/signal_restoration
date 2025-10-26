
This directory contains just a small selection of example files from the set of labelled waveforms found on Zenodo at
https://doi.org/10.5281/zenodo.16872021  
The full dataset is too large to upload to github but these examples should allow execution of scripts in this repo.  

The following text describes the format (lifted from the Zenodo repo):  

```
The format of the files
is as follows (taking the file 19670922.0504.brvk.KODB.SLZb0.030.txt as an example):

# 1967-09-22T05:04:00.000  0.03000    10997    -71866560.00000 BRVK_SLZb
      0         70.437988  0
      1         -0.405301  0
      2         -1.486040  0
      3         -3.619660  0
      4         -6.067526  0
      5         -8.281006  0
      6        -10.185470  0
      7        -11.560674  0
      8         -9.553430  0
      9         -9.328013  0
     10         -8.562012  0
     11         -6.562012  0
etc.

The first line gives
the time of the first sample of the time-series, T0,
the sampling interval in seconds, DT,
the number of samples present, NSAMP,
the epoch time (relative to 1970-00-00Z00:00:00.000) of the first sample,
and the name of the channel as recorded in the original archive.
Each of the NSAMP subsequent lines contains 3 numbers, ISAMP, RVAL, and ICLIP.

ISAMP is the number of the sample, such that the time of the sample is T0 + DTISAMP*.
RVAL is the value of the original data at this sample.
ICLIP is set to:
   zero if the true value is likely well represented by RVAL,
   -1   if the true value is likely less than RVAL (often the negative clipping value), and
   +1   if the true value is likely greater than RVAL (often the positive clipping value).

Many of the flags may be eroneous and spurious values between the clipping
limits are likely to be unflagged.
```
