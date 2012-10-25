#!/usr/bin/env python

#import lsbstego
#import nibabel
import argparse


def main():
    parser = argparse.ArgumentParser(description="Steganographically hides/decodes a message in/from an image")

    subparsers = parser.add_subparsers(help='sub-command help')
    parser_encode = subparsers.add_parser('encode', help='encode help')
    parser_encode.add_argument('infile', nargs=1, type=argparse.FileType('r'), help='Input image file')
    parser_encode.add_argument('mode', nargs=1, type=str, choices=["lsb", "haar"], help='Encoding to use')
    parser_encode.add_argument('msg', help='Message to encode')
    parser_encode.add_argument('outfile', nargs=1, type=argparse.FileType('w'), help='file to write encoded image to')
    parser_encode.set_defaults(op='encode')

    parser_decode = subparsers.add_parser('decode', help='decode help')
    parser_decode.add_argument('infile', nargs=1, type=argparse.FileType('r'), help='Input image file containing the message')
    parser_decode.add_argument('mode', nargs=1, type=str, choices=["lsb", "haar"], help='Decoding to use')
    parser_decode.add_argument('outfile', nargs=1, type=argparse.FileType('w'), default=sys.stdout, help='file to write decoded message to')
    parser_decode.set_defaults(op='decode')

    args = parser.parse_args()

    print args

if __name__ == "__main__":
    import sys
    sys.exit(main())
