#!/bin/sh
numsamp=256
model=set00001_256_40000_def003
# wffile=/home/stg/junk/signal_restoration/ASCII_ARCHIVE/700327.0503.brvk.KODM.SHZm0.030.txt
# wffile=/home/stg/PAPERS/CLIPPING_WORK/ASCII_ARCHIVE/19901024.1459.BRV.TSG.sZ070.026.txt
# wffile=/home/stg/PAPERS/CLIPPING_WORK/ASCII_ARCHIVE/19901024.1459.BRV.TSG.sZ030.026.txt
wffile=/home/stg/PAPERS/CLIPPING_WORK/ASCII_ARCHIVE/19901024.1459.BRV.TSG.sZ100.026.txt
arg1="--number_of_consecutive_samples ${numsamp}"
arg2="--modeldir models "
arg3="--modelname ${model} "
arg4="--ASCIIlabelledwaveform ${wffile}"
python predict_clipped_real_data_mean_heatmap.py ${arg1} ${arg2} ${arg3} ${arg4}
# python predict_clipped_real_data_mean.py ${arg1} ${arg2} ${arg3} ${arg4}
