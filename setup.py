#!/usr/bin/env python

from setuptools import setup, find_packages
from biosas.version import VERSION

setup(name='biosas',
      version=VERSION,
      description='Small Angle Scattering Analysis',
      author='Cameron Neylon',
      author_email='',
      packages=find_packages(),
      include_package_data = True,
      install_requires = [
          'numpy',
          'scipy',
          'matplotlib'
      ]
)

