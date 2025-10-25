#
# select_training_samples.py
#
# We specify 
#
# number_of_training_segments  (integer - should be many thousand)
# number_of_consecutive_samples (integer - should correspond to a few seconds of data, e.g. 256)
# ASCII_file_dir          (string: directory containing all of the files with our data samples)
# metadatafile            (string: file containing number of lines in col 1 and filename in col4 of ASCII files)
# output_file             (string: file into which we will write the output)
#
# The output will consist of lines such as
#
#   2400 0.732 outfiles/731026.0427.brvk.KODM.SLE0.030.txtseg00000000
#   8934 0.747 outfiles/19761230.035700.BRV.sN080.026.txtseg00000093
#   1181 0.761 outfiles/19751029.044659.BRV.sE090.026.txtseg00000126
#   459 0.9 outfiles/19801012.0332.BRV.SKM.s07Z0.032.txtseg00001308
#   16829 0.789 outfiles/19880403.013308.BRV.sN080.026.txtseg00001833
#   1083 0.979 outfiles/690723.0247.brvk.KODB.SHE0.030.txtseg00000000
#
# That is to say that the code that generates the training set and forms the Deep Learning Model
# will use samples 2400 to 2400+number_of_consecutive_samples-1 of the series contained
# in the file outfiles/731026.0427.brvk.KODM.SLE0.030.txtseg00000000
# and will set a clipping level at 0.732, artificially clip the time-series and flag where it
# is below, above, and within the interval [-0.732*maxval:0.732*maxval]
# where the trace is normalized by the absolute maximum (so all values between -1 and +1)
#
import argparse
import random
import sys

scriptname = sys.argv[0]
numarg     = len(sys.argv) - 1

# User-defined parameters
# number_of_consecutive_samples = 256
# number_of_training_segments = 40000
# ASCII_file_dir = "outfiles"
# metadata_file = "outfiles_contents_reordered.txt"
# output_file = "random_samples.txt"

text       = 'Specify '
text      += ' --number_of_consecutive_samples [integer] '
text      += ' --number_of_training_segments [integer] '
text      += ' --ASCII_file_dir [string] '
text      += ' --metadata_file [string] '
text      += ' --output_file [string] '
parser     = argparse.ArgumentParser( description = text )
parser.add_argument("--number_of_consecutive_samples", help="seg. length", default=None, required=True )
parser.add_argument("--number_of_training_segments", help="size of dataset", default=None, required=True )
parser.add_argument("--ASCII_file_dir", help="place to find raw files", default=None, required=True )
parser.add_argument("--metadata_file", help="place to find raw files", default=None, required=True )
parser.add_argument("--output_file", help="place to find raw files", default=None, required=True )

args = parser.parse_args()

number_of_consecutive_samples = int( args.number_of_consecutive_samples )
number_of_training_segments   = int( args.number_of_training_segments   )
ASCII_file_dir                =      args.ASCII_file_dir
metadata_file                 =      args.metadata_file  
output_file                   =      args.output_file    

# Read metadata and parse valid entries
file_info = []
with open(metadata_file, "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 4:
            try:
                nnum = int(parts[0])
                filename = f"{ASCII_file_dir}/{parts[3]}"
                if nnum >= number_of_consecutive_samples:
                    file_info.append((nnum, filename))
            except ValueError:
                continue

# Generate random samples
lowrand = 0.1
with open(output_file, "w") as out:
    for _ in range(number_of_training_segments):
        nnum, filename = random.choice(file_info)
        istart = random.randint(0, nnum - number_of_consecutive_samples)
        rscale = round(random.uniform(lowrand, 1.0), 3)
        out.write(f"{istart} {rscale} {filename}\n")

print(f"Done! {number_of_training_segments} samples written to '{output_file}'.")
