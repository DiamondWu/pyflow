"""creates a test image showing the color encoding scheme."""
#   According to the c++ source code of Daniel Scharstein
#   author: jojo love_faye@live.cn

import numpy as np

from .flow_show import _compute_color

def show_color_scheme():
    """show the color encoding scheme."""
    true_range = 1
    rng = true_range * 1.04

    height, width = 151, 151
    a = height / 2

    x, y = np.meshgrid(range(width), range(height))

    u = x * rng / a - rng
    v = y * rng / a - rng

    img = _compute_color(u, v)

    img[a, :, :] = 0
    img[:, a, :] = 0

    return img
