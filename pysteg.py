#!/usr/bin/env python

import sys
import os
import lsbstego as lsb
import nibabel as nib
import argparse
import dicom
import numpy


def nifti2dicom(data):
    data = numpy.swapaxes(data, 0, 1)
    data = numpy.swapaxes(data, 1, 2)
    data = numpy.swapaxes(data, 0, 1)
    data = nib.orientations.flip_axis(data, axis=1)
    return data


def dicom2nifti(data):
    data = nib.orientations.flip_axis(data, axis=1)
    data = numpy.swapaxes(data, 0, 1)
    data = numpy.swapaxes(data, 1, 2)
    data = numpy.swapaxes(data, 0, 1)
    return data


def encode(img, args):
    if(args.format == "nifti"):
        data = img.get_data()
        data = nifti2dicom(data)
    elif(args.format == "dicom"):
        data = img.pixel_array

    dim = data.shape
    data = data.ravel()

    if(args.mode == "lsb"):
        data = lsb.encode(data, args.msg, delim=";")
    elif(args.mode == "haar"):
        print "Haar not implemented yet"

    data.shape = (dim)
    if(args.format == "nifti"):
        data = dicom2nifti(data)
        return nib.Nifti1Image(data, img.get_affine(), img.get_header())
    elif(args.format == "dicom"):
        img.PixelArray = data.tostring()
        return img


def decode(img, args):
    if(args.format == "nifti"):
        data = img.get_data()
        data = nifti2dicom(data)
    elif(args.format == "dicom"):
        data = img.pixel_array

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
    parser_encode.add_argument('format', type=str, choices=["nifti", "dicom"], help='Format of input file')
    parser_encode.add_argument('mode', type=str, choices=["lsb", "haar"], help='Encoding to use')
    parser_encode.add_argument('msg', help='Message to encode')
    parser_encode.set_defaults(op='encode')

    parser_decode = subparsers.add_parser('decode', help='decode help')
    parser_decode.add_argument('imgfile', help='Image file containing the message to be decoded')
    parser_decode.add_argument('format', type=str, choices=["nifti", "dicom"], help='Format of input file')
    parser_decode.add_argument('mode', type=str, choices=["lsb", "haar"], help='Decoding to use')
    parser_decode.set_defaults(op='decode')

    args = parser.parse_args()

    if not os.path.isfile(args.imgfile):
        print "Can't find input file [{0}]".format(args.imgfile)
        return 2

    if(args.format == "nifti"):
        img = nib.load(args.imgfile)
    elif(args.format == "dicom"):
        img = dicom.read_file(args.imgfile)

    if(args.op == 'encode'):
        img = encode(img, args)
        nib.save(img, args.imgfile)
    elif(args.op == 'decode'):
        msg = decode(img, args)
        print msg

if __name__ == "__main__":
    sys.exit(main())
