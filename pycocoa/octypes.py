
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

# all imports listed explicitly to help PyChecker
from ctypes   import c_bool, c_byte, c_char, c_char_p, c_double, \
                     c_float, c_int, c_int32, c_int64, c_long, \
                     c_longlong, c_short, c_ubyte, c_uint, c_uint32, \
                     c_ulong, c_ulonglong, c_ushort, c_void_p, c_wchar, \
                     POINTER, py_object, sizeof, Structure
from platform import machine as machine
from struct   import calcsize

__version__ = '17.11.19'

__i386__ = machine() == 'i386'  # PYCHOK expected
__LP64__ = calcsize("P") == 8   # 64-bits

DEFAULT_UNICODE = 'utf-8'  # default Python encoding

unichar = c_wchar   # actually a c_ushort in NSString.h,
UniChar = c_ushort  # but need ctypes to convert properly

try:
    _Bytes = bytearray, bytes
    _Strs  = basestring, unicode
except NameError:  # Python 3+
    _Bytes = bytes
    _Strs  = str  # , bytes

if sizeof(c_void_p) == 4:
    c_ptrdiff_t = c_int32
elif sizeof(c_void_p) == 8:
    c_ptrdiff_t = c_int64
else:
    raise ValueError('sizeof(c_void_p): %s' % (sizeof(c_void_p),))

# iter(bytes) yields a 1-char str in Python2, but an int in Python 3+
if isinstance(b'x'[0], bytes):
    _iterbytes = iter
else:  # Python 3+
    def _iterbytes(bstr):
        for i in bstr:  # convert int to bytes
            yield bytes([i])
# double check _iterbytes
for b in _iterbytes(b'a0'):
    assert(isinstance(b, bytes))
del b


def _2bytes(bstr):
    '''Convert str to bytes/unicode if needed.
    '''
    if isinstance(bstr, _Bytes):
        return bstr
    else:
        return bstr.encode(DEFAULT_UNICODE)


def _2clip(bstr, clip=50):
    if bstr and clip > 10:
        n = len(bstr)
        if n > clip:
            t = type(bstr)
            h = clip // 2
            bstr = bstr[:h] + t('....') + bstr[-h:]
        #   if XXX:
        #       bstr += t('[' + str(n) + ']')
    return bstr


def _2str(bstr):
    '''Convert bytes to str/unicode if needed.
    '''
    if isinstance(bstr, _Strs):
        return bstr
    else:
        return bstr.decode(DEFAULT_UNICODE)


# Note CGBase.h located at /System/Library/Frameworks/ApplicationServices
# .framework/Frameworks/CoreGraphics.framework/Headers/CGBase.h defines
# CGFloat as double if __LP64__, otherwise it is float.
if __LP64__:
    NSInteger  = c_long
    NSUInteger = c_ulong
    CGFloat    = c_double

    NSPointEncoding = b'{CGPoint=dd}'
    NSRangeEncoding = b'{_NSRange=QQ}'
    NSRectEncoding  = b'{CGRect={CGPoint=dd}{CGSize=dd}}'
    NSSizeEncoding  = b'{CGSize=dd}'

else:
    NSInteger  = c_int
    NSUInteger = c_uint
    CGFloat    = c_float

    NSPointEncoding = b'{_NSPoint=ff}'
    NSRangeEncoding = b'{_NSRange=II}'
    NSRectEncoding  = b'{_NSRect={_NSPoint=ff}{_NSSize=ff}}'
    NSSizeEncoding  = b'{_NSSize=ff}'

CFArray      = c_void_p  # XXX untested
CFIndex      = c_long
CGGlyph      = c_ushort
CFNumberType = c_uint32
CFTypeID     = c_ulong

# Special case so that NSImage.initWithCGImage_size_() will work.
CGImageEncoding  = b'{CGImage=}'
NSZoneEncoding   = b'{_NSZone=}'
PyObjectEncoding = b'{PyObject=@}'


# wrappers for Objective-C classes, etc.  mostly to
# see more meaningful names in res- and argtypes
class Array(c_void_p):
    '''ObjC array type.
    '''
    pass


class Block(c_void_p):
    '''ObjC block type.
    '''
    pass


class Id(c_void_p):
    '''ObjC id/self type.
    '''
    pass


class Class(Id):  # c_void_p
    '''ObjC class type.
    '''
    pass


class IMP(c_void_p):
    '''ObjC implementation type.
    '''
    pass


class Ivar(c_void_p):
    '''ObjC instance variable type.
    '''
    pass


class Method(c_void_p):
    '''ObjC method type.
    '''
    pass


class Onion(Id):  # XXX or c_void_p?
    '''Union C{Onion} type, to avoid C{ctypes Union} conflict.
    '''
    pass


class Protocol(Id):
    '''ObjC protocol type.
    '''
    pass


class SEL(c_void_p):
    '''ObjC selector/cmd type.
    '''
    pass


class Struct(c_void_p):
    '''ObjC struct type.
    '''
    pass


class Unknown(c_void_p):
    '''Unknown type.
    '''
    pass


class UnknownPtr(c_void_p):
    '''Unknown pointer.
    '''
    pass


class VoidPtr(c_void_p):
    '''Void pointer.
    '''
    pass


# <http://StackOverflow.com/questions/41502199/
#  how-to-decipher-objc-method-description-from-protocol-method-description-list>
class objc_method_description(Structure):
    '''ObjC struct with name and types.
    '''
    _fields_ = ('name', SEL), ('types', c_char_p)


class objc_property_t(c_void_p):
    '''ObjC property Class.
    '''
    pass


class objc_property_attribute_t(Structure):
    '''ObjC struct with name and value.
    '''
    _fields_ = ('name', c_char_p), ('value', c_char_p)


class objc_super(Structure):
    '''ObjC structure with receiver and class.
    '''
    _fields_ = ('receiver', Id), ('super_class', Class)


# from /System/Library/Frameworks/Foundation.framework/Headers/NSGeometry.h
class NSPoint(Structure):
    '''ObjC struct with x and y.
    '''
    _fields_ = ('x', CGFloat), ('y', CGFloat)


# from /System/Library/Frameworks/Foundation.framework/Headers/NSGeometry.h
class NSSize(Structure):
    '''ObjC struct with width and height.
    '''
    _fields_ = ('width', CGFloat), ('height', CGFloat)


class NSRect(Structure):
    '''ObjC struc with origin and size.
    '''
    _fields_ = ('origin', NSPoint), ('size', NSSize)


# CFRange struct defined in CFBase.h
# This replaces the CFRangeMake(LOC, LEN) macro.
class CFRange(Structure):
    '''ObjC struct with location and length (CFIndex-s).
    '''
    _fields_ = ('location', CFIndex), ('length', CFIndex)


# NSRange.h
class NSRange(Structure):
    '''ObjC struct with location and length (NSInteger-s).
    '''
    _fields_ = ('location', NSUInteger), ('length', NSUInteger)


CGPoint = NSPoint
CGRect  = NSRect
CGSize  = NSSize

# NSDate.h
NSTimeInterval = c_double  # a ctype

# map ctypes type to encoding type code
_ctype2encoding = {c_char:     b'c', c_ubyte:     b'C',
                   c_int:      b'i', c_uint:      b'I',
                   c_short:    b's', c_ushort:    b'S',
                   c_long:     b'l', c_ulong:     b'L',
                   c_longlong: b'q', c_ulonglong: b'Q',
                   c_float:    b'f', c_double:    b'd',
                   c_bool:     b'B',
                   c_char_p:   b'*',
                   c_void_p:   b'@',
                   Class:      b'#', Id:          b'@',
                   SEL:        b':',  # c_void:   b'v',
                   py_object:  PyObjectEncoding}


def ctype2encoding(ctype, default=b'?'):
    """Return the type encoding for a given C{ctypes} type.
    """
    return _ctype2encoding.get(ctype, default)


CGFloatEncoding    = ctype2encoding(CGFloat)
NSIntegerEncoding  = ctype2encoding(NSInteger)
NSUIntegerEncoding = ctype2encoding(NSUInteger)

# map for encoding type code to ctypes type
_encoding2ctype = {b'c': c_char,     b'C': c_ubyte,
                   b's': c_short,    b'S': c_ushort,
                   b'i': c_int,      b'I': c_uint,
                   b'l': c_long,     b'L': c_ulong,
                   b'q': c_longlong, b'Q': c_ulonglong,
                   b'f': c_float,    b'd': c_double,
                   b'B': c_bool,     b'v': None,
                   b'*': c_char_p,  # string
                   b'#': Class,     # class
                   b'@': Id,        # Id/self
                   b':': SEL,       # SELector/cmd
                   NSPointEncoding:  NSPoint,
                   NSRangeEncoding:  NSRange,
                   NSRectEncoding:   NSRect,
                   NSSizeEncoding:   NSSize,
                   PyObjectEncoding: py_object,
                   b'[]': Array,
                   b'<>': Block,
                   b'{}': Struct,
                   b'()': Onion,
                   b'?':  Unknown,
                   b'^?': UnknownPtr,
                   b'^v': VoidPtr}

# double check the 2encoding and 2ctype maps
for c_, code in _ctype2encoding.items():
    f_ = _encoding2ctype.get(code, 'missing')
    if c_ != f_ and code not in (b'@',):
        raise AssertionError('code %r ctype %r vs %r' % (code, c_, f_))
del c_, code, f_

# map 'c' to c_byte rather than c_char, because
# otherwise ctypes converts the value into a 1-char
# string which is generally not what we want,
# especially when the 'c' represents a bool
_encoding2ctype[b'c'] = c_byte

_emcoding2ctype = {b'Vv': None,
                   b'^' + CGImageEncoding: c_void_p,
                   b'^' + NSZoneEncoding: c_void_p}


def emcoding2ctype(code, default=None, name='type'):
    '''Return the C{ctypes} type for a single Objective-C type encoding
    for a I{method} result or I{method} argument.
    '''
    try:
        return _emcoding2ctype[code]
    except KeyError:
        pass
    return encoding2ctype(code, default, name)


def encoding2ctype(code, default=None, name='type'):  # MCCABE 20
    '''Return the C{ctypes} type for a single Objective-C type encoding.
    '''
    try:
        return _encoding2ctype[code]
    except KeyError:
        pass

    coderr = code
    if code[:1] == b'r':  # const ptr or decorator
        code = code[1:]
    try:
        if code[-1:] in _TYPESPECIAL:
            c = code[-1:]
            if c == b'"':  # ..."name" suffix
                i = code.find(c)
                if i < 1:
                    raise TypeError
                code = code[:i]  # drop "name"

            elif c == b']':  # array ...[...]
                i = code.find(b'[')
                if i < 0:
                    raise TypeError
                elif i > 0:  # ignore array type
                    code = code[:i + 1] + c
                else:  # convert array to pointer
                    code = b'^' + code[1:-1].strip(b'0123456789')

            else:  # otherwise Block, Struct or Onion
                o = _TYPE2OPENER[c]
                if code[:1] != o:
                    o = b'^' + o
                    if code[:2] != o:
                        raise TypeError
                code = o + c  # {} or ^{}, etc.

        if code[:1] == b'^':
            if len(code) < 2:
                raise TypeError
            ctype = POINTER(_encoding2ctype[code[1:]])
            _encoding2ctype[code] = ctype
            return ctype
        elif len(code):
            return _encoding2ctype[code]
        else:
            raise TypeError

    except TypeError:
        raise TypeError('%s %s encoding %r' % ('invalid',
                        _2str(name), coderr))
    except KeyError:
        pass

    if default is None:
        raise TypeError('%s %s encoding %r' % ('unknown',
                        _2str(name), coderr))
    elif code[:1] == b'^':
        return POINTER(default)
    else:
        return default


def split_emcoding2(encoding, start=0):
    '''Split the type encoding of a I{method} signature into
    separate, single encodings and the combined encoding.

    If necessary, the encoding is extended with the type encoding
    for the hidden method arguments C{id/self} and C{SEL/cmd}.

    Does not handle bitfields, arrays, structs, unions, etc. and
    strips any offset, size or width specifiers from the encoding.

    In the returned 2-tuple (I{codes, encoding}), I{codes} is
    the list of individual type encodings from item I{start=0}
    and I{encoding} the combined type encoding in C{bytes} and
    both extended if needed.

    Example:

    >>> split_emcoding2('v*')
    >>> (['v', '@', ':', '*'], 'v@:*')

    '''
    codes = split_encoding(encoding)
    if codes[1:3] != [b'@', b':']:
        # Add codes for hidden arguments
        codes.insert(1, b'@')  # Id/self type encoding
        codes.insert(2, b':')  # SEL/cmd type encoding

    return codes[start:], b''.join(codes)


_TYPECODESET = set(_iterbytes(b'cCiIsSlLqQfdBv*@#:b^?'))  # _emcoding2ctype.keys()
_TYPESKIPPED = set(_iterbytes(b'0123456789 nNoOrRV'))  # type, width and offsets

_TYPE2CLOSER = {b'{': b'}', b'[': b']', b'(': b')', b'<': b'>'}
_TYPE2OPENER = dict(reversed(_) for _ in _TYPE2CLOSER.items())

_TYPEOPENERS = set(_TYPE2CLOSER.keys())
_TYPECLOSERS = set(_TYPE2CLOSER.values())
_TYPESPECIAL = _TYPECLOSERS.union(b'"')


def split_encoding(encoding):  # MCCABE 18
    '''Split a type encoding into separate type encodings.

    Does not handle bitfields, arrays, structs, unions, etc. and
    strips any offset, size or width specifiers from the encoding.

    Examples:

    >>> split_encoding('^v16@0:8')
    >>> ['^v', '@', ':']

    >>> split_encoding('{CGSize=dd}40@0:8{PyObject=@}Q32')
    >>> ['{CGSize=dd}', '@', ':', '{PyObject=@}', 'Q']

    Supported Type Encodings:

        - B = bool (C++ bool, C99 _Bool)
        - c, C = char, unsigned char
        - f, d = float, double
        - i, I = int, unsigned int
        - l, L = long, unsigned long (32-bit)
        - q, Q = long long, unsigned long long
        - s, S = short, unsigned short
        - t, T = 128-bit int, unsigned int
        - v = void
        - * = string (char *)
        - : = method selector (SEL/cmd)
        - # = class
        - #"name" = class "name"
        - @ = object (instance, statically typed, typed id, etc.)
        - @"name" = instance of class "name"
        - ^type = pointer to type
        - ? = unknown type (among other things, used for function pointers)

    Unsupported Type Encodings:

        - bW = bit field of width W
        - [Ltype] = array of L items of type
        - E{lb}name=type...E{rb} = structure
        - (name=type...) = union
        - <...> = block

    For Objective-C internal use only:

        - n, N = in, inout
        - o, O = out, bycopy
        - r, R = const, byref
        - V = oneway

    Type encodings may be preceeded by a C{"name"}, for example a bit
    field C{"name"b1}, structure fields C{E{lb}CGsize="width"d"heigth"dE{rb}},
    union items, etc. and all such C{"name"} prefixes are ignored.  See
    also U{Type Encodings<http://Developer.Apple.com/library/content/
    documentation/Cocoa/Conceptual/ObjCRuntimeGuide/Articles/ocrtTypeEncodings.html>},
    U{NSHipster Type Encodings<http://NSHipster.com/type-encodings/>} and
    U{Digits in type encoding<http://StackOverflow.com/questions/11527385/
    how-are-the-digits-in-objc-method-type-encoding-calculated/>}.
    '''
    code   = []
    codes  = []
    opened = []     # opened braces, brackets, parensm etc.
    quoted = False  # inside double quotes

    for b in _iterbytes(_2bytes(encoding)):

        if b in _TYPEOPENERS:
            if code and code[-1] != b'^' and not opened:
                codes.append(b''.join(code))
                code = []
            opened.append(_TYPE2CLOSER[b])
            code.append(b)

        elif b in _TYPECLOSERS:
            code.append(b)
            if not opened or b != opened.pop():
                raise ValueError('%s encoding %r' % ('unbalanced',
                                 _2str(b''.join(code))))
            if not opened:
                codes.append(b''.join(code))
                code = []

        elif opened:  # inside braces, etc
            # XXX ignore digits?
            code.append(b)  # stick anything on

        elif b == b'"':
            code.append(b)
            if quoted:  # closing quotes
                code = b''.join(code)
                if code[:2] in (b'@"', b'#"'):
                    # XXX only @"..." and #"..." are OK
                    # XXX what about ^@"..." and ^#"..."?
                    codes.append(code)
                elif code[:1] == b'"':
                    pass  # ignore prefix "name"
                else:
                    raise ValueError('%s encoding %r' % ('invalid',
                                     _2str(code)))
                code = []
            quoted = not quoted

        elif quoted:  # inside quotes
            # XXX only alphanumeric, '_', '.'?
            code.append(b)  # stick anything on

        elif b in _TYPECODESET:
            if code and code[-1] != b'^':
                # not a pointer, previous char != '^'
                codes.append(b''.join(code))
                code = []
            code.append(b)

        elif b in _TYPESKIPPED:
            pass  # ignore type, width and offsets

    if opened:
        raise ValueError('%s encoding %r' % ('unbalanced',
                                             _2str(encoding)))

    if code:  # final type code
        codes.append(b''.join(code))
    return codes


__all__ = tuple(_ for _ in locals().keys() if
                _.startswith(('CG', 'CF', 'NS', 'ObjC', 'split_'))) + \
          ('c_ptrdiff_t', 'PyObjectEncoding', 'unichar', 'UniChar')


def _allist(allist, allocals, version, filename):
    '''Print sorted __all__ names and values.
    '''
    import os

    m = os.path.basename(os.path.splitext(filename)[0])
    for i, n in enumerate(sorted(allist)):
        t = repr(allocals[n]).replace('__main__', m)
        print('%d %s.%s is %s' % (i + 1, m, n, t))
    i = '-' * len(str(i + 1))
    print('%s %s.%s = %r' % (i, m, '__version__', version))


if __name__ == '__main__':

    _allist(__all__, locals(), __version__, __file__)
