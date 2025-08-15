#!/bin/sh
while read line
do
  python one_file_plot.py $line
done < test_files.txt
#
# Let test_files.txt be a file in which 
# every line is the full path to an ASCII masked seismogram
#
