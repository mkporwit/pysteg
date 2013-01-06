import unittest
import haarstego
import numpy


class TestHaarStego(unittest.TestCase):
    def setUp(self):
        self.msg = "It's a trap!"

    def testEncodeAndDecode(self):
        data = numpy.zeros(1000, dtype=numpy.uint32)
        encData = haarstego.encode(data, self.msg)
        decMsgList = haarstego.decode(encData)
        decMsg = haarstego.listToText(decMsgList)
        self.assertEqual(decMsg, "[{0}]".format(self.msg))

    def testEncodeAndDecodeOnRandom(self):
        data = numpy.random.randint(0, high=256, size=1000).astype(numpy.uint32)
        encData = haarstego.encode(data, self.msg)
        decMsgList = haarstego.decode(encData)
        decMsg = haarstego.listToText(decMsgList)
        self.assertEqual(decMsg, "[{0}]".format(self.msg))


suite = unittest.TestLoader().loadTestsFromTestCase(TestHaarStego)
unittest.TextTestRunner(verbosity=2).run(suite)
