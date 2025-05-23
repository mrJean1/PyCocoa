
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Various ObjC and macOS libraries, signatures, constants, etc.

@var Libs: The loaded C{macOS} libraries, all C{.dylib}.
@var Libs.AppKit: The '/System/Library/Frameworks/AppKit.framework/AppKit' library.
@var Libs.C: The '/usr/lib/libc.dylib' library.
@var Libs.CoreFoundation: The '/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation' library.
@var Libs.CoreGraphics: The '/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics' library.
@var Libs.CoreText: The '/System/Library/Frameworks/CoreText.framework/CoreText' library.
@var Libs.Foundation: The '/System/Library/Frameworks/Foundation.framework/Foundation' library.
@var Libs.libc: The '/usr/lib/libc.dylib' library.
@var Libs.libobjc: The '/usr/lib/libobjc.dylib' library.
@var Libs.ObjC: The '/usr/lib/libobjc.dylib' library.
@var Libs.PrintCore: The '/System/Library/Frameworks/ApplicationServices.framework/Frameworks/PrintCore.framework/PrintCore' library.
@var Libs.Quartz: The '/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics' library.

@var NO:  ObjC's False (C{const c_byte}).
@var YES: ObjC's True (C{const c_byte}).
'''
from pycocoa.basics import Adict
from pycocoa.internals import _bNN_, bytes2str, _COMMASPACE_, _Dmain_, _DOT_, \
                              _EQUALS_, _fmt, _fmt_invalid, _NN_, str2bytes  # _UNICODEC
# from pycocoa.lazily import _ALL_LAZY  # from .utils
from pycocoa.octypes import Allocator_t, Array_t, BOOL_t, CFIndex_t, CFRange_t, \
                            CGBitmapInfo_t, CGDirectDisplayID_t, CGError_t, \
                            CGFloat_t, CGGlyph_t, CGPoint_t, CGRect_t, CGSize_t, \
                            Class_t, c_ptrdiff_t, CTFontOrientation_t, \
                            CTFontSymbolicTraits_t, c_void, Data_t, Dictionary_t, \
                            Id_t, IMP_t, Ivar_t, Method_t, Number_t, NumberType_t, \
                            NSInteger_t, NSRect_t, objc_method_description_t, \
                            objc_property_t, objc_property_attribute_t, Protocol_t, \
                            RunLoop_t, SEL_t, Set_t, String_t, TypeID_t, TypeRef_t, \
                            UniChar_t, URL_t
from pycocoa.utils import __arm64__, __i386__, macOSver2, __x86_64__,  _ALL_LAZY

from copy import copy as _copy
from ctypes import byref, cast, CDLL, c_buffer, c_byte, c_char, \
                   c_char_p, c_double, c_float, c_int, c_int8, c_int16, \
                   c_int32, c_int64, CFUNCTYPE, c_long, c_longlong, \
                   c_short, c_size_t, c_uint, c_uint8, c_uint32, \
                   c_void_p, POINTER, sizeof  # c_ubyte, string_at
try:
    from ctypes.util import find_library as _find_library
except ImportError:  # XXX Pythonista/iOS
    def _find_library(*unused):  # PYCHOK redef
        return None  # not found
from os.path import join as _join, sep as _SEP

__all__ = _ALL_LAZY.oslibs
__version__ = '25.04.07'

_framework_ = 'framework'
_leaked2    = []  # leaked memory, 2-tuples (ptr, size)
# 'PointerType' in Python 2.6-, 'PyCPointerType' later
_POINTER_ts =  set(type(POINTER(_)) for _ in (Ivar_t, Method_t, Protocol_t,
               objc_method_description_t, objc_property_t, objc_property_attribute_t))

NO  = False  # c_byte(0)
YES = True   # c_byte(1)


class Libs(Adict):
    '''The loaded C{macOS} libraries, all C{.dylib}.
    '''
    def __setitem__(self, name, lib):
        lib.__doc__ = _fmt('The %r library.', lib._name.rstrip(_DOT_))
        Adict.__setitem__(self, name, lib)

Libs = Libs()  # PYCHOK singleton


class OSlibError(OSError):
    '''Couldn't find or load a macOS C{.dylib} library.
    '''
    def __init__(self, verb, name, *ns):
        t = _fmt("couldn't %s lib %r", verb, name)
        if ns:
            ns = _COMMASPACE_(*map(repr, ns))
            t  = _fmt('%s as %s', t, ns)
        OSError.__init__(self, t)


def _csignature(libfunc, restype, *argtypes, **checkerr):
    # set the result and argument ctypes of a library function
    # plus optionally a 1-argument result function
    libfunc.restype = restype
    if argtypes:
        libfunc.argtypes = argtypes
    if checkerr:
        n, f = checkerr.popitem()
        if not callable(f):
            t = _EQUALS_(n, f)
            raise TypeError(_fmt_invalid(checkerr=t))
        libfunc.errcheck = f
    return libfunc


def _csignature_list(libfunc, restype, *argtypes):
    # set the list result and argument ctypes and
    # install a handler to duplicate the result and
    # avoid leaking the memory of the original list
    libfunc.restype = restype
    if argtypes:
        libfunc.argtypes = argtypes
    # the result type must be a pointer to some other type
    # and the result must be a NULL-terminated array
    if type(restype) in _POINTER_ts:
        # ... and/or _nameOf(restype).startswith('LP_'):
        libfunc.errcheck = _listdup
    return libfunc


def _csignature_str(libfunc, restype, *argtypes):
    # set the string result and argument ctypes and
    # install a handler to duplicate the result and
    # avoid leaking the memory of the original string
    libfunc.restype = restype
    if argtypes:
        libfunc.argtypes = argtypes
    # the result type must be a (w?)char or byte pointer
    # and the result must be a nul-terminated string
    if restype in (c_char_p,):  # c_byte_p
        libfunc.errcheck = _strdup
    return libfunc


def _csignature_variadic(libfunc, restype, *argtypes):
    # set the result type of a variadic function PLUS
    # the types of any fixed arguments, REQUIRED for
    # Apple Silicon!  See issue U{#92892: ARM64 macOS
    # variadic arguments not passed properly in ctypes
    # <https://GitHub.com/python/cpython/issues/92892>}
    libfunc.restype = restype
    if argtypes:
        libfunc.argtypes = argtypes
    return libfunc


def _dllattr(dll, *arg_ctype, **kwd_ctype):  # in .runtime
    # duplicate a C{dll} attribute
    n,  _t = arg_ctype or kwd_ctype.popitem()
    v = _t.in_dll(dll, n)
    # setattr(sys.modules[__name__], n, v)  # into C{this module}
    return v


def _dlllist():  # list all installed C{dylib}s
    try:
        from os import fsdecode as _d
    except ImportError:
        from pycocoa.basics import lambda1 as _d
    # <https://GitHub.com/python/cpython/blob/main/Lib/ctypes/util.py>
    if _libc:
        _n = _libc._dyld_get_image_name
        _n.restype = c_char_p
        _n.argtypes = [c_int]
        for i in range(_libc._dyld_image_count()):
            n = _n(i)
            if n:
                yield _d(n)


def _dup(result, ctype):
    # duplicate a NULL- or nul-terminated array of pointers
    # or string of bytes, leaking the original temporarily
    for n, r in enumerate(result):
        if not r:
            dup = result[:n]  # [result[i] for i in range(n)]
            n  += 1
            break
    else:
        dup = _copy(result)
        n = len(result)
    # leak the original memory
    _free_memory(result, n * sizeof(ctype))
    return dup


if macOSver2() > (10, 15):  # Big Sur and later
    # macOS 11+ (aka 10.16) no longer provides direct loading of
    # system libraries, instead it installs the library after a
    # low-level dlopen(name) call with the library base name,
    # as a result, ctypes.util.find_library may not find any
    # library not previously dlopen'ed in Python 3.8-
    from ctypes import _dlopen

    def _find_lib(name):
        '''Mimick C{ctype.util.find_library}, returning the
           (fully-qualified) name of the library or throwing
           an C{OSlibError} if not found.
        '''
        ns = []
        for n in (_find_library(name), name,
                          _DOT_(name, 'dylib'),
                          _DOT_(name, _framework_), _join(
                          _DOT_(name, _framework_), name)):
            if n:
                try:
                    if _dlopen(n):  # handle OK
                        return n
                except (OSError, TypeError):
                    pass
                ns.append(n)
        raise OSlibError('find', name, *ns)

    _isAppleSi = __arm64__  # and _macOSver2() > (11, 0)
else:
    _isAppleSi =  False

    def _find_lib(name):  # PYCHOK redef
        '''As C{ctype.util.find_library}, but throwing
           an C{OSlibError} if not found.
        '''
        n = _find_library(name)
        if n:
            return n
        raise OSlibError('find', name)


def _free_memory(ptr, size):
    # leak freed memory, but only temporarily
    _leaked2.append((ptr, size))
    # free several, previously leaked memory, but
    # this segfaults or produces erratic results,
    # especially when memory is freed immediately
    if _libc_free and len(_leaked2) > 4:
        ptr, _ = _leaked2.pop(0)
        _libc_free(ptr)


def get_lib(name):
    '''Find and load a C{.dylib} library.

       @param name: The library base name (C{str}).

       @return: The library (C{ctypes.CDLL}).

       @raise OSlibError: No C{B{name}.dylib} library found.

       @note: Private attribute C{._name} shows the library path.
    '''
    try:
        lib = Libs[name]
    except KeyError:
        Libs[name] = lib = _load_lib(_find_lib(name))
    return lib


def get_lib_framework(name, services='ApplicationServices', version=_NN_):
    '''Load a C{Frameworks B{services} B{name}.framework} library.

       @param name: Library base name (C{str}).
       @keyword services: Services framework base name (C{str}).
       @keyword version: C{Framework/Versions/B{version}}, overriding
                         C{'Current'} (C{str}).

       @return: The library (C{ctypes.CDLL}).

       @raise OSlibError: No C{B{name}.framework} library found.

       @note: Private attribute C{._name} shows the library path.

       @example:
        - get_lib_framework('PrintCore')
        - get_lib_framework('Metadata', services='CoreServices')
    '''
    try:
        lib = Libs[name]
    except KeyError:
        n = _DOT_(name, _framework_)
        s = _DOT_(services, _framework_)
        v = _join('Versions', version, name) if version else name  # PYCHOK shadow
        p = _join(_SEP, 'System', 'Library', 'Frameworks', s,
                                             'Frameworks', n, v)
        Libs[name] = lib = _load_lib(p)
#       lib.framework = lib  # for Libs.PrintCore.framework
    return lib


def leaked2():
    '''Return the number of memory leaks.

       @return: 2-Tuple (I{number}, I{size}) with the I{number} of
                memory leaks and total I{size} leaked, in bytes.
    '''
    return len(_leaked2), sum(z for _, z in _leaked2)


def _listdup(result, *unused):  # func, args
    # copy the NULL-terminated list
    # and free the original memory
    return _dup(result, c_void_p) if result else []


def _load_lib(name):  # PYCHOK expected
    '''Load the named library.
    '''
    if name:
        try:
            lib = CDLL(name)  # == cdll.LoadLibrary(name)
            if lib._name:  # qualified name
                return lib
        except (AttributeError, OSError, TypeError):
            pass
        v = 'load'
    else:
        v = 'find'
    raise OSlibError(v, name)


def _strdup(result, *unused):  # func, args
    # copy the nul-terminated string
    # and free the original memory
    return _bNN_.join(_dup(result, c_byte)) if result else _bNN_


# get function free(void *ptr) from the C runtime
# (see <https://GitHub.com/oaubert/python-vlc>, the
# Python binding for VLC in folder generated/*/vlc.py)
_libc = get_lib('libc')  # NOT 'c'
if _libc:  # macOS, linux, etc.
    _libc_free = _libc.free
    _csignature(_libc_free, c_void, c_void_p)
#   _csignature_variadic(_libc.printf, c_int, c_char_p)  # printf(format, ...)
else:  # ignore free, leaking some memory
    _libc_free = None

# <https://Developer.Apple.com/documentation/corefoundation/
#          cfstringbuiltinencodings?language=objc>
kCFStringEncodingISOLatin1     = 0x0201
kCFStringEncodingMacRoman      = 0
kCFStringEncodingASCII         = 0x0600
kCFStringEncodingNonLossyASCII = 0x0BFF
kCFStringEncodingUnicode       = 0x0100
kCFStringEncodingUTF8          = 0x08000100  # shared with .nstypes.py
kCFStringEncodingUTF16         = 0x0100
kCFStringEncodingUTF16BE       = 0x10000100
kCFStringEncodingUTF16LE       = 0x14000100
kCFStringEncodingUTF32         = 0x0c000100
kCFStringEncodingUTF32BE       = 0x18000100
kCFStringEncodingUTF32LE       = 0x1c000100
kCFStringEncodingWindowsLatin1 = 0x0500

CFStringEncoding = kCFStringEncodingUTF8  # or -UTF16
CFStringEncoding_t = c_uint32  # a ctype


_libCF = get_lib('CoreFoundation')
if _libCF:
    # see also framework_constants_via_ctypes.py and -_pyobjc.py
    # <https://Gist.GitHub.com/pudquick/8f65bb9b306f91eafdcc> and
    # <https://Gist.GitHub.com/pudquick/ac8f22326f095ed2690e>
    kCFAllocatorDefault   = _dllattr(_libCF, kCFAllocatorDefault=Allocator_t)  # XXX or NULL
    kCFRunLoopDefaultMode = _dllattr(_libCF, kCFRunLoopDefaultMode=c_void_p)

    _csignature(_libCF.CFArrayAppendValue, Array_t, c_void_p)
    # <https://Developer.Apple.com/documentation/corefoundation/1388741-cfarraycreate>
    _csignature(_libCF.CFArrayCreate, Array_t, Allocator_t, c_void_p, CFIndex_t, c_void_p)
    # <https://Developer.Apple.com/library/content/documentation/CoreFoundation/
    #          Conceptual/CFStrings/Articles/ComparingAndSearching.html>
    _csignature(_libCF.CFArrayCreateMutable, Array_t, Allocator_t, CFIndex_t, c_void_p)
    _csignature(_libCF.CFArrayGetCount, CFIndex_t, Array_t)
    _csignature(_libCF.CFArrayGetTypeID, TypeID_t)
    _csignature(_libCF.CFArrayGetValueAtIndex, c_void_p, Array_t, CFIndex_t)

    _csignature(_libCF.CFAttributedStringCreate, c_void_p, Allocator_t, c_void_p, c_void_p)

    _csignature(_libCF.CFBooleanGetTypeID, TypeID_t)

    _csignature(_libCF.CFDataCreate, Data_t, Allocator_t, c_void_p, CFIndex_t)
    _csignature(_libCF.CFDataGetBytes, c_void, Data_t, CFRange_t, c_void_p)
    _csignature(_libCF.CFDataGetLength, CFIndex_t, Data_t)

    # <https://Developer.Apple.com/documentation/corefoundation/1542050-cfdategettypeid>
    # <https://Developer.Apple.com/documentation/foundation/nsdate>
    _csignature(_libCF.CFDateGetTypeID, TypeID_t)

    # <https://Developer.Apple.com/documentation/corefoundation/cfdictionary-rum>
    # <https://Developer.Apple.com/library/content/documentation/CoreFoundation/
    #          Conceptual/CFMemoryMgmt/Concepts/Ownership.html>
    # <https://Developer.Apple.com/documentation/corefoundation/1516777-cfdictionaryaddvalue>
    _csignature(_libCF.CFDictionaryAddValue, c_void, Dictionary_t, c_void_p, c_void_p)  # (d, key, val)
    _csignature(_libCF.CFDictionaryContainsKey, BOOL_t, Dictionary_t, c_void_p)
    _csignature(_libCF.CFDictionaryContainsValue, BOOL_t, Dictionary_t, c_void_p)
    _csignature(_libCF.CFDictionaryCreateMutable, c_void_p, Allocator_t, CFIndex_t, c_void_p, c_void_p)
    _csignature(_libCF.CFDictionaryGetCount, CFIndex_t, Dictionary_t)
    _csignature(_libCF.CFDictionaryGetCountOfKey, CFIndex_t, Dictionary_t, c_void_p)
    _csignature(_libCF.CFDictionaryGetCountOfValue, CFIndex_t, Dictionary_t, c_void_p)
    _csignature(_libCF.CFDictionaryGetKeysAndValues, c_void, Dictionary_t, c_void_p, c_void_p)
    _csignature(_libCF.CFDictionaryGetTypeID, TypeID_t)
    _csignature(_libCF.CFDictionaryGetValue, c_void_p, Dictionary_t, c_void_p)  # v = (d, key)
    # Returns a Boolean value that indicates whether a given value for a given key
    # is in a dictionary, and returns that value into the last arg if it exists
    _csignature(_libCF.CFDictionaryGetValueIfPresent, BOOL_t, Dictionary_t, c_void_p, c_void_p)  # b = (d, key, byref(val))
    _csignature(_libCF.CFDictionarySetValue, c_void, Dictionary_t, c_void_p, c_void_p)  # (d, key, val)
    # _csignature(_libCF.CFDictionarySetValueForKey, c_void, Dictionary_t, c_void_p, c_void_p)  # (d, key, val)

    _csignature(_libCF.CFGetTypeID, TypeID_t, c_void_p)

    _csignature(_libCF.CFNullGetTypeID, TypeID_t)

    _csignature(_libCF.CFNumberCreate, Number_t, Allocator_t, NumberType_t, c_void_p)
    _csignature(_libCF.CFNumberGetType, NumberType_t, Number_t)
    _csignature(_libCF.CFNumberGetTypeID, TypeID_t)
    _csignature(_libCF.CFNumberGetValue, BOOL_t, Number_t, NumberType_t, c_void_p)  # (n, TypeID, *n)

# <https://GitHub.com/opensource-apple/CF/blob/master/CFNumber.h>
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
                       kCFNumberCFIndexType:   CFIndex_t,
                       kCFNumberNSIntegerType: NSInteger_t,
                       kCFNumberCGFloatType:   CGFloat_t}


def cfNumber2bool(ns, dflt=None):
    '''Create a Python C{bool} from an C{NS/CFBoolNumber}, special case.

       @param ns: The C{NS/CFBoolNumber} (L{ObjCInstance}).
       @keyword dflt: Default for missing value (C{None}).

       @raise TypeError: Unexpected C{NumberType}.

       @return: The bool number (C{bool}) or C{B{dflt}}.
    '''
    nType = _libCF.CFNumberGetType(ns)
    if nType != kCFNumberCharType:
        raise _cfNumberError(ns, nType)
    n =  c_byte()  # c_ubyte, see octypes._encoding2ctype!
    r = _libCF.CFNumberGetValue(ns, nType, byref(n))
    return bool(n.value) if r else dflt


def _cfNumberError(ns, nType):  # helper for cfNumber2bool and cfNumber2num
    t = _fmt('%s(%r): %r', 'NumberType', ns, nType)
    return TypeError(_COMMASPACE_(t, 'unexpected'))


def cfNumber2num(ns, dflt=None):
    '''Create a Python C{int} or C{float} from an C{NS/CFNumber}.

       @param ns: The C{NS/CFNumber} (L{ObjCInstance}).
       @keyword dflt: Default for missing, unobtainable value (C{None}).

       @raise TypeError: Unexpected C{NumberType}.

       @return: The number (C{int} or C{float}) or I{dflt}.
    '''
    nType = _libCF.CFNumberGetType(ns)
    try:
        n = _CFNumberType2ctype[nType]()
    except (KeyError, TypeError):
        raise _cfNumberError(ns, nType)
    r = _libCF.CFNumberGetValue(ns, nType, byref(n))
    return n.value if r else dflt


def cfString2str(ns, dflt=None):  # XXX an NS*String method
    '''Create a Python C{str} or C{unicode} from an C{NS[Mutable]Str[ing]}.

       @param ns: The C{NS[Mutable]Str[ing]} (L{ObjCInstance}).

       @return: The string (C{str} or C{unicode}) or I{dflt}.
    '''
    n = _libCF.CFStringGetLength(ns)
    u = _libCF.CFStringGetMaximumSizeForEncoding(n, CFStringEncoding)
    b =  c_buffer(u + 2)
    r = _libCF.CFStringGetCString(ns, b, len(b), CFStringEncoding)
    # XXX if r: assert isinstance(b.value, _Bytes), 'bytes expected'
    # bytes to unicode in Python 2, to str in Python 3+
    return bytes2str(b.value) if r else dflt  # XXX was .decode(_UNICODEC)


def cfString(ustr):
    '''Create an ObjC C{NS[Constant]String} from a Python string.

       @param ustr: The string value (C{str} or C{unicode}).

       @return: The string instance (C{NS[Constant]String}).
    '''
    return _libCF.CFStringCreateWithCString(None, str2bytes(ustr),
                                                  CFStringEncoding)


if _libCF:
    _csignature(_libCF.CFRelease, c_void, TypeRef_t)
    _csignature(_libCF.CFRetain, TypeRef_t, TypeRef_t)

    _csignature(_libCF.CFRunLoopGetCurrent, c_void_p)
    _csignature(_libCF.CFRunLoopGetMain, c_void_p)

    _csignature(_libCF.CFSetContainsValue, BOOL_t, Set_t, c_void_p)
    _csignature(_libCF.CFSetGetCount, CFIndex_t, Set_t)
    _csignature(_libCF.CFSetGetCountOfValue, CFIndex_t, Set_t, c_void_p)
    _csignature(_libCF.CFSetGetValue, c_void_p, Set_t, c_void_p)
    # PyPy 1.7 is fine with the 2nd arg as POINTER(c_void_p),
    # but CPython ctypes 1.1.0 complains, so just use c_void_p.
    _csignature(_libCF.CFSetGetValues, c_void, Set_t, c_void_p)
    _csignature(_libCF.CFSetGetValueIfPresent, BOOL_t, Set_t, c_void_p, POINTER(c_void_p))

    _csignature(_libCF.CFStringCreateWithCString, String_t, Allocator_t, c_char_p, CFStringEncoding_t)
    _csignature(_libCF.CFStringGetCString, BOOL_t, String_t, c_char_p, CFIndex_t, CFStringEncoding_t)
    _csignature(_libCF.CFStringGetLength, CFIndex_t, String_t)
    _csignature(_libCF.CFStringGetMaximumSizeForEncoding, CFIndex_t, CFIndex_t, CFStringEncoding_t)
    _csignature(_libCF.CFStringGetTypeID, TypeID_t)

    # CFDataRef CFURLCreateBookmarkDataFromFile(CFAllocatorRef allocator, CFURLRef fileURL, CFErrorRef *errorRef)
    _csignature(_libCF.CFURLCreateBookmarkDataFromFile, Data_t, Allocator_t, URL_t, c_void_p)
    # <https://Developer.Apple.com/documentation/corefoundation/cfurlbookmarkresolutionoptions>
    kCFURLBookmarkResolutionWithoutMountingMask = 1 <<  9
    kCFURLBookmarkResolutionWithoutUIMask       = 1 <<  8
    kCFURLBookmarkResolutionWithSecurityScope   = 1 << 10
    # CFURLRef CFURLCreateByResolvingBookmarkData(CFAllocatorRef allocator, CFDataRef bookmark,
    #          CFURLBookmarkResolutionOptions options, CFURLRef relativeToURL,
    #          CFArrayRef resourcePropertiesToInclude, Boolean *isStale, CFErrorRef *error)
    _csignature(_libCF.CFURLCreateByResolvingBookmarkData, URL_t, Allocator_t, Data_t, c_uint, URL_t, c_void_p, BOOL_t, c_void_p)
    # <https://Developer.Apple.com/documentation/corefoundation/1542826-cfurlgetstring>
    _csignature(_libCF.CFURLGetString, String_t, URL_t)
    _csignature(_libCF.CFURLGetTypeID, TypeID_t)


# <https://GitHub.com/al45tair/mac_alias>
# <https://StackOverflow.com/questions/21150169>
# <https://MichaelLynn.GitHub.io/2015/10/24/apples-bookmarkdata-exposed>
def cfURLResolveAlias(alias):
    '''Resolve a macOS file alias.

       @param alias: The alias file (C{NSURL}).

       @return: The alias' target (C{NSURL}) or C{None}.
    '''
    kA =  kCFAllocatorDefault
    ns = _libCF.CFURLCreateBookmarkDataFromFile(kA, cast(alias, URL_t), 0) or None
    if ns:
        kM =  kCFURLBookmarkResolutionWithoutUIMask
        ns = _libCF.CFURLCreateByResolvingBookmarkData(kA, ns, kM, 0, 0, NO, 0)
    return ns


def cfURL2str(url):
    '''Create a Python C{str} from C{CFURL}.

       @param url: The C{CFURL} instance.

       @return: The I{url} as string (C{str}).
    '''
    return cfString2str(_libCF.CFURLGetString(url))


# Even though we don't use this directly, it must be loaded
# to find the NSApplication, NSWindow, and NSView classes.
_libAppKit = get_lib('AppKit')
if _libAppKit:
    NSApplicationDidHideNotification   = _dllattr(_libAppKit, NSApplicationDidHideNotification=c_void_p)
    NSApplicationDidUnhideNotification = _dllattr(_libAppKit, NSApplicationDidUnhideNotification=c_void_p)

    # see NSApplication.nextEventMatchingMask:untilDate:inMode:dequeue:
    NSDefaultRunLoopMode       = _dllattr(_libAppKit, NSDefaultRunLoopMode=RunLoop_t)
    NSEventTrackingRunLoopMode = _dllattr(_libAppKit, NSEventTrackingRunLoopMode=RunLoop_t)
    NSModalPanelRunLoopMode    = _dllattr(_libAppKit, NSModalPanelRunLoopMode=RunLoop_t)
    # UITrackingRunLoopMode    = _dllattr(_libAppKit, UITrackingRunLoopMode=RunLoop_t)

    # <https://Developer.Apple.com/documentation/appkit/1473652-nsrectfill>
    _csignature(_libAppKit.NSRectFill, c_void, POINTER(NSRect_t))

# NSApplication.h
NSApplicationPresentationDefault                 = 0
NSApplicationPresentationHideDock                = 1 << 1
NSApplicationPresentationHideMenuBar             = 1 << 3
NSApplicationPresentationDisableProcessSwitching = 1 << 5
NSApplicationPresentationDisableHideApplication  = 1 << 8

# NSRunningApplication.h
NSApplicationActivationPolicyRegular    = 0
NSApplicationActivationPolicyAccessory  = 1
NSApplicationActivationPolicyProhibited = 2

# <https://GitHub.com/gnustep/libs-gui/blob/master/Headers/AppKit/NSPanel.h>
# <https://GitHub.com/gnustep/libs-gui/blob/master/Headers/AppKit/NSSavePanel.h>
NSFileHandlingPanelCancelButton = NSCancelButton = 0
NSFileHandlingPanelOKButton     = NSOKButton     = 1
# original enum, assumed values from here down
# NSFileHandlingPanelImageButton     = 2
# NSFileHandlingPanelTitleField      = 3
# NSFileHandlingPanelBrowser         = 4
# NSFileHandlingPanelForm            = 5
# NSFileHandlingPanelHomeButton      = 6
# NSFileHandlingPanelDiskButton      = 7
# NSFileHandlingPanelDiskEjectButton = 8

# <https://GitHub.com/gnustep/libs-gui/blob/master/Headers/AppKit/NSEvent.h
# <https://Developer.Apple.com/documentation/appkit/nsevent/1535851-function-key_unicodes>
NSAlphaShiftKeyMask =  1 << 16
NSShiftKeyMask      =  1 << 17
NSControlKeyMask    =  1 << 18
NSAlternateKeyMask  =  1 << 19
NSCommandKeyMask    =  1 << 20
NSNumericPadKeyMask =  1 << 21
NSHelpKeyMask       =  1 << 22
NSFunctionKeyMask   =  1 << 23
NSAnyEventMask      = (1 << 32) - 1  # NSUIntegerMax

NSKeyDown            = 10
NSKeyUp              = 11
NSFlagsChanged       = 12
NSApplicationDefined = 15

NSUpArrowFunctionKey    = 0xF700  # 0x7E
NSDownArrowFunctionKey  = 0xF701  # 0x7D
NSLeftArrowFunctionKey  = 0xF702  # 0x7B
NSRightArrowFunctionKey = 0XF703  # 0x7C
NSF1FunctionKey         = 0xF704  # 0x7A
# etc. for NSF2..NSF19
NSF19FunctionKey        = 0xF716  # 0x50
# NSInsertFunctionKey   = 0xF727  # not on macs
NSDeleteFunctionKey     = 0xF728  # 0x75 forward delete [x>
NSHomeFunctionKey       = 0xF729  # 0x73
# NSBeginFunctionKey    = 0xF72A  # not on macs
NSEndFunctionKey        = 0xF72B  # 0x77
NSPageUpFunctionKey     = 0xF72C  # 0x74
NSPageDownFunctionKey   = 0xF72D  # 0x79
NSClearLineFunctionKey  = 0xF739  # 0x47 clear/num lock
NSHelpFunctionKey       = 0xF746

# <https://Developer.Apple.com/documentation/appkit/
#          nstext/1540619-common_unicode_characters>
# plus all ASCII ctrl+Alpha characters
NSNullCharacter                = 0x0000  # NUL Ctrl+@
NSStartOfHeadingCharacter      = 0x0001  # SOH Ctrl+A
NSStartOfTextCharacter         = 0x0002  # STX Ctrl+B
NSEnterCharacter               = 0x0003  # ETX
NSEndOfTextCharacter           = 0x0003  # ETX Ctrl+C
NSEndOfTransmitCharacter       = 0x0004  # EOT Ctrl+D
NSEnquiryCharacter             = 0x0005  # ENQ Ctrl+E
NSAcknowledgeCharacter         = 0x0006  # ACK Ctrl+F
NSBellCharacter                = 0x0007  # BEL Ctrl+G
NSBackSpaceCharacter           = 0x0008  # BS  Ctrl+H
NSTabCharacter                 = 0x0009  # HT  Ctrl+I
NSHorizontalTabCharacter       = 0x0009  # HT  Ctrl+I
NSNewLineCharacter             = 0x000A  # NL  Ctrl+J
NSLineFeedCharacter            = 0x000A  # LF  Ctrl+J
NSVerticalTabCharacter         = 0x000B  # VT  Ctrl+K
NSFormFeedCharacter            = 0x000C  # FF  Ctrl+L
NSCarriageReturnCharacter      = 0x000D  # CR  Ctrl+M
NSShiftOutCharacter            = 0x000E  # SO  Ctrl+N
NSShiftInCharacter             = 0x000F  # SI  Ctrl+O
NSDataLineEscapeCharacter      = 0x0010  # DLE Ctrl+P
NSDeviceControl1Character      = 0x0011  # DC1 Ctrl+Q XON
NSDeviceControl2Character      = 0x0012  # DC2 Ctrl+R
NSDeviceControl3Character      = 0x0013  # DC3 Ctrl+S XOFF
NSDeviceControl4Character      = 0x0014  # DC4 Ctrl+T
NSNegativeAcknowledgeCharacter = 0x0015  # NAK Ctrl+U
NSSynchronousIdleCharacter     = 0x0016  # SYN Ctrl+V
NSEndOfTransmitBlockCharacter  = 0x0017  # ETB Ctrl+W
NSCancelCharacter              = 0x0018  # CAN Ctrl+X
NSBackTabCharacter             = 0x0019  # BT  Ctrl+Y
NSEndOfMediumCharacter         = 0x0019  # EM  Ctrl+Y
NSSubstituteCharacter          = 0x001A  # SUB Ctrl+Z
NSEscapeCharacter              = 0x001B  # ESC Ctrl+[
NSFileSeparatorCharacter       = 0x001C  # FS  Ctrl+\
NSGroupSeparatorCharacter      = 0x001D  # GS  Ctrl+]
NSRecordSeparatorCharacter     = 0x001E  # RS  Ctrl+^
NSUnitSeparatorCharacter       = 0x001F  # US  Ctrl+_
NSSpaceCharacter               = 0x0020  # SP
NSLineSeparatorCharacter       = 0x2028
NSParagraphSeparatorCharacter  = 0x2029
NSDeleteCharacter              = 0x007F  # 0x75?

# <https://Developer.Apple.com/documentation/appkit/nsbackingstoretype>
NSBackingStoreRetained    = 0  # deprecated
NSBackingStoreNonretained = 1  # deprecated
NSBackingStoreBuffered    = 2

# <https://GitHub.com/gnustep/libs-gui/blob/master/Headers/AppKit/NSTableView.h>
NSTableViewGridNone                     = 0
NSTableViewSolidVerticalGridLineMask    = 1 << 0
NSTableViewSolidHorizontalGridLineMask  = 1 << 1
NSTableViewDashedHorizontalGridLineMask = 1 << 3
# NSTableViewVerticalGridLineMask?

# <https://GitHub.com/gnustep/libs-gui/blob/master/Headers/AppKit/NSText.h>
NSTextAlignmentLeft       = NSLeftTextAlignment      = 0  # == CTTextAlignment.left
if _isAppleSi:  # XXX fswap NSTextAlignmentRight and -Center
    NSTextAlignmentRight  = NSRightTextAlignment     = 2
    NSTextAlignmentCenter = NSCenterTextAlignment    = 1
else:
    NSTextAlignmentRight  = NSRightTextAlignment     = 1  # == CTTextAlignment.right
    NSTextAlignmentCenter = NSCenterTextAlignment    = 2  # == CTTextAlignment.center
NSTextAlignmentJustified  = NSJustifiedTextAlignment = 3  # == CTTextAlignment.justified
NSTextAlignmentNatural    = NSNaturalTextAlignment   = 4  # == CTTextAlignment.natural

NSTextWritingDirectionEmbedding = 0
NSTextWritingDirectionOverride  = 2  # 1 << 1

# /System/Library/Frameworks/AppKit.framework/Headers/NSTrackingArea.h
NSTrackingMouseEnteredAndExited = 0x01
NSTrackingMouseMoved            = 0x02
NSTrackingCursorUpdate          = 0x04
NSTrackingActiveInActiveApp     = 0x40

# /System/Library/Frameworks/AppKit.framework/Headers/NSOpenGL.h
# NSOpenGLPFAAllRenderers          =   1  # choose from all available renderers
# NSOpenGLPFADoubleBuffer          =   5  # choose a double buffered pixel format
# NSOpenGLPFAStereo                =   6  # stereo buffering supported
# NSOpenGLPFAAuxBuffers            =   7  # number of aux buffers
# NSOpenGLPFAColorSize             =   8  # number of color buffer bits
# NSOpenGLPFAAlphaSize             =  11  # number of alpha component bits
# NSOpenGLPFADepthSize             =  12  # number of depth buffer bits
# NSOpenGLPFAStencilSize           =  13  # number of stencil buffer bits
# NSOpenGLPFAAccumSize             =  14  # number of accum buffer bits
# NSOpenGLPFAMinimumPolicy         =  51  # never choose smaller buffers than requested
# NSOpenGLPFAMaximumPolicy         =  52  # choose largest buffers of type requested
# NSOpenGLPFAOffScreen             =  53  # choose an off-screen capable renderer
# NSOpenGLPFAFullScreen            =  54  # choose a full-screen capable renderer
# NSOpenGLPFASampleBuffers         =  55  # number of multi sample buffers
# NSOpenGLPFASamples               =  56  # number of samples per multi sample buffer
# NSOpenGLPFAAuxDepthStencil       =  57  # each aux buffer has its own depth stencil
# NSOpenGLPFAColorFloat            =  58  # color buffers store floating point pixels
# NSOpenGLPFAMultisample           =  59  # choose multisampling
# NSOpenGLPFASupersample           =  60  # choose supersampling
# NSOpenGLPFASampleAlpha           =  61  # request alpha filtering
# NSOpenGLPFARendererID            =  70  # request renderer by ID
# NSOpenGLPFASingleRenderer        =  71  # choose a single renderer for all screens
# NSOpenGLPFANoRecovery            =  72  # disable all failure recovery systems
# NSOpenGLPFAAccelerated           =  73  # choose a hardware accelerated renderer
# NSOpenGLPFAClosestPolicy         =  74  # choose the closest color buffer to request
# NSOpenGLPFARobust                =  75  # renderer does not need failure recovery
# NSOpenGLPFABackingStore          =  76  # back buffer contents are valid after swap
# NSOpenGLPFAMPSafe                =  78  # renderer is multi-processor safe
# NSOpenGLPFAWindow                =  80  # can be used to render to an onscreen window
# NSOpenGLPFAMultiScreen           =  81  # single window can span multiple screens
# NSOpenGLPFACompliant             =  83  # renderer is opengl compliant
# NSOpenGLPFAScreenMask            =  84  # bit mask of supported physical screens
# NSOpenGLPFAPixelBuffer           =  90  # can be used to render to a pbuffer
# NSOpenGLPFARemotePixelBuffer     =  91  # can be used to render offline to a pbuffer
# NSOpenGLPFAAllowOfflineRenderers =  96  # allow use of offline renderers
# NSOpenGLPFAAcceleratedCompute    =  97  # choose a hardware accelerated compute device
# NSOpenGLPFAOpenGLProfile         =  99  # specify an OpenGL Profile to use
# NSOpenGLPFAVirtualScreenCount    = 128  # number of virtual screens in this format
#
# NSOpenGLCPSwapInterval           = 222

# NSOpenGLProfileVersionLegacy     = 0x1000  # choose a Legacy/Pre-OpenGL 3.0 Implementation
# NSOpenGLProfileVersion3_2Core    = 0x3200  # choose an OpenGL 3.2 Core Implementation
# NSOpenGLProfileVersion4_1Core    = 0x4100  # choose an OpenGL 4.1 Core Implementation

# <https://StackOverflow.com/questions/24024723/swift-using-
#  nsstatusbar-statusitemwithlength-and-nsvariablestatusitemlength>
NSSquareStatusItemLength   = -2
NSVariableStatusItemLength = -1

# /System/Library/Frameworks/AppKit.framework/Headers/NSWindow.h
# <https://Developer.Apple.com/documentation/appkit/nswindowstylemask>
# <https://Developer.Apple.com/documentation/appkit/constants>
# note, Deprecated -Mask's are marked with D? or commented out
# note, Previously, NSWindowStyleMaskXyz was named NSXyzWindowMask
# NSWindowStyleMaskBorderless             = 0  # D?
NSWindowStyleMaskTitled                   = 1 << 0  # D?
NSWindowStyleMaskClosable                 = 1 << 1
NSWindowStyleMaskMiniaturizable           = 1 << 2
NSWindowStyleMaskResizable                = 1 << 3
# /System/Library/Frameworks/AppKit.framework/Headers/NSPanel.h
NSWindowStyleMaskUtilityWindow            = 1 << 4  # D?
# <https://GitHub.com/gnustep/libs-gui/blob/master/Headers/AppKit/NSWindow.h>
# NSWindowStyleMaskDocModalWindow         = 1 << 6  # D?
# NSWindowStyleMaskNonactivatingPanel     = 1 << 7  # D?
# NSWindowStyleMaskTexturedBackground     = 1 << 8  # D?
# NSWindowStyleMaskUnscaled?              = 1 << 11  # D?
# NSWindowStyleMaskUnifiedTitleAndToolbar = 1 << 12  # D?
# NSWindowStyleMaskHUDWindow              = 1 << 13  # D?
# NSWindowStyleMaskFullScreen             = 1 << 14  # D?
# NSWindowStyleMaskFullSizeContentView    = 1 << 15  # D?

# the typical WindowStyleMask for NS-/Window
NSWindowStyleMaskUsual = NSWindowStyleMaskClosable  | NSWindowStyleMaskMiniaturizable \
                       | NSWindowStyleMaskResizable | NSWindowStyleMaskTitled

# <https://GitHub.com/gnustep/libs-gui/blob/master/Headers/AppKit/NSWindow.h>
NSWindowCloseButton        = 0
NSWindowMiniaturizeButton  = 1
NSWindowZoomButton         = 2
NSWindowToolbarButton      = 3
NSWindowDocumentIconButton = 4
# typedef NSUInteger NSWindowButton

_libCG = get_lib('CoreGraphics')  # aka Quartz
if _libCG:
    # /System/Library/Frameworks/ApplicationServices.framework/Frameworks/...
    #  CoreGraphics.framework/Headers/CGImage.h
    kCGImageAlphaNone               = 0
    kCGImageAlphaPremultipliedLast  = 1
    kCGImageAlphaPremultipliedFirst = 2
    kCGImageAlphaLast               = 3
    kCGImageAlphaFirst              = 4
    kCGImageAlphaNoneSkipLast       = 5
    kCGImageAlphaNoneSkipFirst      = 6
    kCGImageAlphaOnly               = 7

    kCGImageAlphaPremultipliedLast = 1

    kCGBitmapAlphaInfoMask     = 0x1F
    kCGBitmapFloatComponents   = 1 << 8

    kCGBitmapByteOrderDefault  = 0 << 12
    kCGBitmapByteOrder16Little = 1 << 12
    kCGBitmapByteOrder32Little = 2 << 12
    kCGBitmapByteOrder16Big    = 3 << 12
    kCGBitmapByteOrder32Big    = 4 << 12
    kCGBitmapByteOrderMask     = 7 << 12

    # /System/Library/Frameworks/ApplicationServices.framework/Frameworks/...
    #  ImageIO.framework/Headers/CGImageProperties.h
    try:  # missing in 12.0.1 macOS Monterey
        kCGImagePropertyGIFDictionary = _dllattr(_libCG, kCGImagePropertyGIFDictionary=c_void_p)
        kCGImagePropertyGIFDelayTime  = _dllattr(_libCG, kCGImagePropertyGIFDelayTime=c_void_p)
    except ValueError:
        pass
    # /System/Library/Frameworks/ApplicationServices.framework/Frameworks/...
    #  CoreGraphics.framework/Headers/CGColorSpace.h
    kCGRenderingIntentDefault = 0

    _csignature(_libCG.CGAssociateMouseAndMouseCursorPosition, CGError_t, BOOL_t)
    _csignature(_libCG.CGBitmapContextCreate, c_void_p, c_void_p, c_size_t, c_size_t, c_size_t, c_size_t, c_void_p, CGBitmapInfo_t)
    _csignature(_libCG.CGBitmapContextCreateImage, c_void_p, c_void_p)
    _csignature(_libCG.CGColorSpaceCreateDeviceRGB, c_void_p)
    _csignature(_libCG.CGColorSpaceRelease, c_void, c_void_p)
    _csignature(_libCG.CGContextDrawImage, c_void, c_void_p, CGRect_t, c_void_p)
    _csignature(_libCG.CGContextRelease, c_void, c_void_p)
    _csignature(_libCG.CGContextSetShouldAntialias, c_void,c_void_p, BOOL_t)
    _csignature(_libCG.CGContextSetTextPosition, c_void, c_void_p, CGFloat_t, CGFloat_t)
    _csignature(_libCG.CGCursorIsVisible, BOOL_t)
    _csignature(_libCG.CGDataProviderCopyData, c_void_p, c_void_p)
    _csignature(_libCG.CGDataProviderCreateWithCFData, c_void_p, c_void_p)
    _csignature(_libCG.CGDataProviderRelease, c_void, c_void_p)
    _csignature(_libCG.CGDisplayBounds, CGRect_t, CGDirectDisplayID_t)
    _csignature(_libCG.CGDisplayCapture, CGError_t, CGDirectDisplayID_t)
    _csignature(_libCG.CGDisplayCopyAllDisplayModes, c_void_p, CGDirectDisplayID_t, c_void_p)
    _csignature(_libCG.CGDisplayCopyDisplayMode, c_void_p, CGDirectDisplayID_t)
    _csignature(_libCG.CGDisplayIDToOpenGLDisplayMask, c_uint32, c_uint32)
    _csignature(_libCG.CGDisplayIsBuiltin, BOOL_t, CGDirectDisplayID_t)  # screenID, NSScreenNumber
    _csignature(_libCG.CGDisplayModeCopyPixelEncoding, c_void_p, c_void_p)
    _csignature(_libCG.CGDisplayModeGetHeight, c_size_t, c_void_p)
    _csignature(_libCG.CGDisplayModeGetRefreshRate, c_double, c_void_p)
    _csignature(_libCG.CGDisplayModeGetWidth, c_size_t, c_void_p)
    _csignature(_libCG.CGDisplayModeRelease, c_void, c_void_p)
    _csignature(_libCG.CGDisplayModeRetain, c_void_p, c_void_p)
    _csignature(_libCG.CGDisplayMoveCursorToPoint, CGError_t, CGDirectDisplayID_t, CGPoint_t)
    _csignature(_libCG.CGDisplayRelease, CGError_t, CGDirectDisplayID_t)
    _csignature(_libCG.CGDisplaySetDisplayMode, CGError_t, CGDirectDisplayID_t, c_void_p, c_void_p)
    _csignature(_libCG.CGFontCreateWithDataProvider, c_void_p, c_void_p)
    _csignature(_libCG.CGFontCreateWithFontName, c_void_p, c_void_p)
    _csignature(_libCG.CGGetActiveDisplayList, CGError_t, c_uint32, POINTER(CGDirectDisplayID_t), POINTER(c_uint32))
    _csignature(_libCG.CGGetOnlineDisplayList, CGError_t, c_uint32, POINTER(CGDirectDisplayID_t), POINTER(c_uint32))
    _csignature(_libCG.CGImageCreate, c_void_p, c_size_t, c_size_t, c_size_t, c_size_t, c_size_t, c_void_p, c_uint32, c_void_p, c_void_p, BOOL_t, c_int)
    _csignature(_libCG.CGImageGetBitmapInfo, CGBitmapInfo_t, c_void_p)
    _csignature(_libCG.CGImageGetBitsPerPixel, c_size_t, c_void_p)
    _csignature(_libCG.CGImageGetBytesPerRow, c_size_t, c_void_p)
    _csignature(_libCG.CGImageGetDataProvider, c_void_p, c_void_p)
    _csignature(_libCG.CGImageGetHeight, c_size_t, c_void_p)
    _csignature(_libCG.CGImageGetWidth, c_size_t, c_void_p)
    _csignature(_libCG.CGImageRelease, c_void, c_void_p)
    try:  # missing in 12.0.1 macOS Monterey
        _csignature(_libCG.CGImageSourceCopyPropertiesAtIndex, c_void_p, c_void_p, c_size_t, c_void_p)
        _csignature(_libCG.CGImageSourceCreateImageAtIndex, c_void_p, c_void_p, c_size_t, c_void_p)
        _csignature(_libCG.CGImageSourceCreateWithData, c_void_p, c_void_p, c_void_p)
    except AttributeError:
        pass
    _csignature(_libCG.CGMainDisplayID, CGDirectDisplayID_t)
    _csignature(_libCG.CGShieldingWindowLevel, c_int32)
    _csignature(_libCG.CGWarpMouseCursorPosition, CGError_t, CGPoint_t)

_libCT = get_lib('CoreText')
if _libCT:
    # CoreText constants
    kCTFontAttributeName       = _dllattr(_libCT, kCTFontAttributeName=c_void_p)
    kCTFontFamilyNameAttribute = _dllattr(_libCT, kCTFontFamilyNameAttribute=c_void_p)
    kCTFontTraitsAttribute     = _dllattr(_libCT, kCTFontTraitsAttribute=c_void_p)

    kCTFontSlantTrait          = _dllattr(_libCT, kCTFontSlantTrait=c_void_p)  # traits dict key -> -1.0..+1.0
    kCTFontSymbolicTrait       = _dllattr(_libCT, kCTFontSymbolicTrait=c_void_p)  # traits dict key -> 0
    kCTFontWeightTrait         = _dllattr(_libCT, kCTFontWeightTrait=c_void_p)  # traits dict key -> -1.0..+1.0
    kCTFontWidthTrait          = _dllattr(_libCT, kCTFontWidthTrait=c_void_p)  # traits dict key -> -1.0..+1.0

    _csignature(_libCT.CTFontCreateWithGraphicsFont, c_void_p, c_void_p, CGFloat_t, c_void_p, c_void_p)
    _csignature(_libCT.CTFontCopyFamilyName, c_void_p, c_void_p)
    _csignature(_libCT.CTFontCopyFullName, c_void_p, c_void_p)
    _csignature(_libCT.CTLineCreateWithAttributedString, c_void_p, c_void_p)
    _csignature(_libCT.CTFontCreateWithFontDescriptor, c_void_p, c_void_p, CGFloat_t, c_void_p)
    _csignature(_libCT.CTFontDescriptorCreateWithAttributes, c_void_p, c_void_p)
    _csignature(_libCT.CTFontGetBoundingRectsForGlyphs, CGRect_t, c_void_p, CTFontOrientation_t, POINTER(CGGlyph_t), POINTER(CGRect_t), CFIndex_t)
    _csignature(_libCT.CTFontGetAdvancesForGlyphs, c_double, c_void_p, CTFontOrientation_t, POINTER(CGGlyph_t), POINTER(CGSize_t), CFIndex_t)
    _csignature(_libCT.CTFontGetAscent, CGFloat_t, c_void_p)
    _csignature(_libCT.CTFontGetDescent, CGFloat_t, c_void_p)
    _csignature(_libCT.CTFontGetGlyphsForCharacters, BOOL_t, c_void_p, POINTER(UniChar_t), POINTER(CGGlyph_t), CFIndex_t)
    _csignature(_libCT.CTFontGetSymbolicTraits, CTFontSymbolicTraits_t, c_void_p)
    _csignature(_libCT.CTLineDraw, c_void, c_void_p, c_void_p)

# constants from CTFontTraits.h
kCTFontClassMaskShift = 28

# CTFontSymbolicTraits symbolically describes stylistic aspects of a font.
# The top 4 bits is used to describe appearance of the font while the lower
# 28 bits for typeface.  The font appearance information represented by the
# upper 4 bits can be used for stylistic font matching.
# <https://Developer.Apple.com/documentation/appkit/nsfontmanager/font_traits>
# <https://Developer.Apple.com/documentation/appkit/nsfonttraitmask>
# <https://GitHub.com/tijme/reverse-engineering/blob/master/Billy%20Ellis%20ARM%20Explotation/
#  iPhoneOS9.3.sdk/System/Library/Frameworks/CoreText.framework/Headers/CTFontTraits.h>
NSFontItalicMask      = kCTFontTraitItalic      = 1 << 0
NSFontBoldMask        = kCTFontTraitBold        = 1 << 1
NSFontUnboldMask                                = 1 << 2   # 0x00000004
NSFontNonStandardCharacterSetMask               = 1 << 3   # 0x00000008
NSFontNarrowMask                                = 1 << 4   # 0x00000010
NSFontExpandedMask    = kCTFontTraitExpanded    = 1 << 5   # Expanded and Condensed traits are mutually exclusive
NSFontCondensedMask   = kCTFontTraitCondensed   = 1 << 6   # Additional detail available via kCTFontWidthTrait
NSFontSmallCapsMask                             = 1 << 7   # 0x00000080
NSFontPosterMask                                = 1 << 8   # 0x00000100
NSFontCompressedMask                            = 1 << 9   # 0x00000200
NSFontMonoSpaceMask   = kCTFontTraitMonoSpace   = 1 << 10  # Use fixed-pitch glyphs if available
NSFontVerticalMask    = kCTFontTraitVertical    = 1 << 11  # Use vertical glyph variants and metrics
NSFontUIOptimizedMask = kCTFontTraitUIOptimized = 1 << 12  # Synthesize appropriate attributes for UI rendering such as control titles if necessary
NSFontColorGlyphsMask = kCTFontTraitColorGlyphs = 1 << 13  # Color bitmap glyphs are available
NSFontCompositeMask   = kCTFontTraitComposite   = 1 << 14  # The font is a CFR (Composite font reference)
NSFontUnitalicMask                              = 1 << 24  # 0x01000000

# CTFontStylisticClass classifies certain stylistic qualities of the
# font.  These values correspond closely to the font class values in
# the OpenType 'OS/2' table.  The class values are bundled in the upper
# 4 bits of the CTFontSymbolicTraits and can be obtained via the
# kCTFontClassMaskTrait.
# <https://Developer.Apple.com/documentation/appkit/nsfontfamilyclass>
kCTFontClassUnknown            = NSFontUnknownClass            =  0 << kCTFontClassMaskShift
kCTFontClassOldStyleSerifs     = NSFontOldStyleSerifsClass     =  1 << kCTFontClassMaskShift
kCTFontClassTransitionalSerifs = NSFontTransitionalSerifsClass =  2 << kCTFontClassMaskShift
kCTFontClassModernSerifs       = NSFontModernSerifsClass       =  3 << kCTFontClassMaskShift
kCTFontClassClarendonSerifs    = NSFontClarendonSerifsClass    =  4 << kCTFontClassMaskShift
kCTFontClassSlabSerifs         = NSFontSlabSerifsClass         =  5 << kCTFontClassMaskShift
kCTFontClassFreeformSerifs     = NSFontFreeformSerifsClass     =  7 << kCTFontClassMaskShift
kCTFontClassSansSerif          = NSFontSansSerifClass          =  8 << kCTFontClassMaskShift
kCTFontClassOrnamentals        = NSFontOrnamentalsClass        =  9 << kCTFontClassMaskShift
kCTFontClassScripts            = NSFontScriptsClass            = 10 << kCTFontClassMaskShift
kCTFontClassSymbolic           = NSFontSymbolicClass           = 12 << kCTFontClassMaskShift
kCTFontClassMaskTrait          = NSFontClassMask               = 15 << kCTFontClassMaskShift

_libFoundation = get_lib('Foundation')
if _libFoundation:
    _csignature_variadic(_libFoundation.NSLog, c_void, c_char_p)  # ... like printf(format, ...)
    _csignature(_libFoundation.NSMouseInRect, BOOL_t, CGPoint_t, CGRect_t, BOOL_t)  # CORETEXT  flipped=NO


_libObjC = get_lib('libobjc')
if _libObjC:
    # BOOL class_addIvar(Class_t cls, const char *name, size_t size, uint8_t alignment, const char *types)
    _csignature(_libObjC.class_addIvar, BOOL_t, Class_t, c_char_p, c_size_t, c_uint8, c_char_p)
    # BOOL class_addMethod(Class_t cls, SEL_t name, IMP_t imp, const char *types)
    _csignature(_libObjC.class_addMethod, BOOL_t, Class_t, SEL_t, IMP_t, c_char_p)
    # BOOL class_addProtocol(Class_t cls, Protocol_t *protocol)
    _csignature(_libObjC.class_addProtocol, BOOL_t, Class_t, Protocol_t)
    # BOOL class_conformsToProtocol(Class_t cls, Protocol_t *protocol)
    _csignature(_libObjC.class_conformsToProtocol, BOOL_t, Class_t, Protocol_t)
    # Ivar_t *class_copyIvarList(Class_t cls, unsigned int *outCount)
    # Returns an array of pointers of type Ivar_t describing instance variables.
    # The array has *outCount pointers, NULL terminated.  You must free() the returned array!
    _csignature_list(_libObjC.class_copyIvarList, POINTER(Ivar_t), Class_t, POINTER(c_uint))
    # Method_t *class_copyMethodList(Class_t cls, unsigned int *outCount)
    # Returns an array of pointers of type Method_t describing instance methods.
    # The array has *outCount pointers, NULL terminated.  You must free() the returned array!
    _csignature_list(_libObjC.class_copyMethodList, POINTER(Method_t), Class_t, POINTER(c_uint))
    # objc_property_t *class_copyPropertyList(Class_t cls, unsigned int *outCount)
    # Returns an array of pointers of type objc_property_t describing properties.
    # The array has *outCount pointers, NULL terminated.  You must free() the returned array!
    _csignature_list(_libObjC.class_copyPropertyList, POINTER(objc_property_t), Class_t, POINTER(c_uint))
    # Protocol_t **class_copyProtocolList(Class_t cls, unsigned int *outCount)
    # Returns an array of pointers of type Protocol_t* describing protocols.
    # The array has *outCount pointers, NULL terminated.  You must free() the returned array!
    _csignature_list(_libObjC.class_copyProtocolList, POINTER(Protocol_t), Class_t, POINTER(c_uint))
    # Id_t class_createInstance(Class_t cls, size_t extraBytes)
    _csignature(_libObjC.class_createInstance, Id_t, Class_t, c_size_t)
    # Method_t class_getClassMethod(Class_t aClass, SEL_t aSelector)
    # Will also search superclass for implementations.
    _csignature(_libObjC.class_getClassMethod, Method_t, Class_t, SEL_t)
    # Ivar_t class_getClassVariable(Class_t cls, const char* name)
    _csignature(_libObjC.class_getClassVariable, Ivar_t, Class_t, c_char_p)
    # Method_t class_getInstanceMethod(Class_t aClass, SEL_t aSelector)
    # Will also search superclass for implementations.
    _csignature(_libObjC.class_getInstanceMethod, Method_t, Class_t, SEL_t)
    # size_t class_getInstanceSize(Class_t cls)
    _csignature(_libObjC.class_getInstanceSize, c_size_t, Class_t)
    # Ivar_t class_getInstanceVariable(Class_t cls, const char* name)
    _csignature(_libObjC.class_getInstanceVariable, Ivar_t, Class_t, c_char_p)
    # const char *class_getIvarLayout(Class_t cls)
    _csignature(_libObjC.class_getIvarLayout, c_char_p, Class_t)
    # IMP_t class_getMethodImplementation(Class_t cls, SEL_t name)
    _csignature(_libObjC.class_getMethodImplementation, IMP_t, Class_t, SEL_t)
    # IMP_t class_getMethodImplementation_stret(Class_t cls, SEL_t name)
    # M1 _csignature(_libObjC.class_getMethodImplementation_stret, IMP_t, Class_t, SEL_t)
    # const char *class_getName(Class_t cls)
    _csignature(_libObjC.class_getName, c_char_p, Class_t)
    # objc_property_t class_getProperty(Class_t cls, const char *name)
    _csignature(_libObjC.class_getProperty, objc_property_t, Class_t, c_char_p)
    # Class_t class_getSuperclass(Class_t cls)
    _csignature(_libObjC.class_getSuperclass, Class_t, Class_t)
    # int class_getVersion(Class_t theClass)
    _csignature(_libObjC.class_getVersion, c_int, Class_t)
    # const char *class_getWeakIvarLayout(Class_t cls)
    _csignature(_libObjC.class_getWeakIvarLayout, c_char_p, Class_t)
    # BOOL class_isMetaClass(Class_t cls)
    _csignature(_libObjC.class_isMetaClass, BOOL_t, Class_t)
    # IMP_t class_replaceMethod(Class_t cls, SEL_t name, IMP_t imp, const char *types)
    _csignature(_libObjC.class_replaceMethod, IMP_t, Class_t, SEL_t, IMP_t, c_char_p)
    # BOOL class_respondsToSelector(Class_t cls, SEL_t sel)
    _csignature(_libObjC.class_respondsToSelector, BOOL_t, Class_t, SEL_t)
    # void class_setIvarLayout(Class_t cls, const char *layout)
    _csignature(_libObjC.class_setIvarLayout, c_void, Class_t, c_char_p)
    # Class_t class_setSuperclass(Class_t cls, Class_t newSuper)
    _csignature(_libObjC.class_setSuperclass, Class_t, Class_t, Class_t)
    # void class_setVersion(Class_t theClass, int version)
    _csignature(_libObjC.class_setVersion, c_void, Class_t, c_int)
    # void class_setWeakIvarLayout(Class_t cls, const char *layout)
    _csignature(_libObjC.class_setWeakIvarLayout, c_void, Class_t, c_char_p)

    # const char *ivar_getName(Ivar_t ivar)
    _csignature(_libObjC.ivar_getName, c_char_p, Ivar_t)
    # ptrdiff_t ivar_getOffset(Ivar_t ivar)
    _csignature(_libObjC.ivar_getOffset, c_ptrdiff_t, Ivar_t)
    # const char *ivar_getTypeEncoding(Ivar_t ivar)
    _csignature(_libObjC.ivar_getTypeEncoding, c_char_p, Ivar_t)

    # char *method_copyArgumentType(Method_t method, unsigned int index).
    # You must free() the returned string!
    _csignature_str(_libObjC.method_copyArgumentType, c_char_p, Method_t, c_uint)
    # char *method_copyReturnType(Method_t method).
    # You must free() the returned string, but can't despite the documentation
    # https://Developer.Apple.com/documentation/objectivec/1418777-method_copyreturntype
    _csignature(_libObjC.method_copyReturnType, c_char_p, Method_t)
    # void method_exchangeImplementations(Method_t m1, Method_t m2)
    _csignature(_libObjC.method_exchangeImplementations, c_void, Method_t, Method_t)
    # void method_getArgumentType(Method_t method, unsigned int index, char *dst, size_t dst_len)
    # Functionally similar to strncpy(dst, parameter_type, dst_len).
    _csignature(_libObjC.method_getArgumentType, c_void, Method_t, c_uint, c_char_p, c_size_t)
    # IMP_t method_getImplementation(Method_t method)
    _csignature(_libObjC.method_getImplementation, IMP_t, Method_t)
    # SEL_t method_getName(Method_t method)
    _csignature(_libObjC.method_getName, SEL_t, Method_t)
    # unsigned method_getNumberOfArguments(Method_t method)
    _csignature(_libObjC.method_getNumberOfArguments, c_uint, Method_t)
    # void method_getReturnType(Method_t method, char *dst, size_t dst_len)
    # Functionally similar to strncpy(dst, return_type, dst_len)
    _csignature(_libObjC.method_getReturnType, c_void, Method_t, c_char_p, c_size_t)
    # const char *method_getTypeEncoding(Method_t method)
    _csignature(_libObjC.method_getTypeEncoding, c_char_p, Method_t)
    # IMP_t method_setImplementation(Method_t method, IMP_t imp)
    _csignature(_libObjC.method_setImplementation, IMP_t, Method_t, IMP_t)

    # Class_t objc_allocateClassPair(Class_t superclass, const char *name, size_t extraBytes)
    _csignature(_libObjC.objc_allocateClassPair, Class_t, Class_t, c_char_p, c_size_t)
    # void objc_registerClassPair(Class_t cls)
    _csignature(_libObjC.objc_registerClassPair, c_void, Class_t)

    # Protocol_t **objc_copyProtocolList(unsigned int *outCount)
    # Returns an array of *outcount pointers NULL terminated.  You must free() the array!
    _csignature_list(_libObjC.objc_copyProtocolList, POINTER(Protocol_t), POINTER(c_uint))

    # Id_t objc_getAssociatedObject(Id_t object, void *key)
    _csignature(_libObjC.objc_getAssociatedObject, Id_t, Id_t, c_void_p)
    # void objc_removeAssociatedObjects(Id_t object)
    _csignature(_libObjC.objc_removeAssociatedObjects, c_void, Id_t)
    # void objc_setAssociatedObject(Id_t object, void *key, Id_t value, objc_AssociationPolicy policy)
    _csignature(_libObjC.objc_setAssociatedObject, c_void, Id_t, c_void_p, Id_t, c_int)

    # Class_t objc_getClass(const char *name)
    _csignature(_libObjC.objc_getClass, Class_t, c_char_p)
    # int objc_getClassList(Class_t *buffer, int bufferLen)
    # Pass C{None} for buffer to obtain just the total number of classes.
    _csignature(_libObjC.objc_getClassList, c_int, Class_t, c_int)
    # Class_t objc_getMetaClass(const char *name)
    _csignature(_libObjC.objc_getMetaClass, Class_t, c_char_p)
    # Protocol_t *objc_getProtocol(const char *name)
    _csignature(_libObjC.objc_getProtocol, Protocol_t, c_char_p)

    # You must set return and argument types depending on context.
    # Id_t objc_msgSend(Id_t theReceiver, SEL_t theSelector, ...)
    _csignature(_libObjC.objc_msgSend, Id_t, Id_t, SEL_t)
    # Id_t objc_msgSendSuper(struct objc_super_t *super, SEL_t op, ...)
    _csignature(_libObjC.objc_msgSendSuper, Id_t, c_void_p, SEL_t)
    if __i386__ or __x86_64__:  # only for Intel processor and Intel emulatiom
        # double objc_msgSend_fpret(Id_t self, SEL_t op, ...)
        _csignature(_libObjC.objc_msgSend_fpret, c_float, Id_t, SEL_t)  # c_float, c_longdouble
        # void objc_msgSend_stret(void *stretAddr, Id_t theReceiver, SEL_t theSelector,  ...)
        _csignature(_libObjC.objc_msgSend_stret, c_void, c_void_p, Id_t, SEL_t)
        # void objc_msgSendSuper_stret(struct objc_super_t *super, SEL_t op, ...)
        _csignature(_libObjC.objc_msgSendSuper_stret, c_void, c_void_p, SEL_t)

    # Id_t object_copy(Id_t obj, size_t size)
    _csignature(_libObjC.object_copy, Id_t, Id_t, c_size_t)
    # Id_t object_dispose(Id_t obj)
    _csignature(_libObjC.object_dispose, Id_t, Id_t)
    # Class_t object_getClass(Id_t object)
    _csignature(_libObjC.object_getClass, Class_t, Id_t)
    # const char *object_getClassName(Id_t obj)
    _csignature(_libObjC.object_getClassName, c_char_p, Id_t)
    # Ivar_t object_getInstanceVariable(Id_t obj, const char *name, void **outValue)
    _csignature(_libObjC.object_getInstanceVariable, Ivar_t, Id_t, c_char_p, c_void_p)
    # Id_t object_getIvar(Id_t object, Ivar_t ivar)
    _csignature(_libObjC.object_getIvar, Id_t, Id_t, Ivar_t)
    # Class_t object_setClass(Id_t object, Class_t cls)
    _csignature(_libObjC.object_setClass, c_void_p, c_void_p, c_void_p)
    # Ivar_t object_setInstanceVariable(Id_t obj, const char *name, void *value)
    # Set argtypes based on the data type of the instance variable, see .runtime.set_ivar
    _csignature(_libObjC.object_setInstanceVariable, Ivar_t, Id_t, c_char_p, c_void_p)
    # void object_setIvar(Id_t object, Ivar_t ivar, Id_t value)
    _csignature(_libObjC.object_setIvar, c_void, Id_t, Ivar_t, Id_t)

    # void objc_startCollectorThread(void)
    _csignature(_libObjC.objc_startCollectorThread, c_void)

    # objc_property_attribute_t *property_copyAttributeList(objc_property_t property, unsigned int *outCount)
    # Returns an array of pointers of type objc_property_attribute_t* describing property attributes.
    # The array has *outCount pointers, NULL terminated.  You must free() the returned array!
    _csignature_list(_libObjC.property_copyAttributeList, POINTER(objc_property_attribute_t), objc_property_t, POINTER(c_uint))
    # const char *property_getAttributes(objc_property_t property)
    _csignature(_libObjC.property_getAttributes, c_char_p, objc_property_t)
    # const char *property_getName(objc_property_t property)
    _csignature(_libObjC.property_getName, c_char_p, objc_property_t)

    # void protocol_addMethodDescription(Protocol_t *proto, SEL_t name, const char *types,
    #                                    BOOL isRequiredMethod, BOOL isInstanceMethod)
    _csignature(_libObjC.protocol_addMethodDescription, c_void, Protocol_t, SEL_t, c_char_p, BOOL_t, BOOL_t)
    # void protocol_addProperty(Protocol_t *proto, const char *name, const objc_property_attribute_t *attributes,
    #                           unsigned int attributeCount, BOOL isRequiredProperty, BOOL isInstanceProperty)
    _csignature(_libObjC.protocol_addProperty, c_void, Protocol_t, c_char_p, POINTER(objc_property_attribute_t), c_uint, BOOL_t, BOOL_t)
    # void protocol_addProtocol(Protocol_t *proto, Protocol_t *addition)
    _csignature(_libObjC.protocol_addProtocol, c_void, Protocol_t, Protocol_t)
    # Protocol_t *objc_allocateProtocol(const char *name)
    _csignature(_libObjC.objc_allocateProtocol, Protocol_t, c_char_p)
    # BOOL protocol_conformsToProtocol(Protocol_t *proto, Protocol_t *other)
    _csignature(_libObjC.protocol_conformsToProtocol, BOOL_t, Protocol_t, Protocol_t)
    # struct objc_method_description_t *protocol_copyMethodDescriptionList(Protocol_t *p, BOOL isRequiredMethod,
    #                                   BOOL isInstanceMethod, unsigned int *outCount).  You must free() the returned array!
    _csignature_list(_libObjC.protocol_copyMethodDescriptionList, POINTER(objc_method_description_t), Protocol_t, BOOL_t, BOOL_t, POINTER(c_uint))
    # objc_property_t *protocol_copyPropertyList(Protocol_t *protocol, unsigned int *outCount)
    _csignature_list(_libObjC.protocol_copyPropertyList, POINTER(objc_property_t), Protocol_t, POINTER(c_uint))
    # Protocol_t **protocol_copyProtocolList(Protocol_t *proto, unsigned int *outCount)
    _csignature_list(_libObjC.protocol_copyProtocolList, POINTER(Protocol_t), Protocol_t, POINTER(c_uint))
    # struct objc_method_description_t protocol_getMethodDescription(Protocol_t *p, SEL_t aSel, BOOL isRequiredMethod, BOOL isInstanceMethod)
    _csignature(_libObjC.protocol_getMethodDescription, objc_method_description_t, Protocol_t, SEL_t, BOOL_t, BOOL_t)
    # const char *protocol_getName(Protocol_t *p)
    _csignature(_libObjC.protocol_getName, c_char_p, Protocol_t)
    # void objc_registerProtocol(Protocol_t *proto)
    _csignature(_libObjC.objc_registerProtocol, c_void, Protocol_t)

    # const char *sel_getName(SEL_t aSelector)
    _csignature(_libObjC.sel_getName, c_char_p, SEL_t)
    # BOOL sel_isEqual(SEL_t lhs, SEL_t rhs)
    _csignature(_libObjC.sel_isEqual, BOOL_t, SEL_t, SEL_t)
    # SEL_t sel_getUid(const char *str)
    # Use sel_registerName instead.
    # SEL_t sel_registerName(const char *str)
    _csignature(_libObjC.sel_registerName, SEL_t, c_char_p)

# VLC KIT
# _libVLCKit = get_lib('VLCKit')  # XXX not needed

# callback to handle so-called uncaught ObjC exceptions from libc, different from
# the _libAppKit.NSExceptionHandler, see for example <https://Developer.Apple.com/
# documentation/exceptionhandling/nsexceptionhandler>.  DO NOT use the latter, for
# an example see here <https://OpenSource.Apple.com/source/pyobjc/pyobjc-32/pyobjc/
# pyobjc-framework-ExceptionHandling/Lib/PyObjCTools/Debugging.py.auto.html>.
try:
    _setUncaughtExceptionHandler = _libc.objc_setUncaughtExceptionHandler
except AttributeError:  # macOS 12.0.1 Monterey
    _setUncaughtExceptionHandler = _libAppKit.NSSetUncaughtExceptionHandler
_UncaughtExceptionHandler_t = CFUNCTYPE(None, c_void_p)
_csignature(_setUncaughtExceptionHandler, _UncaughtExceptionHandler_t, _UncaughtExceptionHandler_t)

Libs(C=_libc, ObjC=_libObjC, Quartz=_libCG)

if __name__ == _Dmain_:

    _ = get_lib_framework('PrintCore')

    import sys
    if '-dlllist' in sys.argv:
        from pycocoa.utils import printf, zSIstr
        from os.path import basename, getsize

        p = ''
        for i, n in enumerate(sorted(_dlllist())):
            try:
                n = get_lib(basename(n))._name
            except (AttributeError, OSError):
                pass
            if p != n:
                p = n
                try:
                    z = zSIstr(getsize(n))
                except OSError:
                    z = '---'
                printf('%3d %s  %s', i + 1, n, z)
    else:
        from pycocoa.utils import _all_listing, _varstr

        C = Libs.__class__
        for n_l in Libs.items():
            setattr(C, *n_l)
        print(_varstr(Libs))

        Libs = 'see @var Libs'
        _all_listing(__all__, locals(), libs=True)

# python3 -m pycocoa.oslibs
#
# pycocoa.oslibs.__all__ = tuple(
#  pycocoa.oslibs.get_lib is <function .get_lib at 0x10347b240>,
#  pycocoa.oslibs.get_lib_framework is <function .get_lib_framework at 0x10347b2e0>,
#  pycocoa.oslibs.leaked2 is <function .leaked2 at 0x10347b380>,
#  pycocoa.oslibs.Libs is 'see @var Libs',
#  pycocoa.oslibs.NO is False or 0x0,
#  pycocoa.oslibs.NSAcknowledgeCharacter is 6 or 0x6,
#  pycocoa.oslibs.NSAlphaShiftKeyMask is 65536 or 0x10000 or 1 << 16,
#  pycocoa.oslibs.NSAlternateKeyMask is 524288 or 0x80000 or 1 << 19,
#  pycocoa.oslibs.NSAnyEventMask is 4294967295 or 0xFFFFFFFF,
#  pycocoa.oslibs.NSApplicationActivationPolicyAccessory is 1 or 0x1,
#  pycocoa.oslibs.NSApplicationActivationPolicyProhibited is 2 or 0x2,
#  pycocoa.oslibs.NSApplicationActivationPolicyRegular is 0 or 0x0,
#  pycocoa.oslibs.NSApplicationDefined is 15 or 0xF,
#  pycocoa.oslibs.NSApplicationDidHideNotification is c_void_p(8684431552),
#  pycocoa.oslibs.NSApplicationDidUnhideNotification is c_void_p(8684431648),
#  pycocoa.oslibs.NSApplicationPresentationDefault is 0 or 0x0,
#  pycocoa.oslibs.NSApplicationPresentationDisableHideApplication is 256 or 0x100 or 1 << 8,
#  pycocoa.oslibs.NSApplicationPresentationDisableProcessSwitching is 32 or 0x20 or 1 << 5,
#  pycocoa.oslibs.NSApplicationPresentationHideDock is 2 or 0x2,
#  pycocoa.oslibs.NSApplicationPresentationHideMenuBar is 8 or 0x8 or 1 << 3,
#  pycocoa.oslibs.NSBackingStoreBuffered is 2 or 0x2,
#  pycocoa.oslibs.NSBackingStoreNonretained is 1 or 0x1,
#  pycocoa.oslibs.NSBackingStoreRetained is 0 or 0x0,
#  pycocoa.oslibs.NSBackSpaceCharacter is 8 or 0x8 or 1 << 3,
#  pycocoa.oslibs.NSBackTabCharacter is 25 or 0x19,
#  pycocoa.oslibs.NSBellCharacter is 7 or 0x7,
#  pycocoa.oslibs.NSCancelButton is 0 or 0x0,
#  pycocoa.oslibs.NSCancelCharacter is 24 or 0x18 or 3 << 3,
#  pycocoa.oslibs.NSCarriageReturnCharacter is 13 or 0xD,
#  pycocoa.oslibs.NSCenterTextAlignment is 1 or 0x1,
#  pycocoa.oslibs.NSClearLineFunctionKey is 63289 or 0xF739,
#  pycocoa.oslibs.NSCommandKeyMask is 1048576 or 0x100000 or 1 << 20,
#  pycocoa.oslibs.NSControlKeyMask is 262144 or 0x40000 or 1 << 18,
#  pycocoa.oslibs.NSDataLineEscapeCharacter is 16 or 0x10 or 1 << 4,
#  pycocoa.oslibs.NSDefaultRunLoopMode is <RunLoop_t at 0x103436c50>,
#  pycocoa.oslibs.NSDeleteCharacter is 127 or 0x7F,
#  pycocoa.oslibs.NSDeleteFunctionKey is 63272 or 0xF728 or 7909 << 3,
#  pycocoa.oslibs.NSDeviceControl1Character is 17 or 0x11,
#  pycocoa.oslibs.NSDeviceControl2Character is 18 or 0x12,
#  pycocoa.oslibs.NSDeviceControl3Character is 19 or 0x13,
#  pycocoa.oslibs.NSDeviceControl4Character is 20 or 0x14,
#  pycocoa.oslibs.NSDownArrowFunctionKey is 63233 or 0xF701,
#  pycocoa.oslibs.NSEndFunctionKey is 63275 or 0xF72B,
#  pycocoa.oslibs.NSEndOfMediumCharacter is 25 or 0x19,
#  pycocoa.oslibs.NSEndOfTextCharacter is 3 or 0x3,
#  pycocoa.oslibs.NSEndOfTransmitBlockCharacter is 23 or 0x17,
#  pycocoa.oslibs.NSEndOfTransmitCharacter is 4 or 0x4,
#  pycocoa.oslibs.NSEnquiryCharacter is 5 or 0x5,
#  pycocoa.oslibs.NSEnterCharacter is 3 or 0x3,
#  pycocoa.oslibs.NSEscapeCharacter is 27 or 0x1B,
#  pycocoa.oslibs.NSEventTrackingRunLoopMode is <RunLoop_t at 0x103436cd0>,
#  pycocoa.oslibs.NSF19FunctionKey is 63254 or 0xF716,
#  pycocoa.oslibs.NSF1FunctionKey is 63236 or 0xF704,
#  pycocoa.oslibs.NSFileHandlingPanelCancelButton is 0 or 0x0,
#  pycocoa.oslibs.NSFileHandlingPanelOKButton is 1 or 0x1,
#  pycocoa.oslibs.NSFileSeparatorCharacter is 28 or 0x1C,
#  pycocoa.oslibs.NSFlagsChanged is 12 or 0xC,
#  pycocoa.oslibs.NSFontBoldMask is 2 or 0x2,
#  pycocoa.oslibs.NSFontClarendonSerifsClass is 1073741824 or 0x40000000 or 1 << 30,
#  pycocoa.oslibs.NSFontClassMask is 4026531840 or 0xF0000000 or 15 << 28,
#  pycocoa.oslibs.NSFontColorGlyphsMask is 8192 or 0x2000 or 1 << 13,
#  pycocoa.oslibs.NSFontCompositeMask is 16384 or 0x4000 or 1 << 14,
#  pycocoa.oslibs.NSFontCompressedMask is 512 or 0x200 or 1 << 9,
#  pycocoa.oslibs.NSFontCondensedMask is 64 or 0x40 or 1 << 6,
#  pycocoa.oslibs.NSFontExpandedMask is 32 or 0x20 or 1 << 5,
#  pycocoa.oslibs.NSFontFreeformSerifsClass is 1879048192 or 0x70000000 or 7 << 28,
#  pycocoa.oslibs.NSFontItalicMask is 1 or 0x1,
#  pycocoa.oslibs.NSFontModernSerifsClass is 805306368 or 0x30000000 or 3 << 28,
#  pycocoa.oslibs.NSFontMonoSpaceMask is 1024 or 0x400 or 1 << 10,
#  pycocoa.oslibs.NSFontNarrowMask is 16 or 0x10 or 1 << 4,
#  pycocoa.oslibs.NSFontNonStandardCharacterSetMask is 8 or 0x8 or 1 << 3,
#  pycocoa.oslibs.NSFontOldStyleSerifsClass is 268435456 or 0x10000000 or 1 << 28,
#  pycocoa.oslibs.NSFontOrnamentalsClass is 2415919104 or 0x90000000 or 9 << 28,
#  pycocoa.oslibs.NSFontPosterMask is 256 or 0x100 or 1 << 8,
#  pycocoa.oslibs.NSFontSansSerifClass is 2147483648 or 0x80000000 or 1 << 31,
#  pycocoa.oslibs.NSFontScriptsClass is 2684354560 or 0xA0000000 or 5 << 29,
#  pycocoa.oslibs.NSFontSlabSerifsClass is 1342177280 or 0x50000000 or 5 << 28,
#  pycocoa.oslibs.NSFontSmallCapsMask is 128 or 0x80 or 1 << 7,
#  pycocoa.oslibs.NSFontSymbolicClass is 3221225472 or 0xC0000000 or 3 << 30,
#  pycocoa.oslibs.NSFontTransitionalSerifsClass is 536870912 or 0x20000000 or 1 << 29,
#  pycocoa.oslibs.NSFontUIOptimizedMask is 4096 or 0x1000 or 1 << 12,
#  pycocoa.oslibs.NSFontUnboldMask is 4 or 0x4,
#  pycocoa.oslibs.NSFontUnitalicMask is 16777216 or 0x1000000 or 1 << 24,
#  pycocoa.oslibs.NSFontUnknownClass is 0 or 0x0,
#  pycocoa.oslibs.NSFontVerticalMask is 2048 or 0x800 or 1 << 11,
#  pycocoa.oslibs.NSFormFeedCharacter is 12 or 0xC,
#  pycocoa.oslibs.NSFunctionKeyMask is 8388608 or 0x800000 or 1 << 23,
#  pycocoa.oslibs.NSGroupSeparatorCharacter is 29 or 0x1D,
#  pycocoa.oslibs.NSHelpFunctionKey is 63302 or 0xF746,
#  pycocoa.oslibs.NSHelpKeyMask is 4194304 or 0x400000 or 1 << 22,
#  pycocoa.oslibs.NSHomeFunctionKey is 63273 or 0xF729,
#  pycocoa.oslibs.NSHorizontalTabCharacter is 9 or 0x9,
#  pycocoa.oslibs.NSJustifiedTextAlignment is 3 or 0x3,
#  pycocoa.oslibs.NSKeyDown is 10 or 0xA,
#  pycocoa.oslibs.NSKeyUp is 11 or 0xB,
#  pycocoa.oslibs.NSLeftArrowFunctionKey is 63234 or 0xF702,
#  pycocoa.oslibs.NSLeftTextAlignment is 0 or 0x0,
#  pycocoa.oslibs.NSLineFeedCharacter is 10 or 0xA,
#  pycocoa.oslibs.NSLineSeparatorCharacter is 8232 or 0x2028 or 1029 << 3,
#  pycocoa.oslibs.NSNaturalTextAlignment is 4 or 0x4,
#  pycocoa.oslibs.NSNegativeAcknowledgeCharacter is 21 or 0x15,
#  pycocoa.oslibs.NSNewLineCharacter is 10 or 0xA,
#  pycocoa.oslibs.NSNullCharacter is 0 or 0x0,
#  pycocoa.oslibs.NSNumericPadKeyMask is 2097152 or 0x200000 or 1 << 21,
#  pycocoa.oslibs.NSOKButton is 1 or 0x1,
#  pycocoa.oslibs.NSPageDownFunctionKey is 63277 or 0xF72D,
#  pycocoa.oslibs.NSPageUpFunctionKey is 63276 or 0xF72C,
#  pycocoa.oslibs.NSParagraphSeparatorCharacter is 8233 or 0x2029,
#  pycocoa.oslibs.NSRecordSeparatorCharacter is 30 or 0x1E,
#  pycocoa.oslibs.NSRightArrowFunctionKey is 63235 or 0xF703,
#  pycocoa.oslibs.NSRightTextAlignment is 2 or 0x2,
#  pycocoa.oslibs.NSShiftInCharacter is 15 or 0xF,
#  pycocoa.oslibs.NSShiftKeyMask is 131072 or 0x20000 or 1 << 17,
#  pycocoa.oslibs.NSShiftOutCharacter is 14 or 0xE,
#  pycocoa.oslibs.NSSpaceCharacter is 32 or 0x20 or 1 << 5,
#  pycocoa.oslibs.NSSquareStatusItemLength is -2 or 0x-2,
#  pycocoa.oslibs.NSStartOfHeadingCharacter is 1 or 0x1,
#  pycocoa.oslibs.NSStartOfTextCharacter is 2 or 0x2,
#  pycocoa.oslibs.NSSubstituteCharacter is 26 or 0x1A,
#  pycocoa.oslibs.NSSynchronousIdleCharacter is 22 or 0x16,
#  pycocoa.oslibs.NSTabCharacter is 9 or 0x9,
#  pycocoa.oslibs.NSTableViewDashedHorizontalGridLineMask is 8 or 0x8 or 1 << 3,
#  pycocoa.oslibs.NSTableViewGridNone is 0 or 0x0,
#  pycocoa.oslibs.NSTableViewSolidHorizontalGridLineMask is 2 or 0x2,
#  pycocoa.oslibs.NSTableViewSolidVerticalGridLineMask is 1 or 0x1,
#  pycocoa.oslibs.NSTextAlignmentCenter is 1 or 0x1,
#  pycocoa.oslibs.NSTextAlignmentJustified is 3 or 0x3,
#  pycocoa.oslibs.NSTextAlignmentLeft is 0 or 0x0,
#  pycocoa.oslibs.NSTextAlignmentNatural is 4 or 0x4,
#  pycocoa.oslibs.NSTextAlignmentRight is 2 or 0x2,
#  pycocoa.oslibs.NSTextWritingDirectionEmbedding is 0 or 0x0,
#  pycocoa.oslibs.NSTextWritingDirectionOverride is 2 or 0x2,
#  pycocoa.oslibs.NSTrackingActiveInActiveApp is 64 or 0x40 or 1 << 6,
#  pycocoa.oslibs.NSTrackingCursorUpdate is 4 or 0x4,
#  pycocoa.oslibs.NSTrackingMouseEnteredAndExited is 1 or 0x1,
#  pycocoa.oslibs.NSTrackingMouseMoved is 2 or 0x2,
#  pycocoa.oslibs.NSUnitSeparatorCharacter is 31 or 0x1F,
#  pycocoa.oslibs.NSUpArrowFunctionKey is 63232 or 0xF700 or 247 << 8,
#  pycocoa.oslibs.NSVariableStatusItemLength is -1 or 0x-1,
#  pycocoa.oslibs.NSVerticalTabCharacter is 11 or 0xB,
#  pycocoa.oslibs.NSWindowCloseButton is 0 or 0x0,
#  pycocoa.oslibs.NSWindowDocumentIconButton is 4 or 0x4,
#  pycocoa.oslibs.NSWindowMiniaturizeButton is 1 or 0x1,
#  pycocoa.oslibs.NSWindowStyleMaskClosable is 2 or 0x2,
#  pycocoa.oslibs.NSWindowStyleMaskMiniaturizable is 4 or 0x4,
#  pycocoa.oslibs.NSWindowStyleMaskResizable is 8 or 0x8 or 1 << 3,
#  pycocoa.oslibs.NSWindowStyleMaskTitled is 1 or 0x1,
#  pycocoa.oslibs.NSWindowStyleMaskUsual is 15 or 0xF,
#  pycocoa.oslibs.NSWindowStyleMaskUtilityWindow is 16 or 0x10 or 1 << 4,
#  pycocoa.oslibs.NSWindowToolbarButton is 3 or 0x3,
#  pycocoa.oslibs.NSWindowZoomButton is 2 or 0x2,
#  pycocoa.oslibs.OSlibError is <class .OSlibError>,
#  pycocoa.oslibs.YES is True or 0x1,
# )[153]
# pycocoa.oslibs.version 25.4.7, .isLazy 1, Python 3.13.2 64bit arm64, macOS 15.4, oslibs [AppKit, C, CoreFoundation, CoreGraphics, CoreText, Foundation, libc, libobjc, ObjC, Quartz]

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
