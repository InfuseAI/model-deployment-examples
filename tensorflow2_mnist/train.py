import tensorflow as tf
import argparse
import os
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--dropout', type=float, default=0.2)
args = parser.parse_args()

mnist = tf.keras.datasets.mnist

(x_train, y_train),(x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(512, activation=tf.nn.relu),
  tf.keras.layers.Dropout(args.dropout),
  tf.keras.layers.Dense(10, activation=tf.nn.softmax)
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)
model.evaluate(x_test, y_test)

export_path = "1"
if os.path.isdir(export_path):
    print('Cleaning up\n')
    shutil.rmtree(export_path)

model.save(export_path)
