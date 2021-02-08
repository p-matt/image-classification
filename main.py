from python.WebManager import WebManager
import joblib
from python.Utils import get_image_resized
import sys

sys.path.insert(0, './python')
w, h = 90, 90

model = joblib.load("assets/data/GridSearch_model.pkl").best_estimator_
encoder = joblib.load("assets/data/LabelEncoder.pkl")

wm = WebManager()
server = wm.server

if __name__ == '__main__':
    wm.run()


def get_prediction(X):
    X = get_image_resized(X, w, h)
    return encoder.inverse_transform(model.predict(X.reshape(-1, w, h, 3)))[0]
