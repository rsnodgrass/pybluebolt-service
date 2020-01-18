#!/usr/bin/env python

import os
import sys
import setuptools

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='pybluebolt',
      version='0.0.1',
      packages=[ 'pybluebolt' ],
      description='Python interface for BlueBOLT API',
#      long_description=long_description,
      url='https://github.com/rsnodgrass/pybluebolt',
      author='Ryan Snodgrass',
      author_email='rsnodgrass@gmail.com',
      license='Apache Software License',
      install_requires=[ 'requests>=2.0' ],
      keywords=[ 'flo', 'home automation', 'water monitoring' ], 
      zip_safe=True,
      classifiers=[ "Programming Language :: Python :: 3",
                    "License :: OSI Approved :: Apache Software License",
                    "Operating System :: OS Independent",
      ],
)
