
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

# Several Objective-C/Cheader files are also available at
# <http://GitHub.com/gnustep/libs-gui/tree/master/Headers>

# all imports listed explicitly to help PyChecker
from decimal import Decimal
from ctypes  import ArgumentError, byref, cast, CFUNCTYPE, \
                    c_buffer, c_byte, c_char, c_double, c_float, \
                    c_int, c_int8, c_int16, c_int32, c_int64, \
                    c_long, c_longlong, c_short, c_void_p
from oclibs  import CGFloat, CFIndex, kCFStringEncodingUTF8, \
                    libCF, libF, libobjc
from octypes import _2bytes, _2clip, _2str, _iterbytes, \
                    DEFAULT_UNICODE, Class, Id, NSInteger, \
                    NSPoint, NSRect, NSSize, SEL
from runtime import _xargs, isInstanceOf, ObjCClass, ObjCInstance, \
                    get_selector

__version__ = '17.11.19'


def _noop(arg):
    # inlieu of  lambda arg: arg
    return arg


class CFString(ObjCInstance):
    '''Create a CFString instance for a Python string.
    '''
    def __new__(cls, ustr):
        ustr = libCF.CFStringCreateWithCString(None, _2bytes(ustr), kCFStringEncodingUTF8)
        # the Objective-C class is .objc_class or __NSCFConstantString
        return super(CFString, cls).__new__(cls, c_void_p(ustr))

    def objc_classname(self):
        return '%s(%r)' % (self.__class__.__name__, _2clip(nsString2str(self)))


# some commonly used Foundation and Cocoa classes, described here
# <http://omz-software.com/pythonista/docs/ios/objc_util.html>
NSApplication       = ObjCClass('NSApplication')
NSArray             = ObjCClass('NSArray')
NSAutoreleasePool   = ObjCClass('NSAutoreleasePool')
NSBezierPath        = ObjCClass('NSBezierPath')
NSColor             = ObjCClass('NSColor')
NSData              = ObjCClass('NSData')
NSDecimalNumber_    = ObjCClass('NSDecimalNumber')  # see NSDecimalNumber below
NSDictionary        = ObjCClass('NSDictionary')
NSEnumerator        = ObjCClass('NSEnumerator')
NSImage             = ObjCClass('NSImage')
NSMenu              = ObjCClass('NSMenu')
NSMenuItem          = ObjCClass('NSMenuItem')
NSMutableArray      = ObjCClass('NSMutableArray')
NSMutableData       = ObjCClass('NSMutableData')
NSMutableDictionary = ObjCClass('NSMutableDictionary')
NSMutableSet        = ObjCClass('NSMutableSet')
NSMutableString     = ObjCClass('NSMutableString')
NSNull              = ObjCClass('NSNull')
NSNumber            = ObjCClass('NSNumber')
NSObject            = ObjCClass('NSObject')
NSOpenPanel         = ObjCClass('NSOpenPanel')
NSScreen            = ObjCClass('NSScreen')
NSSet               = ObjCClass('NSSet')
NSStatusBar         = ObjCClass('NSStatusBar')
NSString_           = ObjCClass('NSString')  # see NSString, at below
NSThread            = ObjCClass('NSThread')
NSURL               = ObjCClass('NSURL')
NSView              = ObjCClass('NSView')
NSWindow            = ObjCClass('NSWindow')
NSZeroPoint         = NSPoint(0, 0)


# We need to be able to create raw NSDecimalNumber objects.  If we use
# a normal ObjCClass() wrapper, the return values of constructors will
# be auto-converted back into Python Decimals.  However, we want to
# cache class/selector/method lookups without that overhead every time.
# Originally Rubicon-ObjC/objc/core_foundation.py>
class NSDecimalNumber(ObjCInstance):
    '''Optimized NSDecimalNumber class.
    '''
    objc_class = NSDecimalNumber_
    selector   = None

    def __new__(cls, pyobj):
        if not isinstance(pyobj, Decimal):
            raise TypeError('not %s: %r' % ('Decimal', pyobj))

        if cls.selector is None:
            cls.selector = get_selector('decimalNumberWithString:')
            m = libobjc.class_getClassMethod(cls.objc_class, cls.selector)
            impl = libobjc.method_getImplementation(m)
            cls.constructor = cast(impl, CFUNCTYPE(Id, Id, SEL, Id))

        d = cls.constructor(cast(cls.objc_class, Id), cls.selector,
                            NSString(pyobj.to_eng_string()))
        self = super(NSDecimalNumber, cls).__new__(cls, d)
        return self

    @property
    def value(self):
        '''Return the NSDecimalNumber value as int or float.
        '''
        d = self.doubleValue()  # PYCHOK axpected
        if d.is_integer():
            d = int(d)
        return d

    def ns2decimal(self):
        '''Create a Python Decimal from this NSDecimalNumber.
        '''
        return Decimal(self.value)

    def objc_classname(self):
        '''Return class name as a string.
        '''
        return '%s(%s)' % (self.__class__.__name__, _2clip(str(self.value)))

    def release(self):
        '''Garbage collect this NSDecimalNumber.
        '''
        self.autorelease()  # PYCHOK expected


def NSLog(fmt, *args):
    '''Formatted write to the console.
    '''
    if args:
        fmt %= args
    libF.NSLog(NSString(fmt))


def NSMakePoint(x, y):
    '''Return an NSPoint instance for the given x and y.
    '''
    return NSPoint(x, y)


def NSMakeRect(x, y, w, h):
    '''Return an NSRect instance for the given point and size.
    '''
    return NSRect(NSPoint(x, y), NSSize(w, h))


def NSMakeSize(w, h):
    '''Return an NSSize instance for the given w and h.
    '''
    return NSSize(w, h)


class NSString(CFString):
    '''Auto-released version of the L{CFString} class.
    '''
    def __new__(cls, ustr):
        # the Objective-C class is .objc_class or __NSCFString
        self = super(NSString, cls).__new__(cls, ustr)
        self.autorelease()  # PYCHOK expected
        return self


class at(NSString):
    '''Acronym for the L{NSString} class.
    '''
    # XXX Other possible names for this method: at, ampersat, arobe,
    # apenstaartje (little monkey tail), strudel, klammeraffe (spider
    # monkey), little_mouse, arroba, sobachka (doggie), malpa (monkey),
    # snabel (trunk), papaki (small duck), afna (monkey), kukac (caterpillar).
    pass


def _NS2py(obj, ctype):
    # helper function
    if not isinstance(obj, ctype):
        obj = ctype(obj)
    return ns2py(obj)


def nsArray2listuple(nsArray, ctype=c_void_p):  # XXX an NS*Array method?
    '''Create a Python list or tuple from an NS/CFArray.
    '''
    if isInstanceOf(nsArray, NSMutableArray):
        t = list
    elif isInstanceOf(nsArray, NSArray):
        t = tuple
    else:
        raise TypeError('not an %s: %r' % ('NS/CFArray', nsArray))

    n = libCF.CFArrayGetCount(nsArray)
    return t(_NS2py(libCF.CFArrayGetValueAtIndex(nsArray, i), ctype) for i in range(n))


def nsBoolean2bool(nsBool, default=None):  # XXX an NSBoolean method?
    '''Create a Python bool from an NS/CFBoolean.
    '''
    # XXX need allow c_void_p for nested booleans in lists, sets, etc.?
    if not isInstanceOf(nsBool, NSNumber, c_void_p=c_void_p):
        raise TypeError('not an %s: %r' % ('NS/CFBoolean', nsBool))

    cfType = libCF.CFNumberGetType(nsBool)
    assert cfType == kCFNumberCharType
    num = c_byte()
    if libCF.CFNumberGetValue(nsBool, cfType, byref(num)):
        return True if num.value else False
    return default


def nsData2bytes(nsData, default=b''):  # XXX an NSData method?
    '''Create Python bytes from NS/CFData.
    '''
    if not isInstanceOf(nsData, NSData):
        raise TypeError('not %s: %r' % ('NS/CFData', nsData))

    n = nsData.length()
    if n:
        buf = (c_byte * n)()
        nsData.getBytes_length_(byref(buf), n)
        return b''.join(_iterbytes(buf[:n]))
    return default


def nsDecimalNumber2decimal(nsDecimal):
    '''Create a Python Decimal from an NS/CFDecimalNumber.
    '''
    if not isinstance(nsDecimal, NSDecimalNumber):  # PYCHOK expected
        raise TypeError('not an %s: %r' % ('NS/CFDecimalNumber', nsDecimal))

    return nsDecimal.ns2decimal()


def nsDictionary2dict(nsDict, ctype_keys=c_void_p, ctype_vals=c_void_p):  # XXX an NS*Dictionary method?
    '''Create a Python dict from an NS/CFDictionary.
    '''
    if not isInstanceOf(nsDict, NSMutableDictionary, NSDictionary):
        raise TypeError('not an %s: %r' % ('NS/CFDictionary', nsDict))

    # <http://Developer.Apple.com/documentation/corefoundation/cfdictionary-rum>
    n = libCF.CFDictionaryGetCount(nsDict)
    keys = (ctype_keys * n)()
    vals = (ctype_vals * n)()
    libCF.CFDictionaryGetKeysAndValues(nsDict, byref(keys), byref(vals))
    return dict((_NS2py(keys[i], ctype_keys),
                 _NS2py(vals[i], ctype_vals)) for i in range(n))


def nsNull2none(nsNull):
    '''Creat Python None from an NS/CFNull.
    '''
    if isInstanceOf(nsNull, NSNull, c_void_p=c_void_p):
        return None
    raise TypeError('not %s: %r' % ('NS/CFNull', nsNull))


# <http://GitHub.com/opensource-apple/CF/blob/master/CFNumber.h>
kCFNumberSInt8Type     = 1
kCFNumberSInt16Type    = 2
kCFNumberSInt32Type    = 3
kCFNumberSInt64Type    = 4
kCFNumberFloat32Type   = 5
kCFNumberFloat64Type   = 6
kCFNumberCharType      = 7
kCFNumberShortType     = 8
kCFNumberIntType       = 9
kCFNumberLongType      = 10
kCFNumberLongLongType  = 11
kCFNumberFloatType     = 12
kCFNumberDoubleType    = 13
kCFNumberCFIndexType   = 14
kCFNumberNSIntegerType = 15
kCFNumberCGFloatType   = 16
kCFNumberMaxType       = 16

_CFNumberType2ctype = {kCFNumberSInt8Type:     c_int8,
                       kCFNumberSInt16Type:    c_int16,
                       kCFNumberSInt32Type:    c_int32,
                       kCFNumberSInt64Type:    c_int64,
                       kCFNumberFloat32Type:   c_float,
                       kCFNumberFloat64Type:   c_double,
                       kCFNumberCharType:      c_char,
                       kCFNumberShortType:     c_short,
                       kCFNumberIntType:       c_int,
                       kCFNumberLongType:      c_long,
                       kCFNumberLongLongType:  c_longlong,
                       kCFNumberFloatType:     c_float,
                       kCFNumberDoubleType:    c_double,
                       kCFNumberCFIndexType:   CFIndex,
                       kCFNumberNSIntegerType: NSInteger,
                       kCFNumberCGFloatType:   CGFloat}


def nsNumber2num(nsNumber, default=None):  # XXX an NSNumber method?
    '''Create a Python decimal, int or float from an NS/CFNumber.
    '''
    # XXX need c_void_p for nested numbers in lists, sets, etc.?
    if not isInstanceOf(nsNumber, NSNumber, c_void_p=c_void_p):
        raise TypeError('not an %s: %r' % ('NS/CFNumber', nsNumber))
    # special case for NSDecimalNumber, would become a float
    # since cfType of NSDecimalNumber is kCFNumberDoubleType
    if isinstance(nsNumber, NSDecimalNumber):
        return nsDecimalNumber2decimal(nsNumber)

    cfType = libCF.CFNumberGetType(nsNumber)
    try:
        ctype = _CFNumberType2ctype[cfType]
        num = ctype()
        if libCF.CFNumberGetValue(nsNumber, cfType, byref(num)):
            return num.value
    except KeyError:
        raise TypeError('unhandled %s: %r ' % ('CFNumberType', cfType))
    return default


def nsSet2set(nsSet, ctype=c_void_p):  # XXX NS*Set method?
    '''Create a Python set or frozenset from an NS/CFSet.
    '''
    if isInstanceOf(nsSet, NSMutableSet):
        t = set
    elif isInstanceOf(nsSet, NSSet):
        t = frozenset
    else:
        raise TypeError('not an %s: %r' % ('NS/CFSet', nsSet))

    n = libCF.CFSetGetCount(nsSet)  # == nsSet.count()
    buf = (ctype * n)()
    libCF.CFSetGetValues(nsSet, byref(buf))
    return t(_NS2py(buf[i], ctype) for i in range(n))


def nsString2str(nsString, default=None):  # XXX an NS*String method
    '''Create a Python string or unicode from an NS/CFString.
    '''
    # XXX need c_void_p for nested strings in lists, sets, etc.?
    if not (isinstance(nsString, (CFString, NSString, c_void_p)) or
            isInstanceOf(nsString, NSString_, NSMutableString)):
        raise TypeError('not an %s: %r' % ('NS/CFString', nsString))

    n = libCF.CFStringGetLength(nsString)
    u = libCF.CFStringGetMaximumSizeForEncoding(n, kCFStringEncodingUTF8)
    buf = c_buffer(u + 2)
    if libCF.CFStringGetCString(nsString, buf, len(buf), kCFStringEncodingUTF8):
        # assert(isinstance(buf.value, bytes))
        # bytes to unicode in Python 2 or str in Python 3+
        return _2str(buf.value)  # XXX was .decode(DEFAULT_UNICODE)
    return default


_CFTypeID2py = {libCF.CFArrayGetTypeID():      nsArray2listuple,
                libCF.CFBooleanGetTypeID():    nsBoolean2bool,
                libCF.CFDataGetTypeID():       nsData2bytes,
                libCF.CFDictionaryGetTypeID(): nsDictionary2dict,
                libCF.CFNullGetTypeID():       nsNull2none,
                libCF.CFNumberGetTypeID():     nsNumber2num,
                libCF.CFSetGetTypeID():        nsSet2set,
                libCF.CFStringGetTypeID():     nsString2str}


def ns2py(nsObj, default=None):  # XXX an NSObject method?
    '''Convert an (instance of an) NS/CFObject to the
    equivalent Python type and value.

     - NSArray         -> tuple
     - NSBoolean       -> bool
     - NSData          -> bytes
     - NSDecimalNumber -> Decimal
     - NSDictionary    -> dict
     - NSMutableArray  -> list
     - NSMutableSet    -> set
     - NSMutableString -> str
     - NSNumber        -> int or float
     - NSNull          -> None
     - NSSet           -> frozenset
     - NSString        -> str
    '''
    if nsObj is not None:
        # see Rubicon-ObjC/objc/core_foundation.py
        # if isinstance(nsObj, ObjCInstance):
        #     nsObj = nsObj._as_parameter_
        try:
            typeID = libCF.CFGetTypeID(nsObj)
            r = _CFTypeID2py[typeID](nsObj)
            c = {Class: ObjCClass,
                 Id:    ObjCInstance}.get(type(r), _noop)
            return c(r)
        except ArgumentError as x:
            _xargs(x, libCF.CFGetTypeID.__name__,
                      libCF.CFGetTypeID.argtypes,
                      libCF.CFGetTypeID.restype)
            raise
        except KeyError:
            if default is None:
                t = ', '.join('%d: %s' % t for t in sorted((int(i), f.__name__)
                                           for i, f in _CFTypeID2py.items()))
                t = (typeID, nsObj, t)
                raise TypeError('unhandled TypeID %r: %r {%s}' % t)
    return default


def _bytes2NS(pyobj):
    '''Create NS/CFData from Python bytes.
    '''
    def _length(ns):
        return ns.length()

    return _len2NS(pyobj, NSData.dataWithBytes_length_(pyobj, len(pyobj)),
                         _length)  # XXX lambda ns: ns.length()


def _dict2NS(pyobj):
    '''Create an NSMutableDictionary from a Python dict.
    '''
    # http://Developer.Apple.com/library/content/documentation/Cocoa/
    #        Conceptual/Collections/Articles/Dictionaries.html
    ns = NSMutableDictionary.dictionary()
    for k, v in pyobj.get('iteritems', pyobj.items)():
        ns.setObject_forKey_(py2NS(v), py2NS(k))
    return _len2NS(pyobj, ns, libCF.CFDictionaryGetCount)


def _frozenset2NS(pyobj):
    '''Create an immutable NSSet from a Python frozenset.
    '''
    return _len2NS(pyobj, NSSet.alloc().initWithSet_(_set2NS(pyobj)),
                          libCF.CFSetGetCount)


def _iter2NS(ns, pyobj, getCount):
    # create NS objects for each Python list, frozen/set, tuple item
    for nsobj in map(py2NS, pyobj):
        ns.addObject_(nsobj)
    return _len2NS(pyobj, ns, getCount)


def _len2NS(pyobj, ns, getCount):
    # check the Python len and NS instance count
    n, m = len(pyobj), getCount(ns)
    if m != n:
        t = (ns.objc_classname(), m, _2clip(repr(pyobj)), n)
        raise AssertionError('%s[%s] vs %s[%s]' % t)
    return ns


def _list2NS(pyobj):
    '''Create an NSMutableArray from a Python list.
    '''
    return _iter2NS(NSMutableArray.array(), pyobj, libCF.CFArrayGetCount)


_nsNull = NSNull.alloc().init()


def _none2NS(pyobj):
    '''Create an NSNull from Python's None.
    '''
    if pyobj is None:
        return _nsNull
    raise TypeError('not %s: %r' % ('None', pyobj))


def _set2NS(pyobj):
    '''Create an NSMutableSet from a Python set.
    '''
    return _iter2NS(NSMutableSet.set(), pyobj, libCF.CFSetGetCount)


def _tuple2NS(pyobj):
    '''Create an immutable NSArray from a Python tuple.
    '''
    return _len2NS(pyobj, NSArray.alloc().initWithArray_(_list2NS(pyobj)),
                          libCF.CFArrayGetCount)


def _unicode2NS(pyobj):
    '''Create an NSString from a Python unicode string.
    '''
    return NSString(pyobj.encode(DEFAULT_UNICODE))  # .stringWithUTF8String_


_py2NS = {bool:        NSNumber.numberWithBool_,
          Decimal:     NSDecimalNumber,
          dict:       _dict2NS,
          float:       NSNumber.numberWithDouble_,
          frozenset:  _frozenset2NS,
          int:         NSNumber.numberWithInt_,  # Long_, LongLong_
          list:       _list2NS,
          set:        _set2NS,
          str:         NSString,
          tuple:      _tuple2NS,
          type(None): _none2NS}
try:
    _py2NS.update({bytearray: _bytes2NS,
                   long:       NSNumber.numberWithLongLong_,
                   unicode:   _unicode2NS})
except NameError:  # Python 3+
    _py2NS.update({bytes: _bytes2NS})


def py2NS(pyobj):
    '''Convert an (instance of a) Python object into an
    instance of an NS... Objective-C class as follows:

     - bool      -> NSBoolean/NSNumber
     - bytes     -> NSData
     - bytearray -> NSData
     - Decimal   -> NSDecimalNumber
     - dict      -> NSMutableDictionary
     - float     -> NSNumber
     - frozenset -> NSSet, immutable
     - int       -> NSNumber
     - list      -> NSMutableArray
     - None      -> NSNull
     - set       -> NSMutableSet
     - str       -> NSString, immutable
     - tuple     -> NSArray, immutable
     - unicode   -> NSString, immutable
    '''
    if isinstance(pyobj, ObjCInstance):
        return pyobj
    elif isinstance(pyobj, c_void_p):
        return ObjCInstance(pyobj)

    ns = _py2NS.get(type(pyobj), None)
    if ns:
        return ns(pyobj)
    raise TypeError('unhandled %r' % (pyobj,))


# filter locals() for .__init__.py
__all__ = tuple(_ for _ in locals().keys() if _.startswith((
               'NS', 'ns'))) + ('at', 'CFString', 'py2NS')

if __name__ == '__main__':

    from octypes import _allist

    _allist(__all__, locals(), __version__, __file__)
