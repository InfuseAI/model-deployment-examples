import tensorflow as tf
import glob, os
import numpy as np

class Score:
    def __init__(self, matchCount, totalCount):
        self.matchCount = matchCount
        self.totalCount = totalCount

class MyModel:
    def __init__(self, model_uri):
        self.matchCount = 0
        self.totalCount = 0
        self.loaded = False
        self.model_uri = model_uri

    def load(self):
        self.model = tf.keras.models.load_model(glob.glob(os.path.join(self.model_uri, '*.h5'))[0])
        self.loaded = True

    def predict_raw(self, X):
        if not self.loaded:
            self.load()
        data = X.get("data", {}).get("ndarray")
        data = np.array(data, dtype='float32')
        probability = self.model.predict(data)[0]
        predicted_number = tf.math.argmax(probability)
        return {"predicted_number": predicted_number.numpy().tolist(), "probability": probability.tolist()}

    def send_feedback(self, X, feature_names, reward, truth, routing=""):
        if feature_names:
            if feature_names == truth:
                self.matchCount += 1
        else:
            pred = self.model.predict(X)
            if str(tf.math.argmax(pred[0]).numpy().tolist()) == truth:
                self.matchCount += 1
        self.totalCount += 1

    def metrics(self):
        if not self.totalCount:
            return [{"type": "GAUGE", "key": "phdeploy_accuracy", "value": 1.0}]
        else:
            return [{"type": "GAUGE", "key": "phdeploy_accuracy", "value": self.matchCount / self.totalCount}]
