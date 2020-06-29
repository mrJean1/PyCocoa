
# -*- coding: utf-8 -*-

# The setuptools script to build, install and test a PyCocoa distribution.

# Tested with 64-bit Python 2.7.14, 2.7.15, 3.6.5 and 3.7.0 (and setuptools
# 28.8.0) but only on macOS 10.12 Sierra, 10.13 High Sierra and 10.15.5
# Catalina.

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

from setuptools import setup

__all__ = ()
__version__ = '20.06.30'


def _c2(*names):
    return ' :: '.join(names)


def _long_description():
    with open('README.rst', 'rb') as f:
        t = f.read()
        if isinstance(t, bytes):
            t = t.decode('utf-8')
        return t


def _version():
    with open('pycocoa/__init__.py') as f:
        for t in f.readlines():
            if t.startswith('__version__'):
                v = t.split('=')[-1].strip().strip('\'"')
                return '.'.join(map(str, map(int, v.split('.'))))


_KeyWords=('Cocoa', 'cocoa-python', 'cocoavlc', 'ctypes',
           'macOS', 'MacOSX',
           'Objective-C',
           'PyCocoa', 'Python-VLC',
           'VLC', 'VLCplayer')

setup(
    name='PyCocoa',
    packages=['pycocoa'],
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

    package_data={'pycocoa': ['LICENSE']},

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
        _c2('Programming Language', 'Python', '3.7'),
        _c2('Programming Language', 'Python', '3.8'),
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
