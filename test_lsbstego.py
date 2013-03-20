import unittest
import lsbstego
import numpy

class TestLsbStego(unittest.TestCase):
    def setUp(self):
        self.msg = "It's a trap!"

    def testEncodeAndDecodeTile(self):
        data = numpy.zeros(1000, dtype=numpy.uint32)
        encData = lsbstego.encode(data, self.msg, "tile")
        decMsgList = lsbstego.decode(encData)
        decMsg = lsbstego.listToText(decMsgList)
        self.assertEqual(decMsg, "[{0}]".format(self.msg))

    def testEncodeAndDecodeOnRandomTile(self):
        data = numpy.random.randint(0, high=256, size=1000).astype(numpy.uint32)
        encData = lsbstego.encode(data, self.msg, "tile")
        decMsgList = lsbstego.decode(encData)
        decMsg = lsbstego.listToText(decMsgList)
        self.assertEqual(decMsg, "[{0}]".format(self.msg))

    def testEncodeAndDecodeNotile(self):
        data = numpy.zeros(1000, dtype=numpy.uint32)
        encData = lsbstego.encode(data, self.msg, "notile")
        decMsgList = lsbstego.decode(encData)
        decMsg = lsbstego.listToText(decMsgList)
        self.assertEqual(decMsg, "[{0}]".format(self.msg))

    def testEncodeAndDecodeOnRandomNotile(self):
        data = numpy.random.randint(0, high=256, size=1000).astype(numpy.uint32)
        encData = lsbstego.encode(data, self.msg, "notile")
        decMsgList = lsbstego.decode(encData)
        decMsg = lsbstego.listToText(decMsgList)
        self.assertEqual(decMsg, "[{0}]".format(self.msg))


suite = unittest.TestLoader().loadTestsFromTestCase(TestLsbStego)
unittest.TextTestRunner(verbosity=2).run(suite)
