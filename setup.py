
# -*- coding: utf-8 -*-

# The setuptools script to build, install and test a PyGeodesy distribution.

# Tested with 64-bit Python 2.7.13, 2.7.14 and 3.6.2 (using setuptools
# 28.8.0) but only on macOS 10.12.6 Sierra.

# python setup.py sdist --formats=gztar,bztar,zip  # ztar,tar
# python setup.py bdist_wheel --universal  # XXX
# python setup.py test
# python setup.py install

# <http://packaging.python.org/key_projects/#setuptools>
# <http://packaging.python.org/distributing/>
# <http://Docs.Python.org/2/distutils/sourcedist.html>
# <http://Docs.Python.org/3.6/distutils/sourcedist.html>
# <http://setuptools.readthedocs.io/en/latest/setuptools.html#developer-s-guide>
# <http://setuptools.readthedocs.io/en/latest/setuptools.html#test-build-package-and-run-a-unittest-suite>
# <http://zetcode.com/articles/packageinpython/>

from setuptools import setup

__all__ = ()
__version__ = '18.04.26'


def _c2(*names):
    return ' :: '.join(names)


def _version():
    with open('pycocoa/__init__.py') as f:
        for t in f.readlines():
            if t.startswith('__version__'):
                v = t.split('=')[-1].strip().strip("'").strip('"')
                return '.'.join(map(str, map(int, v.split('.'))))


def _long_description():
    with open('README.rst', 'rb') as f:
        t = f.read()
        if isinstance(t, bytes):
            t = t.decode('utf-8')
        return t


_KeyWords=('Cocoa', 'cocoavlc', 'ctypes',
           'macOS',
           'Objective-C',
           'PyCocosa', 'python-vlc',
           'VLC', 'VLCplayer')

setup(
    name='PyCocoa',
    packages=['pycocoa'],
    description="Python binding to macOS' Objective-C Cocoa",
    version=_version(),

    author='Jean M. Brouwers',
    author_email='mrJean1@Gmail.com',  # 'mrJean1 at Gmail dot com'
    maintainer='Jean M. Brouwers',
    maintainer_email='mrJean1@Gmail.com',  # 'mrJean1 at Gmail dot com'

    license='MIT',
    keywords=' '.join(_KeyWords),
    url='http://GitHub.com/mrJean1/PyCocoa',

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
        _c2('Programming Language', 'Python', '3.6'),
        _c2('Topic', 'Software Development'),
        _c2('Topic', 'Software Development', 'User Interfaces'),
        _c2('Topic', 'Scientific/Engineering', 'Human Machine Interfaces'),
    ],

#   download_url='http://GitHub.com/mrJean1/PyCocoa',
#   entry_points={},
#   include_package_data=False,
#   install_requires=[],
#   namespace_packages=[],
#   py_modules=[],
)
