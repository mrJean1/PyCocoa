
# -*- coding: utf-8 -*-

# License at the end of this file.

'''DEPRECATED classes, constants, functions, internals, modules, etc.
'''
from pycocoa import fonts as _fonts, getters as _getters
from pycocoa.basics import Proxy1ce
from pycocoa.internals import _Dmain_, _nameOf, _property2, _sortuples
from pycocoa.lazily import _ALL_LAZY
from pycocoa.oslibs import Libs,  CDLL
from pycocoa.printers import _libPC
from pycocoa.runtime import OBJC_ASSOCIATION as _OBJC_AN
from pycocoa.screens import Screen as _Screen

# from ctypes import CDLL  # from .oslibs

__all__ = _ALL_LAZY.deprecated
__version__ = '25.04.08'


class _DeprecatedCDLL(CDLL):
    '''(INTERNAL) DEPRECATED C{ctypes.CDLL}.'''
    def __init__(self, lib, doc):
        CDLL.__init__(self, lib._name)
        self.__doc__ = doc
#       self.__lib__ = lib


class _DeprecatedInt(int):
    '''(INTERNAL) DEPRECATED C{int}.'''
    # int.__init__ refuses 2nd arg,
    # hence this __call__ method
    def __call__(self, doc):
        self.__doc__ = doc
        return self


class _DeprecatedScreen(_Screen):
    '''(INTERNAL) DEPRECATED C{Screen}s.'''
    # _name = ...
    def __init__(self, *args, **kwds):  # PYCHOK signature
        _DeprecatedScreen._name = _nameOf(type(self))[:-6]
        _Screen.__init__(self, *args, **kwds)


@Proxy1ce
def bases():  # lazily import bases, I{once}
    '''DEPRECATED on 2025.03.28, use C{pycocoa.baseTypes}.'''
    from pycocoa import baseTypes as bases
#   bases.__name__ = 'bases'
    return bases


libAppKit     = _DeprecatedCDLL(Libs.AppKit,
'''DEPRECATED on 2025.02.25, use C{Libs.AppKit}''')
libCF         = _DeprecatedCDLL(Libs.CoreFoundation,
'''DEPRECATED on 2025.02.25, use C{Libs.CoreFoundation}''')
libCG         = _DeprecatedCDLL(Libs.CoreGraphics,
'''DEPRECATED on 2025.02.25, use C{Libs.CoreGraphics}''')
libCT         = _DeprecatedCDLL(Libs.CoreText,
'''DEPRECATED on 2025.02.25, use C{Libs.CoreText}''')
libFoundation = _DeprecatedCDLL(Libs.Foundation,
'''DEPRECATED on 2025.02.25, use C{Libs.Foundation}''')
libobjc       = _DeprecatedCDLL(Libs.ObjC,
'''DEPRECATED on 2025.02.25, use C{Libs.ObjC}''')
libPC         = _DeprecatedCDLL(_libPC,
'''DEPRECATED on 2025.02.25, use C{Libs.PrintCore}''')

OBJC_ASSOCIATION_ASSIGN           = _DeprecatedInt(_OBJC_AN.ASSIGN)(
'''DEPRECATED on 2025.02.20, use C{OBJC_ASSOCIATION.ASSIGN}.''')
OBJC_ASSOCIATION_COPY             = _DeprecatedInt(_OBJC_AN.COPY)(
'''DEPRECATED on 2025.02.20, use C{OBJC_ASSOCIATION.COPY}.''')
OBJC_ASSOCIATION_COPY_NONATOMIC   = _DeprecatedInt(_OBJC_AN.COPY_NONATOMIC)(
'''DEPRECATED on 2025.02.20, use C{OBJC_ASSOCIATION.COPY_NONATOMIC}.''')
OBJC_ASSOCIATION_RETAIN           = _DeprecatedInt(_OBJC_AN.RETAIN)(
'''DEPRECATED on 2025.02.20, use C{OBJC_ASSOCIATION.RETAIN}.''')
OBJC_ASSOCIATION_RETAIN_NONATOMIC = _DeprecatedInt(_OBJC_AN.RETAIN_NONATOMIC)(
'''DEPRECATED on 2025.02.20, use C{OBJC_ASSOCIATION.RETAIN_NONATOMIC}.''')


class BuiltInScreen(_DeprecatedScreen):
    '''DEPRECATED on 2025.03.16, use C{Screens.BuiltIn}.'''
    pass


class Cache2(_getters._Cache2):
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


class module_property_RO(Proxy1ce):
    '''DEPRECATED on 2025.02.09, use C{Proxy1ce}.'''
    pass


class proxy_RO(Proxy1ce):
    '''DEPRECATED on 2025.04.03, use C{Proxy1ce}.'''
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


def get_classes(*prefixes):
    '''DEPRECATED on 25.03.30, use C{get_classes2}.'''
    return _getters.get_classes2(*prefixes)


def get_ivars(clas, *prefixes):
    '''DEPRECATED on 25.03.30, use C{get_ivars4}.'''
    return _getters.get_ivars4(clas, *prefixes)


def get_libPC():
    '''DEPRECATED on 25.02.25, use C{Libs.PrintCore}.'''
    return libPC


def get_libs():
    '''DEPRECATED on 25.02.25, use C{Libs}.'''
    return Libs.copy()


def get_methods(clas, *prefixes):
    '''DEPRECATED on 25.03.30, use C{get_methods4}.'''
    return _getters.get_methods4(clas, *prefixes)


def get_properties(clas_or_proto, *prefixes):
    '''DEPRECATED on 25.03.30, use C{get_properties4}.'''
    return _getters.get_properties4(clas_or_proto, *prefixes)


def get_protocols(clas, *prefixes):
    '''DEPRECATED on 25.03.30, use C{get_protocols2}.'''
    return _getters.get_protocols2(clas, *prefixes)


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
#  pycocoa.deprecated.bases is <pycocoa.basics.Proxy1ce object at 0x1051a4c00>,
#  pycocoa.deprecated.BuiltInScreen is <class .BuiltInScreen>,
#  pycocoa.deprecated.Cache2 is <class .Cache2>,
#  pycocoa.deprecated.DeepestScreen is <class .DeepestScreen>,
#  pycocoa.deprecated.ExternalScreen is <class .ExternalScreen>,
#  pycocoa.deprecated.fontfamilies is <function .fontfamilies at 0x1051b7ec0>,
#  pycocoa.deprecated.fontnamesof is <function .fontnamesof at 0x1051b8180>,
#  pycocoa.deprecated.fontsof is <function .fontsof at 0x1051b8220>,
#  pycocoa.deprecated.fontsof4 is <function .fontsof4 at 0x1051b82c0>,
#  pycocoa.deprecated.get_classes is <function .get_classes at 0x1051b8360>,
#  pycocoa.deprecated.get_ivars is <function .get_ivars at 0x1051b8400>,
#  pycocoa.deprecated.get_libPC is <function .get_libPC at 0x1051b84a0>,
#  pycocoa.deprecated.get_libs is <function .get_libs at 0x1051b8540>,
#  pycocoa.deprecated.get_methods is <function .get_methods at 0x1051b85e0>,
#  pycocoa.deprecated.get_properties is <function .get_properties at 0x1051b8680>,
#  pycocoa.deprecated.get_protocols is <function .get_protocols at 0x1051b8720>,
#  pycocoa.deprecated.libAppKit is <_DeprecatedCDLL '/System/Library/Frameworks/AppKit.framework/AppKit', handle 3316bddb8 at 0x105184830>,
#  pycocoa.deprecated.libCF is <_DeprecatedCDLL '/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation', handle 3316b9f70 at 0x105141a90>,
#  pycocoa.deprecated.libCG is <_DeprecatedCDLL '/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics', handle 3316a04f8 at 0x105141d10>,
#  pycocoa.deprecated.libCT is <_DeprecatedCDLL '/System/Library/Frameworks/CoreText.framework/CoreText', handle 3316bc168 at 0x105135e00>,
#  pycocoa.deprecated.libFoundation is <_DeprecatedCDLL '/System/Library/Frameworks/Foundation.framework/Foundation', handle 3316bb660 at 0x105135cd0>,
#  pycocoa.deprecated.libobjc is <_DeprecatedCDLL '/usr/lib/libobjc.dylib', handle 3316b76a8 at 0x105167650>,
#  pycocoa.deprecated.libPC is <_DeprecatedCDLL '/System/Library/Frameworks/ApplicationServices.framework/Frameworks/PrintCore.framework/PrintCore', handle 3316dcb70 at 0x1051a4d10>,
#  pycocoa.deprecated.MainScreen is <class .MainScreen>,
#  pycocoa.deprecated.module_property_RO is <class .module_property_RO>,
#  pycocoa.deprecated.OBJC_ASSOCIATION_ASSIGN is 0 or 0x0,
#  pycocoa.deprecated.OBJC_ASSOCIATION_COPY is 771 or 0x303,
#  pycocoa.deprecated.OBJC_ASSOCIATION_COPY_NONATOMIC is 3 or 0x3,
#  pycocoa.deprecated.OBJC_ASSOCIATION_RETAIN is 769 or 0x301,
#  pycocoa.deprecated.OBJC_ASSOCIATION_RETAIN_NONATOMIC is 1 or 0x1,
#  pycocoa.deprecated.property2 is <function .property2 at 0x1051b87c0>,
#  pycocoa.deprecated.proxy_RO is <class .proxy_RO>,
#  pycocoa.deprecated.sortuples is <function .sortuples at 0x1051b8860>,
# )[33]
# pycocoa.deprecated.version 25.4.8, .isLazy 1, Python 3.13.2 64bit arm64, macOS 15.4

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
