import sys
from distutils.core import setup, Extension



compile_args = ['-O3']
'''
ext = []
ext.append(Extension('DC3D',
                  sources = ['dC3D.so'],
                  extra_compile_args=compile_args))
'''
setup(name='gpsFIT',
      version = '0.1.0',
      description = 'GPS data handeling',
      url = 'https://github.com/nvoss12838/gpsFIT.git',
      author = 'Nick Voss',
      author_email = 'nvoss@mail.usf.edu',
      license = 'MIT',
      py_modules = ['fit','gps','equation_builder'],
      install_requires = [],
      dependency_links = [],
      zip_safe = False,
      )
