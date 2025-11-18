#!/bin/sh
# set -x
scriptname=./run_create_and_train_model_sbrl.sh
if [ $# != 3 ]
then
  echo
  echo "USAGE: "
  echo "sh $scriptname   seglen   segdefname            model_definition "
  echo "sh $scriptname    256     set00001_256_40000    def001           "
  echo "sh $scriptname    256     set00002_256_40000    def001           "
  echo "sh $scriptname    256     set00003_256_100000   def001           "
  echo
  echo "sh $scriptname    256     set00001_256_40000    def002           "
  echo "sh $scriptname    256     set00001_256_40000    def003           "
  echo
  echo "sh $scriptname    128     set00004_128_100000   def003_128       "
  echo
  echo "sh $scriptname    256     set0001_256_50000     def001       "
  echo "sh $scriptname    256     set0001_256_50000     def002       "
  echo "sh $scriptname    256     set0001_256_50000     def003       "
  echo "sh $scriptname    256     set0001_256_50000     def004       "
  echo
  echo "sh $scriptname    256     set0002_256_50000     def001       "
  echo "sh $scriptname    256     set0002_256_50000     def002       "
  echo "sh $scriptname    256     set0002_256_50000     def003       "
  echo
  echo "sh $scriptname    256     set0003_256_50000     def001       "
  echo "sh $scriptname    256     set0003_256_50000     def002       "
  echo "sh $scriptname    256     set0003_256_50000     def003       "
  echo
  echo "sh $scriptname    256     set0004_256_50000     def001       "
  echo "sh $scriptname    256     set0004_256_50000     def002       "
  echo "sh $scriptname    256     set0004_256_50000     def003       "
  echo
  echo "sh $scriptname    256     set0005_256_50000     def001       "
  echo "sh $scriptname    256     set0005_256_50000     def002       "
  echo "sh $scriptname    256     set0005_256_50000     def003       "
  echo
  echo "sh $scriptname    256     CODA001_256_100000    def002       "
  echo "sh $scriptname    256     NRA0001_256_100000    def002       "
  echo "sh $scriptname    256     NRA0002_256_10000     def002       "
  echo "sh $scriptname    256     CODA002_256_100000    def002       "
  echo
  echo "sh $scriptname    256     NZ0001_256_100000     def002       "
  echo "sh $scriptname    256     NZall_trial_256_50000     def002       "
  echo
  exit 1
fi
#
seglen=$1
segdefname=$2
modeldef=$3
#
pythonscript=create_and_train_model_sbrl_${modeldef}.py
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
