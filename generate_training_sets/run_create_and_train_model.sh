#!/bin/sh
# set -x
scriptname=./run_create_and_train_model.sh
if [ $# != 3 ]
then
  echo
  echo "USAGE: "
  echo "sh $scriptname   seglen   segdefname            model_definition "
  echo "sh $scriptname    256     set00001_256_40000    def001           "
  echo "sh $scriptname    256     set00002_256_40000    def001           "
  echo "sh $scriptname    256     set00003_256_100000   def001           "
  echo
  exit 1
fi
#
seglen=$1
segdefname=$2
modeldef=$3
#
pythonscript=create_and_train_model_${modeldef}.py
if test ! -r ${pythonscript}
then
  echo "script ${scriptname}"
  echo "Failed to find python script ${pythonscript}"
  exit 1
fi
#
arg1="--number_of_consecutive_samples  ${seglen}"
arg2="--segdefname ${segdefname}"
python ${pythonscript}  ${arg1} ${arg2}
# python create_and_train_model_def001.py  ${arg1} ${arg2}
