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

Now that we have chosen which segments, we have to construct and train the model.  
For this, we need a python script with a name like  
```
create_and_train_model_def001.py
```

Every time that a model definition or loss function is changed, we need to make a new script.
The script is driven by a shell script  
```
sh ./run_create_and_train_model.sh   seglen   segdefname            model_definition
sh ./run_create_and_train_model.sh    256     set00001_256_40000    def001
```

This should generate a model saved in the directory *models* e.g.
```
models/set00001_256_40000_def001
```

The file 
```
linker.sh
```
simply creates a symbolic link to the folder where the waveform segments are held - prevents having long strings in scripts. You will obviously need to adapt this if you use this method.  


The files containing the letters *sbrl* (Scale by running length) replace (in situ) the -1 and +1 of the status functions with -1 or +1 multiplied by the length of the run ... so if you have 4 consecutive -1 values, they will become four consecutive -4 values, etc.  
This is experimental. I do not know if this will improve the models or not.  

