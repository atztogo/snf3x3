import os
import sys
import numpy
from setuptools import setup, Extension

include_dirs = [numpy.get_include()]

setup(name='snf3x3',
      version='0.1',
      setup_requires=['numpy', 'setuptools'],
      description='This is the SNF3x3 module.',
      author='Atsushi Togo',
      author_email='atz.togo@gmail.com',
      packages=['snf3x3'],
      install_requires=['numpy'],
      provides=['snf3x3'],
      platforms=['all'])

