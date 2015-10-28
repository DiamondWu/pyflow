"""Flow file IO."""
#   According to the c++ source code of Daniel Scharstein
#   author: jojo love_faye@live.cn

import numpy as np

TAG_FLOAT = 202021.25
TAG_STR = 'PIEH'

UNKNOWN_FLOW_THRESHOLD = 1e9

def flow_file_sanity_check(func):
    """decorator to check the flow file name."""
    def flow_file_io_func(*args):
        # sanity check
        file_name = args[0]
        if not file_name.strip():
            raise ValueError("empty filename.")
        if len(file_name.split('.')) == 1:
            raise ValueError("ext required.")
        if file_name.split('.')[-1] != 'flo':
            raise ValueError("ext error.")
        return func(*args)

    return flow_file_io_func

@flow_file_sanity_check
def read_flow_file(file_name):
    """read_flow_file read a flow file FILENAME into 2-band image IMG."""
    with open(file_name, 'rb') as flow_file:
        tag, = np.fromfile(flow_file, np.float32, 1)
        width, height = np.fromfile(flow_file, np.uint32, 2)
        # sanity check
        if tag != TAG_FLOAT:
            raise ValueError("read_flow_file: wrong tag.")
        if not 1 < width < 99999:
            raise ValueError("read_flow_file: illegal width.")
        if not 1 < height < 99999:
            raise ValueError("read_flow_file: illegal height.")

        n_bands = 2

        tmp = np.fromfile(flow_file, np.float32)
        img = tmp.reshape(height, width, n_bands)

    return img

@flow_file_sanity_check
def write_flow_file(file_name, flow):
    """write_flow_file writes a 2-band image IMG into flow file FILENAME."""
    height, width, n_bands = flow.shape
    shape = np.array((width, height), dtype=np.uint32)

    if n_bands != 2:
        raise ValueError('write_flow_file: flow must have two bands')

    with open(file_name, 'wb') as flow_file:
        np.float32(TAG_FLOAT).tofile(flow_file)
        shape.tofile(flow_file)
        flow.astype(np.float32).tofile(flow_file)
