
# -*- coding: utf-8 -*-

u'''Print L{pycocoa} all public attributes, pycocoa version, Python
release, etc. by using C{python -m pycocoa [-all]} from the command line.
'''
from pycocoa import __all__ as _alls, _locals, _pycocoa_package
from pycocoa.lazily import _isPython3,  _sys
from pycocoa.utils import _all_listing, _all_versions  # PYCHOK expected

if _isPython3:  # get pycocoa.__all__ from .lazily
    from pycocoa import *  # PYCHOK expected

_all_versions(_file_=_pycocoa_package)
if len(_sys.argv) > 1 and '-all'.startswith(_sys.argv[-1]):
    _all_listing(_alls, _locals(), libs=True, _file_=_pycocoa_package)

from pycocoa.runtime import _ObjCDeallocObserver
_ObjCDeallocObserver._testIvar1()

__all__ = ()
__version__ = '25.02.25'

# % python3 -m pycocoa -all
#
# pycocoa.version 25.2.25, .isLazy 1, Python 3.13.2 64bit arm64, macOS 14.6.1
#
#  pycocoa.add_ivar is <function pycocoa.runtime.add_ivar at 0x104995440>,
#  pycocoa.add_method is <function pycocoa.runtime.add_method at 0x1049976a0>,
#  pycocoa.add_protocol is <function pycocoa.runtime.add_protocol at 0x104997740>,
#  pycocoa.add_subclass is <function pycocoa.runtime.add_subclass at 0x1049977e0>,
#  pycocoa.Adict is <class pycocoa.internals.Adict>,
#  pycocoa.AlertPanel is <class pycocoa.panels.AlertPanel>,
#  pycocoa.AlertStyle.Critical=2,
#                    .Info=1,
#                    .Warning=0,
#  pycocoa.Allocator_t is <class pycocoa.octypes.Allocator_t>,
#  pycocoa.App is <class pycocoa.apps.App>,
#  pycocoa.app_title is <function pycocoa.apps.app_title at 0x104a38400>,
#  pycocoa.apps is <module 'pycocoa.apps' from '.../pycocoa/apps.py'>,
#  pycocoa.Array_t is <class ctypes.c_void_p>,
#  pycocoa.aspect_ratio is <function pycocoa.utils.aspect_ratio at 0x104684220>,
#  pycocoa.at is <class pycocoa.nstypes.at>,
#  pycocoa.AutoResize.HeightSizable=1<<4,
#                    .MaxXMargin=1<<2,
#                    .MaxYMargin=1<<5,
#                    .MinXMargin=1,
#                    .MinYMargin=1<<3,
#                    .NotSizable=0,
#                    .Sizable=18,
#                    .WidthSizable=2,
#  pycocoa.AutoResizeError is <class pycocoa.windows.AutoResizeError>,

#  ... <deleted> ...

#  pycocoa.unichar_t is <class ctypes.c_wchar>,
#  pycocoa.unicode2NS is <function pycocoa.pytypes.unicode2NS at 0x1049d5e40>,
#  pycocoa.Union_t is <class pycocoa.octypes.Union_t>,
#  pycocoa.Unknown_t is <class pycocoa.octypes.Unknown_t>,
#  pycocoa.UnknownPtr_t is <class pycocoa.octypes.UnknownPtr_t>,
#  pycocoa.url2NS is <function pycocoa.pytypes.url2NS at 0x1049d5ee0>,
#  pycocoa.URL_t is <class pycocoa.octypes.URL_t>,
#  pycocoa.utils is <module 'pycocoa.utils' from '.../pycocoa/utils.py'>,
#  pycocoa.version is '25.2.25',
#  pycocoa.VoidPtr_t is <class pycocoa.octypes.VoidPtr_t>,
#  pycocoa.Window is <class pycocoa.windows.Window>,
#  pycocoa.WindowError is <class pycocoa.windows.WindowError>,
#  pycocoa.windows is <module 'pycocoa.windows' from '.../pycocoa/windows.py'>,
#  pycocoa.WindowStyle.Closable=2,
#                     .Miniaturizable=1<<2,
#                     .Resizable=1<<3,
#                     .Titled=1,
#                     .Typical=15,
#                     .Utility=1<<4,
#  pycocoa.WindowStyleError is <class pycocoa.windows.WindowStyleError>,
#  pycocoa.windowStyles is <function pycocoa.windows.windowStyles at 0x104ef1bc0>,
#  pycocoa.YES is True or 0x1,
#  pycocoa.z1000str is <function pycocoa.utils.z1000str at 0x104685300>,
#  pycocoa.zfstr is <function pycocoa.utils.zfstr at 0x1046853a0>,
#  pycocoa.zSIstr is <function pycocoa.utils.zSIstr at 0x104685440>,
# )[589]
# pycocoa.version 25.2.25, .isLazy 1, Python 3.13.2 64bit arm64, macOS 14.7.3, oslibs [AppKit, C, CoreFoundation, CoreGraphics, CoreText, Foundation, libc, libobjc, ObjC, PrintCore, PrintCore.framework, Quartz]

# % python3.13 -m pycocoa
# pycocoa.version 25.2.25, .isLazy 1, Python 3.13.2 64bit arm64, macOS 14.7.3

# % python3.12 -m pycocoa
# pycocoa.version 25.2.25, .isLazy 1, Python 3.12.7 64bit arm64, macOS 14.7.3

# % python3.11 -m pycocoa
# pycocoa.version 25.2.25, .isLazy 1, Python 3.11.5 64bit arm64, macOS 14.7.3

# % python3.10 -m pycocoa
# pycocoa.version 25.2.25, .isLazy 1, Python 3.10.8 64bit arm64, macOS 14.7.3

# % python3.9 -m pycocoa
# pycocoa.version 25.2.25, .isLazy 1, Python 3.9.6 64bit arm64, macOS 14.7.3

# % python3.8 -m pycocoa
# pycocoa.version 25.2.25, .isLazy 1, Python 3.8.10 64bit arm64_x86_64, macOS 10.16

# % python3.7 -m pycocoa
# pycocoa.version 25.2.25, .isLazy 1, Python 3.7.6 64bit arm64_x86_64, macOS 10.16

# % python2.7 -m pycocoa
# pycocoa.version 25.2.25, .isLazy None, Python 2.7.18 64bit arm64_x86_64, macOS 10.16

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2018-2025 -- mrJean1 at Gmail -- All Rights Reserved.
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
