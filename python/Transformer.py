from sklearn.base import BaseEstimator, TransformerMixin
from skimage.feature import hog
import numpy as np


class RGB2GrayTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return np.dot(X[..., :3], [0.2989, 0.5870, 0.1140]).astype(int)


class HogTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, ppc=(8, 8), cpb=(2, 2), orientations=8):
        self.ppc = ppc
        self.cpb = cpb
        self.orientations = orientations

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None, visualize=False):
        return np.array([hog(x, pixels_per_cell=self.ppc, cells_per_block=self.cpb, orientations=self.orientations,
                             visualize=visualize) for x in X])
