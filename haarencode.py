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
    msgpath = os.path.abspath(args[2])

    os.path.exists(imgpath)
    os.path.exists(msgpath)

    img = nib.load(imgpath)
    data = img.get_data()
    origdata = img.get_data()
    hdr = img.get_header()
    affine = img.get_affine()

    msgfile = open(msgpath, 'r')
    msglen = os.stat(msgpath).st_size
    msg = msgfile.read(msglen)
    msgfile.close()

    msgarr = numpy.fromstring(msg, dtype=numpy.uint8)
    maskarr = numpy.zeros(msglen * 8, dtype=numpy.uint16)

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

    lcount = 0
    for layer in data:
        coeffs = pywt.dwt2(layer, 'haar')
        cA, (cH, cV, cD) = coeffs
        cdim = cD.shape
        cdata = cD.ravel()
        for zero in range(0, cdata.size):
            if(cdata[zero] < 2):
                cdata[zero] = 0
                print type(cdata[zero])
        
        mask = 0 
        for offset in range(0, cdata.size):
            if((offset) == cdata.size):
                break
            elif(mask == maskarr.size):
                break 
            while(cdata[offset] > 2):
                offset += 1
            cdata[offset] = maskarr[mask]
            mask+=1
                    
        cD.shape = (cdim)
        coeffs = (cA, (cH, cV, cD))
        layer = pywt.idwt2(coeffs, 'haar')
        print lcount
        lcount += 1

    newimg = nib.nifti1.Nifti1Image(data, affine, hdr)
    newbasename = "haar_" + os.path.basename(imgpath)
    nib.nifti1.save(newimg, os.path.join(os.path.dirname(imgpath), newbasename))
    #newimg.to_filename(os.path.join(os.path.dirname(imgpath), newbasename))
        
if __name__ == "__main__":
    sys.exit(main(*sys.argv))
