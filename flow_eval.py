"""Performace measures."""
#   author: jojo love_faye@live.cn

from __future__ import division

import numpy as np

from .flow_io import UNKNOWN_FLOW_THRESHOLD

def calc_end_point_error(flow, ground_truth):
    """calculate the end point error."""
    # check shape
    if not flow.shape == ground_truth.shape:
        raise ValueError('flow must have the same size as gt')
    epe = np.sqrt(np.sum((flow - ground_truth) ** 2, axis=2))

    # fix unknown flow
    u_comp = ground_truth[:, :, 0]
    v_comp = ground_truth[:, :, 1]

    idx_unknown = np.logical_or(abs(u_comp) > UNKNOWN_FLOW_THRESHOLD,\
                                abs(v_comp) > UNKNOWN_FLOW_THRESHOLD)
    idx_unknown = np.logical_or(idx_unknown, np.logical_or(np.isnan(u_comp), np.isnan(v_comp)))

    epe[idx_unknown] = 0

    return epe

def calc_stat_epe(flow, ground_truth):
    """calculate the statistic of end point error."""
    epe = calc_end_point_error(flow, ground_truth)

    return (np.mean(epe),
            np.std(epe),
            np.sum(epe > 0.5)/epe.size * 100,
            np.sum(epe > 1.0)/epe.size * 100,
            np.sum(epe > 2.0)/epe.size * 100)
