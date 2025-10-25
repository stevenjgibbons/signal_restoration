We want to generate training sets (i.e. sets of labelled, clipped signals, together with the complete waveforms).
To do this we need a "bank" of representative signals (that are, to the best of our knowledge, complete) and we want to make sets of training data - repeatably and traceably so that we can determine exactly which set of
signals went into each set of training data.  

For these tests, we have collected 4793 ASCII files containing the values of consecutive samples from the Borovoye data sets that are (at first sight!) not clipped. Sometimes the whole waveform is unclipped. Other times, short segments of the signals are clipped and we extract the values before, between, and after that are assumed to be within range.  

The file "outfiles_contents_reordered.txt" contains the names of all of these ASCII files.  
Representative lines look like this:  

```
     99957      99957    1499355 19830924.0500.BRV.SKM.s09E0.024.txtseg00000000
    102302     102302    1534530 19880914.0358.BRV.SKM.s07Z0.024.txtseg00001199
```

Only columns 1 and 4 matter - the number of lines in the file and the name of the file.  

For each training set, we want a large number of segments of a given length
(e.g. 256 samples - which, given 40 Hz data - is 6.4 seconds long).  
This length should contain many cycles of short period seismic data - both
for P-waves, coda, and surface waves - but not be so long that it contains full waveforms
and not be so short that we vary trivially.  
This parameter  
```
number_of_consecutive_samples
```
should be experimented with.  

The python program select_training_samples.py generates the index files and the shell script
run_select_training_samples.sh orchestrates this script, generating the output file names,
such that  

```
sh run_select_training_samples.sh

# sh ./run_select_training_samples.sh   seglen   numseg    setID
sh ./run_select_training_samples.sh    256      40000    set00001
sh ./run_select_training_samples.sh    256      40000    set00002
sh ./run_select_training_samples.sh    256     100000    set00003
```

generates the files

```
indices_files/set00001_256_40000.txt
indices_files/set00002_256_40000.txt
indices_files/set00003_256_100000.txt
```


