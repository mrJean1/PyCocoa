
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

'''ObjC classes C{NS...} and conversions from C{NS...} to Python and vice versa.
'''
# all imports listed explicitly to help PyChecker
from decimal import Decimal as _Decimal
from ctypes  import ArgumentError, byref, cast, c_buffer, c_byte, \
                    CFUNCTYPE, c_void_p
from getters import get_selector
from oclibs  import cfNumber2bool, cfNumber2num, kCFStringEncodingUTF8, \
                    libCF, libFoundation, libobjc
from octypes import Array_t, Class_t, c_struct_t, Id_t, ObjC_t, SEL_t, Set_t
from runtime import isInstanceOf, ObjCClass, ObjCInstance, _Xargs
from utils   import bytes2str, clip, DEFAULT_UNICODE, _exports, \
                    _Globals, instanceof, iterbytes, missing, str2bytes

__version__ = '18.04.21'


def _lambda(arg):
    # inlieu of  lambda arg: arg
    return arg


def _ns2ctype2py(ns, ctype):
    # helper function
    if not isinstance(ns, ctype):
        ns = ctype(ns)
    return ns2py(ns)


class _Constants(object):
    '''Only constant, readable attributes.
    '''
    def __init__(self, *unused):
        raise AssertionError('%s is constant' % (self.__class__.__name__,))

    __setattr__ = __init__


class _Types(_Constants):
    '''Holder of the Python Types, to avoid circular imports.
    '''
    Dict       = None  # set by .dicts.py
    Item       = None
    FrozenDict = None  # set by .dicts.py
    FrozenSet  = None  # set by .sets.py
    List       = None  # set by .listuples.py
    Menu       = None
    OpenPanel  = None
    Set        = None  # set by .sets.py
    Str        = None  # set by .strs.py
    Table      = None
    Tuple      = None  # set by .listuples.py
    Window     = None

    @staticmethod
    def listypes():
        for a, v in sorted(_Types.__dict__.items()):
            if not a.startswith('_'):
                print('_Types.%-11s %r' % (a + ':', v))


class CFStr(ObjCInstance):
    '''Python wrapper for the ObjC C{CFString} class,
    creating I{retained} instances, by default.
    '''
    _str = None

    def __new__(cls, ustr):
        ustr = str(ustr)
        ns = libCF.CFStringCreateWithCString(None, str2bytes(ustr), kCFStringEncodingUTF8)
        # the ObjC class is ._objc_class or __NSCFConstantString
        self = super(CFStr, cls).__new__(cls, ns)  # Id_t
        self._str = ustr
        return self

    def __str__(self):
        return '%s(%r)' % (self.objc_classname, clip(self.value))

#   @property
#   def objc_classname(self):
#       return self.__class__.__name__

    @property
    def value(self):
        '''Return the C{CFStr} value as str.
        '''
        if self._str is None:
            self._str = nsString2str(self)
        return self._str

    str = value


# some commonly used Foundation and Cocoa classes, described here
# <http://omz-software.com/pythonista/docs/ios/objc_util.html>

# NS... classes marked ** have Python versions, like NSStr, for
# for use by runtime.isInstanceOf repectively octypes.instanceof
NSApplication          = ObjCClass('NSApplication')
NSArray                = ObjCClass('NSArray')  # immutable
NSAutoreleasePool      = ObjCClass('NSAutoreleasePool')
NSBezierPath           = ObjCClass('NSBezierPath')
NSBundle               = ObjCClass('NSBundle')
NSColor                = ObjCClass('NSColor')
NSConstantString       = ObjCClass('NSConstantString')  # use NSStr
NSData                 = ObjCClass('NSData')
NSDecimalNumber        = ObjCClass('NSDecimalNumber')  # ** use NSDecimal
NSDictionary           = ObjCClass('NSDictionary')  # immutable
NSDockTile             = ObjCClass('NSDockTile')
NSEnumerator           = ObjCClass('NSEnumerator')
NSFont                 = ObjCClass('NSFont')
NSImage                = ObjCClass('NSImage')
NSMenu                 = ObjCClass('NSMenu')
NSMenuItem             = ObjCClass('NSMenuItem')
NSMutableArray         = ObjCClass('NSMutableArray')
NSMutableData          = ObjCClass('NSMutableData')
NSMutableDictionary    = ObjCClass('NSMutableDictionary')
NSMutableSet           = ObjCClass('NSMutableSet')
NSMutableString        = ObjCClass('NSMutableString')
NSConcreteNotification = ObjCClass('NSConcreteNotification')
NSNotification         = ObjCClass('NSNotification')
NSNull                 = ObjCClass('NSNull')
NSNumber               = ObjCClass('NSNumber')
NSObject               = ObjCClass('NSObject')
NSOpenPanel            = ObjCClass('NSOpenPanel')
# NSPoint              = ObjCClass('NSPoint')  # doesn't exist, use NSPoint_t
# NSRect               = ObjCClass('NSRect')  # doesn't exist, use NSRect_t
# NSRange              = ObjCClass('NSRange')  # doesn't exist, use NSRange_t
NSScreen               = ObjCClass('NSScreen')
NSScrollView           = ObjCClass('NSScrollView')
NSSet                  = ObjCClass('NSSet')
# NSSize               = ObjCClass('NSSize')  # doesn't exist, use NSSize_t
NSStatusBar            = ObjCClass('NSStatusBar')
NSString               = ObjCClass('NSString')  # ** use NSStr or 'at'
NSTableColumn          = ObjCClass('NSTableColumn')
NSTableView            = ObjCClass('NSTableView')
NSThread               = ObjCClass('NSThread')
NSURL                  = ObjCClass('NSURL')
NSView                 = ObjCClass('NSView')
NSWindow               = ObjCClass('NSWindow')

# some NS... types and /singletons
NSBool     = NSNumber.numberWithBool_
NSDouble   = NSNumber.numberWithDouble_
NSFalse    = False  # NSBool(False)  # c_byte
NSFloat    = NSNumber.numberWithDouble_
NSInt      = NSNumber.numberWithInt_
NSLong     = NSNumber.numberWithLong_
NSLongLong = NSNumber.numberWithLongLong_
NSnil      = None  # nil return value
NSNone     = NSNull.alloc().init()  # singleton
NSTrue     = True  # NSBool(True)  # c_byte


# We need to be able to create raw NSDecimalNumber objects.  If we use
# a normal ObjCClass() wrapper, the return values of constructors will
# be auto-converted back into Python Decimals.  However, we want to
# cache class/selector/method lookups without that overhead every time.
# Originally, an older rev of .../Rubicon-ObjC/objc/core_foundation.py.
class NSDecimal(ObjCInstance):
    '''Optimized C{NSDecimalNumber} class.
    '''
    _Class = NSDecimalNumber
    _IMP   = None
    _SEL   = None

    def __new__(cls, py):
        if isinstance(py, NSDecimal):
            py = py.Decimal
        else:
            py = _Decimal(py)  # from Decimal, float, int, str
        py = py.to_eng_string()  # XXX to maintain accuracy

        if None in (cls._IMP, cls._SEL):
            cls._SEL = get_selector('decimalNumberWithString:')
            m = libobjc.class_getClassMethod(cls._Class, cls._SEL)
            m = libobjc.method_getImplementation(m)
            cls._IMP = cast(m, CFUNCTYPE(Id_t, Id_t, SEL_t, Id_t))

        d = cls._IMP(cast(cls._Class, Id_t), cls._SEL, NSStr(py))
        self = super(NSDecimal, cls).__new__(cls, d)
# XXX?  self._objc_ptr = self._as_parameter_ = d  # for ctypes
        return self

    def __str__(self):
        return '%s(%s)' % (self.objc_classname, self.value)

    @property
    def double(self):
        '''Return this C{NSDecimal} as float.
        '''
        return self.doubleValue()  # PYCHOK expected

#   @property
#   def objc_classname(self):
#       return self.__class__.__name__

    @property
    def value(self):
        '''Return this C{NSDecimal} as Python C{Decimal}.
        '''
        d = self.doubleValue()  # PYCHOK expected
        if d.is_integer():
            d = int(d)
        return _Decimal(d)

    Decimal = value


class NSStr(CFStr):
    '''Python wrapper for the ObjC L{NSString} class,
    creating I{auto-released} instances, by default.
    '''
    def __new__(cls, ustr, auto=True):
        # the ObjC class is .objc_class or __NSCFString
        self = super(NSStr, cls).__new__(cls, ustr)
        if auto:
            self.autorelease()  # PYCHOK expected
        return self


class at(NSStr):
    '''Acronym for the L{NSStr} wrapper.
    '''
    # XXX Other possible names for this method: at, ampersat, arobe,
    # apenstaartje (little monkey tail), strudel, klammeraffe (spider
    # monkey), little_mouse, arroba, sobachka (doggie), malpa (monkey),
    # snabel (trunk), papaki (small duck), afna (monkey), kukac (caterpillar).
    pass


def isNone(obj):
    '''Return True if I{obj} is nil, None, C{NSNone}, etc.
    '''
    return obj in (None, NSnil, NSNone)


def nsArray2listuple(ns, ctype=Array_t):  # XXX an NS*Array method?
    '''Create a Python list or tuple from an C{NSArray}.
    '''
    # XXX order is critial, NSMutableArray before NSArray
    if isInstanceOf(ns, NSMutableArray, NSArray, name='ns') is NSMutableArray:
        t = list
    else:
        t = tuple
    n = libCF.CFArrayGetCount(ns)
    f = libCF.CFArrayGetValueAtIndex
    return t(_ns2ctype2py(f(ns, i), ctype) for i in range(n))


def nsBoolean2bool(ns, dflt=missing):  # XXX an NSBoolean method?
    '''Create a Python bool from an C{NSBool[ean]}.
    '''
    # XXX need allow c_void_p for nested booleans in lists, sets, etc.?
    isInstanceOf(ns, NSNumber, c_void_p, name='ns')

    return cfNumber2bool(ns, dflt=dflt)


def nsBundleRename(nsTitle, match='Python'):
    '''Change the bundle title if the current title matches.

    @param nsTitle: New bundle title (L{NSStr}).
    @keyword match: Optional, previous title to match (string).

    @return: The previous bundle title (string) or None.

    @note: Used to mimick C{NSApplication.setTitle_(nsTitle)},
           the name of the app shown in the menu bar.
    '''
    t = nsTitle and ns2py(nsTitle)
    if t:
        _Globals.argv0 = bytes2str(t)

    p, ns = None, NSBundle.mainBundle()
    if ns:
        ns = ns.localizedInfoDictionary() or ns.infoDictionary()
        if ns:
            p = ns.objectForKey_(_CFBundleName) or None
            if p:
                p = ns2py(p, dflt='') or ''
                if match in ('', None, p) and t:  # can't be empty
                    ns.setObject_forKey_(nsTitle, _CFBundleName)
    return p


def nsData2bytes(ns, dflt=b''):  # XXX an NSData method?
    '''Create Python bytes from C{NSData}.
    '''
    isInstanceOf(ns, NSData, name='ns')
    n = ns.length()
    if n:
        buf = (c_byte * n)()
        ns.getBytes_length_(byref(buf), n)
        return b''.join(iterbytes(buf[:n]))
    return dflt


def nsDecimalNumber2decimal(ns):
    '''Create a Python Decimal from an C{NSDecimalNumber}.
    '''
    instanceof(ns, NSDecimal, name='ns')
    return ns.Decimal


def nsDictionary2dict(ns, ctype_keys=c_void_p, ctype_vals=c_void_p):  # XXX an NS*Dictionary method?
    '''Create a Python dict from an C{NSDictionary}.
    '''
    # <http://Developer.Apple.com/documentation/corefoundation/cfdictionary-rum>
    n = libCF.CFDictionaryGetCount(ns)
    keys = (ctype_keys * n)()
    vals = (ctype_vals * n)()
    libCF.CFDictionaryGetKeysAndValues(ns, byref(keys), byref(vals))
    return dict((_ns2ctype2py(keys[i], ctype_keys),
                 _ns2ctype2py(vals[i], ctype_vals)) for i in range(n))


def nsIter2(ns, reverse=False):
    '''Iterate over an C{NS...}'s enumerator.
    '''
    if reverse:
        ns = ns.reverseObjectEnumerator()
    else:
        ns = ns.objectEnumerator()
    while True:
        o = ns.nextObject()  # nil for end
        if o in (NSnil, None):
            break
        yield ns2Type(o), o


def nsLog(fmt, *args):
    '''Formatted write to the console.
    '''
    if args:
        fmt %= args
    # NSLog is variadic, printf-like
    libFoundation.NSLog(NSStr(fmt))


def nsNull2none(ns):
    '''Creat Python None from an C{NS/CFNull}.
    '''
    isInstanceOf(ns, NSNull, c_void_p, name='ns')
    return None


def nsNumber2num(ns, dflt=missing):  # XXX an NSNumber method?
    '''Create a Python decimal, int or float from an C{NSNumber}.
    '''
    # special case for NSDecimal, would become a float
    # since cfType of NSDecimal is kCFNumberDoubleType
    if isinstance(ns, NSDecimal):
        return nsDecimalNumber2decimal(ns)
    # XXX need c_void_p for nested numbers in lists, sets, etc.?
    isInstanceOf(ns, NSNumber, c_void_p, name='ns')

    return cfNumber2num(ns, dflt=dflt)


def nsOf(inst):
    '''Return the C{.NS} object of a Python Type instance.
    '''
    try:
        return inst.NS
    except AttributeError:  # see also .bases.NS.setter
        if isinstance(inst, (ObjCInstance, c_struct_t, ObjC_t)):
            return inst  # XXXX ????
    raise TypeError('%s is non-NS: %r' % ('inst', inst))


def nsSet2set(ns, ctype=Set_t):  # XXX NS*Set method?
    '''Create a Python set or frozenset from an C{NSSet}.
    '''
    if isInstanceOf(ns, NSMutableSet, NSSet, name='ns') is NSSet:
        s = frozenset
    else:
        s = set

    n = libCF.CFSetGetCount(ns)  # == nsSet.count()
    buf = (ctype * n)()
    libCF.CFSetGetValues(ns, byref(buf))
    return s(_ns2ctype2py(buf[i], ctype) for i in range(n))


def nsString2str(ns, dflt=None):  # XXX an NS*String method
    '''Create a Python string or unicode from an L{NSStr}.
    '''
    # XXX need c_void_p for nested strings in lists, sets, etc.?
    if not instanceof(ns, CFStr, NSStr, c_void_p):
        isInstanceOf(ns, NSConstantString, NSMutableString, NSString,
                         c_void_p, name='ns')

    n = libCF.CFStringGetLength(ns)
    u = libCF.CFStringGetMaximumSizeForEncoding(n, kCFStringEncodingUTF8)
    buf = c_buffer(u + 2)
    if libCF.CFStringGetCString(ns, buf, len(buf), kCFStringEncodingUTF8):
        # XXX assert(isinstance(buf.value, _Bytes))
        # bytes to unicode in Python 2, to str in Python 3+
        return bytes2str(buf.value)  # XXX was .decode(DEFAULT_UNICODE)
    return dflt


_CFTypeID2py = {libCF.CFArrayGetTypeID():      nsArray2listuple,
                libCF.CFBooleanGetTypeID():    nsBoolean2bool,
                libCF.CFDataGetTypeID():       nsData2bytes,
                libCF.CFDictionaryGetTypeID(): nsDictionary2dict,
                libCF.CFNullGetTypeID():       nsNull2none,
                libCF.CFNumberGetTypeID():     nsNumber2num,
                libCF.CFSetGetTypeID():        nsSet2set,
                libCF.CFStringGetTypeID():     nsString2str}


def _CFTypeID2py_items():
    for i, ns in _CFTypeID2py.items():
        yield int(i), ns.__name__


def ns2py(ns, dflt=None):  # XXX an NSObject method?
    '''Convert (an instance of) an ObjC class to an instance
    of the equivalent Python type and value or Python wrapper.

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
     - NSStr/CFStr     -> str
    '''
    if isinstance(ns, (CFStr, NSStr)):
        return ns.str

    elif ns is not None:  # not isNone(ns)
        # see Rubicon-ObjC/objc/core_foundation.py
        # if isinstance(ns, ObjCInstance):
        #     ns = ns._as_parameter_
        try:
            typeID = libCF.CFGetTypeID(ns)
            r = _CFTypeID2py[typeID](ns)
            c = {Class_t: ObjCClass,
                 Id_t:    ObjCInstance}.get(type(r), _lambda)
            return c(r)

        except ArgumentError as x:
            _Xargs(x, libCF.CFGetTypeID.__name__,
                      libCF.CFGetTypeID.argtypes,
                      libCF.CFGetTypeID.restype)
            raise

        except KeyError:
            if dflt is None:
                t = ', '.join('TypeID[%d]: %s' % t for t in
                              sorted(_CFTypeID2py_items()))
                raise TypeError('unhandled %s[%r]: %r {%s}' %
                               ('TypeID', typeID, ns, t))
    return dflt


def ns2Type(ns):
    '''Convert an C{NS/Instance} object to an instance of
    the corresponding Python Type.
    '''
    try:
        return ns.Type(ns)
    except AttributeError:
        pass

    # XXX order is critial, NSMutableArray first
    if isInstanceOf(ns, NSMutableArray) is NSMutableArray:
        _Type = _Types.List
    elif isInstanceOf(ns, NSArray) is NSArray:
        _Type = _Types.Tuple

    # XXX order is critial, NSMutableDictionary first
    elif isInstanceOf(ns, NSMutableDictionary) is NSMutableDictionary:
        _Type = _Types.Dict
    elif isInstanceOf(ns, NSDictionary) is NSDictionary:
        _Type = _Types.FrozenDict

    # XXX order is critial, NSMutableSet first
    elif isInstanceOf(ns, NSMutableSet) is NSMutableSet:
        _Type = _Types.Set
    elif isInstanceOf(ns, NSSet) is NSSet:
        _Type = _Types.FrozenSet

    elif instanceof(ns, NSStr):
        _Type = _Types.Str

    else:
        # print('ns2Type(%r) -> %s' % (ns.objc_class, type(ns2py(ns))))
        _Type = ns2py

    # save the Python Type or ns2py convertor at the NS/Class
    # to expedite future conversions of such class instances
    ns.objc_class._Type = _Type
    return _Type(ns)


_NSFalse = NSBool(False)  # singleton
_NSTrue  = NSBool(True)   # singleton


def bool2NS(py):
    '''Create an C{NSBool} instance from a Python bool.
    '''
    return _NSTrue if py else _NSFalse


def bytes2NS(py):
    '''Create an C{NSData} instance from Python bytes.
    '''
    def _NSData_length(ns):  # XXX lambda ns: ns.length()
        return ns.length()

    return _len2NS(py, NSData.dataWithBytes_length_(py, len(py)),
                      _NSData_length)


def dict2NS(py):
    '''Create an C{NSMutableDictionary} instance from a Python dict.
    '''
    # http://Developer.Apple.com/library/content/documentation/Cocoa/
    #        Conceptual/Collections/Articles/Dictionaries.html
    ns = NSMutableDictionary.dictionary()
    for k, v in py.get('iteritems', py.items)():
        ns.setObject_forKey_(py2NS(v), py2NS(k))
    return _len2NS(py, ns, libCF.CFDictionaryGetCount)


def frozenset2NS(py):
    '''Create an (immutable) C{NSSet} instance from a Python frozenset.
    '''
    return _len2NS(py, NSSet.alloc().initWithSet_(set2NS(py)),
                       libCF.CFSetGetCount)


def int2NS(py):
    '''Create an C{NSNumber} instance from a Python int or long.
    '''
    if abs(py) < 1 << 31:
        return NSInt(py)
    elif abs(py) < 1 << 63:
        return NSLong(py)
    else:
        return NSLongLong(py)


def _iter2NS(ns, py, getCount):
    # create NS objects for each Python list, frozen/set, tuple item
    for ns_obj in map(py2NS, py):
        ns.addObject_(ns_obj)
    return _len2NS(py, ns, getCount)


def _len2NS(py, ns, getCount):
    # check the Python len and NS instance count
    n, m = len(py), getCount(ns)
    if m != n:
        t = (ns.objc_classname, m, clip(repr(py)), n)
        raise AssertionError('%s[%s] vs %s[%s]' % t)
    return ns


def list2NS(py):
    '''Create an C{NSMutableArray} instance from a Python list.
    '''
    return _iter2NS(NSMutableArray.array(), py, libCF.CFArrayGetCount)


def None2NS(py):
    '''Create an C{NSNone} from Python's None.
    '''
    if py is None:
        return NSNone
    raise TypeError('not %s: %r' % ('None', py))


def set2NS(py):
    '''Create an C{NSMutableSet} instance from a Python set.
    '''
    return _iter2NS(NSMutableSet.set(), py, libCF.CFSetGetCount)


def str2NS(py, auto=True):
    '''Create an NSStr instance from a Python str.
    '''
    return NSStr(py, auto=auto)


def tuple2NS(py):
    '''Create an immutable C{NSArray} instance from a Python tuple.
    '''
    return _len2NS(py, NSArray.alloc().initWithArray_(list2NS(py)),
                       libCF.CFArrayGetCount)


def unicode2NS(py):
    '''Create an C{NSStr} instance from a Python unicode string.
    '''
    return NSStr(py.encode(DEFAULT_UNICODE))  # .stringWithUTF8String_


_py2NS = {bool:       bool2NS,
         _Decimal:    NSDecimal,
          dict:       dict2NS,
          float:      NSDouble,
          frozenset:  frozenset2NS,
          int:        int2NS,
          list:       list2NS,
          set:        set2NS,
          str:        str2NS,
          tuple:      tuple2NS,
          type(None): None2NS}
try:
    _py2NS.update({bytearray: bytes2NS,
                   long:      int2NS,
                   unicode:   unicode2NS})
except NameError:  # Python 3+
    _py2NS.update({bytes: bytes2NS})


def py2NS(py):
    '''Convert (an instance of) a Python object into an
    instance of the equivalent C{NS...} ObjC class:

     - bool      -> NSBoolean/NSNumber
     - bytes     -> NSData
     - bytearray -> NSData
     - Decimal   -> NSDecimal
     - dict      -> NSMutableDictionary
     - float     -> NSNumber
     - frozenset -> NSSet, immutable
     - int       -> NSNumber
     - list      -> NSMutableArray
     - None      -> NSNull
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
    '''Return the C{NS/Instance} of/for a Python Type instance.
    '''
    try:
        return py.NS
    except AttributeError:
        return py2NS(py)


# moved to the end, to let CFStr settle
_CFBundleName = CFStr('CFBundleName')

# filter locals() for .__init__.py
__all__ = _exports(locals(), 'at', 'CFStr', 'isNone',
                   starts=('NS', 'ns'),
                   ends='2NS')

if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)
