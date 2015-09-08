"""
    Color codes flow field.
"""
#   According to the c++ source code of Daniel Scharstein
#   author: jojo love_faye@live.cn

import numpy
import pylab
import pyflow

UNKNOWN_FLOW_THRESHOLD = 1e9
UNKNOWN_FLOW = 1e10

def _makeColorWheel():
    """
        color encoding scheme

        adapted from the color circle idea described at
        http://members.shaw.ca/quadibloc/other/colint.htm
    """
    RY, YG, GC, CB, BM, MR = 15,  6,  4, 11, 13,  6
    ncols = RY + YG + GC + CB + BM + MR

    colorwheel = numpy.zeros((ncols, 3))
    col = 0
    colorwheel[0:RY, 0] = 1
    colorwheel[0:RY, 1] = numpy.arange(RY, dtype = float)/RY
    col += RY
    colorwheel[col:col+YG, 0] = 1 - numpy.arange(YG, dtype = float)/YG
    colorwheel[col:col+YG, 1] = 1
    col += YG
    colorwheel[col:col+GC, 1] = 1
    colorwheel[col:col+GC, 2] = numpy.arange(GC, dtype = float)/GC
    col += GC
    colorwheel[col:col+CB, 1] = 1 - numpy.arange(CB, dtype = float)/CB
    colorwheel[col:col+CB, 2] = 1
    col += CB
    colorwheel[col:col+BM, 2] = 1
    colorwheel[col:col+BM, 0] = numpy.arange(BM, dtype = float)/BM
    col += BM
    colorwheel[col:col+MR, 2] = 1 - numpy.arange(MR, dtype = float)/MR
    colorwheel[col:col+MR, 0] = 1

    return colorwheel

def _computeColor(u, v):
    """
        computeColor color codes flow field U, V
    """
    nan_idx = numpy.logical_or(numpy.isnan(u), numpy.isnan(v))
    u[nan_idx] = 0
    v[nan_idx] = 0

    colorwheel = _makeColorWheel()
    ncols, ch = colorwheel.shape

    rad = numpy.sqrt(u**2 + v**2)
    angle = numpy.arctan2(-v, -u)/numpy.pi

    fk = (angle+1)/2 * (ncols - 1)
    k0 = numpy.floor(fk).astype(numpy.int)
    k1 = k0 + 1
    k1[k1 == ncols] = 0
    f = fk - k0

    img = numpy.zeros((u.shape[0], u.shape[1], 3))

    for i in range(ch):
        tmp = colorwheel[:, i]
        color0 = tmp[k0]
        color1 = tmp[k1]
        color = (1-f)*color0 + f*color1

        idx = rad <= 1
        color[idx] = 1 - rad[idx] * (1 - color[idx])
        color[~idx] = color[~idx] * 0.75
        img[:, :, i] = color * (1 - nan_idx)

    return img

def flow2color(flow, max_flow = 0):
    """
        color codes flow field, normalize based on speified value or maximum
        flow present.
    """
    height, width, nBands = flow.shape

    if (nBands != 2):
        raise ValueError('flow2color: flow must have two bands')

    u = flow[:, :, 0]
    v = flow[:, :, 1]

    # fix unknown flow
    idx_unknown = numpy.logical_or(abs(u) > UNKNOWN_FLOW_THRESHOLD, abs(v) > UNKNOWN_FLOW_THRESHOLD)
    u[idx_unknown] = 0
    v[idx_unknown] = 0

    rad = numpy.sqrt(u**2 + v**2)
    maxrad = max(-1, numpy.max(rad))

    if max_flow != 0:
        maxrad = max_flow

    u = u/(maxrad + numpy.spacing(1))
    v = v/(maxrad + numpy.spacing(1))

    img = _computeColor(u, v)

    idx = numpy.tile(idx_unknown.reshape(height, width, 1), [1, 1, 3])
    img[idx] = 0

    return img

if __name__ == "__main__":
    import pylab
    import flowIO
    
    flow = flowIO.readFlowFile(r"flow10.flo")
    img = flow2color(flow)

    pylab.imshow(img)