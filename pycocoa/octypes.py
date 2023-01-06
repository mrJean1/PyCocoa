
# -*- coding: utf-8 -*-

# License at the end of this file.

'''ObjC C{..._t} type definitions and some additional C{ctypes}.

Names starting with C{c_} are C{ctypes}, names ending with C{_t}
are ObjC types defined in terms of a C{ctypes} C{c_} type.

@var Array_t:                ObjC C{NSArray} ctype.
@var CFIndex_t:              ObjC C{CFIndex} ctype.
@var CFStringEncoding_t:     ObjC C{CFStringEncoding} ctype.
@var CGBitmapInfo_t:         ObjC C{CGBitmapInfo} ctype.
@var CGDirectDisplayID_t:    ObjC C{CGDirectDisplayID} ctype.
@var CGError_t:              ObjC C{CGError} ctype.
@var CGFloat_t:              ObjC C{CGFloat} ctype.
@var CTFontOrientation_t :   Objc C{CTFontOrientation} ctype.
@var CTFontSymbolicTraits_t: Objc C{CTFontSymbolicTraits} ctype.
@var CGGlyph_t:              ObjC C{CGGlyph} ctype.
@var Data_t:                 ObjC C{CFDataRef} ctype.
@var Dictionary_t:           ObjC C{NSDictionary} ctype.
@var NSDoubl_t:              ObjC C{CFDataRef} ctype.
@var NSFloat_t:              ObjC C{NSFloat} ctype.
@var NSInteger_t:            ObjC C{NSInteger} ctype.
@var NSTimeInterval_t:       ObjC C{NSTimeInterval} ctype.
@var NSUInteger_t:           ObjC C{NSUInteger} ctype.
@var NumberType_t:           ObjC C{NSNumberType} ctype.
@var Number_t:               ObjC C{NSNumber} ctype.
@var OptionFlags_t:          ObjC C{CFOptionFlags} ctype.
@var Set_t:                  ObjC C{NSSet} ctype.
@var String_t:               ObjC C{CFStringRef} ctype.
@var TimeInterval_t:         ObjC C{CFTimeInterval} ctype.
@var TypeID_t:               ObjC C{CFTypeID} ctype.
@var UniChar_t:              Unicode C{unsigned short} ctype.
@var unichar_t:              Unicode C{wchar} ctype.
'''
# all imports listed explicitly to help PyChecker
# from pycocoa.getters import get_selectornameof
from pycocoa.lazily import _ALL_LAZY, _bNN_, _NN_
from pycocoa.utils  import _bCOLON_, bytes2str, inst2strepr, \
                            iterbytes, missing, property_RO, \
                            str2bytes

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

__all__ = _ALL_LAZY.octypes
__version__ = '21.11.04'

z = sizeof(c_void_p)
if z == 4:
    c_ptrdiff_t = c_int32
    __LP64__ = False
elif z == 8:
    c_ptrdiff_t = c_int64
    __LP64__ = True
else:
    raise ValueError('sizeof(c_void_p): %s' % (z,))
del z

from platform import machine as m
m = m()  # see .utils.machine
__arm64__  = m == 'arm64'   # PYCHOK see .oslibs._Apple_Si
__i386__   = m == 'i386'    # PYCHOK expected
__x86_64__ = m == 'x86_64'  # PYCHOK also Intel emulation
del m

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


def _bJoin(codes):
    # join bytes
    return _bNN_.join(codes)


# Note CGBase.h at /System/Library/Frameworks/ApplicationServices
# .framework/Frameworks/CoreGraphics.framework/Headers/CGBase.h
# defines CG/Float as double if __LP64__, otherwise it is float.
# Also, these types can't be subclasses of c_... ctypes.
if __LP64__:
    CGFloat_t    = c_double  # CGFloat.nativeType
    NSInteger_t  = c_long    # == Int_t?
    NSUInteger_t = c_ulong   # == Uint_t?

    NSIntegerMax = 0x7fffffffffffffff

    NSPointEncoding = CGPointEncoding = b'{CGPoint=dd}'
    NSRangeEncoding                   = b'{_NSRange=QQ}'
    NSRectEncoding  = CGRectEncoding  = b'{CGRect={CGPoint=dd}{CGSize=dd}}'
    NSSizeEncoding  = CGSizeEncoding  = b'{CGSize=dd}'

else:
    CGFloat_t    = c_float  # CGFloat.nativeType
    NSInteger_t  = c_int    # == Int_t?
    NSUInteger_t = c_uint   # == Uint_t?

    NSIntegerMax = 0x7fffffff

    NSPointEncoding = b'{_NSPoint=ff}'
    NSRangeEncoding = b'{_NSRange=II}'
    NSRectEncoding  = b'{_NSRect={_NSPoint=ff}{_NSSize=ff}}'
    NSSizeEncoding  = b'{_NSSize=ff}'

    CGPointEncoding = NSPointEncoding.replace(b'_NS', b'CG')
    CGRectEncoding  = NSRectEncoding.replace( b'_NS', b'CG')
    CGSizeEncoding  = NSSizeEncoding.replace( b'_NS', b'CG')


# NSFloatMax = GCGFloat.greatestFiniteMagnitude()
# NSFloatMin = GCGFloat.leastNonzeroMagnitude()
CFIndex_t = NSInteger_t  # == Int, no CGIndex_t?
# Special case so that NSImage.initWithCGImage_size_() will work.
CGImageEncoding  = b'{CGImage=}'
NSZoneEncoding   = b'{_NSZone=}'
PyObjectEncoding = b'{PyObject=@}'


# wrappers for ObjC classes, structs, etc.  mostly
# to see more meaningful names in res- and argtypes
class Allocator_t(ObjC_t):  # Id_t
    '''ObjC C{CFAllocatorRef} type.
    '''
    pass


Array_t = c_void_p  # ObjC C{NSArray} ctype


class Block_t(ObjC_t):
    '''ObjC C{block} type.
    '''
    pass


class BOOL_t(c_bool):
    '''ObjC C{boolean} type.
    '''
    pass


Data_t       = c_void_p  # ObjC C{CFDataRef} ctype
Dictionary_t = c_void_p  # ObjC C{NSDictionary} ctype


class Id_t(ObjC_t):
    '''ObjC C{Id/self} type, encoding b'@'.
    '''
    pass

# objc_id = Id_t


class Class_t(Id_t):  # ObjC_t
    '''ObjC C{Class} type, encoding b'#'.
    '''
    pass


class IMP_t(ObjC_t):
    '''ObjC C{IMPlementation} type.
    '''
    pass


class Ivar_t(ObjC_t):
    '''ObjC C{instance variable} type.
    '''
    pass


class Method_t(ObjC_t):
    '''ObjC C{method} type.
    '''
    pass


Number_t      = c_void_p  # ObjC C{NSNumber} ctype
NumberType_t  = c_ulong   # c_uint32
OptionFlags_t = c_ulong   # ObjC C{CFOptionFlags} ctype


class Protocol_t(Id_t):
    '''ObjC C{protocol} type.
    '''
    pass


class RunLoop_t(Id_t):
    '''ObjC C{CFRunLoopRef} type.
    '''
    pass


class SEL_t(ObjC_t):
    '''ObjC C{SELector/cmd} type, encoding C{b':'}.
    '''
    _name_ = None
#   def __new__(cls, name_=None):
#       self = libobjc.sel_registerName(str2bytes(name_))
#       return self

    def __repr__(self):
        return '<%s(%s)>' % (self.__class__.__name__, self)

    def __str__(self):
        return 'None' if self.value is None else bytes2str(self.name_)

    @property_RO
    def name_(self):
        if self._name_ is None:
            if self.value is None:
                raise ValueError('Null %r' % (self,))
            from pycocoa.getters import get_selectornameof
            self._name_ = get_selectornameof(self) or 'SEL_t'
        return self._name_


Set_t    = c_void_p  # ObjC C{NSset} ctype
String_t = c_void_p  # ObjC C{CFStringRef} ctype


class Struct_t(ObjC_t):
    '''ObjC C{struct} type.
    '''
    pass


# unhashable type if class(ObjC_t)
TimeInterval_t = c_double  # ObjC CFTimeInterval type, != NSTimeInterval_t
TypeID_t       = c_ulong   # ObjC CFTypeID type


class TypeRef_t(ObjC_t):  # ObjC CFTypeRef type
    '''ObjC opaque type.
    '''
    pass


class Union_t(Id_t):  # XXX or ObjC_t?
    '''ObjC C{union} type.
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


class URL_t(Id_t):
    '''ObjC C{URL} type.
    '''
    pass


class VoidPtr_t(ObjC_t):
    '''Same as C{c_void_p}, but distinguishable from C{c_void_p}.
    '''
    pass


# <https://StackOverflow.com/questions/41502199/
#  how-to-decipher-objc-method-description-from-protocol-method-description-list>
class objc_method_description_t(c_struct_t):
    '''ObjC C{struct} with fields C{name} and C{types} (C{SEL_t}, C{c_char_p}).
    '''
    _fields_ = ('name', SEL_t), ('types', c_char_p)


class objc_property_t(ObjC_t):
    '''ObjC C{property} Class.
    '''
    pass


class objc_property_attribute_t(c_struct_t):
    '''ObjC C{struct} with fields C{name} and C{value} (both C{c_char_p}).
    '''
    _fields_ = ('name', c_char_p), ('value', c_char_p)


class objc_super_t(c_struct_t):
    '''ObjC C{struct} with fields C{receiver} and C{class} (C{Id_t}, C{Class_t}).
    '''
    _fields_ = ('receiver', Id_t), ('super_class', Class_t)


objc_super_t_ptr = POINTER(objc_super_t)  # used in .runtime.send_super and .__init__

NSDouble_t = c_double  # always 64-bit double
NSFloat_t  = c_float   # always 32-bit float


# NSRange.h
class NSRange_t(c_struct_t):
    '''ObjC C{struct} with fields C{loc[ation]} and C{len[gth]} (both C{NSUInteger_t}).
    '''
    _fields_ = ('location', NSUInteger_t), ('length', NSUInteger_t)


# CF/Range struct defined in CFBase.h
class CFRange_t(c_struct_t):
    '''ObjC C{struct} with fields C{loc[ation]} and C{len[gth]} (both C{CFIndex_t}).
    '''
    _fields_ = ('location', CFIndex_t), ('length', CFIndex_t)


# from /System/Library/Frameworks/Foundation.framework/Headers/NSGeometry.h
class NSPoint_t(c_struct_t):  # == CGPoint_t
    '''ObjC C{struct} with fields C{x} and C{y} (both C{CGFloat_t}).
    '''
    _fields_ = ('x', CGFloat_t), ('y', CGFloat_t)


# from /System/Library/Frameworks/Foundation.framework/Headers/NSGeometry.h
class NSSize_t(c_struct_t):  # == CGSize_t
    '''ObjC C{struct} with fields C{width} and C{height} (both C{CGFloat_t}).
    '''
    _fields_ = ('width', CGFloat_t), ('height', CGFloat_t)


class NSRect_t(c_struct_t):  # == CGRect_t
    '''ObjC C{struct} with fields C{origin} and C{size} (C{NSPoint_t}, C{NSSize_t}).
    '''
    _fields_ = ('origin', NSPoint_t), ('size', NSSize_t)


class NSRect4_t(NSRect_t):
    '''ObjC C{struct}, like L{NSRect_t} with different signature and properties.
    '''
    def __init__(self, x=0, y=0, width=0, height=0):
        if width < 0:
            width = -width
            x -= width

        if height < 0:
            height = -height
            y -= height

        super(NSRect4_t, self).__init__(NSPoint_t(x, y), NSSize_t(width, height))

    def __repr__(self):
        r = inst2strepr(self, repr, 'x', 'y', 'width', 'height')
        return '<%s at %#x>' % (r, id(self))

    def __str__(self):
        return inst2strepr(self, str, 'x', 'y', 'width', 'height')

    @property_RO
    def bottom(self):
        '''Get the bottom y coordinate (C{float}).
        '''
        return self.y

    @property_RO
    def height(self):
        '''Get the height (C{float}).
        '''
        return self.size.height

    @property_RO
    def left(self):
        '''Get the lower x coordinate (C{float}).
        '''
        return self.x

    @property_RO
    def right(self):
        '''Get the upper x coordinate (C{float}).
        '''
        return self.x + self.width

    @property_RO
    def top(self):
        '''Get the upper y coordinate (C{float}).
        '''
        return self.y + self.heigth

    @property_RO
    def width(self):
        '''Get the width (C{float}).
        '''
        return self.size.width

    @property_RO
    def x(self):
        '''Get the x coordinate (C{float}).
        '''
        return self.origin.x

    @property_RO
    def y(self):
        '''Get the y coordinate (C{float}).
        '''
        return self.origin.y


CGBitmapInfo_t         = c_uint32   # CGImage.h
CGDirectDisplayID_t    = c_uint32   # CGDirectDisplay.h
CGError_t              = c_int32    # CGError.h
CGGlyph_t              = c_uint16   # c_ushort
CGPoint_t              = NSPoint_t  # 32-bit encoding is different
CGRect_t               = NSRect_t   # 32-bit encoding is different
CGSize_t               = NSSize_t   # 32-bit encoding is different
CTFontOrientation_t    = c_uint32   # CTFontDescriptor.h
CTFontSymbolicTraits_t = c_uint32   # CTFontTraits.h

# for backward compatibility with cocoa-python:
NSMakePoint = NSPoint_t
NSMakeRange = NSRange_t  # CFRangeMake(LOC, LEN)
NSMakeRect  = NSRect4_t
NSMakeSize  = NSSize_t

NSNotFound  = NSIntegerMax
NSPointZero = NSPoint_t(0, 0)

# NSDate.h
NSTimeInterval_t = c_double  # a ctype, != TimeInterval_t

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
                   SEL_t:     _bCOLON_,
                   py_object:  PyObjectEncoding}

# add c_?longlong only if different from c_?long
if sizeof(c_longlong) != sizeof(c_long):
    _ctype2encoding.update({c_longlong: b'q'})
if sizeof(c_ulonglong) != sizeof(c_ulong):
    _ctype2encoding.update({c_ulonglong: b'Q'})


def ctype2encoding(ctype, dflt=b'?'):
    '''Return the type encoding for a given C{ctypes} type.

       @param ctype: The type (C{ctypes}).
       @keyword dflt: Default encoding (C{bytes}).

       @return: The type encoding (C{bytes}).
    '''
    return _ctype2encoding.get(ctype, dflt)


NSFloatEncoding    = ctype2encoding(NSFloat_t)
NSIntegerEncoding  = ctype2encoding(NSInteger_t)
NSUIntegerEncoding = ctype2encoding(NSUInteger_t)

# map for encoding type code to ctypes type, in .nstypes.nsValue2type
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
        raise RuntimeError('code %r ctype %r vs %r' % (code, c_, f_))
del c_, code, f_

# map 'c' to c_byte rather than c_char, because
# otherwise ctypes converts the value into a 1-char
# string which is generally not what we want,
# especially when the 'c' represents a bool
_encoding2ctype[b'c'] = c_byte  # C_ubyte, see oslibs.cfNumber2bool!

_emcoding2ctype = {b'Vv': c_void,
                   b'^' + CGImageEncoding: c_void_p,
                   b'^' + NSZoneEncoding:  c_void_p}

if CGPointEncoding != NSPointEncoding:  # in 32-bit
    _encoding2ctype.update({CGPointEncoding: CGPoint_t})
if CGRectEncoding  != NSRectEncoding:  # in 32-bit
    _encoding2ctype.update({CGRectEncoding:  CGRect_t})
if CGSizeEncoding  != NSSizeEncoding:  # in 32-bit
    _encoding2ctype.update({CGSizeEncoding:  CGSize_t})


def emcoding2ctype(code, dflt=missing, name='type'):
    '''Return the C{ctypes} type for a single ObjC type encoding
       code for a I{method} result or I{method} argument.

       @param code: The type encoding (C{bytes}).
       @keyword dflt: Default result (C{ctype}).
       @keyword name: Name of the method (C{str}).

       @return: The C{ctype} (C{ctypes}).

       @raise TypeCodeError: Invalid or unbalanced I{code}, unless
                             a I{dflt} C{ctype} is provided.
    '''
    try:
        return _emcoding2ctype[code]
    except KeyError:
        pass
    return encoding2ctype(code, dflt, name)


def encoding2ctype(code, dflt=missing, name='type'):  # MCCABE 20
    '''Return the C{ctypes} type for a single ObjC type encoding code.

       @param code: The type encoding (C{bytes}).
       @keyword dflt: Default encoding (C{ctype}).
       @keyword name: Name of the type (C{str}).

       @return: The C{ctype} (C{ctypes}).

       @raise TypeCodeError: Invalid or unbalanced I{code}, unless
                             a I{dflt} C{ctype} is provided.
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
            o = _TYPECLOSERS[c]
            i = code.find(o)
            if i < 0 or i > 4 or code[:i].strip(b'^'):  # != _bNN_
                raise TypeCodeError
            # if i > 1 code should only contain a name, see ^^{example}
            # above Table 6-2 at <https://Developer.Apple.com/library/
            # archive/documentation/Cocoa/Conceptual/ObjCRuntimeGuide/
            # Articles/ocrtTypeEncodings.html>
            code = code[:i + 1] + c

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
       for the hidden method arguments C{Id/self} and C{SEL/cmd}.

       @note: Does not handle C{bitfield}s, C{array}s, C{struct}s,
              C{union}s, etc. and strips any offset, size or width
              specifiers from the encoding.

       @return: 2-Tuple (I{codes, encoding}), where I{codes} is the list
                of individual type encodings from item I{start=0} and
                I{encoding} is the combined type encoding in C{bytes},
                both extended with C{Id/self} and C{SEL/cmd} iff needed.

       @raise TypeCodeError: Invalid or unbalanced I{encoding}.

       @example:

       >>> split_emcoding2('v*')
       >>> (['v', '@', ':', '*'], 'v@:*')
    '''
    codes = split_encoding(encoding)
    if codes[1:3] != [b'@', _bCOLON_]:
        # Add codes for hidden arguments
        codes.insert(1,  b'@')     # Id/self type encoding
        codes.insert(2, _bCOLON_)  # SEL/cmd type encoding

    return codes[start:], _bJoin(codes)


_TYPECODESET = set(iterbytes(b'cCiIsSlLqQfdBvP*@#:b^?'))  # _emcoding2ctype.keys()
_TYPESKIPPED = set(iterbytes(b'0123456789 nNoOrRV'))  # type, width and offsets

_TYPEOPENERS = {b'{': b'}', b'[': b']', b'(': b')', b'<': b'>'}  # opener->closer
_TYPECLOSERS = dict(reversed(_) for _ in _TYPEOPENERS.items())   # closer->opener


def split_encoding(encoding):  # MCCABE 18
    '''Split a type encoding into separate type encodings.

       Does not handle C{bitfield}s, C{array}s, C{struct}s, C{union}s,
       etc. and strips any offset, size or width specifiers from the
       encoding.

       @return: The individual type encodings (C{list}).

       @raise TypeCodeError: Invalid or unbalanced I{encoding}.

       @example:

       >>> split_encoding('^v16@0:8')
       >>> ['^v', '@', ':']

       >>> split_encoding('{CGSize=dd}40@0:8{PyObject=@}Q32')
       >>> ['{CGSize=dd}', '@', ':', '{PyObject=@}', 'Q']

       Supported Type Encodings:

           - B = bool (C++ bool, C99 _Bool)
           - c, C = char, unsigned char
           - f, d = float, double
           - i, I = int, unsigned int
           - l, L = long, unsigned long (32-bit in 64-bit Apps)
           - q, Q = long long, unsigned long long
           - s, S = short, unsigned short
           - t, T = 128-bit int, unsigned int
           - v = void
           - * = string (char *)
           - : = method selector C{SEL/cmd}
           - # = class
           - #"name" = class "name"
           - @ = object instance C{Id/self} or statically typed
           - @"name" = instance C{Id/self} of class "name"
           - ^type = pointer to type
           - ? = unknown type (among other things, used for function pointers)

       PyCocoa specific:

           - P = Python object, shorthand for C{PyObjectEncoding}

       Unsupported Type Encodings:

           - bW = bitfield of width W
           - [Ltype] = array of L items of type
           - E{lb}name=type...E{rb} = structure
           - (name=type...) = union
           - <...> = block
           - ?<...> = block with signature

       Unknown or for ObjC internal use:

           - A = ?
           - j = ?
           - n, N = in, inout
           - o, O = out, bycopy
           - r, R = const, byref
           - V = oneway

       @note: Type encodings may be preceeded by C{"name"}, for example a
              C{bitfield} C{"name"b1}, C{struct} items C{E{lb}CGsize="width"d"heigth"dE{rb}},
              C{union} items, etc. and all such C{"name"} prefixes are ignored.

       @see: U{Type Encodings<https://Developer.Apple.com/library/content/documentation/
             Cocoa/Conceptual/ObjCRuntimeGuide/Articles/ocrtTypeEncodings.html>},
             U{NSHipster Type Encodings<https://NSHipster.com/type-encodings>} and
             U{Digits in type encoding<https://StackOverflow.com/questions/11527385/
             how-are-the-digits-in-objc-method-type-encoding-calculated>}.
    '''
    code   = []
    codes  = []
    opened = []     # opened braces, brackets, parensm etc.
    quoted = False  # inside double quotes

    for b in iterbytes(str2bytes(encoding)):

        if b in _TYPEOPENERS:
            if code and code[-1] != b'^' and not opened:
                codes.append(_bJoin(code))
                code = []
            opened.append(_TYPEOPENERS[b])
            code.append(b)

        elif b in _TYPECLOSERS:
            code.append(b)
            if not opened or b != opened.pop():
                raise TypeCodeError('encoding %s: %r' % ('unbalanced',
                                    bytes2str(_bJoin(code))))
            if not opened:
                codes.append(_bJoin(code))
                code = []

        elif opened:  # inside braces, etc
            # XXX ignore digits?
            code.append(b)  # stick anything on

        elif b == b'"':
            code.append(b)
            if quoted:  # closing quotes
                code = _bJoin(code)
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
                codes.append(_bJoin(code))
                code = []
            code.append(b)

        elif b in _TYPESKIPPED:
            pass  # ignore type, width and offsets

    if opened:
        raise TypeCodeError('encoding %s: %r' % ('unbalanced', bytes2str(encoding)))

    if code:  # final type code
        codes.append(_bJoin(code))
    return codes


if __name__ == '__main__':

    from pycocoa.utils import _all_listing, bytes2repr, \
                              _Globals, printf

    _Globals.argv0 = _NN_

    def _c(ctype):
        return 'c_void' if ctype is c_void else ctype.__name__

    printf('%s ...', 'ctype2encoding', nl=1)
    i = 0
    for c, e in sorted((_c(c), e) for c, e in _ctype2encoding.items()):
        i += 1
        printf('%4s: %-9s -> %s', i, c, bytes2repr(e))

    printf('%s ...', 'encoding2ctype', nl=1)
    e = _encoding2ctype.copy()
    e.update(_emcoding2ctype)
    i = 0
    for e, c in sorted(e.items()):
        i += 1
        printf('%4s: %-5s -> %s', i, bytes2repr(e), _c(c))

    printf('%s ...', 'checking NS...Encoding', nl=1)
    for t, e in ((NSPoint_t, NSPointEncoding),
                 (NSRange_t, NSRangeEncoding),
                 (NSRect_t,  NSRectEncoding),
                 (NSSize_t,  NSSizeEncoding)):
        c = _bJoin(ctype2encoding(c) for _, c in t._fields_)
        c = _bJoin((b'=', c, b'}'))
        if not e.endswith(c):
            printf('  %s: %r != %r', t.__name__, c, e)

    _all_listing(__all__, locals())

# % python3 -m pycocoa.octypes
#
# ctype2encoding ...
#    1: Class_t   -> b'#'
#    2: Id_t      -> b'@'
#    3: NSPoint_t -> b'{CGPoint=dd}'
#    4: NSRange_t -> b'{_NSRange=QQ}'
#    5: NSRect_t  -> b'{CGRect={CGPoint=dd}{CGSize=dd}}'
#    6: NSSize_t  -> b'{CGSize=dd}'
#    7: SEL_t     -> b':'
#    8: c_bool    -> b'B'
#    9: c_char    -> b'c'
#   10: c_char_p  -> b'*'
#   11: c_double  -> b'd'
#   12: c_float   -> b'f'
#   13: c_int     -> b'i'
#   14: c_long    -> b'l'
#   15: c_short   -> b's'
#   16: c_ubyte   -> b'C'
#   17: c_uint    -> b'I'
#   18: c_ulong   -> b'L'
#   19: c_ushort  -> b'S'
#   20: c_void_p  -> b'@'
#   21: py_object -> b'{PyObject=@}'
#
# encoding2ctype ...
#    1: b'#'  -> Class_t
#    2: b'()' -> Union_t
#    3: b'*'  -> c_char_p
#    4: b':'  -> SEL_t
#    5: b'<>' -> Block_t
#    6: b'?'  -> Unknown_t
#    7: b'@'  -> Id_t
#    8: b'B'  -> c_bool
#    9: b'C'  -> c_ubyte
#   10: b'I'  -> c_uint
#   11: b'L'  -> c_ulong
#   12: b'P'  -> py_object
#   13: b'Q'  -> c_ulong
#   14: b'S'  -> c_ushort
#   15: b'Vv' -> c_void
#   16: b'[]' -> c_void_p
#   17: b'^?' -> UnknownPtr_t
#   18: b'^v' -> VoidPtr_t
#   19: b'^{CGImage=}' -> c_void_p
#   20: b'^{_NSZone=}' -> c_void_p
#   21: b'c'  -> c_byte
#   22: b'd'  -> c_double
#   23: b'f'  -> c_float
#   24: b'i'  -> c_int
#   25: b'l'  -> c_long
#   26: b'q'  -> c_long
#   27: b's'  -> c_short
#   28: b'v'  -> c_void
#   29: b'{CGPoint=dd}' -> NSPoint_t
#   30: b'{CGRect={CGPoint=dd}{CGSize=dd}}' -> NSRect_t
#   31: b'{CGSize=dd}' -> NSSize_t
#   32: b'{PyObject=@}' -> py_object
#   33: b'{_NSRange=QQ}' -> NSRange_t
#   34: b'{}' -> Struct_t
#
# checking NS...Encoding ...
#   NSRange_t: b'=LL}' != b'{_NSRange=QQ}'
#
# pycocoa.octypes.__all__ = tuple(
#  pycocoa.octypes.Allocator_t is <class .Allocator_t>,
#  pycocoa.octypes.Array_t is <class ctypes.c_void_p>,
#  pycocoa.octypes.Block_t is <class .Block_t>,
#  pycocoa.octypes.BOOL_t is <class .BOOL_t>,
#  pycocoa.octypes.c_ptrdiff_t is <class ctypes.c_long>,
#  pycocoa.octypes.c_struct_t is <class .c_struct_t>,
#  pycocoa.octypes.c_void is None,
#  pycocoa.octypes.CFIndex_t is <class ctypes.c_long>,
#  pycocoa.octypes.CFRange_t is <class .CFRange_t>,
#  pycocoa.octypes.CGBitmapInfo_t is <class ctypes.c_uint>,
#  pycocoa.octypes.CGDirectDisplayID_t is <class ctypes.c_uint>,
#  pycocoa.octypes.CGError_t is <class ctypes.c_int>,
#  pycocoa.octypes.CGFloat_t is <class ctypes.c_double>,
#  pycocoa.octypes.CGGlyph_t is <class ctypes.c_ushort>,
#  pycocoa.octypes.CGImageEncoding is b'{CGImage=}',
#  pycocoa.octypes.CGPoint_t is <class .NSPoint_t>,
#  pycocoa.octypes.CGPointEncoding is b'{CGPoint=dd}',
#  pycocoa.octypes.CGRect_t is <class .NSRect_t>,
#  pycocoa.octypes.CGRectEncoding is b'{CGRect={CGPoint=dd}{CGSize=dd}}',
#  pycocoa.octypes.CGSize_t is <class .NSSize_t>,
#  pycocoa.octypes.CGSizeEncoding is b'{CGSize=dd}',
#  pycocoa.octypes.Class_t is <class .Class_t>,
#  pycocoa.octypes.CTFontOrientation_t is <class ctypes.c_uint>,
#  pycocoa.octypes.CTFontSymbolicTraits_t is <class ctypes.c_uint>,
#  pycocoa.octypes.Data_t is <class ctypes.c_void_p>,
#  pycocoa.octypes.Dictionary_t is <class ctypes.c_void_p>,
#  pycocoa.octypes.Id_t is <class .Id_t>,
#  pycocoa.octypes.IMP_t is <class .IMP_t>,
#  pycocoa.octypes.Ivar_t is <class .Ivar_t>,
#  pycocoa.octypes.Method_t is <class .Method_t>,
#  pycocoa.octypes.NSDouble_t is <class ctypes.c_double>,
#  pycocoa.octypes.NSFloat_t is <class ctypes.c_float>,
#  pycocoa.octypes.NSFloatEncoding is b'f',
#  pycocoa.octypes.NSInteger_t is <class ctypes.c_long>,
#  pycocoa.octypes.NSIntegerEncoding is b'l',
#  pycocoa.octypes.NSIntegerMax is 9223372036854775807 or 0x7FFFFFFFFFFFFFFF,
#  pycocoa.octypes.NSMakePoint is <class .NSPoint_t>,
#  pycocoa.octypes.NSMakeRange is <class .NSRange_t>,
#  pycocoa.octypes.NSMakeRect is <class .NSRect4_t>,
#  pycocoa.octypes.NSMakeSize is <class .NSSize_t>,
#  pycocoa.octypes.NSNotFound is 9223372036854775807 or 0x7FFFFFFFFFFFFFFF,
#  pycocoa.octypes.NSPoint_t is <class .NSPoint_t>,
#  pycocoa.octypes.NSPointEncoding is b'{CGPoint=dd}',
#  pycocoa.octypes.NSPointZero is <NSPoint_t(x=0.0, y=0.0) at 0x1030a8fc0>,
#  pycocoa.octypes.NSRange_t is <class .NSRange_t>,
#  pycocoa.octypes.NSRangeEncoding is b'{_NSRange=QQ}',
#  pycocoa.octypes.NSRect4_t is <class .NSRect4_t>,
#  pycocoa.octypes.NSRect_t is <class .NSRect_t>,
#  pycocoa.octypes.NSRectEncoding is b'{CGRect={CGPoint=dd}{CGSize=dd}}',
#  pycocoa.octypes.NSSize_t is <class .NSSize_t>,
#  pycocoa.octypes.NSSizeEncoding is b'{CGSize=dd}',
#  pycocoa.octypes.NSTimeInterval_t is <class ctypes.c_double>,
#  pycocoa.octypes.NSUInteger_t is <class ctypes.c_ulong>,
#  pycocoa.octypes.NSUIntegerEncoding is b'L',
#  pycocoa.octypes.NSZoneEncoding is b'{_NSZone=}',
#  pycocoa.octypes.Number_t is <class ctypes.c_void_p>,
#  pycocoa.octypes.NumberType_t is <class ctypes.c_ulong>,
#  pycocoa.octypes.objc_method_description_t is <class .objc_method_description_t>,
#  pycocoa.octypes.objc_property_attribute_t is <class .objc_property_attribute_t>,
#  pycocoa.octypes.objc_property_t is <class .objc_property_t>,
#  pycocoa.octypes.objc_super_t is <class .objc_super_t>,
#  pycocoa.octypes.ObjC_t is <class .ObjC_t>,
#  pycocoa.octypes.OptionFlags_t is <class ctypes.c_ulong>,
#  pycocoa.octypes.Protocol_t is <class .Protocol_t>,
#  pycocoa.octypes.PyObjectEncoding is b'{PyObject=@}',
#  pycocoa.octypes.RunLoop_t is <class .RunLoop_t>,
#  pycocoa.octypes.SEL_t is <class .SEL_t>,
#  pycocoa.octypes.Set_t is <class ctypes.c_void_p>,
#  pycocoa.octypes.split_emcoding2 is <function .split_emcoding2 at 0x1032405e0>,
#  pycocoa.octypes.split_encoding is <function .split_encoding at 0x103240670>,
#  pycocoa.octypes.String_t is <class ctypes.c_void_p>,
#  pycocoa.octypes.Struct_t is <class .Struct_t>,
#  pycocoa.octypes.TimeInterval_t is <class ctypes.c_double>,
#  pycocoa.octypes.TypeCodeError is <class .TypeCodeError>,
#  pycocoa.octypes.TypeID_t is <class ctypes.c_ulong>,
#  pycocoa.octypes.TypeRef_t is <class .TypeRef_t>,
#  pycocoa.octypes.UniChar_t is <class ctypes.c_ushort>,
#  pycocoa.octypes.unichar_t is <class ctypes.c_wchar>,
#  pycocoa.octypes.Union_t is <class .Union_t>,
#  pycocoa.octypes.Unknown_t is <class .Unknown_t>,
#  pycocoa.octypes.UnknownPtr_t is <class .UnknownPtr_t>,
#  pycocoa.octypes.URL_t is <class .URL_t>,
#  pycocoa.octypes.VoidPtr_t is <class .VoidPtr_t>,
# )[83]
# pycocoa.octypes.version 21.11.04, .isLazy 1, Python 3.11.0 64bit arm64, macOS 13.0.1

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2023 -- mrJean1 at Gmail -- All Rights Reserved.
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
