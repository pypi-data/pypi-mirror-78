import numpy as np
from huoyanlib.numpy import _raise_hnumpyerror_int_str


def length(x):
    try:
        y = np.array(x)
    except TypeError:
        _raise_hnumpyerror_int_str()
    return np.linalg.norm(y)


def equal(a, b):
    return np.all(a == b)
