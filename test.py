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

    flow = pyflow.readFlowFile(r"flow10.flo")
    pyflow.writeFlowFile("test.flo", flow)
    g = pyflow.readFlowFile(r"test.flo")

    assert_equal(flow, g)

    img = pyflow.flow2color(flow)
    pylab.imshow(img)

    color_scheme = pyflow.showColorScheme()
    pylab.imshow(color_scheme)

    prev = cv2.imread("frame10.png")
    next = cv2.imread("frame11.png")
    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    next_gray = cv2.cvtColor(next, cv2.COLOR_BGR2GRAY)
    fbflow = cv2.calcOpticalFlowFarneback(prev_gray, next_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    epe = pyflow.calcEndPointError(fbflow, flow)
    print pyflow.calcStatEPE(epe)
