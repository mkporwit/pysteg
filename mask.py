import numpy
import copy
import pywt


encCount = 0


def applyLSB(data, mask, tiling):
    global encCount
    if(data.size < mask.size):
        raise Exception("Data is not big enough to accommodate the mask")

    if tiling is "tile":
        numMasks = data.size / mask.size
        # grow the mask by tiling it
        mask = numpy.tile(mask, numMasks)
        newmask = copy.deepcopy(mask.astype(type(data[0])))
        # zero-fill the end to match the size of the data
        newmask.resize(data.size)
        if(data.size != newmask.size):
            raise Exception("Data and Mask are not the same size")
    else:
        numMasks = 1
        newmask = mask

    for i in range(0, newmask.size):
        if(newmask[i] == 0):
            data[i] &= (~newmask[i] - 1)
        else:
            data[i] |= newmask[i]

    encCount += numMasks

    return data


def extractLSB(data):
    return (data & 1).astype(numpy.uint8)


def applyHaar(data, mask):
    global encCount
    lcount = 0

    for layer in data:
        coeffs = pywt.dwt2(layer, 'haar')
        cA, (cH, cV, cD) = coeffs
        cdim = cD.shape
        cdata = cD.ravel()
        if(cdata.size < mask.size):
            raise Exception("Data is not big enough to accommodate the mask")

        counts = numpy.bincount(cdata)
        # number of elements with a coefficient of 0 or 1, that can be
        # repurposed to encode the message
        space = counts[0] + counts[1]

        if(space < mask.size):
            print "Layer {0} cannot accommodate the mask. Skipping.".format(lcount)
            continue

        numMasks = space / mask.size
        # grow the mask by tiling it
        mask = numpy.tile(mask, numMasks)
        newmask = copy.deepcopy(mask.astype(type(cdata[0])))
        # zero-fill the end to match the amount of space in this layer
        newmask.resize(space)

        if(cdata.size != newmask.size):
            raise Exception("Mask is not the same size as the space available")

        maskInd = 0
        for offset in range(0, cdata.size):
            if(offset == cdata.size):
                break
            elif(maskInd == newmask.size):
                break
            while(cdata[offset] > 2):
                offset += 1
            cdata[offset] = newmask[maskInd]
            maskInd += 1

        encCount += numMasks

        cD.shape = (cdim)
        coeffs = (cA, (cH, cV, cD))
        layer = pywt.idwt2(coeffs, 'haar')
        lcount += 1
