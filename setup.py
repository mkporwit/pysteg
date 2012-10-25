#!/usr/bin/env python

import setuptools

setuptools.setup(name='pysteg',
                 version='0.1',
                 description='Python scripts for steganography on DICOM and NIfTI images',
                 author='Marcin Krzysztof Porwit',
                 author_email='mkporwit@porwit.net',
                 url='https://github.com/mkporwit/pysteg',
                 packages=setuptools.find_packages(),
                 install_requires=['numpy'],
                 test_suite='tests',
                 )
