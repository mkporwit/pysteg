import sys
import os
import numpy
import nibabel as nib
import pywt

def usage(progname):
    print "Usage: " + progname + " <NIFTI_filename> <message_filename>"

def main(*args):
    if(len(args) < 3):
        usage(args[0])

    imgpath = os.path.abspath(args[1])
    os.path.exists(imgpath)

    img = nib.load(imgpath)
    data = img.get_data()

    msg = ""
    destchar = numpy.zeros(1, numpy.uint8)
    
    lcount = 0
    for layer in data:
        coeffs = pywt.dwt2(layer, 'haar')
        cA, (cH, cV, cD) = coeffs
        cdata = cD.ravel()        

        shift = 0;
        for offset in range(0, cdata.size):
            if((offset) == cdata.size):
                break
            if(cdata[offset] < 2):
                if(cdata[offset] == 1):
                    destchar[0] = destchar[0] | (0x1 << (7 - shift))
                shift += 1
                if(shift == 8):
                    shift = shift % 8
                    if(destchar[0] != 0):
                        msg += destchar.tostring()
                    
        print lcount
        lcount += 1

    msgpath = os.path.abspath(args[2])
    fp = open(msgpath, 'w')
    fp.write(msg)
    fp.close()
        
if __name__ == "__main__":
    sys.exit(main(*sys.argv))
