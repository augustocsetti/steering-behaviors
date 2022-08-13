import numpy as np


def normalizeto(vector, max):
    if np.linalg.norm(vector) > 0:
        return (vector/np.linalg.norm(vector)) * max
    else:
        return np.zeros(2) 