
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

'''Module defining ObjC I{..._t} types from standard I{ctypes}.

   Names starting with I{c_} are I{ctypes}, names ending with I{_t}
   are ObjC types defined in terms of a I{ctypes} I{c_} type.
'''
# all imports listed explicitly to help PyChecker
from ctypes import c_bool, c_byte, c_char, c_char_p, c_double, \
                   c_float, c_int, c_int32, c_int64, c_long, \
                   c_longlong, c_short, c_ubyte, c_uint, c_uint16, \
                   c_uint32, c_ulong, c_ulonglong, c_ushort, \
                   c_void_p, c_wchar, \
                   POINTER, py_object, sizeof, Structure
try:
    from ctypes import c_void
except ImportError:
    c_void = None
from platform import machine  # as machine

# from getters import get_selectornameof
from utils import bytes2str, _exports, inst2strepr, iterbytes, \
                  missing, str2bytes

__version__ = '18.04.16'

if sizeof(c_void_p) == 4:
    c_ptrdiff_t = c_int32
elif sizeof(c_void_p) == 8:
    c_ptrdiff_t = c_int64
else:
    raise ValueError('sizeof(c_void_p): %s' % (sizeof(c_void_p),))

__i386__ = machine() == 'i386'  # PYCHOK expected
__LP64__ = c_ptrdiff_t is c_int64   # 64-bits

unichar_t = c_wchar   # actually a c_ushort in NSString_.h,
UniChar_t = c_ushort  # but need ctypes to convert properly


class c_struct_t(Structure):
    '''Base type to pretty-print I{ctypes} C{Structures}.
    '''
    def _attrs(self):
        for f, _ in self._fields_:  # PYCHOK expected
            yield f

    def __repr__(self):
        r = inst2strepr(self, repr, *self._attrs())
        return '<%s at %#x>' % (r, id(self))

    def __str__(self):
        return inst2strepr(self, str, *self._attrs())


class ObjC_t(c_void_p):
    '''Base type to pretty-print I{ctypes} C{c_void_p}.
    '''
    def __repr__(self):
        return '<%s at %#x>' % (self, id(self))

    def __str__(self):
        return self.__class__.__name__


class TypeCodeError(ValueError):
    '''Error in ObjC type encoding.
    '''
    pass


# Note CGBase.h at /System/Library/Frameworks/ApplicationServices
# .framework/Frameworks/CoreGraphics.framework/Headers/CGBase.h
# defines CG/Float as double if __LP64__, otherwise it is float.
# Also, these types can't be subclasses of c_... ctypes.
if __LP64__:
    CGFloat_t    = c_double  # CGFloat.nativeType
    NSInteger_t  = c_long    # == Int?
    NSUInteger_t = c_ulong   # == Uint?

    NSIntegerMax = 0x7fffffffffffffff

    NSPointEncoding = b'{CGPoint=dd}'
    NSRangeEncoding = b'{_NSRange=QQ}'
    NSRectEncoding  = b'{CGRect={CGPoint=dd}{CGSize=dd}}'
    NSSizeEncoding  = b'{CGSize=dd}'

else:
    CGFloat_t    = c_float  # CGFloat.nativeType
    NSInteger_t  = c_int    # == Int?
    NSUInteger_t = c_uint   # == Uint?

    NSIntegerMax = 0x7fffffff

    NSPointEncoding = b'{_NSPoint=ff}'
    NSRangeEncoding = b'{_NSRange=II}'
    NSRectEncoding  = b'{_NSRect={_NSPoint=ff}{_NSSize=ff}}'
    NSSizeEncoding  = b'{_NSSize=ff}'

# Special case so that NSImage.initWithCGImage_size_() will work.
CGImageEncoding  = b'{CGImage=}'
NSZoneEncoding   = b'{_NSZone=}'
PyObjectEncoding = b'{PyObject=@}'


# wrappers for ObjC classes, structs, etc.  mostly
# to see more meaningful names in res- and argtypes
class Allocator_t(ObjC_t):
    '''ObjC allocator type.
    '''
    pass


Array_t = c_void_p  # ObjC array type.


class Block_t(ObjC_t):
    '''ObjC block type.
    '''
    pass


class BOOL_t(c_bool):
    '''ObjC boolean type.
    '''
    pass


Data_t       = c_void_p
Dictionary_t = c_void_p


class Id_t(ObjC_t):
    '''ObjC id/self type, end=coding b'@'.
    '''
    pass

# objc_id = Id_t


class Class_t(Id_t):  # ObjC_t
    '''ObjC class type, encoding b'#'.
    '''
    pass


class IMP_t(ObjC_t):
    '''ObjC implementation type.
    '''
    pass


class Ivar_t(ObjC_t):
    '''ObjC instance variable type.
    '''
    pass


class Method_t(ObjC_t):
    '''ObjC method type.
    '''
    pass


Number_t     = c_void_p
NumberType_t = c_ulong  # c_uint32


class Union_t(Id_t):  # XXX or ObjC_t?
    '''ObjC union type.
    '''
    pass


class Protocol_t(Id_t):
    '''ObjC protocol type.
    '''
    pass


class SEL_t(ObjC_t):
    '''ObjC selector/cmd type, encoding b':'.
    '''
    _name = None
#   def __new__(cls, name=None):
#       self = libobjc.sel_registerName(str2bytes(name))
#       return self

    def __repr__(self):
        return '<%s(%s)>' % (self.__class__.__name__, self)

    def __str__(self):
        return 'None' if self.value is None else bytes2str(self.name)

    @property
    def name(self):
        if self._name is None:
            if self.value is None:
                raise ValueError('Null %r' % (self,))
            from getters import get_selectornameof
            self._name = get_selectornameof(self)
        return self._name


Set_t = c_void_p  # ObjC set type.
String_t = c_void_p  # ObjC string type.


class Struct_t(ObjC_t):
    '''ObjC struct type.
    '''
    pass


# unhashable type if class(ObjC_t)
TypeID_t = c_ulong  # ObjC/CF TypeID type


class TypeRef_t(ObjC_t):
    '''ObjC opaque type.
    '''
    pass


class Unknown_t(ObjC_t):
    '''Unknown type.
    '''
    pass


class UnknownPtr_t(ObjC_t):
    '''Unknown pointer.
    '''
    pass


class VoidPtr_t(ObjC_t):
    '''Same as, but distinguishable from C{c_void_p}.
    '''
    pass


# <http://StackOverflow.com/questions/41502199/
#  how-to-decipher-objc-method-description-from-protocol-method-description-list>
class objc_method_description_t(c_struct_t):
    '''ObjC struct with .name and .types.
    '''
    _fields_ = ('name', SEL_t), ('types', c_char_p)


class objc_property_t(ObjC_t):
    '''ObjC property Class.
    '''
    pass


class objc_property_attribute_t(c_struct_t):
    '''ObjC struct with .name and .value.
    '''
    _fields_ = ('name', c_char_p), ('value', c_char_p)


class objc_super_t(c_struct_t):
    '''ObjC struct with .receiver and .class.
    '''
    _fields_ = ('receiver', Id_t), ('super_class', Class_t)


NSDouble_t = c_double  # always 64-bit double
NSFloat_t  = c_float   # always 32-bit float


# NSRange.h
class NSRange_t(c_struct_t):  # !+ CGRange_t!!!
    '''ObjC struct with .loc[ation] and .len[gth] (NSUInteger-s).
    '''
    _fields_ = ('location', NSUInteger_t), ('length', NSUInteger_t)


# from /System/Library/Frameworks/Foundation.framework/Headers/NSGeometry.h
class NSPoint_t(c_struct_t):  # == CGPoint_t
    '''ObjC struct with .x and .y.
    '''
    _fields_ = ('x', CGFloat_t), ('y', CGFloat_t)


# from /System/Library/Frameworks/Foundation.framework/Headers/NSGeometry.h
class NSSize_t(c_struct_t):  # == CGSize_t
    '''ObjC struct with .width and .height.
    '''
    _fields_ = ('width', CGFloat_t), ('height', CGFloat_t)


class NSRect_t(c_struct_t):  # == CGRect_t
    '''ObjC struct with .origin and .size.
    '''
    _fields_ = ('origin', NSPoint_t), ('size', NSSize_t)


class NSRect4_t(NSRect_t):
    '''Class NSRect_t with different signature and properties.
    '''
    def __init__(self, x=0, y=0, width=0, height=0):
        if width < 0:
            x += width
            width = -width

        if height < 0:
            y += height
            height = -height

        super(NSRect4_t, self).__init__(NSPoint_t(x, y), NSSize_t(width, height))

    def __repr__(self):
        r = inst2strepr(self, repr, 'x', 'y', 'width', 'height')
        return '<%s at %#x>' % (r, id(self))

    def __str__(self):
        return inst2strepr(self, str, 'x', 'y', 'width', 'height')

    @property
    def bottom(self):
        return self.y

    @property
    def left(self):
        return self.x

    @property
    def height(self):
        return self.size.height

    @property
    def right(self):
        return self.x + self.width

    @property
    def top(self):
        return self.y + self.heigth

    @property
    def width(self):
        return self.size.width

    @property
    def x(self):
        return self.origin.x

    @property
    def y(self):
        return self.origin.y


CGBitmapInfo_t         = c_uint32  # CGImage.h
CGDirectDisplayID_t    = c_uint32  # CGDirectDisplay.h
CGError_t              = c_int32   # CGError.h
CGGlyph_t              = c_uint16  # c_ushort
CGIndex_t              = NSInteger_t  # == Int
CGPoint_t              = NSPoint_t
CGRect_t               = NSRect_t
CGSize_t               = NSSize_t
CTFontOrientation_t    = c_uint32  # CTFontDescriptor.h
CTFontSymbolicTraits_t = c_uint32  # CTFontTraits.h


# CF/Range struct defined in CFBase.h
class CGRange_t(c_struct_t):
    '''ObjC struct with .location and .length (CF/Index-s).
    '''
    _fields_ = ('location', CGIndex_t), ('length', CGIndex_t)


# for backward compatibility with cocoa-python:
NSMakePoint = NSPoint_t
NSMakeRange = NSRange_t  # CFRangeMake(LOC, LEN)
NSMakeRect  = NSRect4_t
NSMakeSize  = NSSize_t

NSNotFound  = NSIntegerMax
NSPointZero = NSPoint_t(0, 0)

# NSDate.h
NSTimeInterval_t = c_double  # a ctype

# map ctypes type to ObjC encoding type code
_ctype2encoding = {c_char:     b'c', c_ubyte:     b'C',
                   c_int:      b'i', c_uint:      b'I',
                   c_short:    b's', c_ushort:    b'S',
                   c_long:     b'l', c_ulong:     b'L',
                   c_float:    b'f', c_double:    b'd',
                   c_bool:     b'B',
                   c_char_p:   b'*',
                   c_void_p:   b'@',  # c_void:   b'v',
                   Class_t:    b'#',
                   Id_t:       b'@',
                   NSPoint_t:  NSPointEncoding,
                   NSRange_t:  NSRangeEncoding,
                   NSRect_t:   NSRectEncoding,
                   NSSize_t:   NSSizeEncoding,
                   SEL_t:      b':',
                   py_object:  PyObjectEncoding}

# add c_?longlong only if different from c_?long
if sizeof(c_longlong) != sizeof(c_long):
    _ctype2encoding.update({c_longlong: b'q'})
if sizeof(c_ulonglong) != sizeof(c_ulong):
    _ctype2encoding.update({c_ulonglong: b'Q'})


def ctype2encoding(ctype, dflt=b'?'):
    '''Return the type encoding for a given C{ctypes} type.
    '''
    return _ctype2encoding.get(ctype, dflt)


NSFloatEncoding    = ctype2encoding(NSFloat_t)
NSIntegerEncoding  = ctype2encoding(NSInteger_t)
NSUIntegerEncoding = ctype2encoding(NSUInteger_t)

# map for encoding type code to ctypes type
_encoding2ctype = {b'c': c_char,     b'C': c_ubyte,
                   b's': c_short,    b'S': c_ushort,
                   b'i': c_int,      b'I': c_uint,
                   b'l': c_long,     b'L': c_ulong,
                   b'q': c_longlong, b'Q': c_ulonglong,  # == c_(u)long?
                   b'f': c_float,    b'd': c_double,
                   b'B': c_bool,     b'v': c_void,
                   b'*': c_char_p,  # string
                   b'#': Class_t,   # class
                   b'@': Id_t,      # Id/self
                   b':': SEL_t,     # SELector/cmd
                   NSPointEncoding:  NSPoint_t,
                   NSRangeEncoding:  NSRange_t,
                   NSRectEncoding:   NSRect_t,
                   NSSizeEncoding:   NSSize_t,
                   PyObjectEncoding: py_object,
                   b'P':             py_object,  # for convenience
                   b'[]': Array_t,
                   b'<>': Block_t,
                   b'{}': Struct_t,
                   b'()': Union_t,
                   b'?':  Unknown_t,
                   b'^?': UnknownPtr_t,
                   b'^v': VoidPtr_t}

# double check the 2encoding and 2ctype mappings
for c_, code in _ctype2encoding.items():
    f_ = _encoding2ctype.get(code, 'missing')
    if c_ != f_ and code not in (b'@',):
        raise AssertionError('code %r ctype %r vs %r' % (code, c_, f_))
del c_, code, f_

# map 'c' to c_byte rather than c_char, because
# otherwise ctypes converts the value into a 1-char
# string which is generally not what we want,
# especially when the 'c' represents a bool
_encoding2ctype[b'c'] = c_byte  # C_ubyte, see oclibs.cfNumber2bool!

_emcoding2ctype = {b'Vv': c_void,
                   b'^' + CGImageEncoding: c_void_p,
                   b'^' + NSZoneEncoding:  c_void_p}


def emcoding2ctype(code, dflt=missing, name='type'):
    '''Return the C{ctypes} type for a single ObjC type encoding
    for a I{method} result or I{method} argument.
    '''
    try:
        return _emcoding2ctype[code]
    except KeyError:
        pass
    return encoding2ctype(code, dflt, name)


def encoding2ctype(code, dflt=missing, name='type'):  # MCCABE 20
    '''Return the C{ctypes} type for a single ObjC type encoding.
    '''
    try:
        return _encoding2ctype[code]
    except KeyError:
        pass

    coderr = code
    if code[:1] == b'r':  # const ptr or decorator
        code = code[1:]
    try:
        c = code[-1:]
        if c == b'"':  # ..."name" suffix
            i = code.find(c)
            if i < 1:
                raise TypeCodeError
            code = code[:i]  # drop "name"

        elif c == b']':  # array ...[...]
            i = code.find(b'[')
            if i < 0:
                raise TypeCodeError
            elif i > 0:  # ignore array type
                code = code[:i + 1] + c
            else:  # convert array to pointer
                code = b'^' + code[1:-1].strip(b'0123456789')

        elif c in _TYPECLOSERS:  # Block, Struct or Union
            o = _TYPE2OPENER[c]
            if code[:1] != o:
                o = b'^' + o
                if code[:2] != o:
                    raise TypeCodeError
            code = o + c  # {} or ^{}, etc.

        if code[:1] == b'^':
            if len(code) < 2:
                raise TypeCodeError
#           ctype = POINTER(_encoding2ctype[code[1:]])  # breaks on '^^^...'
            ctype = POINTER(encoding2ctype(code[1:]))  # allows '^^^...'
            _encoding2ctype[code] = ctype
            return ctype
        elif len(code):
            return _encoding2ctype[code]
        else:
            raise TypeCodeError

    except TypeCodeError:
        raise TypeCodeError('%s encoding %s: %r' % (bytes2str(name), 'invalid', coderr))
    except KeyError:
        pass

    if dflt is missing:
        raise TypeCodeError('%s encoding %s: %r' % (bytes2str(name), 'unknown', coderr))
    elif code[:1] == b'^':
        return POINTER(dflt)
    else:
        return dflt


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


_TYPECODESET = set(iterbytes(b'cCiIsSlLqQfdBvP*@#:b^?'))  # _emcoding2ctype.keys()
_TYPESKIPPED = set(iterbytes(b'0123456789 nNoOrRV'))  # type, width and offsets

_TYPE2CLOSER = {b'{': b'}', b'[': b']', b'(': b')', b'<': b'>'}
_TYPE2OPENER = dict(reversed(_) for _ in _TYPE2CLOSER.items())

_TYPEOPENERS = set(_TYPE2CLOSER.keys())
_TYPECLOSERS = set(_TYPE2CLOSER.values())


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

        - P = Python object (like PyObjectEncoding)

    Unsupported Type Encodings:

        - bW = bitfield of width W
        - [Ltype] = array of L items of type
        - E{lb}name=type...E{rb} = structure
        - (name=type...) = union
        - <...> = block

    For ObjC internal use only:

        - n, N = in, inout
        - o, O = out, bycopy
        - r, R = const, byref
        - V = oneway

    Type encodings may be preceeded by a C{"name"}, for example a bitfield
    C{"name"b1}, structure items C{E{lb}CGsize="width"d"heigth"dE{rb}},
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

    for b in iterbytes(str2bytes(encoding)):

        if b in _TYPEOPENERS:
            if code and code[-1] != b'^' and not opened:
                codes.append(b''.join(code))
                code = []
            opened.append(_TYPE2CLOSER[b])
            code.append(b)

        elif b in _TYPECLOSERS:
            code.append(b)
            if not opened or b != opened.pop():
                raise TypeCodeError('encoding %s: %r' % ('unbalanced',
                                    bytes2str(b''.join(code))))
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
                    raise TypeCodeError('encoding %s: %r' % ('invalid',
                                        bytes2str(code)))
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
        raise TypeCodeError('encoding %s: %r' % ('unbalanced', bytes2str(encoding)))

    if code:  # final type code
        codes.append(b''.join(code))
    return codes


__all__ = _exports(locals(), 'PyObjectEncoding', 'TypeCodeError', 'c_void',
                   starts=('CG', 'CF', 'NS', 'ObjC', 'is', 'split_'),
                   ends='_t')

if __name__ == '__main__':

    from utils import _allisting, bytes2repr

    def _c(ctype):
        return 'c_void' if ctype is c_void else ctype.__name__

    print('\n%s ...' % ('ctype2encoding',))
    i = 0
    for c, e in sorted((_c(c), e) for c, e in _ctype2encoding.items()):
        i += 1
        print(' %2s: %-9s -> %s' % (i, c, bytes2repr(e)))

    print('\n%s ...' % ('encoding2ctype',))
    e = _encoding2ctype.copy()
    e.update(_emcoding2ctype)
    i = 0
    for e, c in sorted(e.items()):
        i += 1
        print(' %2s: %-5s -> %s' % (i, bytes2repr(e), _c(c)))

    print('\n%s ...' % ('check NS...Encoding',))
    for t, e in ((NSPoint_t, NSPointEncoding),
                 (NSRange_t, NSRangeEncoding),
                 (NSRect_t,  NSRectEncoding),
                 (NSSize_t,  NSSizeEncoding)):
        c = b''.join(ctype2encoding(c) for _, c in t._fields_)
        c = b'=%s}' % (c,)
        if not e.endswith(c):
            print('  %s: %r != %r' % (t.__name__, c, e))

    _allisting(__all__, locals(), __version__, __file__)
