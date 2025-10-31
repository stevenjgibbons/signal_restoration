
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
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
parser.add_argument("--modeldir", help="folder in which models are found", default="models", required=False )
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

def process_file(filename):
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
    status = np.array([d[1] for d in data], dtype=np.float32)

    if np.all(status == 0):
        print("No clipped samples")
        return

    max_abs = np.max(np.abs(y))
    y_scaled = y / max_abs

    predictions = [[] for _ in range(len(y))]

    # for i in range(len(y) - segment_length + 1):
    for i in range( 0, len(y) - segment_length + 1, 20):
        window_status = status[i:i+segment_length]
        if np.any(window_status != 0):
            print ("Window ", i )
            y_clipped = np.clip(y_scaled[i:i+segment_length], -1.0, 1.0)
            window_input = np.stack((y_clipped, window_status), axis=-1).reshape(1, segment_length, 2)
            y_pred_scaled = model.predict(window_input, verbose=0)[0]
            y_pred = y_pred_scaled * max_abs
            for j in range(segment_length):
                if window_status[j] != 0:
                    predictions[i + j].append(y_pred[j])

    # Replace clipped values with mean prediction
    for j in range(len(y)):
        if status[j] != 0 and predictions[j]:
            y[j] = np.mean(predictions[j])

    # Plot
    plt.figure(figsize=(12, 5))
    unclipped_indices = np.where(status == 0)[0]
    # plt.plot(unclipped_indices, y[unclipped_indices], color='blue', label='Original')
    allindices = np.where(status != 6)[0]
    plt.plot(allindices, y[allindices], color='black', label='Reconstructed')
    plt.plot(allindices, y_orig[allindices], color='green', label='Original')

    clipped_indices = np.where(status != 0)[0]
    for j in clipped_indices:
        if predictions[j]:
            hist, _ = np.histogram(predictions[j], bins=100, range=(min(y), max(y)))
            for k, count in enumerate(hist):
                if count > 0:
                    plt.plot(j, min(y) + (k / 100) * (max(y) - min(y)), 'o', color='red', alpha=min(1.0, count / 5), markersize=4)

    plt.title("Predictions for Clipped Samples with Median Replacement")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.tight_layout()
    plt.show()

process_file(filename)
