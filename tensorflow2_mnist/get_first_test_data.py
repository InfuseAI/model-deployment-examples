import tensorflow as tf
import argparse
import os
import shutil

mnist = tf.keras.datasets.mnist

(x_train, y_train),(x_test, y_test) = mnist.load_data()

image = tf.image.encode_jpeg(tf.expand_dims(x_test[0], 2), quality=100, format='grayscale')
tf.io.write_file('first_image.jpg', image)

x_train, x_test = x_train / 255.0, x_test / 255.0

print("first tensor")
print(x_test[0].tolist())
print("first number")
print(y_test[0])
