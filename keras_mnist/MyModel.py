from keras.models import load_model
from PIL import Image
from io import BytesIO
import numpy as np

class MyModel(object):
    def __init__(self):
        print('calling init()...')
        self.model = load_model('keras-mnist.h5')

    def predict(self, request, names=None, meta=None):
        print('calling predict()...')
        imageStream = BytesIO(request)
        image = Image.open(imageStream).resize((28, 28)).convert('L')

        data = np.asarray(image)
        data = np.expand_dims(data, axis=0)
        data = np.expand_dims(data, axis=-1)
        return self.model.predict(data)

    def tags(self):
        return {}

    def metrics(self):
        return []
