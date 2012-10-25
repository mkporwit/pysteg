import mask
import unittest
import numpy


class TestMask(unittest.TestCase):
    def setUp(self):
        self.data = numpy.zeros(20, dtype=numpy.uint32)
        self.mask = numpy.array([0, 1, 0, 1, 0, 1], dtype=numpy.uint8)

    def testApplyAndExtract(self):
        outputMask = mask.extractLSB(mask.applyLSB(self.data, self.mask))
        outputMask.resize(self.mask.size)
        numpy.testing.assert_array_equal(outputMask, self.mask)

    def testApplyAndExtractOnRandom(self):
        data = numpy.random.randint(0, high=2, size=1000).astype(numpy.uint32)
        inputMask = numpy.random.randint(
            0, high=2, size=73).astype(numpy.uint8)
        encodedData = mask.applyLSB(data, inputMask)
        outputMask = mask.extractLSB(encodedData).astype(numpy.uint8)
        outputMask.resize(inputMask.size)
        numpy.testing.assert_array_equal(outputMask, inputMask)


suite = unittest.TestLoader().loadTestsFromTestCase(TestMask)
unittest.TextTestRunner(verbosity=2).run(suite)
