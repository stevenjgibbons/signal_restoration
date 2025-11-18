#!/bin/sh
numsamp=256
# model=set00001_256_40000_def003
# model=NRA0001_256_100000_def002
# model=CODA001_256_100000_def002
# model=CODA002_256_100000_def002
# model=NZ0001_256_100000_def002
model=NZall_trial_256_50000_def002
# model=set0005_256_200000_def002
# model=set0002_256_200000_def003
# wffile=/home/stg/junk/signal_restoration/ASCII_ARCHIVE/700327.0503.brvk.KODM.SHZm0.030.txt
# wffile=/home/stg/PAPERS/CLIPPING_WORK/ASCII_ARCHIVE/19901024.1459.BRV.TSG.sZ070.026.txt
## wffile=/home/stg/PAPERS/CLIPPING_WORK/ASCII_ARCHIVE/19901024.1459.BRV.TSG.sZ100.026.txt
# wffile=/home/stg/PAPERS/CLIPPING_WORK/ASCII_ARCHIVE/19791024.055959.BRV.TSG.sZ070.026.txt
#BELOW incorrectly labelled. Badly clipped
# wffile=/home/stg/PAPERS/CLIPPING_WORK/ASCII_ARCHIVE/730216.0503.brvk.KODB.SHZ0.030.txt
#BELOW coda only
# wffile=/home/stg/PAPERS/CLIPPING_WORK/ASCII_ARCHIVE/test_fix400.txt
#BELOW full signal with violent clipping
# wffile=/home/stg/PAPERS/CLIPPING_WORK/ASCII_ARCHIVE/730216.0503.brvk.KODB.SHZ0.030_fix400.txt
#BELOW Next is a good NZ signal to test
# wffile=/home/stg/PAPERS/CLIPPING_WORK/ASCII_ARCHIVE/19901024.1459.BRV.TSG.sZ030.026.txt
# The NC602 example does not work well
# wffile=/home/stg/PAPERS/CLIPPING_WORK/ASCII_ARCHIVE/NC602sz_1990-10-24T14.00.00.000.txt
# wffile=/home/stg/PAPERS/CLIPPING_WORK/ASCII_ARCHIVE/NC602sz_1990-10-24T14.00.00.000_clip7000.txt
#noclippedsamples wffile=/data_large/stg/PAPERS/CLIPPING_WORK/BRVK_archive/ASCII_ARCHIVE/19881204.0521.BRV.SKM.s06Z0.096.txt
# wffile=/data_large/stg/PAPERS/CLIPPING_WORK/BRVK_archive/ASCII_ARCHIVE/19881204.0521.BRV.TSG.sE090.026.txt
wffile=/data_large/stg/PAPERS/CLIPPING_WORK/BRVK_archive/ASCII_ARCHIVE/19710927.0603.brvk.KODM.SHZm0.030.txt
arg1="--number_of_consecutive_samples ${numsamp}"
arg2="--modeldir sbrl_models "
arg3="--modelname ${model} "
arg4="--ASCIIlabelledwaveform ${wffile}"
python predict_clipped_real_data_sbrl_heatmap_fix.py ${arg1} ${arg2} ${arg3} ${arg4}
# python predict_clipped_real_data_mean.py ${arg1} ${arg2} ${arg3} ${arg4}
