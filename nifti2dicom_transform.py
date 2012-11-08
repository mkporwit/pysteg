import numpy
nidata2 = numpy.swapaxes(nidata, 0, 1)
nidata2 = numpy.swapaxes(nidata2, 1, 2)
nidata2 = numpy.swapaxes(nidata2, 0, 1)
nidata3 = nib.orientations.flip_axis(nidata2, axis=1)
