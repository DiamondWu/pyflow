#import unittest

#class Test_test(unittest.TestCase):
#    def test_A(self):
#        self.fail("Not implemented")

#if __name__ == '__main__':
#    unittest.main()

if __name__ == "__main__":
    from numpy.testing import assert_equal
    import pylab
    import pyflow as f

    flow = f.readFlowFile(r"flow10.flo")
    f.writeFlowFile("test.flo", flow)
    g = f.readFlowFile(r"test.flo")

    assert_equal(flow, g)

    img = f.flow2color(flow)

    pylab.imshow(img)
