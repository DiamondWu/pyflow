"""
    Performace measures.
"""
#   author: jojo love_faye@live.cn

from __future__ import division

import numpy as np

from .flowIO import UNKNOWN_FLOW_THRESHOLD

def fix_unknown(flow):
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

def calcEndPointError(flow, gt):
    # check shape
    if not flow.shape == gt.shape:
        raise ValueError('flow must have the same size as gt')
    epe = np.sqrt(np.sum((flow - gt) ** 2, axis = 2))

    # fix unknown flow
    u = gt[:, :, 0]
    v = gt[:, :, 1]
    idx_unknown = np.logical_or(np.logical_or(abs(u) > UNKNOWN_FLOW_THRESHOLD, abs(v) > UNKNOWN_FLOW_THRESHOLD),\
                                np.logical_or(np.isnan(u), np.isnan(v)))
    
    epe[idx_unknown] = 0

    return epe

def calcStatEPE(epe):
    return (np.mean(epe),
            np.std(epe),
            np.sum(epe>0.5)/epe.size,
            np.sum(epe>1.0)/epe.size,
            np.sum(epe>2.0)/epe.size,
            )
