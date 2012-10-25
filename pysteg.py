#!/usr/bin/env python

import sys
import os
import lsbstego as lsb
import nibabel as nib
import argparse


def encode(img, args):
    data = img.get_data()
    dim = data.shape
    data = data.ravel()

    if(args.mode == "lsb"):
        data = lsb.encode(data, args.msg, delim=";")
    elif(args.mode == "haar"):
        print "Haar not implemented yet"

    data.shape = (dim)
    import pdb
    pdb.set_trace()
    return nib.Nifti1Image(data, img.get_affine(), img.get_header())


def decode(img, args):
    data = img.get_data()
    data = data.ravel()

    if(args.mode == "lsb"):
        msgDataList = lsb.decode(data, delim=";")
        return lsb.listToText(msgDataList)
    elif(args.mode == "haar"):
        return "Haar not implemented yet"


def main():
    parser = argparse.ArgumentParser(description="Steganographically hides/decodes a message in/from an image")

    subparsers = parser.add_subparsers(help='sub-command help')
    parser_encode = subparsers.add_parser('encode', help='encode help')
    parser_encode.add_argument('imgfile', help='Image file. Encoding will modify it.')
    parser_encode.add_argument('mode', type=str, choices=["lsb", "haar"], help='Encoding to use')
    parser_encode.add_argument('msg', help='Message to encode')
    parser_encode.set_defaults(op='encode')

    parser_decode = subparsers.add_parser('decode', help='decode help')
    parser_decode.add_argument('imgfile', help='Image file containing the message')
    parser_decode.add_argument('mode', type=str, choices=["lsb", "haar"], help='Decoding to use')
    parser_decode.set_defaults(op='decode')

    args = parser.parse_args()

    if not os.path.isfile(args.imgfile):
        print "Can't find input file [{0}]".format(args.imgfile)
        return 2

    img = nib.load(args.imgfile)
    if(args.op == 'encode'):
        img = encode(img, args)
        nib.save(img, args.imgfile)
    elif(args.op == 'decode'):
        msg = decode(img, args)
        print msg

if __name__ == "__main__":
    sys.exit(main())
