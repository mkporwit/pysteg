import sys
import os
import numpy
import nibabel as nib
import text2bits

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

    dim = data.shape
    newdata = data.ravel()
    print type(newdata[0])
    maskarr = (text2bits.text2uint8mask(msgarr)).astype(type(newdata[0]))
    sys.exit(0)
    maskcount = 0
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

    #lcount = 0
    #for layer in data:
    #    dim1, dim2 = layer.shape
    #    layer = layer.ravel()
    #    for mask in range(0, layer.size, maskarr.size):
    #        for offset in range(0, maskarr.size, 1):
    #            if(mask+offset) == layer.size:
    #                break
    #            if(maskarr[offset] == 0x1):
    #                layer[mask+offset] = layer[mask+offset] | 0x1
    #        else:
    #            layer[mask+offset] = layer[mask+offset] & (0xFFFF-1)
    #            
    #    print lcount
    #    lcount += 1
    #    layer.shape = (dim1, dim2)

    newimg = nib.nifti1.Nifti1Image(newdata, affine, hdr)
    newbasename = "lsb_" + os.path.basename(imgpath)
    nib.nifti1.save(newimg, os.path.join(os.path.dirname(imgpath), newbasename))
    #newimg.to_filename(os.path.join(os.path.dirname(imgpath), newbasename))
        
if __name__ == "__main__":
    sys.exit(main(*sys.argv))
