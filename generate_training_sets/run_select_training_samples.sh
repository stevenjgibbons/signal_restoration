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
  echo
  echo "sh $scriptname    256      50000    set0001_050000  "
  echo "sh $scriptname    256      50000    set0002_050000  "
  echo "sh $scriptname    256      50000    set0003_050000  "
  echo "sh $scriptname    256      50000    set0004_050000  "
  echo "sh $scriptname    256      50000    set0005_050000  "
  echo
  echo "sh $scriptname    256     100000    set0001_100000  "
  echo "sh $scriptname    256     100000    set0002_100000  "
  echo "sh $scriptname    256     100000    set0003_100000  "
  echo "sh $scriptname    256     100000    set0004_100000  "
  echo "sh $scriptname    256     100000    set0005_100000  "
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
