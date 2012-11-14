import numpy
import nibabel as nib


def nifti2dicom(data):
    data = numpy.swapaxes(data, 0, 1)
    data = numpy.swapaxes(data, 1, 2)
    data = numpy.swapaxes(data, 0, 1)
    data = nib.orientations.flip_axis(data, axis=1)
    return data


def dicom2nifti(data):
    data = nib.orientations.flip_axis(data, axis=1)
    data = numpy.swapaxes(data, 0, 1)
    data = numpy.swapaxes(data, 1, 2)
    data = numpy.swapaxes(data, 0, 1)
    return data
