import tensorflow as tf

class Model:
    def __init__(self):
        self._model = tf.keras.models.load_model('model')

    def predict(self, X, feature_names=None, meta=None):
        output = self._model.predict(X)
        return output
