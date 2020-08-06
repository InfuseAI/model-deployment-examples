import tensorflow as tf

class MNISTModel:
    def __init__(self):
        self._model = tf.keras.models.load_model('1')

    def predict(self, X, feature_names=None, meta=None):
        output = self._model.predict(X)
        probability = output[0]
        predicted_number = tf.math.argmax(probability)
        return {"predicted_number": predicted_number.numpy().tolist(), "probability": probability.tolist()}

    def tags(self):
        return {}

    def metrics(self):
        return []
