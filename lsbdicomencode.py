import sys
import os
import numpy
import dicom

def usage(progname):
    print "Usage: " + progname + " <NIFTI_filename> <message_filename>"
    sys.exit()

def main(*args):
    if(len(args) < 3):
        usage(args[0])

    imgpath = os.path.abspath(args[1])
    msgpath = os.path.abspath(args[2])

    os.path.exists(imgpath)
    os.path.exists(msgpath)

    ds = dicom.read_file(imgpath)
    meta = ds.file_meta

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

    dim = ds.pixel_array.shape
    maskcount = 0
    newdata = ds.pixel_array.ravel()
    for mask in range(0, newdata.size, maskarr.size):
        for offset in range(0, maskarr.size, 1):
            if((mask+offset) == newdata.size):
                break
            if(maskarr[offset] == 0x1):
                newdata[mask+offset] = newdata[mask+offset] | 0x1
            else:
                newdata[mask+offset] = newdata[mask+offset] & (0xFFFF-1)
            
        print maskcount, "of", newdata.size/maskarr.size
        maskcount += 1
        
    newdata.shape = (dim)
    ds.pixel_array = newdata

    print ds.pixel_array.shape, type(ds.pixel_array[0][0][0])
    ds.PixelData = ds.pixel_array.tostring()
    ds.file_meta = meta
    newbasename = "lsb_" + os.path.basename(imgpath)
    ds.save_as(os.path.join(os.path.dirname(imgpath), newbasename))
        
if __name__ == "__main__":
    sys.exit(main(*sys.argv))
