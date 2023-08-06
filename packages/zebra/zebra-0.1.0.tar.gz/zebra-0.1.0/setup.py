#!/usr/bin/env python
import sys
from setuptools import setup

classifiers = ['Development Status :: 5 - Production/Stable',
               'Operating System :: Microsoft :: Windows',
               'Operating System :: Unix',
               "Operating System :: MacOS :: MacOS X",
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 3',
               'Topic :: Printing']

setup(name             = 'zebra',
      version          = '0.1.0',
      py_modules       = ['zebra'],
      author           = 'Ben Croston',
      author_email     = 'ben@croston.org',
      maintainer       = 'Ben Croston',
      maintainer_email = 'ben@croston.org',
      url              = 'http://www.wyre-it.co.uk/zebra/',
      description      = 'A package to communicate with (Zebra) label printers',
      long_description = open('README.rst').read() + '\n' + open('CHANGELOG.rst').read(),
      long_description_content_type = 'text/x-rst',
      platforms        = 'Windows, Unix, MacOSX',
      classifiers      = classifiers,
      license          = 'MIT',
      install_requires = ["pywin32;platform_system=='Windows'"])
