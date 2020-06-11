import numpy
from setuptools import setup, Extension

include_dirs = ['../c', numpy.get_include()]
sources = ['../c/snf3x3.c']
extra_compile_args = []
extra_link_args = []
define_macros = []

extension = Extension('snf3x3._snf3x3',
                      include_dirs=include_dirs,
                      sources=['_snf3x3.c'] + sources,
                      extra_compile_args=extra_compile_args,
                      extra_link_args=extra_link_args,
                      define_macros=define_macros)

setup(name='snf3x3',
      version='0.1',
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
