#
# create_and_train_model_sbrl_def002.py
#
# sbrl is "scaled by run length" so that the -1 and 1 of the 
# clipped status are multiplied by the number of consecutive clipped samples.
#
# Needs to be supplied with a string indicating the stem of the 
# segment definition file, e.g. set00001_256_40000
# Needs to be provided with an integer with the segment length, e.g. 256
# Please hard code "modeldefIDcode =" below with the name of this model
# For this script, it is def002.
# If we change the model specifications, then we should make a new script
# with "_def002" replaced with something else.
# The output will be saved under "sbrl_models/" + segdefname + "_def002"
# so that we can be sure to separate models trained with different
# models or loss functions.
#
# Differs from def001 by the addition of a Gaussian layer for smoothing.
#

import argparse
import sys
import numpy as np
import tensorflow as tf

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

class GaussianSmoothing(tf.keras.layers.Layer):
    def __init__(self, kernel_size=5, sigma=1.0, **kwargs):
        super(GaussianSmoothing, self).__init__(**kwargs)
        self.kernel_size = kernel_size
        self.sigma = sigma

    def build(self, input_shape):
        x = tf.range(-self.kernel_size // 2 + 1, self.kernel_size // 2 + 1, dtype=tf.float32)
        gauss = tf.exp(-0.5 * tf.square(x) / tf.square(self.sigma))
        gauss /= tf.reduce_sum(gauss)
        self.gauss_filter = tf.reshape(gauss, [self.kernel_size, 1, 1])

    def call(self, inputs):
        inputs = tf.expand_dims(inputs, axis=-1)
        smoothed = tf.nn.conv1d(inputs, self.gauss_filter, stride=1, padding='SAME')
        return tf.squeeze(smoothed, axis=-1)

from sklearn.model_selection import train_test_split

scriptname = sys.argv[0]
numarg     = len(sys.argv) - 1
modeldefIDcode = "def002"

# User-defined parameters
# number_of_consecutive_samples = 256
# segdefname (Stem of the file containing the segment definitions under
# the directory "indices_files")

text       = 'Specify '
text      += ' --number_of_consecutive_samples [integer] '
text      += ' --segdefname [string] '
parser     = argparse.ArgumentParser( description = text )
parser.add_argument("--number_of_consecutive_samples", help="seg. length", default=None, required=True )
parser.add_argument("--segdefname", help="code to identify segment specification", default=None, required=True )

args = parser.parse_args()

number_of_consecutive_samples = int( args.number_of_consecutive_samples )
segdefname                    =      args.segdefname 

# Parameters
number_of_consecutive_samples = 256
random_samples_file = "indices_files" + "/" + segdefname + ".txt"
modelname           = "sbrl_models"   + "/" + segdefname + "_" + modeldefIDcode

# Containers
X_clipped = []
X_status = []
Y_original = []

# Read and process each sample
with open(random_samples_file, "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) != 3:
            continue

        first_node = int(parts[0])
        rscale = float(parts[1])
        filename = parts[2]

        try:
            with open(filename, "r") as data_file:
                data = [float(x.strip()) for x in data_file.readlines()]
        except FileNotFoundError:
            continue

        if first_node + number_of_consecutive_samples > len(data):
            continue

        y = np.array(data[first_node:first_node + number_of_consecutive_samples], dtype=np.float32)
        max_abs = np.max(np.abs(y))
        #
        # We ignore this segment if the maximum absolute value is below 50.0
        # It clearly needs to be greater than zero to avoid a division by zero error
        # but many of the segments with very small values are just noise and/or
        # artefacts.
        #
        if max_abs < 50.0:
            continue
        y = y / max_abs

        y_clipped     = np.clip(y, -rscale, rscale)
        y_status      = np.where(y > rscale, 1, np.where(y < -rscale, -1, 0))
        y_rbcl_status = multiply_by_run_length( y_status )

        X_clipped.append(y_clipped)
        X_status.append(y_rbcl_status)
        Y_original.append(y)

# Convert to numpy arrays
X_clipped = np.array(X_clipped, dtype=np.float32)
X_status = np.array(X_status, dtype=np.float32)
Y_original = np.array(Y_original, dtype=np.float32)

# Combine clipped and status into a single input tensor
X_combined = np.stack((X_clipped, X_status), axis=-1)

# Split into train, eval, test sets
X_train, X_temp, y_train, y_temp = train_test_split(X_combined, Y_original, test_size=0.3, random_state=42)
X_eval, X_test, y_eval, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Define a deeper model with larger kernel sizes and LeakyReLU
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(256, 2)),
    tf.keras.layers.Conv1D(64, kernel_size=3, padding='same'),
    tf.keras.layers.LeakyReLU(),
    tf.keras.layers.Conv1D(64, kernel_size=3, padding='same'),
    tf.keras.layers.LeakyReLU(),
    tf.keras.layers.MaxPooling1D(pool_size=2),
    tf.keras.layers.Conv1D(128, kernel_size=5, padding='same'),
    tf.keras.layers.LeakyReLU(),
    tf.keras.layers.Conv1D(128, kernel_size=5, padding='same'),
    tf.keras.layers.LeakyReLU(),
    tf.keras.layers.MaxPooling1D(pool_size=2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(1024),
    tf.keras.layers.LeakyReLU(),
    tf.keras.layers.Dense(512),
    tf.keras.layers.LeakyReLU(),
    tf.keras.layers.Dense(256),
    GaussianSmoothing(kernel_size=5, sigma=1.0)
])

# Custom loss function with corrected underestimation logic
def custom_loss(y_true, y_pred, status):
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)
    status = tf.cast(status, tf.float32)

    mse = tf.square(y_true - y_pred)

    # First and second derivative smoothness
    smoothness_1 = tf.square(y_pred[:, 1:] - y_pred[:, :-1])
    smoothness_2 = tf.square(y_pred[:, 2:] - 2 * y_pred[:, 1:-1] + y_pred[:, :-2])
    smoothness_loss = tf.reduce_mean(smoothness_1) + 0.5 * tf.reduce_mean(smoothness_2)

    high_clip_mask = status >= 1
    low_clip_mask = status <= -1
    under_high = tf.logical_and(high_clip_mask, y_pred < y_true)
    under_low = tf.logical_and(low_clip_mask, y_pred > y_true)
    underestimation = tf.logical_or(under_high, under_low)

    underestimation_penalty = tf.where(underestimation, tf.square(y_true - y_pred) * 2.0, 0.0)

    total_loss = tf.reduce_mean(mse + underestimation_penalty) + 0.1 * smoothness_loss
    return total_loss

# Optimizer
optimizer = tf.keras.optimizers.Adam()

# Custom training loop
train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train)).batch(64)
eval_dataset = tf.data.Dataset.from_tensor_slices((X_eval, y_eval)).batch(64)

for epoch in range(10):
    print(f"Epoch {epoch+1}/10")
    for step, (x_batch, y_batch) in enumerate(train_dataset):
        with tf.GradientTape() as tape:
            y_pred = model(x_batch, training=True)
            status_batch = x_batch[:, :, 1]
            loss_value = custom_loss(y_batch, y_pred, status_batch)

        grads = tape.gradient(loss_value, model.trainable_weights)
        optimizer.apply_gradients(zip(grads, model.trainable_weights))

    # Evaluate
    eval_loss = tf.keras.metrics.Mean()
    eval_mae = tf.keras.metrics.MeanAbsoluteError()
    for x_batch, y_batch in eval_dataset:
        y_pred = model(x_batch, training=False)
        status_batch = x_batch[:, :, 1]
        eval_loss.update_state(custom_loss(y_batch, y_pred, status_batch))
        eval_mae.update_state(y_batch, y_pred)

    print(f"Validation Loss: {eval_loss.result().numpy()}, Validation MAE: {eval_mae.result().numpy()}")

# Evaluate on test set
y_test_pred = model.predict(X_test)
test_mse = tf.reduce_mean(tf.square(y_test - y_test_pred)).numpy()
test_mae = tf.reduce_mean(tf.abs(y_test - y_test_pred)).numpy()
print(f"Test Loss: {test_mse}, Test MAE: {test_mae}")

# Save the model
model.save( modelname )
