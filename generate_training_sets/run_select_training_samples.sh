#!/bin/sh
# set -x
scriptname=./run_select_training_samples.sh
if [ $# != 3 ]
then
  echo
  echo "USAGE: "
  echo "sh $scriptname   seglen   numseg    setID "
  echo "sh $scriptname    256      40000    set00001  "
  echo "sh $scriptname    256      40000    set00002  "
  echo "sh $scriptname    256     100000    set00003  "
  echo
  echo "sh $scriptname    128     100000    set00004  "
  echo
  echo "Maybe best to include the number of segments in the set names"
  echo "No - not needed as the number of samples is added to the string!"
  echo
  echo "sh $scriptname    256      1000     set0001         "
  echo "sh $scriptname    256      1000     set0002         "
  echo "sh $scriptname    256      1000     set0003         "
  echo "sh $scriptname    256      1000     set0004         "
  echo "sh $scriptname    256      1000     set0005         "
  echo
  echo "sh $scriptname    256      10000    set0001         "
  echo "sh $scriptname    256      10000    set0002         "
  echo "sh $scriptname    256      10000    set0003         "
  echo "sh $scriptname    256      10000    set0004         "
  echo "sh $scriptname    256      10000    set0005         "
  echo
  echo "sh $scriptname    256      50000    set0001         "
  echo "sh $scriptname    256      50000    set0002         "
  echo "sh $scriptname    256      50000    set0003         "
  echo "sh $scriptname    256      50000    set0004         "
  echo "sh $scriptname    256      50000    set0005         "
  echo
  echo "sh $scriptname    256     100000    set0001         "
  echo "sh $scriptname    256     100000    set0002         "
  echo "sh $scriptname    256     100000    set0003         "
  echo "sh $scriptname    256     100000    set0004         "
  echo "sh $scriptname    256     100000    set0005         "
  echo
  echo "sh $scriptname    256     200000    set0001         "
  echo "sh $scriptname    256     200000    set0002         "
  echo "sh $scriptname    256     200000    set0003         "
  echo "sh $scriptname    256     200000    set0004         "
  echo "sh $scriptname    256     200000    set0005         "
  exit 1
fi
#
seglen=$1
numseg=$2
setID=$3
#
# Fixed variables
#
ASCII_file_dir=outfiles
metadatafile=outfiles_contents_reordered.txt
#
if test ! -d indices_files
then
  mkdir indices_files
fi
#
outfile=indices_files/${setID}_${seglen}_${numseg}.txt
if test -r ${outfile}
then
  echo "File ${outfile} already exists. Choose another setID"
  exit 1
fi
arg1="--number_of_consecutive_samples  ${seglen}"
arg2="--number_of_training_segments    ${numseg}"
arg3="--ASCII_file_dir                 ${ASCII_file_dir}"
arg4="--metadata_file                  ${metadatafile}"
arg5="--output_file                    ${outfile}"
echo python select_training_samples.py ${arg1} ${arg2} ${arg3} ${arg4} ${arg5}
python select_training_samples.py ${arg1} ${arg2} ${arg3} ${arg4} ${arg5}
