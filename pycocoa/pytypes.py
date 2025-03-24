
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Conversions from C{NS...} ObjC instances to Python.
'''
from pycocoa.internals import bytes2str, _ByteStrs, _COLON_, \
                             _DEFAULT_UNICODE, _Dmain_, frozendict, \
                             _isgenerator, _isiterable, _Ints, \
                             _SPACE_, _unhandled_
from pycocoa.lazily import _ALL_LAZY,  _fmt, _fmt_invalid, _instr
from pycocoa.nstypes import NSArray, NSData, NSDate, NSDecimal, \
                            NSDictionary, NSDouble, NSLongLong, \
                            NSMain, NSMutableArray, NSMutableSet, \
                            NSMutableDictionary, NSMutableString, \
                            NSSet, _NSStr, NSStr, NSString, NSURL
from pycocoa.oslibs import _libCF
from pycocoa.runtime import ObjCInstance
from pycocoa.utils import clipstr, isinstanceOf

from ctypes import c_void_p
from decimal import Decimal as _Decimal
from types import GeneratorType as _Generator

__all__ = _ALL_LAZY.pytypes
__version__ = '25.02.25'

_MAXLONG = (1 << 63)  # == _MAXLONGLONG!
_Numbers = _Ints + (float, _Decimal)

_raiser_py = dict(raiser='py')


def bool2NS(py):
    '''Create an C{NSBoolean} from a Python C{bool}.

       @param py: The value (C{int} or C{bool}).

       @return: The C{NSMain.BooleanYES} or C{.BooleanNO}
                singleton (C{NSBoolean}).
    '''
    return NSMain.BooleanYES if py else NSMain.BooleanNO  # c_byte's


def bytes2NS(py):
    '''Create an C{NSData} from Python C{bytes}.

       @param py: The value (C{bytes}).

       @return: The ObjC instance (C{NSData}).

       @raise TypeError: If I{py} not C{bytes} or C{str}.

       @raise RuntimeError: If C{len} vs C{count} assertion failed.
    '''
    def _NSData_length(ns):  # XXX lambda ns: ns.length()
        return ns.length()

    isinstanceOf(py, *_ByteStrs, **_raiser_py)
    return _len2NS(py, NSData.dataWithBytes_length_(py, len(py)),
                      _NSData_length)


def decimal2NS(py):
    '''Create an C{NSDecimal} from a Python C{Decimal}.

       @param py: The value (C{Decimal}, C{float}, C{int} or C{str}).

       @return: The value (C{NSDecimal}).

       @raise TypeError: If I{py} not a C{Decimal}, C{float}, C{int}
                         or C{str}.

       @raise ValueError: Invalid decimal I{py}.
    '''
    isinstanceOf(py, str, *_Numbers, **_raiser_py)
    try:
        py = _Decimal(py)
    except Exception:
        t = _fmt_invalid(_Decimal.__name__, py=clipstr(repr(py)))
        raise ValueError(t)
    return NSDecimal(py)


def dict2NS(py):
    '''Create an C{NSMutableDictionary} from a Python C{dict} or C{frozendict}.

       @return: The ObjC instance (C{NSMutableDictionary}).

       @see: Function L{dicts2NS} for further details.
    '''
    return _dicts2NS(py, frozen=False)


def _dicts2NS(py, frozen=False):
    # https://Developer.Apple.com/library/content/documentation/Cocoa/
    #         Conceptual/Collections/Articles/Dictionaries.html
    isinstanceOf(py, frozendict, dict, **_raiser_py)
    ns = NSMutableDictionary.dictionary()
    for k, v in py.get('iteritems', py.items)():
        ns.setObject_forKey_(py2NS(v), py2NS(k))
    ns = _len2NS(py, ns, _libCF.CFDictionaryGetCount)
    if frozen:
        ns = NSDictionary.alloc().initWithDictionary_(ns)
        ns._from_py2NS = True
    return ns


def dicts2NS(py):
    '''Create an C{NS[Mutable]Dictionary} from a Python C{dict} or C{frozendict}.

       @param py: The value (C{dict} or C{frozendict}).

       @return: The ObjC instance (C{NSMutableDictionary} or immutable C{NSDictionary}).

       @raise RuntimeError: If C{len} vs C{count} assertion failed.

       @raise TypeError: If I{py} is not a C{dict} or C{frozendict}.

       @see: Functions L{dict2NS} and L{frozendict2NS}.
    '''
    return _dicts2NS(py, frozen=isinstance(py, frozendict))


def float2NS(py):
    '''Create an C{NSDouble} instance from a Python C{float} or C{int}.

       @param py: The value (C{float} or C{int}).

       @return: The ObjC instance (C{NSDouble}).

       @raise TypeError: If I{py} not a C{float} or C{int}.
    '''
    isinstanceOf(py, float, *_Ints, **_raiser_py)
    return NSDouble(float(py))


def frozendict2NS(py):
    '''Create an C{NSDictionary} from a Python C{frozendict} or C{dict}.

       @return: The ObjC instance (C{NSDictionary}, immutable).

       @see: Function L{dicts2NS} for further details.
    '''
    return _dicts2NS(py, frozen=True)


def frozenset2NS(py):
    '''Create an C{NSSet} from a Python C{frozenset} or C{set}.

       @return: The ObjC instance (C{NSSet}, immutable).

       @see: Function L{sets2NS} for further details.
    '''
    return _sets2NS(py, frozen=True)


def generator2NS(py, frozen=True):
    '''Create an C{NS[Mutable]Array} from a Python C{generator}.

       @param py: The value (C{generator}).
       @keyword frozen: If C{True}, return an immutable C{NSArray}, otherwise
                        an C{NSMutableArray} (C{bool}).

       @return: The ObjC instance (C{NSMutableArray} or immutable C{NSArray}).

       @raise TypeError: If I{py} not a C{generator}.
    '''
    if _isgenerator(py) or isinstanceOf(py, _Generator, **_raiser_py):
        return _listuple2NS(py, frozen=frozen, count=False)


def int2NS(py, NS=None):
    '''Create an C{NSNumber} from a Python C{int} or C{long}.

       @param py: The value (C{int} or C{long}).
       @keyword NS: Alternate C{NSNumber} ObjC class to use when I{py}
                    exceeds the C{NSLong} or C{NSLongLong} range, for
                    example C{NS=NSDecimal}.

       @return: The ObjC instance (C{NSNumber} or C{NS} alternate).

       @raise TypeError: If I{py} not an C{int} or C{long}.

       @raise ValueError: If I{py} exceeds C{NSLong} range and
                          if no C{NS} alternate is specified.
    '''
    isinstanceOf(py, *_Ints, **_raiser_py)
    if _MAXLONG > py >= -_MAXLONG:
        NS = NSLongLong  # or NSLong
    elif not callable(NS):
        t = _fmt_invalid('NSLong', py=clipstr(repr(py)))
        raise ValueError(t)
    return NS(py)


def _iter2NS(ns, py, getCount):
    '''(INTERNAL) Create NS objects for each item in a Python C{list},
       C{frozen/set}, C{tuple}, C{generator}, C{map} or C{range}.
    '''
    for ns_obj in map(py2NS, py):
        ns.addObject_(ns_obj)
    return _len2NS(py, ns, getCount)


def iterable2NS(py, frozen=True):
    '''Create an C{NS[Mutable]Array} from a Python C{iterable}.

       @param py: The value (C{iterable}).
       @keyword frozen: If C{True}, return an immutable C{NSArray}, otherwise
                        an C{NSMutableArray} (C{bool}).

       @return: The ObjC instance (C{NSMutableArray} or immutable C{NSArray}).

       @raise TypeError: If I{py} is not C{iterable}.
    '''
    if not _isiterable(py):
        t = _fmt_invalid('iterable', py=clipstr(repr(py)))
        raise TypeError(t)
    return _listuple2NS(py, frozen=frozen, count=False)


def _len2NS(py, ns, getCount=None):
    '''(INTERNAL) Check the inital Python C{len} vs the final
       C{NS...} instance C{count}.
    '''
    if getCount:
        n, m = len(py), getCount(ns)
        if m != n:
            t = _fmt('len %s[%s] vs %s[%s]', ns.objc_classname, m,
                                             clipstr(repr(py)), n)
            raise RuntimeError(t)
    return ns


def list2NS(py):
    '''Create an C{NSMutableArray} from a Python C{list} or C{tuple}.

       @return: The ObjC instance (C{NSMutableArray}).

       @see: Function L{listuple2NS} for further details.
    '''
    isinstanceOf(py, list, tuple, **_raiser_py)
    return _listuple2NS(py, frozen=False)


def _listuple2NS(py, frozen=False, count=True):
    '''(INTERNAL) Create an C{NS[Mutable]Array}.
    '''
    _g = _libCF.CFArrayGetCount if count else None
    ns = _iter2NS(NSMutableArray.array(), py, _g)
    if frozen:
        ns = _len2NS(py, NSArray.alloc().initWithArray_(ns), _g)
        ns._from_py2NS = True
    return ns


def listuple2NS(py):
    '''Create an C{NS[Mutable]Array} from a Python C{list} or C{tuple}.

       @param py: The value (C{list} or C{tuple}).

       @return: The ObjC instance (C{NSMutableArray} or immutable C{NSArray}).

       @raise RuntimeError: If C{len} vs C{count} assertion failed.

       @see: Functions L{list2NS} and L{tuple2NS}.
    '''
    isinstanceOf(py, list, tuple, **_raiser_py)
    return _listuple2NS(py, frozen=isinstance(py, tuple))


def map2NS(py, frozen=True):
    '''Create an C{NS[Mutable]Array} from a Python C{map}.

       @param py: The value (C{map}).
       @keyword frozen: If C{True}, return an immutable C{NSArray}, otherwise
                        an C{NSMutableArray} (C{bool}).

       @return: The ObjC instance (C{NSArray} or C{NSMutableArray}).
    '''
    isinstanceOf(py, map, **_raiser_py)
    return _listuple2NS(py, frozen=frozen, count=False)


def None2NS(py):
    '''Return the C{NSNull} singleton for Python's C{None}.

       @param py: The value (C{None}).

       @return: The singleton (C{NSNull}).

       @raise ValueError: If I{py} is not C{None}.
    '''
    if py is None:
        return NSMain.Null
    raise ValueError(_fmt_invalid(None, py=repr(py)))


def py2NS(py):
    '''Convert (an instance of) a Python object into an
       instance of the equivalent C{NS...} ObjC class:

       @param py: The value (C{Python type}).

       @return: The ObjC instance (L{ObjCInstance}).

       @raise TypeError: Unhandled, unexpected C{Python type}.

       @note: Conversion map:
        - bool       -> NSBoolean/NSNumber
        - bytes      -> NSData (Python 3+ only)
        - bytearray  -> NSData
        - Decimal    -> NSDecimal
        - dict       -> NSMutableDictionary
        - float      -> NSNumber
        - frozendict -> NSDictionary, immutable
        - frozenset  -> NSSet, immutable
        - generator  -> NSArray, immutable (like tuple)
        - int        -> NSNumber
        - list       -> NSMutableArray
        - map        -> NSArray, immutable (like tuple, Python 3+ only)
        - None       -> NSNull
        - range      -> NSArray, immutable (like tuple)
        - set        -> NSMutableSet
        - str        -> NSStr, immutable
        - tuple      -> NSArray, immutable
        - unicode    -> NSStr, immutable

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
        else:  # some other types?
            if _isiterable(py):
                ns = iterable2NS
            else:
                t = _instr(type, 'py')
                t = _fmt('%s: %r', t, py)
                raise TypeError(_SPACE_(_unhandled_, t))
        _py2NS[type(py)] = ns
    return ns(py)


def range2NS(py, frozen=True):
    '''Create an C{NS[Mutable]Array} from a Python C{range}.

       @param py: The value (C{range}).
       @keyword frozen: If C{True}, return an immutable C{NSArray}, otherwise
                        an C{NSMutableArray} (C{bool}).

       @return: The ObjC instance (C{NSMutableArray} or immutable C{NSArray}).
    '''
    # isinstanceOf(py, range, **_raiser_py)
    return _listuple2NS(py, frozen=frozen, count=False)


def set2NS(py):
    '''Create an C{NSMutableSet} from a Python C{set} or C{frozenset}.

       @return: The ObjC instance (C{NSMutableSet}).

       @see: Function L{sets2NS} for further details.
    '''
    return _sets2NS(py, frozen=False)


def _sets2NS(py, frozen=False):
    '''(INTERNAL) Create an C{NS[Mutable]Set}.
    '''
    isinstanceOf(py, frozenset, set, **_raiser_py)
    _g = _libCF.CFSetGetCount
    ns = _iter2NS(NSMutableSet.set(), py, _g)
    if frozen:
        ns = _len2NS(py, NSSet.alloc().initWithSet_(ns), _g)
        ns._from_py2NS = True
    return ns


def sets2NS(py):
    '''Create an C{NS[Mutable]Set} instance from a Python C{set} or C{frozenset}.

       @param py: The value (C{set} or C{frozenset}).

       @return: The ObjC instance (C{NSMutableSet} or immutable C{NSSet}).

       @raise RuntimeError: If C{len} vs C{count} assertion failed.

       @raise TypeError: If I{py} is not C{set} nor C{frozenset}.
    '''
    return _sets2NS(py, frozen=isinstance(py, frozenset))


def str2NS(py):
    '''Create an C{NSStr} instance from a Python C{str}.

       @param py: The value (C{str}).

       @return: The ObjC instance (C{NSStr}).

       @see: Function L{strs2NS}.
    '''
    return NSStr(py)


def strs2NS(py, frozen=True):
    '''Create an C{NS[Mutable]String} from a Python C{str}.

       @param py: The value (C{str}).
       @keyword frozen: If C{True}, return an immutable C{NSString}, otherwise
                        an C{NSMutableString} (C{bool}).

       @return: The ObjC instance (C{NSMutableString} or immutable C{NSString}).

       @see: Function L{str2NS}.
    '''
    NS = NSString if frozen else NSMutableString
    return NS.alloc().init(str(py))


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
    elif isinstanceOf(py, *_Numbers, **_raiser_py):
        s, t = since, float(py)
    NS = NSDate.alloc()
    m_ = NS.initWithTimeIntervalSince1970_ if s == 1970 else (
         NS.initWithTimeIntervalSinceNow_  if s != 2001 else
         NS.initWithTimeIntervalSinceReferenceDate_)
    return m_(t)


def tuple2NS(py):
    '''Create an immutable C{NSArray} instance from a Python C{tuple} or C{list}.

       @return: The ObjC instance (C{NSArray}, immutable).

       @see: Function L{listuple2NS} for further details.
    '''
    isinstanceOf(py, list, tuple, **_raiser_py)
    return _listuple2NS(py, frozen=True)


def unicode2NS(py):
    '''Create an C{NSStr} instance from a Python C{unicode} string.

       @param py: The value (C{unicode}).

       @return: The ObjC instance (C{NSStr}).
    '''
    return NSStr(py.encode(_DEFAULT_UNICODE))  # .stringWithUTF8String_


def url2NS(py, url2=None):
    '''Create an C{NSURL} instance from a Python string.

       @param py: The URL (C{str} or C{unicode}).
       @keyword url2: Optionally, relative to this URL (C{str} or C{unicode}).

       @return: The ObjC instance (C{NSURL}).

       @see: U{URL<https://Developer.Apple.com/documentation/foundation/url>}
             for parsing an C{NSURL}.
    '''
    ns = _NSStr(py)
    NS =  NSURL.alloc()
    if _COLON_ in bytes2str(py):
        nu = NS.initWithString_(ns) if not url2 else \
             NS.initWithString_relativeToURL_(ns, url2NS(url2))
    elif url2:
        nu = NS.initFileURLWithPath_relativeToURL_(ns, url2NS(url2))
    else:
        nu = NS.initFileURLWithPath_(ns)
    return nu


def type2NS(py):
    '''Create the C{NS...} ObjC object for a Python Type (or wrapper) instance.

       @param py: The value (C{Type}).

       @return: The ObjC instance (L{ObjCInstance}).

       @raise TypeError: Unhandled, unexpected C{Type}.

       @see: Function L{py2NS}.
    '''
    try:
        return py.NS
    except AttributeError:
        return py2NS(py)


_py2NS = {bool:       bool2NS,
          bytearray:  bytes2NS,
         _Decimal:    decimal2NS,
          dict:       dict2NS,
          float:      float2NS,
          frozendict: frozendict2NS,
          frozenset:  frozenset2NS,
         _Generator:  generator2NS,
          int:        int2NS,
#        _Iterable:   iterable2NS,
          list:       list2NS,
          range:      range2NS,
          set:        set2NS,
          str:        str2NS,
          tuple:      tuple2NS,
          type(None): None2NS}
try:
    _py2NS.update({long:    int2NS,
                   unicode: unicode2NS})
except NameError:  # Python 3+
    _py2NS.update({bytes: bytes2NS,
                   map:   map2NS})

if __name__ == _Dmain_:

    from pycocoa.utils import _all_listing

    _all_listing(__all__, locals())

# % python3 -m pycocoa.pytypes
#
# pycocoa.pytypes.__all__ = tuple(
#  pycocoa.pytypes.bool2NS is <function .bool2NS at 0x1049b4d60>,
#  pycocoa.pytypes.bytes2NS is <function .bytes2NS at 0x1049b4fe0>,
#  pycocoa.pytypes.decimal2NS is <function .decimal2NS at 0x104d1ae80>,
#  pycocoa.pytypes.dict2NS is <function .dict2NS at 0x104d1b100>,
#  pycocoa.pytypes.dicts2NS is <function .dicts2NS at 0x104d1b240>,
#  pycocoa.pytypes.float2NS is <function .float2NS at 0x104d1b2e0>,
#  pycocoa.pytypes.frozendict2NS is <function .frozendict2NS at 0x104d1b380>,
#  pycocoa.pytypes.frozenset2NS is <function .frozenset2NS at 0x104d1b420>,
#  pycocoa.pytypes.generator2NS is <function .generator2NS at 0x104d1b4c0>,
#  pycocoa.pytypes.int2NS is <function .int2NS at 0x104d1b560>,
#  pycocoa.pytypes.iterable2NS is <function .iterable2NS at 0x104d1b6a0>,
#  pycocoa.pytypes.list2NS is <function .list2NS at 0x104d1b7e0>,
#  pycocoa.pytypes.listuple2NS is <function .listuple2NS at 0x104d1b920>,
#  pycocoa.pytypes.map2NS is <function .map2NS at 0x104d1b9c0>,
#  pycocoa.pytypes.None2NS is <function .None2NS at 0x104d1ba60>,
#  pycocoa.pytypes.py2NS is <function .py2NS at 0x104d1bb00>,
#  pycocoa.pytypes.range2NS is <function .range2NS at 0x104d1bba0>,
#  pycocoa.pytypes.set2NS is <function .set2NS at 0x104d1bc40>,
#  pycocoa.pytypes.sets2NS is <function .sets2NS at 0x104d1bd80>,
#  pycocoa.pytypes.str2NS is <function .str2NS at 0x104d1be20>,
#  pycocoa.pytypes.strs2NS is <function .strs2NS at 0x104d1bec0>,
#  pycocoa.pytypes.time2NS is <function .time2NS at 0x104d1bf60>,
#  pycocoa.pytypes.tuple2NS is <function .tuple2NS at 0x104d1c040>,
#  pycocoa.pytypes.type2NS is <function .type2NS at 0x104d1c220>,
#  pycocoa.pytypes.unicode2NS is <function .unicode2NS at 0x104d1c0e0>,
#  pycocoa.pytypes.url2NS is <function .url2NS at 0x104d1c180>,
# )[26]
# pycocoa.pytypes.version 25.2.25, .isLazy 1, Python 3.13.2 64bit arm64, macOS 14.7.3

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
