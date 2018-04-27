
# -*- coding: utf-8 -*-

# Originally <http://GitHub.com/phillip-nguyen/cocoa-python>

# objective-ctypes
#
# Copyright (C) 2011 Phillip Nguyen -- All rights reserved.
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

# MIT License <http://opensource.org/licenses/MIT>
#
# Copyright (C) 2017-2018 mrJean1 at Gmail dot com
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

# Several Objective-C/C header files are also available at
# <http://GitHub.com/gnustep/libs-gui/tree/master/Headers>

'''Conversions from ObjC C{NS...} instances to Python.
'''
# all imports listed explicitly to help PyChecker
from decimal import Decimal as _Decimal
from ctypes  import c_void_p
from nstypes import NSArray, NSBool, NSData, NSDecimal, NSDouble, \
                    NSInt, NSLong, NSLongLong, NSMutableArray, \
                    NSMutableDictionary, NSMutableSet, NSNone, \
                    NSSet, NSStr, NSURL
from oslibs  import libCF
from runtime import ObjCInstance
from types   import GeneratorType as _generator
from utils   import clip, DEFAULT_UNICODE, _exports, _Ints

__version__ = '18.04.26'


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
        t = (ns.objc_classname, m, clip(repr(py)), n)
        raise AssertionError('%s[%s] vs %s[%s]' % t)
    return ns


_NSFalse = NSBool(False)  # singleton
_NSTrue  = NSBool(True)   # singleton


def bool2NS(py):
    '''Create an C{NSBool} instance from a Python C{bool}.

       @param py: The value (C{int} or C{bool}).

       @return: The C{NS...} singleton (C{NSBool}).
    '''
    return _NSTrue if py else _NSFalse


def bytes2NS(py):
    '''Create an C{NSData} instance from Python C{bytes}.

       @param py: The value (C{bytes}).

       @return: The ObjC instance (C{NSData}).

       @raise AssertionError: If C{len} vs C{count} assertion failed.
    '''
    def _NSData_length(ns):  # XXX lambda ns: ns.length()
        return ns.length()

    return _len2NS(py, NSData.dataWithBytes_length_(py, len(py)),
                      _NSData_length)


def dict2NS(py):
    '''Create an C{NSMutableDictionary} instance from a Python C{dict}.

       @param py: The value (C{dict}).

       @return: The ObjC instance (C{NSMutableDictionary}).

       @raise AssertionError: If C{len} vs C{count} assertion failed.
    '''
    # http://Developer.Apple.com/library/content/documentation/Cocoa/
    #        Conceptual/Collections/Articles/Dictionaries.html
    ns = NSMutableDictionary.dictionary()
    for k, v in py.get('iteritems', py.items)():
        ns.setObject_forKey_(py2NS(v), py2NS(k))
    return _len2NS(py, ns, libCF.CFDictionaryGetCount)


def frozenset2NS(py):
    '''Create an (immutable) C{NSSet} instance from a Python C{frozenset}.

       @param py: The value (C{frozenset}).

       @return: The ObjC instance (C{NSSet}).

       @raise AssertionError: If C{len} vs C{count} assertion failed.
    '''
    return _len2NS(py, NSSet.alloc().initWithSet_(set2NS(py)),
                       libCF.CFSetGetCount)


def generator2NS(py):
    '''Create an C{NSArray} instance from a Python C{generator}.

       @param py: The value (C{generator}).

       @return: The ObjC instance (C{NSArray}).

       @raise AssertionError: If C{len} vs C{count} assertion failed.
    '''
    return tuple2NS(tuple(py))


def int2NS(py):
    '''Create an C{NSNumber} instance from a Python C{int} or C{long}.

       @param py: The value (C{int} or C{long}).

       @return: The ObjC instance (C{NSInt}, C{NSLong}, or C{NSLongLong}).

       @raise TypeError: If C{py} not an C{int} or C{long}.
    '''
    if isinstance(py, _Ints):
        if abs(py) < 1 << 31:
            return NSInt(py)
        elif abs(py) < 1 << 63:
            return NSLong(py)
        else:
            return NSLongLong(py)
    raise TypeError('%s not %s: %r' % ('py', 'int', py))


def list2NS(py):
    '''Create an C{NSMutableArray} instance from a Python C{list}.

       @param py: The value (C{list}).

       @return: The ObjC instance (C{NSMutableArray}).

       @raise AssertionError: If C{len} vs C{count} assertion failed.
    '''
    return _iter2NS(NSMutableArray.array(), py, libCF.CFArrayGetCount)


def map2NS(py):
    '''Create an C{NSArray} instance from a Python C{map}.

       @param py: The value (C{map}).

       @return: The ObjC instance (C{NSArray}).

       @raise AssertionError: If C{len} vs C{count} assertion failed.
    '''
    return tuple2NS(tuple(py))


def None2NS(py):
    '''Return the C{NSNone} singleton for Python's C{None}.

       @param py: The value (C{None}).

       @return: The singleton (C{NSNone}).

       @raise ValueError: If I{py} is not C{None}.
    '''
    if py is None:
        return NSNone
    raise ValueError('%s not %s: %r' % ('py', 'None', py))


def range2NS(py):
    '''Create an C{NSArray} instance from a Python C{range}.

       @param py: The value (C{range}).

       @return: The ObjC instance (C{NSArray}).

       @raise AssertionError: If C{len} vs C{count} assertion failed.
    '''
    return tuple2NS(tuple(py))


def set2NS(py):
    '''Create an C{NSMutableSet} instance from a Python C{set}.

       @param py: The value (C{set}).

       @return: The ObjC instance (C{NSMutableSet}).

       @raise AssertionError: If C{len} vs C{count} assertion failed.
    '''
    return _iter2NS(NSMutableSet.set(), py, libCF.CFSetGetCount)


def str2NS(py, auto=True):
    '''Create an C{NSStr} instance from a Python C{str}.

       @param py: The value (C{str}).
       @keyword auto: Retain or auto-release (bool).

       @return: The ObjC instance (C{NSStr[ing]}).
    '''
    return NSStr(py, auto=auto)


def tuple2NS(py):
    '''Create an immutable C{NSArray} instance from a Python C{tuple}.

       @param py: The value (C{tuple}).

       @return: The ObjC instance (C{NSArray}).

       @raise AssertionError: If C{len} vs C{count} assertion failed.
    '''
    return _len2NS(py, NSArray.alloc().initWithArray_(list2NS(py)),
                       libCF.CFArrayGetCount)


def unicode2NS(py, auto=True):
    '''Create an C{NSStr} instance from a Python C{unicode} string.

       @param py: The value (C{unicode}).
       @keyword auto: Retain or auto-release (bool).

       @return: The ObjC instance (C{NSStr[ing]}).
    '''
    return NSStr(py.encode(DEFAULT_UNICODE), auto=auto)  # .stringWithUTF8String_


def url2NS(py, url2=None):
    '''Create an C{NSURL} instance from a Python string.

       @param py: The URL (C{str} or C{unicode}).
       @keyword url2: Optionally, relative to this URL (C{str} or C{unicode}).

       @return: The ObjC instance (C{NSURL}).

       @see: U{URL<http://Developer.Apple.com//documentation/foundation/url>}
             for parsing an C{NSURL}.
    '''
    ns = NSStr(py)
    if url2:
        return NSURL.alloc().initWithString_relativeToURL_(ns, url2NS(url2))
    else:
        return NSURL.alloc().initWithString_(ns)


_py2NS = {bool:       bool2NS,
          bytearray:  bytes2NS,
         _Decimal:    NSDecimal,
          dict:       dict2NS,
          float:      NSDouble,
          frozenset:  frozenset2NS,
         _generator:  generator2NS,
          int:        int2NS,
          list:       list2NS,
          set:        set2NS,
          range:      range2NS,
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
    '''
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
            raise TypeError('unhandled %s(%s): %r' % ('type', 'py', py))
        _py2NS[type(py)] = ns
    return ns(py)


def type2NS(py):
    '''Create an C{NS/Instance} for a Python Type or wrapper instance.

       @param py: The value (C{Type}).

       @return: The ObjC instance (L{ObjCInstance}).

       @raise TypeError: Unhandled, unexpected C{Type}.

       @see: Function L{py2NS}.
    '''
    try:
        return py.Ns
    except AttributeError:
        return py2NS(py)


# filter locals() for .__init__.py
__all__ = _exports(locals(),
                   ends='2NS')

if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)
