"""
    Performace measures.
"""
#   author: jojo love_faye@live.cn

import numpy as np

from .flowIO import UNKNOWN_FLOW_THRESHOLD
import sys

def fix_unknown(flow):
    height, width, nBands = flow.shape

    if nBands != 2:
        raise ValueError('flow2color: flow must have two bands')

    u = np.copy(flow[:, :, 0])
    v = np.copy(flow[:, :, 1])

    # fix unknown flow
    idx_unknown = np.logical_or(abs(u) > UNKNOWN_FLOW_THRESHOLD, abs(v) > UNKNOWN_FLOW_THRESHOLD)
    u[idx_unknown] = 0
    v[idx_unknown] = 0

    return fixed_flow

def calcEndPointError(self, flow, gt):
    pass

def calcAngleError(self, flow, gt):
    pass
