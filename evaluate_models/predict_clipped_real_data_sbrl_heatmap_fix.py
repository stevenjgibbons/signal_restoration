
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from numpy.linalg import lstsq
import argparse
import sys

scriptname = sys.argv[0]
numarg     = len(sys.argv) - 1

text       = 'Specify '
text      += ' --number_of_consecutive_samples [integer] '
text      += ' --modeldir [string] '
text      += ' --modelname [string] '
text      += ' --ASCIIlabelledwaveform [string] '
parser     = argparse.ArgumentParser( description = text )
parser.add_argument("--number_of_consecutive_samples", help="seg. length", default=None, required=True )
parser.add_argument("--modeldir", help="folder in which models are found", default="sbrl_models", required=False )
parser.add_argument("--modelname", help="ID code of model", default=None, required=True )
parser.add_argument("--ASCIIlabelledwaveform", help="name of file with labelled waveform", default=None, required=True )

args = parser.parse_args()

number_of_consecutive_samples = int( args.number_of_consecutive_samples )
modeldir                      =      args.modeldir
modelname                     =      args.modelname
filename                      =      args.ASCIIlabelledwaveform

segment_length = number_of_consecutive_samples
model_path = modeldir + '/' + modelname
model = load_model(model_path)

def multiply_by_run_length(arr):
    result = np.zeros_like(arr)
    n = len(arr)
    i = 0

    while i < n:
        if arr[i] == 0:
            result[i] = 0
            i += 1
        else:
            val = arr[i]
            # Find the length of the consecutive run
            run_start = i
            while i < n and arr[i] == val:
                i += 1
            run_length = i - run_start
            # Assign multiplied values to the run
            result[run_start:i] = val * run_length
    return result

def fix_y_pred(y, y_pred, status, POSRATIO):
    # Step 1: Compute offset
    y_pred_max = np.max(y_pred)
    offset = POSRATIO * y_pred_max - np.min(y_pred)

    # Shift y and y_pred
    y_shift = y + offset
    y_pred_shift = y_pred + offset

    # Step 2: Define ratio_vec where abs(status) < 0.01
    mask_defined = np.abs(status) < 0.01
    ratio_vec = np.full_like(y, np.nan)
    ratio_vec[mask_defined] = y_shift[mask_defined] / y_pred_shift[mask_defined]

    # Step 3: Extend ratio_vec to all indices
    indices = np.arange(len(y))
    if np.any(mask_defined):
        idefmin = np.min(indices[mask_defined])
        idefmax = np.max(indices[mask_defined])

        # Fill before idefmin
        if idefmin > 0:
            ratio_vec[:idefmin] = ratio_vec[idefmin]

        # Fill after idefmax
        if idefmax < len(y) - 1:
            ratio_vec[idefmax + 1:] = ratio_vec[idefmax]

        # Interpolate linearly for undefined values
        defined_indices = indices[~np.isnan(ratio_vec)]
        defined_values = ratio_vec[~np.isnan(ratio_vec)]
        ratio_vec = np.interp(indices, defined_indices, defined_values)

    # Step 4: Compute y_pred_fixed
    y_pred_fixed_shift = y_pred_shift * ratio_vec
    y_pred_fixed = y_pred_fixed_shift - offset

    return y_pred_fixed, ratio_vec

def process_file(filename):
    POSRATIO = 10.0
    with open(filename, "r") as f:
        lines = f.readlines()[1:]

    data = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) != 3:
            continue
        _, y_val, status_val = parts
        data.append((float(y_val), int(status_val)))

    y      = np.array([d[0] for d in data], dtype=np.float32)
    y_orig = np.array([d[0] for d in data], dtype=np.float32)
    stat   = np.array([d[1] for d in data], dtype=np.float32)
    status = multiply_by_run_length( stat )

    if np.all(status == 0):
        print("No clipped samples")
        return

    ## DO NOT SCALE HERE!
    ## max_abs = np.max(np.abs(y))
    ## y_scaled = y / max_abs

    predictions = [[] for _ in range(len(y))]

    # for i in range(len(y) - segment_length + 1):
    for i in range( 0, len(y) - segment_length + 1, 10):
        window_status = status[i:i+segment_length]
        if np.any(window_status != 0):
            print ("Window ", i )
            y_window        = y[i:i+segment_length]
            # max_abs_local   = np.max( np.abs(y_window) )
            window_input = np.stack((y_window, window_status), axis=-1).reshape(1, segment_length, 2)
            y_pred_init   = model.predict(window_input, verbose=0)[0]
            y_pred, ratio_vec = fix_y_pred(y_window, y_pred_init, window_status, POSRATIO)
            for j in range(segment_length):
                if window_status[j] != 0:
                    predictions[i + j].append(y_pred[j])

    # Replace clipped values with mean prediction
    for j in range(len(y)):
        if status[j] != 0 and predictions[j]:
            y[j] = np.mean(predictions[j])

    # Plot
    plt.figure(figsize=(12, 5))
    # unclipped_indices = np.where(status == 0)[0]
    # plt.plot(unclipped_indices, y[unclipped_indices], color='blue', label='Original')
    allindices = np.where(status != 6)[0]
    plt.plot(allindices, y[allindices], color='black', label='Reconstructed')
    plt.plot(allindices, y_orig[allindices], color='green', label='Original')

    clipped_indices = np.where(status != 0)[0]

    plt.title("Predictions for Clipped Samples with Median Replacement")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.tight_layout()
    plt.show()

process_file(filename)
