import tensorflow as tf

class MNISTModel:
    def __init__(self):
        self.loaded = False

    def load(self):
        self._model = tf.keras.models.load_model('1')
        self.loaded = True

    def predict(self, X, feature_names=None, meta=None):
        if not self.loaded:
            self.load()
        output = self._model.predict(X)
        probability = output[0]
        predicted_number = tf.math.argmax(probability)
        return {"predicted_number": predicted_number.numpy().tolist(), "probability": probability.tolist()}