"""
    creates a test image showing the color encoding scheme.
"""
#   According to the c++ source code of Daniel Scharstein
#   author: jojo love_faye@live.cn

import numpy as np

from .flowShow import _computeColor

def showColorScheme():
    true_range = 1
    rng = true_range * 1.04

    height, width = 151, 151
    a = height / 2

    x, y = np.meshgrid(range(width), range(height))

    u = x * rng / a - rng;
    v = y * rng / a - rng;

    img = _computeColor(u, v)

    img[a, :, :] = 0
    img[:, a, :] = 0

    return img
