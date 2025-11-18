import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from scipy.interpolate import CubicSpline

def compute_derivative(vals, status):
    """
    Compute derivative using prioritized finite difference formulas (1)-(8),
    then interpolate missing values with cubic spline for smoothness.

    Parameters:
    -----------
    vals : np.ndarray
        Array of values (length nsamp).
    status : np.ndarray
        Array of same length as vals, where status[i] == 0 means vals[i] is valid.

    Returns:
    --------
    deriv : np.ndarray
        Estimated derivative array.
    """
    nsamp = len(vals)
    deriv = np.full(nsamp, np.nan)

    for i in range(nsamp):
        print ( i, vals[i], status[i] )
        if status[i] != 0:
            continue

        # (1)
        if i >= 2 and i <= nsamp - 3 and all(status[j] == 0 for j in [i-2, i-1, i+1, i+2]):
            deriv[i] = (0.083333 * vals[i-2] - 0.666667 * vals[i-1] +
                        0.666667 * vals[i+1] - 0.083333 * vals[i+2])
            continue

        # (2)
        if i >= 1 and i <= nsamp - 3 and all(status[j] == 0 for j in [i-1, i, i+1, i+2]):
            deriv[i] = (-0.333333 * vals[i-1] - 0.500000 * vals[i] +
                        1.000000 * vals[i+1] - 0.166667 * vals[i+2])
            continue

        # (3)
        if i >= 2 and i <= nsamp - 2 and all(status[j] == 0 for j in [i-2, i-1, i, i+1]):
            deriv[i] = (0.166667 * vals[i-2] - 1.000000 * vals[i-1] +
                        0.500000 * vals[i] + 0.333333 * vals[i+1])
            continue

        # (4)
        if i >= 1 and i <= nsamp - 2 and all(status[j] == 0 for j in [i-1, i+1]):
            deriv[i] = (-0.500000 * vals[i-1] + 0.500000 * vals[i+1])
            continue

        # (5)
        if i >= 2 and i <= nsamp - 1 and all(status[j] == 0 for j in [i-2, i-1, i]):
            deriv[i] = (0.500000 * vals[i-2] - 2.000000 * vals[i-1] +
                        1.500000 * vals[i])
            continue

        # (6)
        if i >= 0 and i <= nsamp - 3 and all(status[j] == 0 for j in [i, i+1, i+2]):
            deriv[i] = (-1.500000 * vals[i] + 2.000000 * vals[i+1] -
                        0.500000 * vals[i+2])
            continue

        # (7)
        if i >= 0 and i <= nsamp - 2 and all(status[j] == 0 for j in [i, i+1]):
            deriv[i] = (-1.000000 * vals[i] + 1.000000 * vals[i+1])
            continue

        # (8)
        if i >= 1 and all(status[j] == 0 for j in [i-1, i]):
            deriv[i] = (-1.000000 * vals[i-1] + 1.000000 * vals[i])
            continue

    
    # Edge condition: set deriv[0] and deriv[-1] to 0 if undefined
    if np.isnan(deriv[0]):
        deriv[0] = 0.0
    if np.isnan(deriv[-1]):
        deriv[-1] = 0.0

    # Interpolate missing values
    valid_idx = np.where(~np.isnan(deriv))[0]
    missing_idx = np.where(np.isnan(deriv))[0]

    if len(valid_idx) > 3:
        cs = CubicSpline(np.arange(nsamp)[valid_idx], deriv[valid_idx])
        deriv[missing_idx] = cs(missing_idx)
    else:
        deriv[missing_idx] = np.interp(missing_idx, valid_idx, deriv[valid_idx])

    return deriv

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
# def fix_y_pred(y, y_pred, status, POSRATIO):

# Parameters
POSRATIO       = 10
segment_length = 256
# clip_threshold = 0.2
clip_threshold = 0.30
# modelname      = "../generate_training_sets/models/set00001_256_40000_def003"
# modelname      = "../generate_training_sets/models/set0001_256_50000_def001"
# modelname      = "../generate_training_sets/models/set00001_256_40000_def001"
# modelname      = "../generate_training_sets/models/set00003_256_100000_def001"
# First line of this file is 
# 11045 0.373 outfiles/19720826.0347.brvk.KODB.SHZ0.030.txtseg00000590
# samplesfile    = "../generate_training_sets/indices_files/set00003_256_100000.txt"
samplesfile    = "./test_256.txt"
# modelname      = "../generate_training_sets/models/set0001_256_50000_def004"
# modelname      = "../generate_training_sets/models/NRA0001_256_100000_def002"
# modelname      = "../generate_training_sets/models/CODA001_256_100000_def002"
# modelname      = "../generate_training_sets/models/NRA0002_256_10000_def002"
# modelname      = "../generate_training_sets/models/CODA002_256_100000_def002"
# modelname      = "../generate_training_sets/models/set0004_256_100000_def003"
# modelname      = "../generate_training_sets/models/NZ0001_256_100000_def002"
modelname      = "../generate_training_sets/sbrl_models/NZall_trial_256_50000_def002"

# Load model (assuming your format works)
model = load_model( modelname )

# Read all lines from random_samples.txt
with open(samplesfile, "r") as f:
    lines = f.readlines()

# Loop through each line
for line_index, line in enumerate(lines):
    line = line.strip()
    if not line:
        continue

    try:
        first_node, rscale, filename = line.split()
        first_node = int(first_node)
        rscale = float(rscale)

        # Read the data file
        with open(filename, "r") as data_file:
            data = [float(x.strip()) for x in data_file.readlines()]

        # Extract the segment
        y = np.array(data[first_node:first_node + segment_length])

        # Normalize
        max_abs = np.max(np.abs(y))
        if max_abs < 50.0:
            continue
        y_scaled = y / max_abs

        # Artificial clipping
        y_clipped = np.copy(y_scaled)
        status = np.zeros(segment_length)

        for i in range(segment_length):
            if y_scaled[i] > clip_threshold:
                y_clipped[i] = clip_threshold
                status[i] = 1
            elif y_scaled[i] < -clip_threshold:
                y_clipped[i] = -clip_threshold
                status[i] = -1

        deriv  = compute_derivative(y, status)
        # Prepare input
        # clip_ratio    = np.mean(np.abs(status) > 0)
        clip_ratio    = 1.0
        status_scaled = multiply_by_run_length( status )
        x_input = np.stack((y_clipped, status_scaled), axis=-1).reshape(1, segment_length, 2)

        # Predict
        y_pred_scaled = model.predict(x_input, verbose=0)[0]
        y_pred = y_pred_scaled * max_abs

        y_pred_fixed, ratio_vec = fix_y_pred(y, y_pred, status, POSRATIO)
        # Plot
        plt.figure(figsize=(10, 4))
        plt.plot(y, label='Original y', color='black')
        plt.plot(y_clipped * max_abs, label='Clipped y', color='blue')
        plt.plot(y_pred_fixed, label='Predicted y', color='grey')
        plt.plot(deriv, label='Derivative', color='magenta')
        plt.title(f"Sample {line_index + 1}: {filename} leaky large kernel")
        plt.xlabel( modelname )
        # plt.xlabel("Sample Index")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error processing line {line_index + 1}: {e}")
        continue
