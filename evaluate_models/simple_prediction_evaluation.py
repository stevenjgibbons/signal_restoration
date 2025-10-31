import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

# Parameters
segment_length = 256
clip_threshold = 0.2
# modelname      = "../generate_training_sets/models/set00001_256_40000_def003"
# modelname      = "../generate_training_sets/models/set0001_256_50000_def001"
# modelname      = "../generate_training_sets/models/set00001_256_40000_def001"
# modelname      = "../generate_training_sets/models/set00003_256_100000_def001"
samplesfile    = "../generate_training_sets/indices_files/set00003_256_100000.txt"
modelname      = "../generate_training_sets/models/set0002_256_200000_def003"

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

        # Prepare input
        x_input = np.stack((y_clipped, status), axis=-1).reshape(1, segment_length, 2)

        # Predict
        y_pred_scaled = model.predict(x_input, verbose=0)[0]
        y_pred = y_pred_scaled * max_abs

        # Plot
        plt.figure(figsize=(10, 4))
        plt.plot(y, label='Original y', color='black')
        plt.plot(y_clipped * max_abs, label='Clipped y', color='blue')
        plt.plot(y_pred, label='Predicted y', color='grey')
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
