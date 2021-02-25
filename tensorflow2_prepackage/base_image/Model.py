import tensorflow as tf

class Model:
    def __init__(self):
        self.loaded = False

    def load(self):
        self._model = tf.keras.models.load_model('model')
        self.loaded = True

    def predict(self, X, feature_names=None, meta=None):
        if not self.loaded:
            self.load()
        output = self._model.predict(X)
        return output

    def tags(self):
        return {}

    def metrics(self):
        return []
