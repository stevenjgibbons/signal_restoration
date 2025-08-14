# signal_restoration
A testbed for the reconstruction of clipped seismic signals with a focus on the nuclear explosion signals from the Borovoye Geophysical Observatory, Kazakhstan, as described by An et al. (2015): http://dx.doi.org/10.1016/j.grj.2015.02.014


# Background  
An et al. (2015) describe in detail an archive of nuclear explosion signals recorded between 1966 and 1996 at the Borovoye Geophysical Observatory in Kazakhstan. The original waveforms are made openly available on https://www.ldeo.columbia.edu/res/pi/Monitoring/Data/ . The waveforms are recorded with different gains such that some of them are "complete" (capturing the full dynamic range of the signals) while others are clipped. I have taken many of the waveforms from this archive and, as best I can, labelled which samples are clipped. It is my intention to use this repo as a testbed for the reconstruction of clipped waveforms. There are many papers in the literature that address this subject and I plan to explore the applicability and effectiveness of different methods. I am open to the possibility (probability) that a meaningful reconstruction is impossible for many of the signal segments here, and am equally convinced that many signals can almost certainly be restored using existing methods.  

The folder *ASCII_ARCHIVE* contains the selected waveforms written out in an ASCII format for easy visualization, and flagged to the best of my ability (using a few simple python algorithms) which samples are "correct" and which are clipped. The format of the files is as follows (taking the file *19670922.0504.brvk.KODB.SLZb0.030.txt* as an example):  
```
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
...
```
The first line gives the time of the first sample of the time-series, *T0*, the sampling interval in seconds, *DT*, the number of samples present, *NSAMP*, the epoch time (relative to 1970-00-00Z00:00:00.000) of the first sample, and the name of the channel as recorded in the original archive.  
Each of the *NSAMP* subsequent lines contains 3 numbers, *ISAMP*, *RVAL*, and *ICLIP*.  

*ISAMP* is the number of the sample, such that the time of the sample is *T0 + DT*ISAMP*.  
*RVAL* is the value of the original data at this sample.  
*ICLIP* is set to zero if the true value is likely well represented by *RVAL*, *-1* if the true value is likely less than *RVAL* (often the negative clipping value), and *+1* if the true value is likely greater than *RVAL* (often the positive clipping value).  

Many of the flags may be eroneous and spurious values between the clipping limits are likely to be unflagged.  






# References

An, V. A., Ovtchinnikov, V. M., Kaazik, P. B., Adushkin, V. V., Sokolova, I. N., Aleschenko, I. B., Mikhailova, N. N., Kim, W.-Y., Richards, P. G., Patton, H. J., Scott Phillips, W., Randall, G., & Baker, D. (2015). A digital seismogram archive of nuclear explosion signals, recorded at the Borovoye Geophysical Observatory, Kazakhstan, from 1966 to 1996. GeoResJ, 6, 141–163. https://doi.org/10.1016/j.grj.2015.02.014

