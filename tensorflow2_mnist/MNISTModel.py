import numpy as np
import tensorflow as tf
from PIL import Image
import requests
from io import BytesIO

class MNISTModel:
    def __init__(self):
        self._model = tf.keras.models.load_model('1')

    def predict_raw(self, request):
        data = request.get("data", {})
        input_type = request.get("data", {}).get("type")
        input_data = None
        if input_type == "tensor":
            input_data = data.get("input")
        if input_type == "url":
            response = requests.get(data.get("input"))
            img = Image.open(BytesIO(response.content))
            input_data = tf.keras.preprocessing.image.img_to_array(img, data_format="channels_first")
            input_data = input_data / 255.0
        input_data = np.array(input_data, dtype=np.float64)
        output = self._model.predict(input_data)
        predicted_number = tf.math.argmax(output[0], axis=0)
        return {"predicted_number": predicted_number.numpy().tolist(), "probability": output.tolist()}

