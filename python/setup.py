import os
import numpy
from setuptools import setup, Extension

if os.path.exists('src'):
    source_dir = "src"
else:
    source_dir = os.path.join(os.pardir, "src")

include_dirs = [source_dir, numpy.get_include()]
sources = [os.path.join(source_dir, 'snf3x3.c'), ]
extra_compile_args = []
extra_link_args = []
define_macros = []

version_nums = [None, None, None]
with open(os.path.join(source_dir, "snf3x3.h")) as w:
    for line in w:
        for i, chars in enumerate(("MAJOR", "MINOR", "MICRO")):
            if chars in line:
                version_nums[i] = int(line.split()[2])

extension = Extension('snf3x3._snf3x3',
                      include_dirs=include_dirs,
                      sources=['_snf3x3.c'] + sources,
                      extra_compile_args=extra_compile_args,
                      extra_link_args=extra_link_args,
                      define_macros=define_macros)

version = ".".join(["%d" % n for n in version_nums])

setup(name='snf3x3',
      version=version,
      setup_requires=['numpy', 'setuptools'],
      description='This is the SNF3x3 module.',
      author='Atsushi Togo',
      author_email='atz.togo@gmail.com',
      url='https://github.com/atztogo/snf3x3',
      packages=['snf3x3'],
      install_requires=['numpy', ],
      provides=['snf3x3'],
      platforms=['all'],
      ext_modules=[extension])
