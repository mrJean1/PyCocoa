
# -*- coding: utf-8 -*-

u'''Print L{pycocoa} all public attributes, pycocoa version, Python
release, etc. by using C{python -m pycocoa [-all]} from the command line.
'''
from pycocoa.internals import _presegfaulty, _pycocoa_
from pycocoa.lazily import _isPython3,  sys
from pycocoa.utils import _all_listing, _all_versions  # PYCHOK expected
# import sys  # from .lazily

_all_versions(_file_=_pycocoa_)
_presegfaulty()  # see .__init__

if len(sys.argv) > 1 and '-all'.startswith(sys.argv[-1]):
    from pycocoa import __all__ as _alls, _locals, _pycocoa_package
    assert _pycocoa_ == _pycocoa_package
    if _isPython3:  # get pycocoa.__all__ from .lazily
        from pycocoa import *  # PYCHOK expected
    _all_listing(_alls, _locals(), libs=True, _file_=_pycocoa_)
else:
    from pycocoa.runtime import _ObjCDeallocObserver
    _ObjCDeallocObserver._testIvar1()

__all__ = ()
__version__ = '25.03.23'

# % python3 -m pycocoa -all
#
# pycocoa.version 25.3.25, .isLazy 1, Python 3.13.2 64bit arm64, macOS 15.3.2
#
# pycocoa.__all__ = tuple(
#  pycocoa.add_ivar is <function pycocoa.runtime.add_ivar at 0x1052e82c0>,
#  pycocoa.add_method is <function pycocoa.runtime.add_method at 0x1052ea520>,
#  pycocoa.add_protocol is <function pycocoa.runtime.add_protocol at 0x1052ea5c0>,
#  pycocoa.add_subclass is <function pycocoa.runtime.add_subclass at 0x1052ea660>,
#  pycocoa.Adict is <class pycocoa.internals.Adict>,
#  pycocoa.AlertPanel is <class pycocoa.panels.AlertPanel>,
#  pycocoa.AlertStyle.Critical=2,
#                    .Info=1,
#                    .Warning=0,
#  pycocoa.Allocator_t is <class pycocoa.octypes.Allocator_t>,
#  pycocoa.App is <class pycocoa.apps.App>,
#  pycocoa.app_title is <function pycocoa.apps.app_title at 0x10562b240>,
#  pycocoa.apps is <module 'pycocoa.apps' from '/Users/jean/Library/CloudStorage/Dropbox/Projects/ObjC-Cocoa/PyCocoa/pycocoa/apps.py'>,
#  pycocoa.Array_t is <class ctypes.c_void_p>,
#  pycocoa.aspect_ratio is <function pycocoa.utils.aspect_ratio at 0x105190a40>,
#  pycocoa.at is <class pycocoa.nstypes.at>,
#  pycocoa.AutoResize.HeightSizable=16 or 1<<4,
#                    .MaxXMargin=4 or 1<<2,
#                    .MaxYMargin=32 or 1<<5,
#                    .MinXMargin=1,
#                    .MinYMargin=8 or 1<<3,
#                    .NotSizable=0,
#                    .Sizable=18,
#                    .WidthSizable=2,
#  pycocoa.AutoResizeError is <class pycocoa.windows.AutoResizeError>,

#  ... <deleted> ...

#  pycocoa.UniChar_t is <class ctypes.c_ushort>,
#  pycocoa.unichar_t is <class ctypes.c_wchar>,
#  pycocoa.unicode2NS is <function pycocoa.pytypes.unicode2NS at 0x105181260>,
#  pycocoa.Union_t is <class pycocoa.octypes.Union_t>,
#  pycocoa.Unknown_t is <class pycocoa.octypes.Unknown_t>,
#  pycocoa.UnknownPtr_t is <class pycocoa.octypes.UnknownPtr_t>,
#  pycocoa.url2NS is <function pycocoa.pytypes.url2NS at 0x105181300>,
#  pycocoa.URL_t is <class pycocoa.octypes.URL_t>,
#  pycocoa.utils is <module 'pycocoa.utils' from '/Users/jean/Dropbox/Projects/ObjC-Cocoa/PyCocoa/pycocoa/utils.py'>,
#  pycocoa.version is '25.3.18',
#  pycocoa.VoidPtr_t is <class pycocoa.octypes.VoidPtr_t>,
#  pycocoa.Window is <class pycocoa.windows.Window>,
#  pycocoa.WindowError is <class pycocoa.windows.WindowError>,
#  pycocoa.windows is <module 'pycocoa.windows' from '/Users/jean/Dropbox/Projects/ObjC-Cocoa/PyCocoa/pycocoa/windows.py'>,
#  pycocoa.WindowStyle.Closable=2,
#                     .Miniaturizable=4 or 1<<2,
#                     .Resizable=8 or 1<<3,
#                     .Titled=1,
#                     .Typical=15,
#                     .Utility=16 or 1<<4,
#  pycocoa.WindowStyleError is <class pycocoa.windows.WindowStyleError>,
#  pycocoa.windowStyles is <function pycocoa.windows.windowStyles at 0x1089aa660>,
#  pycocoa.YES is True or 0x1,
#  pycocoa.z1000str is <function pycocoa.utils.z1000str at 0x104de2480>,
#  pycocoa.zfstr is <function pycocoa.utils.zfstr at 0x104de2520>,
#  pycocoa.zSIstr is <function pycocoa.utils.zSIstr at 0x104de25c0>,
# )[600]
# pycocoa.version 25.3.25, .isLazy 1, Python 3.13.2 64bit arm64, macOS 15.3.2, oslibs [AppKit, C, CoreFoundation, CoreGraphics, CoreText, Foundation, libc, libobjc, ObjC, PrintCore, Quartz]

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
# pycocoa.version 25.2.28, .isLazy None, Python 2.7.18 64bit arm64_x86_64, macOS 10.16

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
