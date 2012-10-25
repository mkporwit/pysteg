import numpy
import copy


def applyLSB(data, mask):
    if(data.size < mask.size):
        raise Exception("Data is not big enough to accommodate the mask")

    numMasks = data.size / mask.size
    # grow the mask by tiling it
    mask = numpy.tile(mask, numMasks)
    newmask = copy.deepcopy(mask.astype(type(data[0])))
    # zero-fill the end to match the size of the data
    newmask.resize(data.size)

    if(data.size != newmask.size):
        raise Exception("Data and Mask are not the same size")

    for i in range(0, data.size):
        if(newmask[i] == 0):
            data[i] &= (~newmask[i] - 1)
        else:
            data[i] |= newmask[i]

    return data


def extractLSB(data):
    return (data & 1).astype(numpy.uint8)
