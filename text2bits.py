import numpy


def text2uint8mask(msg):
    msgarr = numpy.fromstring(msg, dtype=numpy.uint8)
    msglen = msgarr.size
    maskarr = numpy.zeros(msglen * 8, dtype=numpy.uint8)

    arrind = 0
    for char in msgarr:
        for shift in range(8):
            if(arrind == maskarr.size):
                break
            if(char & (0x1 << (7 - shift))):
                maskarr[arrind] = 1
            else:
                maskarr[arrind] = 0
            arrind += 1

    return maskarr


def uint8mask2text(maskarr):
    msg = ""
    destchar = numpy.zeros(1, numpy.uint8)
    if(True != isinstance(maskarr[0], numpy.uint8)):
        raise Exception("uint8mask2text: array is not of type numpy.uint8")

    for char in range(0, maskarr.size, 8):
        destchar[0] = 0
        for shift in range(8):
            if(maskarr[char + shift] == 1):
                destchar[0] = destchar[0] | (0x1 << (7 - shift))

        if(destchar[0] != 0):
            msg += destchar.tostring()

    return msg
