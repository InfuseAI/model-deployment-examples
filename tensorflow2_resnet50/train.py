import argparse
import os
import shutil

import tensorflow as tf
import tensorflow_hub as hub

model = tf.keras.Sequential([hub.KerasLayer("https://tfhub.dev/google/imagenet/resnet_v2_50/classification/5")])
model.build([None, 224, 224, 3])

export_path = "1"
if os.path.isdir(export_path):
    print('Cleaning up\n')
    shutil.rmtree(export_path)

model.save(export_path)
