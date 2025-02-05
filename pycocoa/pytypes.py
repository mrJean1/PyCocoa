
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Conversions from C{NS...} ObjC instances to Python.
'''
# all imports listed explicitly to help PyChecker
from pycocoa.lazily import _ALL_LAZY, _COLON_, _Dmain_, _fmt, \
                           _fmt_invalid, _instr
from pycocoa.nstypes import NSArray, NSData, NSDate, NSDecimal, \
                            NSDictionary, NSDouble, NSLongLong, \
                            NSMain, NSMutableArray, NSMutableSet, \
                            NSMutableDictionary, NSSet, NSStr, NSURL
from pycocoa.oslibs import libCF
from pycocoa.runtime import ObjCInstance, release
from pycocoa.utils import bytes2str, _ByteStrs, clipstr, \
                          DEFAULT_UNICODE, _Ints, isinstanceOf

from ctypes import c_void_p
from decimal import Decimal as _Decimal
from types import GeneratorType as _Generator

__all__ = _ALL_LAZY.pytypes
__version__ = '25.02.04'

_MAXLONG = (1 << 63)  # == _MAXLONGLONG!
_Numbers = _Ints + (float, _Decimal)


def _iter2NS(ns, py, getCount):
    '''(INTERNAL) Create NS objects for each item in a Python C{list},
       C{frozen/set}, C{tuple}, C{generator}, C{map} or C{range}.
    '''
    for ns_obj in map(py2NS, py):
        ns.addObject_(ns_obj)
    return _len2NS(py, ns, getCount)


def _len2NS(py, ns, getCount):
    '''(INTERNAL) Check the inital Python C{len} vs the final
       C{NS...} instance C{count}.
    '''
    n, m = len(py), getCount(ns)
    if m != n:
        t = _fmt('%s[%s] vs %s[%s]', ns.objc_classname, m,
                                     clipstr(repr(py)), n)
        raise RuntimeError(t)
    return ns


def _list2NS(py):
    '''(INTERNAL) Create an C{NSMutableArray} instance from a
       type-checked Python C{list} or C{tuple}.
    '''
    return _iter2NS(NSMutableArray.array(), py, libCF.CFArrayGetCount)


def _set2NS(py):
    '''(INTERNAL) Create an C{NSMutableSet} instance from a
       type-checke Python C{set} or C{frozenset}.
    '''
    return _iter2NS(NSMutableSet.set(), py, libCF.CFSetGetCount)


def bool2NS(py):
    '''Create an C{NSBoolean} instance from a Python C{bool}.

       @param py: The value (C{int} or C{bool}).

       @return: The C{NSMain.BooleanYES} or C{.BooleanNO}
                singleton (C{NSBoolean}).
    '''
    return NSMain.BooleanYES if py else NSMain.BooleanNO  # c_byte's


def bytes2NS(py):
    '''Create an C{NSData} instance from Python C{bytes}.

       @param py: The value (C{bytes}).

       @return: The ObjC instance (C{NSData}).

       @raise RuntimeError: If C{len} vs C{count} assertion failed.
    '''
    def _NSData_length(ns):  # XXX lambda ns: ns.length()
        return ns.length()

    if isinstanceOf(py, *_ByteStrs, name='py'):
        return _len2NS(py, NSData.dataWithBytes_length_(py, len(py)),
                          _NSData_length)


def decimal2NS(py):
    '''Create an C{NSDecimal} instance from a Python C{Decimal}.

       @param py: The value (C{Decimal}, C{float}, C{int} or C{str}).

       @return: The instance ( C{NSDecimal}).

       @raise TypeError: If C{py} not a C{Decimal}, C{float}, C{int}
                         or C{str}.

       @raise ValueError: Invalid decimal C{py}.
    '''
    if isinstanceOf(py, str, *_Numbers, name='py'):
        try:
            py = _Decimal(py)
        except Exception:
            t = _fmt_invalid(_Decimal.__name__, py=repr(py))
            raise ValueError(t)
        return NSDecimal(py)


def dict2NS(py, frozen=False):
    '''Create an C{NS[Mutable]Dictionary} instance from a Python C{dict}.

       @param py: The value (C{dict}).
       @keyword frozen: Immutable (C{bool}), mutable otherwise.

       @return: The ObjC instance (C{NSDictionary} or C{NSMutableDictionary}).

       @raise RuntimeError: If C{len} vs C{count} assertion failed.
    '''
    # https://Developer.Apple.com/library/content/documentation/Cocoa/
    #         Conceptual/Collections/Articles/Dictionaries.html
    if isinstanceOf(py, dict, name='py'):
        ns = NSMutableDictionary.dictionary()
        for k, v in py.get('iteritems', py.items)():
            ns.setObject_forKey_(py2NS(v), py2NS(k))
        ns = _len2NS(py, ns, libCF.CFDictionaryGetCount)
        if frozen:
            ns = NSDictionary.alloc().initWithDictionary_(ns)
            ns._from_py2NS = True
        return ns


def float2NS(py):
    '''Create an C{NSDouble} instance from a Python C{float} or C{int}.

       @param py: The value (C{float} or C{int}).

       @return: The ObjC instance (C{NSDouble}).

       @raise TypeError: If C{py} not a C{float} or C{int}.
    '''
    if isinstanceOf(py, float, *_Ints, name='py'):
        return NSDouble(float(py))


def frozenset2NS(py):
    '''Create an (immutable) C{NSSet} instance from a Python C{frozenset}.

       @param py: The value (C{frozenset}).

       @return: The ObjC instance (C{NSSet}).

       @raise RuntimeError: If C{len} vs C{count} assertion failed.
    '''
    if isinstanceOf(py, frozenset, set, name='py'):
        ns = _len2NS(py, NSSet.alloc().initWithSet_(_set2NS(py)),
                         libCF.CFSetGetCount)
        ns._from_py2NS = True
        return ns


def generator2NS(py):
    '''Create an C{NSArray} instance from a Python C{generator}.

       @param py: The value (C{generator}).

       @return: The ObjC instance (C{NSArray}).

       @raise RuntimeError: If C{len} vs C{count} assertion failed.
    '''
    if isinstanceOf(py, _Generator, name='py'):
        return tuple2NS(tuple(py))


def int2NS(py, NS=None):
    '''Create an C{NSNumber} instance from a Python C{int} or C{long}.

       @param py: The value (C{int} or C{long}).
       @keyword NS: Alternate C{NSNumber} ObjC class to use when C{py}
                    exceeds the C{NSLong} or C{NSLongLong} range, for
                    example C{NS=NSDecimal}.

       @return: The ObjC instance (C{NSNumber} or C{NS} alternate).

       @raise TypeError: If C{py} not an C{int} or C{long}.

       @raise ValueError: If C{py} exceeds C{NSLong} range and
                          if no C{NS} alternate is specified.
    '''
    if isinstanceOf(py, _Ints, name='py'):
        if _MAXLONG > py >= -_MAXLONG:
            NS = NSLongLong  # or NSLong
        elif not callable(NS):
            t = _fmt_invalid('NSLong', py=repr(py))
            raise ValueError(t)
        return NS(py)


def list2NS(py):
    '''Create an C{NSMutableArray} instance from a Python C{list}.

       @param py: The value (C{list}).

       @return: The ObjC instance (C{NSMutableArray}).

       @raise RuntimeError: If C{len} vs C{count} assertion failed.
    '''
    if isinstanceOf(py, list, name='py'):
        return _list2NS(py)


def map2NS(py):
    '''Create an C{NSArray} instance from a Python C{map}.

       @param py: The value (C{map}).

       @return: The ObjC instance (C{NSArray}).

       @raise RuntimeError: If C{len} vs C{count} assertion failed.
    '''
    # XXX isinstanceOf(py, map, name='py')
    return tuple2NS(tuple(py))


def None2NS(py):
    '''Return the C{NSNull} singleton for Python's C{None}.

       @param py: The value (C{None}).

       @return: The singleton (C{NSNull}).

       @raise ValueError: If I{py} is not C{None}.
    '''
    if py is None:
        return NSMain.Null
    raise ValueError(_fmt_invalid(None, py=repr(py)))


def range2NS(py):
    '''Create an C{NSArray} instance from a Python C{range}.

       @param py: The value (C{range}).

       @return: The ObjC instance (C{NSArray}).

       @raise RuntimeError: If C{len} vs C{count} assertion failed.
    '''
    # XXX isinstanceOf(py, range, name='py')
    return tuple2NS(tuple(py))


def set2NS(py):
    '''Create an C{NSMutableSet} instance from a Python C{set}.

       @param py: The value (C{set}).

       @return: The ObjC instance (C{NSMutableSet}).

       @raise RuntimeError: If C{len} vs C{count} assertion failed.
    '''
    if isinstanceOf(py, set, name='py'):
        return _set2NS(py)


def str2NS(py):
    '''Create an C{NSStr} instance from a Python C{str}.

       @param py: The value (C{str}).

       @return: The ObjC instance (C{NSStr}).
    '''
    return NSStr(py)


def time2NS(py=None, since=1970):
    '''Create an C{NSDate} instance from a timestamp.

       @keyword py: The timestamp in seconds (C{float}, C{int}).
       @keyword since: Epoch start (1970, 2001) otherwise now.

       @return: The ObjC instance (C{NSDate}).

       @note: Using C{B{py}=None} means C{B{py}=0, B{since}=None}
              or C{B{py}=time.time(), B{since}=1970}.
    '''
    if py is None:
        s = t = 0.0
    elif isinstanceOf(py, name='py', *_Numbers):
        s, t = since, float(py)
    NS = NSDate.alloc()
    m_ = NS.initWithTimeIntervalSince1970_ if s == 1970 else (
         NS.initWithTimeIntervalSinceReferenceDate_ if s == 2001 else
         NS.initWithTimeIntervalSinceNow_)
    return m_(t)


def tuple2NS(py):
    '''Create an immutable C{NSArray} instance from a Python C{tuple}.

       @param py: The value (C{tuple}).

       @return: The ObjC instance (C{NSArray}).

       @raise RuntimeError: If C{len} vs C{count} assertion failed.
    '''
    if isinstanceOf(py, tuple, list, name='py'):
        ns = _len2NS(py, NSArray.alloc().initWithArray_(_list2NS(py)),
                         libCF.CFArrayGetCount)
        ns._from_py2NS = True
        return ns


def unicode2NS(py):
    '''Create an C{NSStr} instance from a Python C{unicode} string.

       @param py: The value (C{unicode}).

       @return: The ObjC instance (C{NSStr}).
    '''
    return NSStr(py.encode(DEFAULT_UNICODE))  # .stringWithUTF8String_


def url2NS(py, url2=None):
    '''Create an C{NSURL} instance from a Python string.

       @param py: The URL (C{str} or C{unicode}).
       @keyword url2: Optionally, relative to this URL (C{str} or C{unicode}).

       @return: The ObjC instance (C{NSURL}).

       @see: U{URL<https://Developer.Apple.com/documentation/foundation/url>}
             for parsing an C{NSURL}.
    '''
    ns = release(NSStr(py))
    NS = NSURL.alloc()
    if _COLON_ in bytes2str(py):
        nu = NS.initWithString_(ns) if not url2 else \
             NS.initWithString_relativeToURL_(ns, url2NS(url2))
    elif url2:
        nu = NS.initFileURLWithPath_relativeToURL_(ns, url2NS(url2))
    else:
        nu = NS.initFileURLWithPath_(ns)
    return nu


_py2NS = {bool:       bool2NS,
          bytearray:  bytes2NS,
         _Decimal:    decimal2NS,
          dict:       dict2NS,
          float:      float2NS,
          frozenset:  frozenset2NS,
         _Generator:  generator2NS,
          int:        int2NS,
          list:      _list2NS,
          range:      range2NS,
          set:       _set2NS,
          str:        str2NS,
          tuple:      tuple2NS,
          type(None): None2NS}
try:
    _py2NS.update({long:    int2NS,
                   unicode: unicode2NS})
except NameError:  # Python 3+
    _py2NS.update({bytes: bytes2NS,
                   map:   map2NS})


def py2NS(py):
    '''Convert (an instance of) a Python object into an
       instance of the equivalent C{NS...} ObjC class:

       @param py: The value (C{Python type}).

       @return: The ObjC instance (L{ObjCInstance}).

       @raise TypeError: Unhandled, unexpected C{Python type}.

       @note: Conversion map:
        - bool      -> NSBoolean/NSNumber
        - bytes     -> NSData (Python 3+ only)
        - bytearray -> NSData
        - Decimal   -> NSDecimal
        - dict      -> NSMutableDictionary
        - float     -> NSNumber
        - frozenset -> NSSet, immutable
        - generator -> NSArray, immutable (like tuple)
        - int       -> NSNumber
        - list      -> NSMutableArray
        - map       -> NSArray, immutable (like tuple, Python 3+ only)
        - None      -> NSNull
        - range     -> NSArray, immutable (like tuple)
        - set       -> NSMutableSet
        - str       -> NSStr, immutable
        - tuple     -> NSArray, immutable
        - unicode   -> NSStr, immutable

       @see: U{Converting values between Python and Objective-C
              <https://PythonHosted.org/pyobjc/core/typemapping.html>}
    '''
    try:
        return py.NS
    except AttributeError:
        pass

    if isinstance(py, ObjCInstance):
        return py
    elif isinstance(py, c_void_p):
        return ObjCInstance(py)

    ns = _py2NS.get(type(py), None)
    if not ns:
        # handle Set, other (mutable) Types,
        # by extending the _py2NS table
        for ty, ns in _py2NS.items():
            if isinstance(py, ty):
                break
        else:
            t = _instr(type.__name__, 'py')
            raise TypeError(_fmt('unhandled %s: %r', t, py))
        _py2NS[type(py)] = ns
    return ns(py)


def type2NS(py):
    '''Create the C{NS...} ObjC object for a Python Type or wrapper instance.

       @param py: The value (C{Type}).

       @return: The ObjC instance (L{ObjCInstance}).

       @raise TypeError: Unhandled, unexpected C{Type}.

       @see: Function L{py2NS}.
    '''
    try:
        return py.NS
    except AttributeError:
        return py2NS(py)


if __name__ == _Dmain_:

    from pycocoa.utils import _all_listing

    _all_listing(__all__, locals())

# % python3 -m pycocoa.pytypes
#
# pycocoa.pytypes.__all__ = tuple(
#  pycocoa.pytypes.bool2NS is <function .bool2NS at 0x100ad14e0>,
#  pycocoa.pytypes.bytes2NS is <function .bytes2NS at 0x100ad1580>,
#  pycocoa.pytypes.decimal2NS is <function .decimal2NS at 0x100ad1620>,
#  pycocoa.pytypes.dict2NS is <function .dict2NS at 0x100ad16c0>,
#  pycocoa.pytypes.float2NS is <function .float2NS at 0x100ad1760>,
#  pycocoa.pytypes.frozenset2NS is <function .frozenset2NS at 0x100ad1800>,
#  pycocoa.pytypes.generator2NS is <function .generator2NS at 0x100ad18a0>,
#  pycocoa.pytypes.int2NS is <function .int2NS at 0x100ad1940>,
#  pycocoa.pytypes.list2NS is <function .list2NS at 0x100ad19e0>,
#  pycocoa.pytypes.map2NS is <function .map2NS at 0x100ad1a80>,
#  pycocoa.pytypes.None2NS is <function .None2NS at 0x100ad1b20>,
#  pycocoa.pytypes.py2NS is <function .py2NS at 0x100ad2020>,
#  pycocoa.pytypes.range2NS is <function .range2NS at 0x100ad1bc0>,
#  pycocoa.pytypes.set2NS is <function .set2NS at 0x100ad1c60>,
#  pycocoa.pytypes.str2NS is <function .str2NS at 0x100ad1d00>,
#  pycocoa.pytypes.time2NS is <function .time2NS at 0x100ad1da0>,
#  pycocoa.pytypes.tuple2NS is <function .tuple2NS at 0x100ad1e40>,
#  pycocoa.pytypes.type2NS is <function .type2NS at 0x100ad20c0>,
#  pycocoa.pytypes.unicode2NS is <function .unicode2NS at 0x100ad1ee0>,
#  pycocoa.pytypes.url2NS is <function .url2NS at 0x100ad1f80>,
# )[20]
# pycocoa.pytypes.version 25.2.4, .isLazy 1, Python 3.13.1 64bit arm64, macOS 14.6.1

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
