#!/bin/sh
scriptname=./cut_256_samples.sh
if [ $# != 1 ]
then
  echo
  echo "USAGE: "
  echo "sh $scriptname   startsamp "
  echo "sh $scriptname    2560     "
  echo
  exit 1
fi
#
inputfile=19710927.0603.brvk.KODM.SHZm0.030.txt
nsamp=$1
esamp=`expr $nsamp + 256`
outfile=cut_segments/startsamp_${nsamp}.txt
awk 'NR > NSAMP && NR <= ESAMP {print $2}' NSAMP=$nsamp ESAMP=$esamp $inputfile > ${outfile}
