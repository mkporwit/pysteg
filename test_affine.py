import unittest
import numpy
import copy
import affine


class TestAffine(unittest.TestCase):
    def setUp(self):
        self.data = numpy.random.randint(0, high=256, size=170 * 256 * 256).astype(numpy.uint32)
        self.data.shape = (170, 256, 256)

    def testIdemNifti2Dicom2Nifi(self):
        dicom_data = copy.deepcopy(self.data)
        dicom_data = affine.nifti2dicom(affine.dicom2nifti(dicom_data))
        self.assertTrue(numpy.array_equal(dicom_data, self.data))


suite = unittest.TestLoader().loadTestsFromTestCase(TestAffine)
unittest.TextTestRunner(verbosity=2).run(suite)
