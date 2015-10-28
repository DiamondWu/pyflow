""" Color codes flow field. """
#   According to the c++ source code of Daniel Scharstein
#   author: jojo love_faye@live.cn

from __future__ import division
import numpy as np

from .io import UNKNOWN_FLOW_THRESHOLD

def _make_color_wheel():
    """ color encoding scheme

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

def _compute_color(u_comp, v_comp):
    """computeColor color codes flow field U, V."""
    color_wheel = _make_color_wheel()
    ncols, n_channels = color_wheel.shape

    rad = np.sqrt(u_comp**2 + v_comp**2)
    angle = np.arctan2(-v_comp, -u_comp)/np.pi

    fk = (angle+1)/2 * (ncols - 1)
    k0 = np.floor(fk).astype(np.int)
    k1 = k0 + 1
    k1[k1 == ncols] = 0
    f = fk - k0

    img = np.zeros((u_comp.shape[0], u_comp.shape[1], 3))

    for i in range(n_channels):
        color = (1-f)*color_wheel[k0, i] + f*color_wheel[k1, i]

        idx = rad <= 1
        color[idx] = 1 - rad[idx] * (1 - color[idx])
        color[~idx] = color[~idx] * 0.75
        img[:, :, i] = color

    return img

def flow_to_color(flow, max_flow=0):
    """color codes flow field, normalize based on speified value or maximum flow present."""
    height, width, n_bands = flow.shape

    if n_bands != 2:
        raise ValueError('flow_to_color: flow must have two bands')

    u_comp = np.copy(flow[:, :, 0])
    v_comp = np.copy(flow[:, :, 1])

    # fix unknown flow
    idx_unknown = np.logical_or(abs(u_comp) > UNKNOWN_FLOW_THRESHOLD,\
                                abs(v_comp) > UNKNOWN_FLOW_THRESHOLD)
    idx_unknown = np.logical_or(idx_unknown, np.logical_or(np.isnan(u_comp), np.isnan(v_comp)))
    u_comp[idx_unknown] = 0
    v_comp[idx_unknown] = 0

    rad = np.sqrt(u_comp**2 + v_comp**2)
    maxrad = max(-1, np.max(rad))

    if max_flow != 0:
        maxrad = max_flow

    if maxrad == 0:
        maxrad = 1

    u_comp = u_comp / maxrad
    v_comp = v_comp / maxrad

    img = _compute_color(u_comp, v_comp)

    idx = np.tile(idx_unknown.reshape(height, width, 1), [1, 1, 3])
    img[idx] = 0

    return img
