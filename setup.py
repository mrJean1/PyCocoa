
# -*- coding: utf-8 -*-

# The setuptools script to build, install and test a PyCocoa distribution.

# Tested with 64-bit Python 3.13, 3.12, 3.11, 3.10, 3.9, 3.8.6, 3.7, 3.6,5
# and 2.7.14-18 (and setuptools 28.8.0) but only on macOS 15.3-4 Sequoia,
# 14.6.1 Sonoma, 13.0.1 Ventura, 12.0.1 Monterey, macOS 11.0.1-6.1 (10.16)
# Big Sur, 10.15.5-7 Catalina, 10.13 High Sierra and 10.12 Sierra.

# python setup.py sdist --formats=gztar,bztar,zip  # ztar,tar
# python setup.py bdist_wheel --universal  # XXX
# python setup.py test
# python setup.py install

# <https://Packaging.Python.org/key_projects/#setuptools>
# <https://Packaging.Python.org/distributing/>
# <https://Docs.Python.org/2/distutils/sourcedist.html>
# <https://Docs.Python.org/3.6/distutils/sourcedist.html>
# <https://SetupTools.ReadTheDocs.io/en/latest/setuptools.html#developer-s-guide>
# <https://SetupTools.ReadTheDocs.io/en/latest/setuptools.html#test-build-package-and-run-a-unittest-suite>
# <https://ZetCode.com/articles/packageinpython/>

from os import getenv
from setuptools import setup

__all__ = ()
__version__ = '25.04.03'

_pycocoa_ = 'pycocoa'
_PACKAGE  = _pycocoa_  # 'PyCocoa'


def _c2(*names):
    return ' :: '.join(names)


def _long_description():
    with open('README.rst', 'rb') as f:
        t = f.read()
        if isinstance(t, bytes):
            t = t.decode('utf-8')
        return t


def _version():
    with open(_pycocoa_ + '/__init__.py') as f:
        for t in f.readlines():
            if t.startswith('__version__'):
                v = t.split('=')[-1].strip().strip('\'"')
                c = getenv('PYCOCOA_DIST_RC', '')
                return '.'.join(map(str, map(int, v.split('.')))) + c


_KeyWords=('Apple-Si', 'Apple-Silicon', 'arm64_x86_64',
           'Cocoa', 'cocoa-python', 'cocoavlc', 'ctypes',
           'fault', 'faults', 'faulthandler',
           'macOS', 'MacOSX',
           'Obj-C', 'Objective-C',
           _pycocoa_, 'Python-VLC',
           'segfaulty', 'transparent',
           'VLC', 'VLCplayer')

setup(name=_PACKAGE,
      packages=[_pycocoa_],
      description="Basic Python binding to macOS' Objective-C Cocoa",
      version=_version(),

      author='Jean M. Brouwers',
      author_email='mrJean1@Gmail.com',  # 'mrJean1 at Gmail'
      maintainer='Jean M. Brouwers',
      maintainer_email='mrJean1@Gmail.com',  # 'mrJean1 at Gmail'

      license='MIT',
      keywords=' '.join(_KeyWords),
      url='https://GitHub.com/mrJean1/PyCocoa',

      long_description=_long_description(),

      package_data={_PACKAGE: ['LICENSE']},

      test_suite='test.testsuite',

      zip_safe=False,
      classifiers=[
          _c2('Development Status', '4 - Beta'),
          _c2('Environment', 'MacOS X', 'Cocoa'),
          _c2('Intended Audience', 'Developers'),
          _c2('License', 'OSI Approved', 'BSD License'),
          _c2('License', 'OSI Approved', 'MIT License'),
          _c2('Operating System', 'MacOS', 'MacOS X'),
          _c2('Programming Language', 'Python'),
          _c2('Programming Language', 'Python', '2.7'),
#         _c2('Programming Language', 'Python', '3.7'),
#         _c2('Programming Language', 'Python', '3.8'),
          _c2('Programming Language', 'Python', '3.9'),
          _c2('Programming Language', 'Python', '3.10'),
          _c2('Programming Language', 'Python', '3.11'),
          _c2('Programming Language', 'Python', '3.12'),
          _c2('Programming Language', 'Python', '3.13'),
          _c2('Topic', 'Software Development'),
          _c2('Topic', 'Software Development', 'User Interfaces'),
          _c2('Topic', 'Scientific/Engineering', 'Human Machine Interfaces'),
      ],

#   download_url='https://GitHub.com/mrJean1/PyCocoa',
#   entry_points={},
#   include_package_data=False,
#   install_requires=[],
#   namespace_packages=[],
#   py_modules=[],
)
