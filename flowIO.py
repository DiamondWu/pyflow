"""
    Flow file IO.
"""
#   According to the c++ source code of Daniel Scharstein
#   author: jojo love_faye@live.cn

import struct

import numpy as np

TAG_FLOAT = 202021.25
TAG_STR = 'PIEH'

UNKNOWN_FLOW_THRESHOLD = 1e9

def readFlowFile(file_name):
    """
        readFlowFile read a flow file FILENAME into 2-band image IMG
    """

    # sanity check
    if not file_name.strip():
        raise ValueError("readFlowFile: empty filename.")

    if len(file_name.split('.')) == 1:
        raise ValueError("readFlowFile: ext required.")
    if (file_name.split('.')[-1] != 'flo'):
        raise ValueError("readFlowFile: ext error.")

    with open(file_name, 'rb') as flow_file:
        (tag, width, height) = struct.unpack('fii', flow_file.read(4 + 4 + 4))
        # sanity check
        if tag != TAG_FLOAT:
            raise ValueError("readFlowFile: wrong tag.")
        if not (1 < width < 99999):
            raise ValueError("readFlowFile: illegal width.")
        if not (1 < height < 99999):
            raise ValueError("readFlowFile: illegal height.")

        nBands = 2

        tmp = np.array(struct.unpack('f'*width*height*nBands, flow_file.read()))
        img = tmp.reshape(height, width, nBands)

    return img

def writeFlowFile(flow, file_name):
    """
        writeFlowFile writes a 2-band image IMG into flow file FILENAME
    """

    # sanity check
    if not file_name.strip():
        raise ValueError("writeFlowFile: empty filename.")

    if len(file_name.split('.')) == 1:
        raise ValueError("writeFlowFile: ext required.")
    if (file_name.split('.')[-1] != 'flo'):
        raise ValueError("writeFlowFile: ext error.")

    height, width, nBands = flow.shape

    if (nBands != 2):
        raise ValueError('writeFlowFile: flow must have two bands')

    with open(file_name, 'wb') as flow_file:
        flow_file.write(struct.pack('fii', TAG_FLOAT, width, height))
        flow_file.write(struct.pack('f'*flow.size, *flow.reshape(flow.size)))
