import text2bits as tb
import unittest
import numpy


class TestText2Bits(unittest.TestCase):
    def setUp(self):
        self.plainText = "this is a test text"
        self.uint8Text = "01110100011010000110100101110011001000000110100101110011001000000110000100100000011101000110010101110011011101000010000001110100011001010111100001110100"
        self.iterable = (c for c in self.uint8Text)
        self.uint8Mask = numpy.fromiter(self.iterable, numpy.uint8)

    def test_text2uint8mask(self):
        maskarr = tb.text2uint8mask(self.plainText)
        numpy.testing.assert_array_equal(maskarr, self.uint8Mask)

    def test_uint8mask2text(self):
        msg = tb.uint8mask2text(self.uint8Mask)
        self.assertEqual(msg, self.plainText)

    def test_text2mask2text(self):
        msg = tb.uint8mask2text(tb.text2uint8mask(self.plainText))
        self.assertEqual(msg, self.plainText)

suite = unittest.TestLoader().loadTestsFromTestCase(TestText2Bits)
unittest.TextTestRunner(verbosity=2).run(suite)
