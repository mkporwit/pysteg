import sys
import os
import numpy
import nibabel as nib

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
    
    newdata = data.ravel()
    for char in range(0, newdata.size, 8):
        destchar[0] = 0
        for shift in range(8):
            if(newdata[char + shift] == 1):
                destchar[0] = destchar[0] | (0x1 << (7 - shift))
            
        if(destchar[0] != 0):
            msg += destchar.tostring()
                
        print lcount, "of", newdata.size/8
        lcount += 1

    msgpath = os.path.abspath(args[2])
    fp = open(msgpath, 'w')
    fp.write(msg)
    fp.close()
        
if __name__ == "__main__":
    sys.exit(main(*sys.argv))
