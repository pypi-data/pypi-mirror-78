import numpy as np


def cosine_distance(x1, x2):
    a = np.matmul(np.transpose(x1), x2)
    b = np.sum(np.multiply(x1, x1))
    c = np.sum(np.multiply(x2, x2))
    return 1 - (a / (np.sqrt(b) * np.sqrt(c)))


def euclidean_distance(x1, x2):
    x = x1 - x2
    d = np.sqrt(np.sum(np.multiply(x, x)))
    return d


def l2_normalize(x):
    return x / np.sqrt(np.sum(np.multiply(x, x)))

