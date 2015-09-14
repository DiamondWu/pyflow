"""test module"""
#import unittest

#class Test_test(unittest.TestCase):
#    def test_A(self):
#        self.fail("Not implemented")

#if __name__ == '__main__':
#    unittest.main()

if __name__ == "__main__":
    from numpy.testing import assert_equal
    import cv2
    import pylab
    import pyflow

    flow = pyflow.read_flow_file(r"flow10.flo")
    pyflow.write_flow_file("test.flo", flow)
    g = pyflow.read_flow_file(r"test.flo")

    assert_equal(flow, g)

    img = pyflow.flow_to_color(flow)
    pylab.imshow(img)

    pylab.imshow(pyflow.show_color_scheme())

    prev_frame = cv2.imread("frame10.png")
    next_frame = cv2.imread("frame11.png")
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    next_gray = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)
    fbflow = cv2.calcOpticalFlowFarneback(prev_gray, next_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    print pyflow.calc_stat_epe(fbflow, flow)
