#!/bin/sh
numsamp=256
# model=set00001_256_40000_def003
model=CODA001_256_100000_def002
model=set0005_256_200000_def002
# wffile=/home/stg/junk/signal_restoration/ASCII_ARCHIVE/700327.0503.brvk.KODM.SHZm0.030.txt
wffile=/home/stg/PAPERS/CLIPPING_WORK/ASCII_ARCHIVE/19901024.1459.BRV.TSG.sZ070.026.txt
## wffile=/home/stg/PAPERS/CLIPPING_WORK/ASCII_ARCHIVE/19901024.1459.BRV.TSG.sZ100.026.txt
# wffile=/home/stg/PAPERS/CLIPPING_WORK/ASCII_ARCHIVE/19791024.055959.BRV.TSG.sZ070.026.txt
#BELOW incorrectly labelled. Badly clipped
# wffile=/home/stg/PAPERS/CLIPPING_WORK/ASCII_ARCHIVE/730216.0503.brvk.KODB.SHZ0.030.txt
#BELOW coda only
# wffile=/home/stg/PAPERS/CLIPPING_WORK/ASCII_ARCHIVE/test_fix400.txt
#BELOW full signal with violent clipping
wffile=/home/stg/PAPERS/CLIPPING_WORK/ASCII_ARCHIVE/730216.0503.brvk.KODB.SHZ0.030_fix400.txt
#BELOW Next is a good NZ signal to test
# wffile=/home/stg/PAPERS/CLIPPING_WORK/ASCII_ARCHIVE/19901024.1459.BRV.TSG.sZ030.026.txt
arg1="--number_of_consecutive_samples ${numsamp}"
arg2="--modeldir models "
arg3="--modelname ${model} "
arg4="--ASCIIlabelledwaveform ${wffile}"
python predict_clipped_real_data_mean_heatmap_fix.py ${arg1} ${arg2} ${arg3} ${arg4}
# python predict_clipped_real_data_mean.py ${arg1} ${arg2} ${arg3} ${arg4}
