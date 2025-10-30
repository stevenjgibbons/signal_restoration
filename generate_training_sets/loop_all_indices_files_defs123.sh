#!/bin/sh
for indexfile in indices_files/*_256_*.txt
do
  stem=`basename ${indexfile} .txt`
  sh ./run_create_and_train_model.sh   256   ${stem}  def001
  sh ./run_create_and_train_model.sh   256   ${stem}  def002
  sh ./run_create_and_train_model.sh   256   ${stem}  def003
done
