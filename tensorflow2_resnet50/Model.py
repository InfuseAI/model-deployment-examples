from io import BytesIO
from PIL import Image
import numpy as np
import tensorflow as tf

class Model:
    def __init__(self):
        self.loaded = False

    def load(self):
        self._model = tf.keras.models.load_model('1')
        self.loaded = True

    def predict(self, X, feature_names=None, meta=None):
        if not self.loaded:
            self.load()
        img = Image.open(BytesIO(X)).convert('RGB')
        img = img.resize((224, 224))
        img = np.array(img).astype(np.float32)
        X = np.copy(img)
        X /= 255.0
        X = np.expand_dims(X, axis=0)
        output = self._model.predict(X)
        probability = output[0]
        predicted_number = tf.math.argmax(probability)
        return {"predicted_number": predicted_number.numpy().tolist(), "probability": probability.tolist()}
