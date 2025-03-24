
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Deprecated classes, constants, functions, internals, etc.
'''
from pycocoa import fonts as _fonts
from pycocoa.getters import _Cache2
from pycocoa.internals import _property2, proxy_RO, _sortuples
from pycocoa.lazily import _ALL_LAZY, _Dmain_
from pycocoa.oslibs import Libs
from pycocoa.printers import _libPC
from pycocoa.runtime import OBJC_ASSOCIATION as _OBJC_AN
from pycocoa.screens import Screen as _Screen

__all__ = _ALL_LAZY.deprecated
__version__ = '25.03.16'

libAppKit     =  Libs.AppKit
'''DEPRECATED on 2025.02.25, use C{Libs.AppKit}'''
libCF         =  Libs.CoreFoundation
'''DEPRECATED on 2025.02.25, use C{Libs.CoreFoundation}'''
libCG         =  Libs.CoreGraphics
'''DEPRECATED on 2025.02.25, use C{Libs.CoreGraphics}'''
libCT         =  Libs.CoreText
'''DEPRECATED on 2025.02.25, use C{Libs.CoreText}'''
libFoundation =  Libs.Foundation
'''DEPRECATED on 2025.02.25, use C{Libs.Foundation}'''
libobjc       =  Libs.ObjC
'''DEPRECATED on 2025.02.25, use C{Libs.ObjC}'''
libPC         = _libPC
'''DEPRECATED on 2025.02.25, use C{Libs.PrintCore}'''

OBJC_ASSOCIATION_ASSIGN           = _OBJC_AN.ASSIGN
'''DEPRECATED on 2025.02.20, use C{OBJC_ASSOCIATION.ASSIGN}.'''
OBJC_ASSOCIATION_COPY             = _OBJC_AN.COPY
'''DEPRECATED on 2025.02.20, use C{OBJC_ASSOCIATION.COPY}.'''
OBJC_ASSOCIATION_COPY_NONATOMIC   = _OBJC_AN.COPY_NONATOMIC
'''DEPRECATED on 2025.02.20, use C{OBJC_ASSOCIATION.COPY_NONATOMIC}.'''
OBJC_ASSOCIATION_RETAIN           = _OBJC_AN.RETAIN
'''DEPRECATED on 2025.02.20, use C{OBJC_ASSOCIATION.RETAIN}.'''
OBJC_ASSOCIATION_RETAIN_NONATOMIC = _OBJC_AN.RETAIN_NONATOMIC
'''DEPRECATED on 2025.02.20, use C{OBJC_ASSOCIATION.RETAIN_NONATOMIC}.'''


class _DeprecatedScreen(_Screen):
    '''(INTERNAL) DEPRECATED C{Screen}s.'''
    # _name = ...
    def __init__(self, *args, **kwds):  # PYCHOK signature
        _DeprecatedScreen._name = type(self).__name__[:-6]
        _Screen.__init__(self, *args, **kwds)


class BuiltInScreen(_DeprecatedScreen):
    '''DEPRECATED on 2025.03.16, use C{Screens.BuiltIn}.'''
    pass


class Cache2(_Cache2):
    '''DEPRECATED on 2025.02.15, I{to be removed}.'''
    pass


class DeepestScreen(_DeprecatedScreen):
    '''DEPRECATED on 2025.03.16, use C{Screens.Deepest}.'''
    pass


class ExternalScreen(_DeprecatedScreen):
    '''DEPRECATED on 2025.03.16, use C{Screens.External}.'''
    pass


class MainScreen(_DeprecatedScreen):
    '''DEPRECATED on 2025.03.16, use C{Screens.Main}.'''
    pass


class module_property_RO(proxy_RO):
    '''DEPRECATED on 2025.02.09, use C{proxy_RO}.'''
    pass


def fontfamilies(*prefixes):
    '''DEPRECATED on 25.03.13, use C{fontFamilies}.'''
    return _fonts.fontFamilies(*prefixes)


def fontnamesof(family):
    '''DEPRECATED on 25.03.13, use C{fontNamesOf}.'''
    return _fonts.fontNamesOf(family)


def fontsof(family, **size_weight):
    '''DEPRECATED on 25.03.13, use C{fontsOf}.'''
    return _fonts.fontsOf(family, **size_weight)


def fontsof4(family):
    '''DEPRECATED on 25.03.13, use C{fontsOf4}.'''
    return _fonts.fontsOf4(family)


def get_libPC():
    '''DEPRECATED on 25.02.25, use C{Libs.PrintCore}.'''
    return libPC


def get_libs():
    '''DEPRECATED on 25.02.25, use C{Libs}.'''
    return Libs.copy()


def property2(inst, name):
    '''DEPRECATED on 25.02.16, I{to be removed}.'''
    return _property2(inst, name)


def sortuples(iterable):
    '''DEPRECATED on 25.02.09, I{to be removed}.'''
    return _sortuples(iterable)


if __name__ == _Dmain_:

    from pycocoa.utils import _all_listing

    _all_listing(__all__, locals())

#  % python3 -m pycocoa.deprecated

# pycocoa.deprecated.__all__ = tuple(
#  pycocoa.deprecated.BuiltInScreen is <class .BuiltInScreen>,
#  pycocoa.deprecated.Cache2 is <class .Cache2>,
#  pycocoa.deprecated.DeepestScreen is <class .DeepestScreen>,
#  pycocoa.deprecated.ExternalScreen is <class .ExternalScreen>,
#  pycocoa.deprecated.fontfamilies is <function .fontfamilies at 0x1015887c0>,
#  pycocoa.deprecated.fontnamesof is <function .fontnamesof at 0x101908400>,
#  pycocoa.deprecated.fontsof is <function .fontsof at 0x1019084a0>,
#  pycocoa.deprecated.fontsof4 is <function .fontsof4 at 0x101908540>,
#  pycocoa.deprecated.get_libPC is <function .get_libPC at 0x1019085e0>,
#  pycocoa.deprecated.get_libs is <function .get_libs at 0x101908680>,
#  pycocoa.deprecated.libAppKit is <CDLL '/System/Library/Frameworks/AppKit.framework/AppKit', handle 3eed350a0 at 0x1015d5e50>,
#  pycocoa.deprecated.libCF is <CDLL '/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation', handle 3eed394f8 at 0x1015d5a90>,
#  pycocoa.deprecated.libCG is <CDLL '/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics', handle 3eed375c0 at 0x1015d6710>,
#  pycocoa.deprecated.libCT is <CDLL '/System/Library/Frameworks/CoreText.framework/CoreText', handle 3eed3b5b0 at 0x1015d6850>,
#  pycocoa.deprecated.libFoundation is <CDLL '/System/Library/Frameworks/Foundation.framework/Foundation', handle 3eed38b28 at 0x1015d6990>,
#  pycocoa.deprecated.libobjc is <CDLL '/usr/lib/libobjc.dylib', handle 3eed3ce04 at 0x1015d6ad0>,
#  pycocoa.deprecated.libPC is <CDLL '/System/Library/Frameworks/ApplicationServices.framework/Frameworks/PrintCore.framework/PrintCore', handle 3ee2d8b38 at 0x10126b750>,
#  pycocoa.deprecated.MainScreen is <class .MainScreen>,
#  pycocoa.deprecated.module_property_RO is <class .module_property_RO>,
#  pycocoa.deprecated.OBJC_ASSOCIATION_ASSIGN is 0 or 0x0,
#  pycocoa.deprecated.OBJC_ASSOCIATION_COPY is 771 or 0x303,
#  pycocoa.deprecated.OBJC_ASSOCIATION_COPY_NONATOMIC is 3 or 0x3,
#  pycocoa.deprecated.OBJC_ASSOCIATION_RETAIN is 769 or 0x301,
#  pycocoa.deprecated.OBJC_ASSOCIATION_RETAIN_NONATOMIC is 1 or 0x1,
#  pycocoa.deprecated.property2 is <function .property2 at 0x101908720>,
#  pycocoa.deprecated.sortuples is <function .sortuples at 0x1019087c0>,
# )[26]
# pycocoa.deprecated.version 25.3.16, .isLazy 1, Python 3.13.2 64bit arm64, macOS 15.3.2

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2025 -- mrJean1 at Gmail -- All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
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

# Originally <https://GitHub.com/phillip-nguyen/cocoa-python>

# objective-ctypes
#
# Copyright (C) 2011 -- Phillip Nguyen -- All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of objective-ctypes nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
