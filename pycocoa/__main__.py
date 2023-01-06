
# -*- coding: utf-8 -*-

u'''Print L{pycocoa} all public attributes, PyCocoa version, Python
release, etc. by using C{python -m pycocoa [-all]} from the command line.
'''
import sys

from pycocoa import __all__ as _all_, _locals, _pycocoa as _package
from pycocoa.utils import _all_listing, _all_versions, _Python3  # PYCHOK expected

if _Python3:  # get pycocoa.__all__ from .lazily
    from pycocoa import *  # PYCHOK expected

_all_versions(_file_=_package)
if len(sys.argv) > 1 and '-all'.startswith(sys.argv[-1]):
    _all_listing(_all_, _locals(), libs=True, _file_=_package)

from pycocoa.runtime import _nsDeallocObserverIvar1
_nsDeallocObserverIvar1()  # check the _NSDeallocObserver class

__all__ = ()
__version__ = '23.01.06'

# % python3 -m pycocoa
# pycocoa.version 23.01.06, .isLazy 1, Python 3.11.0 64bit arm64, macOS 13.0.1

# % python3.10 -m pycocoa
# pycocoa.version 23.1.6, .isLazy 1, Python 3.10.8 64bit arm64, macOS 13.0.1

# % python3.9 -m pycocoa
# pycocoa.version 23.1.6, .isLazy 1, Python 3.9.6 64bit arm64, macOS 13.0.1

# % python3.8 -m pycocoa
# pycocoa.version 23.1.6, .isLazy 1, Python 3.8.10 64bit arm64_x86_64, macOS 10.16

# % python3.7 -m pycocoa
# pycocoa.version 23.1.6, .isLazy 1, Python 3.7.6 64bit arm64_x86_64, macOS 10.16

# % python3.6 -m pycocoa
# pycocoa.version 23.1.6, .isLazy None, Python 3.6.5 64bit arm64_x86_64, macOS 10.16

# % python2.7 -m pycocoa
# pycocoa.version 23.1.6, .isLazy None, Python 2.7.18 64bit arm64_x86_64, macOS 10.16

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2018-2023 -- mrJean1 at Gmail -- All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
