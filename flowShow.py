"""
    Color codes flow field.
"""
#   According to the c++ source code of Daniel Scharstein
#   author: jojo love_faye@live.cn

from __future__ import division
import numpy as np

from .flowIO import UNKNOWN_FLOW_THRESHOLD

def _makeColorWheel():
    """
        color encoding scheme

        adapted from the color circle idea described at
        http://members.shaw.ca/quadibloc/other/colint.htm
    """
    RY, YG, GC, CB, BM, MR = 15, 6, 4, 11, 13, 6
    ncols = RY + YG + GC + CB + BM + MR

    colorwheel = np.zeros((ncols, 3))
    col = 0
    colorwheel[0:RY, 0] = 1
    colorwheel[0:RY, 1] = np.arange(RY)/RY
    col += RY
    colorwheel[col:col+YG, 0] = 1 - np.arange(YG)/YG
    colorwheel[col:col+YG, 1] = 1
    col += YG
    colorwheel[col:col+GC, 1] = 1
    colorwheel[col:col+GC, 2] = np.arange(GC)/GC
    col += GC
    colorwheel[col:col+CB, 1] = 1 - np.arange(CB)/CB
    colorwheel[col:col+CB, 2] = 1
    col += CB
    colorwheel[col:col+BM, 2] = 1
    colorwheel[col:col+BM, 0] = np.arange(BM)/BM
    col += BM
    colorwheel[col:col+MR, 2] = 1 - np.arange(MR)/MR
    colorwheel[col:col+MR, 0] = 1

    return colorwheel

def _computeColor(u, v):
    """
        computeColor color codes flow field U, V
    """
    colorwheel = _makeColorWheel()
    ncols, ch = colorwheel.shape

    rad = np.sqrt(u**2 + v**2)
    angle = np.arctan2(-v, -u)/np.pi

    fk = (angle+1)/2 * (ncols - 1)
    k0 = np.floor(fk).astype(np.int)
    k1 = k0 + 1
    k1[k1 == ncols] = 0
    f = fk - k0

    img = np.zeros((u.shape[0], u.shape[1], 3))

    for i in range(ch):
        tmp = colorwheel[:, i]
        color0 = tmp[k0]
        color1 = tmp[k1]
        color = (1-f)*color0 + f*color1

        idx = rad <= 1
        color[idx] = 1 - rad[idx] * (1 - color[idx])
        color[~idx] = color[~idx] * 0.75
        img[:, :, i] = color

    return img

def flow2color(flow, max_flow=0):
    """
        color codes flow field, normalize based on speified value or maximum
        flow present.
    """
    height, width, nBands = flow.shape

    if nBands != 2:
        raise ValueError('flow2color: flow must have two bands')

    u = np.copy(flow[:, :, 0])
    v = np.copy(flow[:, :, 1])

    # fix unknown flow
    idx_unknown = np.logical_or(np.logical_or(abs(u) > UNKNOWN_FLOW_THRESHOLD, abs(v) > UNKNOWN_FLOW_THRESHOLD),\
                                np.logical_or(np.isnan(u), np.isnan(v)))
    u[idx_unknown] = 0
    v[idx_unknown] = 0

    rad = np.sqrt(u**2 + v**2)
    maxrad = max(-1, np.max(rad))

    if max_flow != 0:
        maxrad = max_flow

    if maxrad == 0:
        maxrad = 1 

    u = u / maxrad
    v = v / maxrad

    img = _computeColor(u, v)

    idx = np.tile(idx_unknown.reshape(height, width, 1), [1, 1, 3])
    img[idx] = 0

    return img
