
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Deprecated classes, constants, functions, internals, etc.
'''
from pycocoa.getters import _Cache2
from pycocoa.internals import _property2, proxy_RO, _sortuples
from pycocoa.lazily import _ALL_LAZY, _Dmain_
from pycocoa.runtime import OBJC_ASSOCIATION as _OBJC_AN

__all__ = _ALL_LAZY.deprecated
__version__ = '25.02.22'

OBJC_ASSOCIATION_ASSIGN           = _OBJC_AN.ASSIGN
OBJC_ASSOCIATION_COPY             = _OBJC_AN.COPY
OBJC_ASSOCIATION_COPY_NONATOMIC   = _OBJC_AN.COPY_NONATOMIC
OBJC_ASSOCIATION_RETAIN           = _OBJC_AN.RETAIN
OBJC_ASSOCIATION_RETAIN_NONATOMIC = _OBJC_AN.RETAIN_NONATOMIC
'''DEPRECATED on 2025.02.20, use OBJC_ASSOCIATION.ASSIGN, etc.'''


class Cache2(_Cache2):
    '''DEPRECATED on 2025.02.15, I{to be removed}.'''
    pass


class module_property_RO(proxy_RO):
    '''DEPRECATED on 2025.02.09, use C{proxy_RO}.'''
    pass


def property2(inst, name):
    '''DEPRECATED on 25.02.16, I{to be removed}.'''
    return _property2(inst, name)


def sortuples(iterable):
    '''DEPRECATED on 25.02.09, I{to be removed}.'''
    return _sortuples(iterable)


if __name__ == _Dmain_:

    from pycocoa.utils import _all_listing

    _all_listing(__all__, locals())

# % python3 -m pycocoa.deprecated
#
# pycocoa.deprecated.__all__ = tuple(
#  pycocoa.deprecated.Cache2 is <class .Cache2>,
#  pycocoa.deprecated.module_property_RO is <class .module_property_RO>,
#  pycocoa.deprecated.property2 is <function .property2 at 0x10089cb80>,
#  pycocoa.deprecated.sortuples is <function .sortuples at 0x1009d3060>,
# )[4]
# pycocoa.deprecated.version 25.2.22, .isLazy 1, Python 3.13.2 64bit arm64, macOS 14.7.3

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
