"""
    tools for collecting data in flowsets.
"""
import os

from sklearn.cross_validation import train_test_split

class FlowSet(object):
    def __init__(self):
        self.frame_list = []
        self.train_list = []
        self.test_list = []

    def shuffle(self):
        self.train_list, self.test_list = train_test_split(self.frame_list)


class SintelFlowSet(FlowSet):
    def __init__(self, path):
        FlowSet.__init__(self)
        self.collect_sintel_files(path)
        self.shuffle()

    def _get_triple(self, flow_file):
        ext = 'png'
        fprev_file = flow_file.replace('flow','final').replace('flo', ext)
        pre = fprev_file.split('.')[0].split('_')
        pre[2] = str(int(pre[2])+1).zfill(4)
        fnext_file= '.'.join(('_'.join(pre), ext))
        return (flow_file, fprev_file, fnext_file)

    def collect_sintel_files(self, path):
        for parent, dirs, files in os.walk(path):
            self.frame_list += [self._get_triple(os.path.join(parent, file)) for file in files[1:]]
