
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Various ObjC and macOS libraries, signatures, constants, etc.

@var libAppKit:     The macOS C{AppKit} library (C{ctypes.CDLL}).
@var libCF:         The macOS C{CoreFoundation} library (C{ctypes.CDLL}).
@var libCT:         The macOS C{CoreText} library (C{ctypes.CDLL}).
@var libFoundation: The macOS C{Foundation} library (C{ctypes.CDLL}).
@var libobjc:       The macOS C{objc} library (C{ctypes.CDLL}).
@var libquartz:     The macOS C{quartz} library (C{ctypes.CDLL}).

@var NO:  ObjC's False (C{const c_byte}).
@var YES: ObjC's True (C{const c_byte}).

'''
# all imports listed explicitly to help PyChecker
from ctypes  import byref, cast, cdll, c_buffer, c_byte, c_char, c_char_p, \
                    c_double, c_float, \
                    c_int, c_int8, c_int16, c_int32, c_int64, \
                    CFUNCTYPE, c_long, c_longlong, c_short, c_size_t, \
                    c_uint, c_uint8, c_uint32, c_void_p, \
                    POINTER, sizeof  # c_ubyte, string_at
from octypes import Allocator_t, Array_t, BOOL_t, CFIndex_t, \
                    CFRange_t, CGBitmapInfo_t, CGDirectDisplayID_t, \
                    CGError_t, CGFloat_t, CGGlyph_t, CGPoint_t, \
                    CGRect_t, CGSize_t, Class_t, c_ptrdiff_t, \
                    CTFontOrientation_t, CTFontSymbolicTraits_t, \
                    c_void, Data_t, Dictionary_t, Id_t, IMP_t, Ivar_t, \
                    Method_t, Number_t, NumberType_t, TypeID_t, \
                    NSInteger_t, NSRect_t, objc_method_description_t, \
                    objc_property_t, objc_property_attribute_t, \
                    Protocol_t, SEL_t, Set_t, String_t, \
                    TypeRef_t, UniChar_t, URL_t
from utils   import bytes2str, _exports, str2bytes

try:
    from ctypes.util import find_library as _find_lib
except ImportError:  # XXX Pythonista/iOS
    def _find_lib(unused):
        return None

__version__ = '18.07.25'
_leaked2    = []  # leaked memory, 2-tuples (ptr, size)
_libs_cache = {}  # loaded libraries, by name

NO  = False  # c_byte(0)
YES = True   # c_byte(1)


def _csignature(libfunc, restype, *argtypes):
    # set the result and argument ctypes of a library function
    libfunc.restype = restype
    if argtypes:
        libfunc.argtypes = argtypes


def _csignature_list(libfunc, restype, *argtypes):
    # set the list result and argument ctypes and
    # install a handler to duplicate the result and
    # avoid leaking the memory of the original list
    libfunc.restype = restype
    if argtypes:
        libfunc.argtypes = argtypes
    # the result type must be a pointer to some other type,
    # 'PointerType' in Python 2.6-, 'PyCPointerType' later
    # and the result must be a NULL-terminated array
    if restype.__class__.__name__ in ('PyCPointerType', 'PointerType'):
        # ... and/or restype.__name__.startswith('LP_'):
        libfunc.errcheck = _listdup


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


def _csignature_variadic(libfunc, restype, *unused):
    # set only the result type of a variadic function
    libfunc.restype = restype


def _dup(result, ctype):
    # duplicate a NULL- or nul-terminated array of pointers
    # or string of bytes, leaking the original temporarily
    n = 0
    while result[n]:
        n += 1
    dup = result[:n]  # [result[i] for i in range(n)]

    # leak the original memory, only temporarily
    _leaked2.append((result, (n + 1) * sizeof(ctype)))
    # free several, previously leaked memory, but
    # this segfaults or produces erratic results,
    # especially when memory is freed immediately
    if _libc_free and len(_leaked2) > 4:
        ptr, _ = _leaked2.pop(0)
        _libc_free(ptr)

    return dup


def get_lib(name):
    '''Find and load a C{.dylib} library.

       @param name: The library base name (str).

       @return: The library (C{ctypes.CDLL}).

       @note: Private attribute C{._name} shows the library file name.
    '''
    try:
        lib = _libs_cache[name]
    except KeyError:
        lib = cdll.LoadLibrary(_find_lib(name))
        _libs_cache[name] = lib
    return lib


# get function free(void *ptr) from the C runtime
# (see <http://GitHub.com/oaubert/python-vlc>, the
# Python binding for VLC in folder generated/*/vlc.py)
_libc = get_lib('c')
if _libc:  # macOS, linux, etc.
    _libc_free = _libc.free
    _csignature(_libc_free, c_void, c_void_p)
else:  # ignore free, leaking some memory
    _libc_free = None
del _libc


def leaked2():
    '''Return the number of memory leaks.

       @return: 2-Tuple (I{number}, I{size}) with the I{number} of
                memory leaks and total I{size} leaked, in bytes.
    '''
    return len(_leaked2), sum(t[1] for t in _leaked2)


def _listdup(result, *unused):  # func, args
    # copy the NULL-terminated list
    # and free the original memory
    return _dup(result, c_void_p) if result else []


def _strdup(result, *unused):  # func, args
    # copy the nul-terminated string
    # and free the original memory
    return b''.join(_dup(result, c_byte)) if result else b''


# CORE FOUNDATION

libCF = get_lib('CoreFoundation')

kCFAllocatorDefault   = Allocator_t.in_dll(libCF, 'kCFAllocatorDefault')  # XXX or NULL
kCFRunLoopDefaultMode =    c_void_p.in_dll(libCF, 'kCFRunLoopDefaultMode')

# <http://Developer.Apple.com/documentation/corefoundation/
#         cfstringbuiltinencodings?language=objc>
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

_csignature(libCF.CFArrayAppendValue, Array_t, c_void_p)
# <http://Developer.Apple.com/documentation/corefoundation/1388741-cfarraycreate?language=objc>
_csignature(libCF.CFArrayCreate, Array_t, Allocator_t, c_void_p, CFIndex_t, c_void_p)
# <http://Developer.Apple.com/library/content/documentation/CoreFoundation/
#         Conceptual/CFStrings/Articles/ComparingAndSearching.html>
_csignature(libCF.CFArrayCreateMutable, Array_t, Allocator_t, CFIndex_t, c_void_p)
_csignature(libCF.CFArrayGetCount, CFIndex_t, Array_t)
_csignature(libCF.CFArrayGetTypeID, TypeID_t)
_csignature(libCF.CFArrayGetValueAtIndex, c_void_p, Array_t, CFIndex_t)

_csignature(libCF.CFAttributedStringCreate, c_void_p, Allocator_t, c_void_p, c_void_p)

_csignature(libCF.CFBooleanGetTypeID, TypeID_t)

_csignature(libCF.CFDataCreate, Data_t, Allocator_t, c_void_p, CFIndex_t)
_csignature(libCF.CFDataGetBytes, c_void, Data_t, CFRange_t, c_void_p)
_csignature(libCF.CFDataGetLength, CFIndex_t, Data_t)
_csignature(libCF.CFDataGetTypeID, TypeID_t)

# <http://Developer.Apple.com//documentation/corefoundation/cfdictionary-rum>
# <http://Developer.Apple.com//library/content/documentation/CoreFoundation/
#         Conceptual/CFMemoryMgmt/Concepts/Ownership.html>
# <http://Developer.Apple.com//documentation/corefoundation/1516777-cfdictionaryaddvalue>
_csignature(libCF.CFDictionaryAddValue, c_void, Dictionary_t, c_void_p, c_void_p)  # (d, key, val)
_csignature(libCF.CFDictionaryContainsKey, BOOL_t, Dictionary_t, c_void_p)
_csignature(libCF.CFDictionaryContainsValue, BOOL_t, Dictionary_t, c_void_p)
_csignature(libCF.CFDictionaryCreateMutable, c_void_p, Allocator_t, CFIndex_t, c_void_p, c_void_p)
_csignature(libCF.CFDictionaryGetCount, CFIndex_t, Dictionary_t)
_csignature(libCF.CFDictionaryGetCountOfKey, CFIndex_t, Dictionary_t, c_void_p)
_csignature(libCF.CFDictionaryGetCountOfValue, CFIndex_t, Dictionary_t, c_void_p)
_csignature(libCF.CFDictionaryGetKeysAndValues, Dictionary_t, c_void_p, c_void_p)
_csignature(libCF.CFDictionaryGetTypeID, TypeID_t)
_csignature(libCF.CFDictionaryGetValue, c_void_p, Dictionary_t, c_void_p)  # (d, key)
# Returns a Boolean value that indicates whether a given value for a given key
# is in a dictionary, and returns that value into the last arg if it exists
_csignature(libCF.CFDictionaryGetValueIfPresent, BOOL_t, Dictionary_t, c_void_p, c_void_p)  # (d, key, byref(val)
_csignature(libCF.CFDictionarySetValue, c_void, Dictionary_t, c_void_p, c_void_p)  # (d, key, val)
# _csignature(libCF.CFDictionarySetValueForKey, c_void, Dictionary_t, c_void_p, c_void_p)  # (d, key, val)

_csignature(libCF.CFGetTypeID, TypeID_t, c_void_p)

_csignature(libCF.CFNullGetTypeID, TypeID_t)

_csignature(libCF.CFNumberCreate, Number_t, Allocator_t, NumberType_t, c_void_p)
_csignature(libCF.CFNumberGetType, NumberType_t, Number_t)
_csignature(libCF.CFNumberGetTypeID, TypeID_t)
_csignature(libCF.CFNumberGetValue, BOOL_t, Number_t, NumberType_t, c_void_p)  # (n, TypeID, *n)

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
                       kCFNumberCFIndexType:   CFIndex_t,
                       kCFNumberNSIntegerType: NSInteger_t,
                       kCFNumberCGFloatType:   CGFloat_t}


def cfNumber2bool(ns, dflt=None):
    '''Create a Python C{bool} from an C{NS/CFBoolNumber}, special case.

       @param ns: The C{NS/CFBoolNumber} (L{ObjCInstance}).
       @keyword dflt: Default for missing value (C{None}).

       @raise TypeError: Unexpected C{NumberType}.

       @return: The bool (C{bool}) or I{dflt}.
    '''
    numType = libCF.CFNumberGetType(ns)
    if numType != kCFNumberCharType:
        raise TypeError('unexpected %s(%r): %r' % ('NumberType', ns, numType))
    num = c_byte()  # c_ubyte, see octypes._encoding2ctype!
    if libCF.CFNumberGetValue(ns, numType, byref(num)):
        return True if num.value else False
    else:
        return dflt


def cfNumber2num(ns, dflt=None):
    '''Create a Python C{int} or C{float} from an C{NS/CFNumber}.

       @param ns: The C{NS/CFNumber} (L{ObjCInstance}).
       @keyword dflt: Default for missing, unobtainable value (C{None}).

       @raise TypeError: Unexpected C{NumberType}.

       @return: The number (C{int} or C{float}) or I{dflt}.
    '''
    numType = libCF.CFNumberGetType(ns)
    try:
        ctype = _CFNumberType2ctype[numType]
        num = ctype()
        if libCF.CFNumberGetValue(ns, numType, byref(num)):
            return num.value
        else:
            return dflt
    except KeyError:
        raise TypeError('unhandled %s(%r): %r' % ('NumberType', ns, numType))


def cfString2str(ns, dflt=None):  # XXX an NS*String method
    '''Create a Python C{str} or C{unicode} from an C{NS[Mutable]Str[ing]}.

       @param ns: The C{NS[Mutable]Str[ing]} (L{ObjCInstance}).

       @return: The string (C{str} or C{unicode}) or I{dflt}.
    '''
    n = libCF.CFStringGetLength(ns)
    u = libCF.CFStringGetMaximumSizeForEncoding(n, CFStringEncoding)
    buf = c_buffer(u + 2)
    if libCF.CFStringGetCString(ns, buf, len(buf), CFStringEncoding):
        # XXX assert isinstance(buf.value, _Bytes), 'bytes expected'
        # bytes to unicode in Python 2, to str in Python 3+
        return bytes2str(buf.value)  # XXX was .decode(DEFAULT_UNICODE)
    return dflt


def cfString(ustr):
    '''Create an ObjC C{NS[Constant]String} from a Python string.

       @param ustr: The string value (C{str} or C{unicode}).

       @return: The string instance (C{NS[Constant]String}).
    '''
    return libCF.CFStringCreateWithCString(None, str2bytes(ustr),
                                                 CFStringEncoding)


_csignature(libCF.CFRelease, c_void, TypeRef_t)
_csignature(libCF.CFRetain, TypeRef_t, TypeRef_t)

_csignature(libCF.CFRunLoopGetCurrent, c_void_p)
_csignature(libCF.CFRunLoopGetMain, c_void_p)

_csignature(libCF.CFSetContainsValue, BOOL_t, Set_t, c_void_p)
_csignature(libCF.CFSetGetCount, CFIndex_t, Set_t)
_csignature(libCF.CFSetGetCountOfValue, CFIndex_t, Set_t, c_void_p)
_csignature(libCF.CFSetGetValue, c_void_p, Set_t, c_void_p)
# PyPy 1.7 is fine with the 2nd arg as POINTER(c_void_p),
# but CPython ctypes 1.1.0 complains, so just use c_void_p.
_csignature(libCF.CFSetGetValues, c_void, Set_t, c_void_p)
_csignature(libCF.CFSetGetValueIfPresent, BOOL_t, Set_t, c_void_p, POINTER(c_void_p))

_csignature(libCF.CFStringCreateWithCString, String_t, Allocator_t, c_char_p, CFStringEncoding_t)
_csignature(libCF.CFStringGetCString, BOOL_t, String_t, c_char_p, CFIndex_t, CFStringEncoding_t)
_csignature(libCF.CFStringGetLength, CFIndex_t, String_t)
_csignature(libCF.CFStringGetMaximumSizeForEncoding, CFIndex_t, CFIndex_t, CFStringEncoding_t)
_csignature(libCF.CFStringGetTypeID, TypeID_t)

# CFDataRef CFURLCreateBookmarkDataFromFile(CFAllocatorRef allocator, CFURLRef fileURL, CFErrorRef *errorRef)
_csignature(libCF.CFURLCreateBookmarkDataFromFile, Data_t, Allocator_t, URL_t, c_void_p)
# <http://Developer.Apple.com/documentation/corefoundation/cfurlbookmarkresolutionoptions>
kCFURLBookmarkResolutionWithoutMountingMask = 1 <<  9
kCFURLBookmarkResolutionWithoutUIMask       = 1 <<  8
kCFURLBookmarkResolutionWithSecurityScope   = 1 << 10
# CFURLRef CFURLCreateByResolvingBookmarkData(CFAllocatorRef allocator, CFDataRef bookmark,
#          CFURLBookmarkResolutionOptions options, CFURLRef relativeToURL,
#          CFArrayRef resourcePropertiesToInclude, Boolean *isStale, CFErrorRef *error)
_csignature(libCF.CFURLCreateByResolvingBookmarkData, URL_t, Allocator_t, Data_t, c_uint, URL_t, c_void_p, BOOL_t, c_void_p)


# <http://GitHub.com/al45tair/mac_alias>
# <http://StackOverflow.com/questions/21150169/
#       how-to-use-mac-finder-to-list-all-aliases-in-a-folder/21151368>
# <http://MichaelLynn.GitHub.io/2015/10/24/apples-bookmarkdata-exposed/>
def cfURLResolveAlias(alias):
    '''Resolve a macOS file alias.

       @param alias: The alias file (L{NSURL}).

       @return: The alias' target (L{NSURL}) or C{None}.
    '''
    ns = libCF.CFURLCreateBookmarkDataFromFile(kCFAllocatorDefault, cast(alias, URL_t), 0) or None
    if ns:
        ns = libCF.CFURLCreateByResolvingBookmarkData(kCFAllocatorDefault, ns,
                                                      kCFURLBookmarkResolutionWithoutUIMask, 0, 0, NO, 0)
    return ns


# APPLICATION KIc
# Even though we don't use this directly, it must be loaded so that
# we can find the NSApplication, NSWindow, and NSView classes.
libAppKit = get_lib('AppKit')

NSApplicationDidHideNotification   = c_void_p.in_dll(libAppKit, 'NSApplicationDidHideNotification')
NSApplicationDidUnhideNotification = c_void_p.in_dll(libAppKit, 'NSApplicationDidUnhideNotification')
NSDefaultRunLoopMode               = c_void_p.in_dll(libAppKit, 'NSDefaultRunLoopMode')
NSEventTrackingRunLoopMode         = c_void_p.in_dll(libAppKit, 'NSEventTrackingRunLoopMode')

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

# <http://Developer.Apple.com/documentation/exceptionhandling/nsexceptionhandler>
NSExceptionHandler_t = CFUNCTYPE(None, c_void_p)
_csignature(libAppKit.NSSetUncaughtExceptionHandler, None, NSExceptionHandler_t)

# <http://GitHub.com/gnustep/libs-gui/blob/master/Headers/AppKit/NSPanel.h>
# <http://GitHub.com/gnustep/libs-gui/blob/master/Headers/AppKit/NSSavePanel.h>
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

# /System/Library/Frameworks/AppKit.framework/Headers/NSEvent.h
NSAnyEventMask = 0xFFFFFFFF     # NSUIntegerMax

NSKeyDown            = 10
NSKeyUp              = 11
NSFlagsChanged       = 12
NSApplicationDefined = 15

NSAlphaShiftKeyMask = 1 << 16
NSShiftKeyMask      = 1 << 17
NSControlKeyMask    = 1 << 18
NSAlternateKeyMask  = 1 << 19
NSCommandKeyMask    = 1 << 20
NSNumericPadKeyMask = 1 << 21
NSHelpKeyMask       = 1 << 22
NSFunctionKeyMask   = 1 << 23

NSInsertFunctionKey   = 0xF727
NSDeleteFunctionKey   = 0xF728
NSHomeFunctionKey     = 0xF729
NSBeginFunctionKey    = 0xF72A
NSEndFunctionKey      = 0xF72B
NSPageUpFunctionKey   = 0xF72C
NSPageDownFunctionKey = 0xF72D

# /System/Library/Frameworks/AppKit.framework/Headers/NSGraphics.h
NSBackingStoreRetained    = 0
NSBackingStoreNonretained = 1
NSBackingStoreBuffered    = 2

# <http://GitHub.com/gnustep/libs-gui/blob/master/Headers/AppKit/NSTableView.h>
NSTableViewGridNone                     = 0
NSTableViewSolidVerticalGridLineMask    = 1 << 0
NSTableViewSolidHorizontalGridLineMask  = 1 << 1
NSTableViewDashedHorizontalGridLineMask = 1 << 3
# NSTableViewVerticalGridLineMask?

# <http://GitHub.com/gnustep/libs-gui/blob/master/Headers/AppKit/NSText.h>
NSTextAlignmentLeft      = NSLeftTextAlignment      = 0
NSTextAlignmentRight     = NSRightTextAlignment     = 1
NSTextAlignmentCenter    = NSCenterTextAlignment    = 2
NSTextAlignmentJustified = NSJustifiedTextAlignment = 3
NSTextAlignmentNatural   = NSNaturalTextAlignment   = 4

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
# NSOpenGLPFAVirtualScreenCount    = 128  # number of virtual screens in this format
#
# NSOpenGLCPSwapInterval           = 222

# <http://StackOverflow.com/questions/24024723/swift-using-
#  nsstatusbar-statusitemwithlength-and-nsvariablestatusitemlength>
NSSquareStatusItemLength   = -2
NSVariableStatusItemLength = -1

# /System/Library/Frameworks/AppKit.framework/Headers/NSWindow.h
# <http://Developer.Apple.com//documentation/appkit/nswindowstylemask>
# <http://Developer.Apple.com//documentation/appkit/constants>
# note, Deprecated -Mask's are marked with D? or commented out
# note, Previously, NSWindowStyleMaskXyz was named NSXyzWindowMask
# NSWindowStyleMaskBorderless             = 0  # D?
NSWindowStyleMaskTitled                   = 1 << 0  # D?
NSWindowStyleMaskClosable                 = 1 << 1
NSWindowStyleMaskMiniaturizable           = 1 << 2
NSWindowStyleMaskResizable                = 1 << 3
# /System/Library/Frameworks/AppKit.framework/Headers/NSPanel.h
NSWindowStyleMaskUtilityWindow            = 1 << 4  # D?
# <http://GitHub.com/gnustep/libs-gui/blob/master/Headers/AppKit/NSWindow.h>
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

# <http://GitHub.com/gnustep/libs-gui/blob/master/Headers/AppKit/NSWindow.h>
NSWindowCloseButton        = 0
NSWindowMiniaturizeButton  = 1
NSWindowZoomButton         = 2
NSWindowToolbarButton      = 3
NSWindowDocumentIconButton = 4
# typedef NSUInteger NSWindowButton

# <http://Developer.Apple.com/documentation/appkit/1473652-nsrectfill>
_csignature(libAppKit.NSRectFill, c_void, POINTER(NSRect_t))

# QUARTZ / COREGRAPHICS
libquartz = get_lib('quartz')

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

kCGBitmapAlphaInfoMask   = 0x1F
kCGBitmapFloatComponents = 1 << 8

kCGBitmapByteOrderDefault  = 0 << 12
kCGBitmapByteOrder16Little = 1 << 12
kCGBitmapByteOrder32Little = 2 << 12
kCGBitmapByteOrder16Big    = 3 << 12
kCGBitmapByteOrder32Big    = 4 << 12
kCGBitmapByteOrderMask     = 7 << 12

# /System/Library/Frameworks/ApplicationServices.framework/Frameworks/...
#  ImageIO.framework/Headers/CGImageProperties.h
kCGImagePropertyGIFDictionary = c_void_p.in_dll(libquartz, 'kCGImagePropertyGIFDictionary')
kCGImagePropertyGIFDelayTime  = c_void_p.in_dll(libquartz, 'kCGImagePropertyGIFDelayTime')

# /System/Library/Frameworks/ApplicationServices.framework/Frameworks/...
#  CoreGraphics.framework/Headers/CGColorSpace.h
kCGRenderingIntentDefault = 0

_csignature(libquartz.CGAssociateMouseAndMouseCursorPosition, CGError_t, BOOL_t)
_csignature(libquartz.CGBitmapContextCreate, c_void_p, c_void_p, c_size_t, c_size_t, c_size_t, c_size_t, c_void_p, CGBitmapInfo_t)
_csignature(libquartz.CGBitmapContextCreateImage, c_void_p, c_void_p)
_csignature(libquartz.CGColorSpaceCreateDeviceRGB, c_void_p)
_csignature(libquartz.CGColorSpaceRelease, c_void, c_void_p)
_csignature(libquartz.CGContextDrawImage, c_void, c_void_p, CGRect_t, c_void_p)
_csignature(libquartz.CGContextRelease, c_void, c_void_p)
_csignature(libquartz.CGContextSetShouldAntialias, c_void,c_void_p, BOOL_t)
_csignature(libquartz.CGContextSetTextPosition, c_void, c_void_p, CGFloat_t, CGFloat_t)
_csignature(libquartz.CGCursorIsVisible, BOOL_t)
_csignature(libquartz.CGDataProviderCopyData, c_void_p, c_void_p)
_csignature(libquartz.CGDataProviderCreateWithCFData, c_void_p, c_void_p)
_csignature(libquartz.CGDataProviderRelease, c_void, c_void_p)
_csignature(libquartz.CGDisplayBounds, CGRect_t, CGDirectDisplayID_t)
_csignature(libquartz.CGDisplayCapture, CGError_t, CGDirectDisplayID_t)
_csignature(libquartz.CGDisplayCopyAllDisplayModes, c_void_p, CGDirectDisplayID_t, c_void_p)
_csignature(libquartz.CGDisplayCopyDisplayMode, c_void_p, CGDirectDisplayID_t)
_csignature(libquartz.CGDisplayIDToOpenGLDisplayMask, c_uint32, c_uint32)
_csignature(libquartz.CGDisplayModeCopyPixelEncoding, c_void_p, c_void_p)
_csignature(libquartz.CGDisplayModeGetHeight, c_size_t, c_void_p)
_csignature(libquartz.CGDisplayModeGetRefreshRate, c_double, c_void_p)
_csignature(libquartz.CGDisplayModeGetWidth, c_size_t, c_void_p)
_csignature(libquartz.CGDisplayModeRelease, c_void, c_void_p)
_csignature(libquartz.CGDisplayModeRetain, c_void_p, c_void_p)
_csignature(libquartz.CGDisplayMoveCursorToPoint, CGError_t, CGDirectDisplayID_t, CGPoint_t)
_csignature(libquartz.CGDisplayRelease, CGError_t, CGDirectDisplayID_t)
_csignature(libquartz.CGDisplaySetDisplayMode, CGError_t, CGDirectDisplayID_t, c_void_p, c_void_p)
_csignature(libquartz.CGFontCreateWithDataProvider, c_void_p, c_void_p)
_csignature(libquartz.CGFontCreateWithFontName, c_void_p, c_void_p)
_csignature(libquartz.CGGetActiveDisplayList, CGError_t, c_uint32, POINTER(CGDirectDisplayID_t), POINTER(c_uint32))
_csignature(libquartz.CGImageCreate, c_void_p, c_size_t, c_size_t, c_size_t, c_size_t, c_size_t, c_void_p, c_uint32, c_void_p, c_void_p, BOOL_t, c_int)
_csignature(libquartz.CGImageGetBitmapInfo, CGBitmapInfo_t, c_void_p)
_csignature(libquartz.CGImageGetBitsPerPixel, c_size_t, c_void_p)
_csignature(libquartz.CGImageGetBytesPerRow, c_size_t, c_void_p)
_csignature(libquartz.CGImageGetDataProvider, c_void_p, c_void_p)
_csignature(libquartz.CGImageGetHeight, c_size_t, c_void_p)
_csignature(libquartz.CGImageGetWidth, c_size_t, c_void_p)
_csignature(libquartz.CGImageRelease, c_void, c_void_p)
_csignature(libquartz.CGImageSourceCopyPropertiesAtIndex, c_void_p, c_void_p, c_size_t, c_void_p)
_csignature(libquartz.CGImageSourceCreateImageAtIndex, c_void_p, c_void_p, c_size_t, c_void_p)
_csignature(libquartz.CGImageSourceCreateWithData, c_void_p, c_void_p, c_void_p)
_csignature(libquartz.CGMainDisplayID, CGDirectDisplayID_t)
_csignature(libquartz.CGShieldingWindowLevel, c_int32)
_csignature(libquartz.CGWarpMouseCursorPosition, CGError_t, CGPoint_t)

# CORETEXT
libCT = get_lib('CoreText')

# CoreText constants
kCTFontAttributeName       = c_void_p.in_dll(libCT, 'kCTFontAttributeName')
kCTFontFamilyNameAttribute = c_void_p.in_dll(libCT, 'kCTFontFamilyNameAttribute')
kCTFontTraitsAttribute     = c_void_p.in_dll(libCT, 'kCTFontTraitsAttribute')

kCTFontSlantTrait          = c_void_p.in_dll(libCT, 'kCTFontSlantTrait')  # traits dict key -> -1.0..+1.0
kCTFontSymbolicTrait       = c_void_p.in_dll(libCT, 'kCTFontSymbolicTrait')  # traits dict key -> 0
kCTFontWeightTrait         = c_void_p.in_dll(libCT, 'kCTFontWeightTrait')  # traits dict key -> -1.0..+1.0
kCTFontWidthTrait          = c_void_p.in_dll(libCT, 'kCTFontWidthTrait')  # traits dict key -> -1.0..+1.0

# constants from CTFontTraits.h
kCTFontClassMaskShift = 28

# CTFontSymbolicTraits symbolically describes stylistic aspects of a font.
# The top 4 bits is used to describe appearance of the font while the lower
# 28 bits for typeface.  The font appearance information represented by the
# upper 4 bits can be used for stylistic font matching.
# <http://Developer.Apple.com/documentation/appkit/nsfontmanager/font_traits>
# <http://Developer.Apple.com/documentation/appkit/nsfonttraitmask>
# <http://GitHub.com/tijme/reverse-engineering/blob/master/Billy%20Ellis%20ARM%20Explotation/
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
# <http://Developer.Apple.com/documentation/appkit/nsfontfamilyclass>
kCTFontClassUnknown             = NSFontUnknownClass            =  0 << kCTFontClassMaskShift
kCTFontClassOldStyleSerifs      = NSFontOldStyleSerifsClass     =  1 << kCTFontClassMaskShift
kCTFontClassTransitionalSerifs  = NSFontTransitionalSerifsClass =  2 << kCTFontClassMaskShift
kCTFontClassModernSerifs        = NSFontModernSerifsClass       =  3 << kCTFontClassMaskShift
kCTFontClassClarendonSerifs     = NSFontClarendonSerifsClass    =  4 << kCTFontClassMaskShift
kCTFontClassSlabSerifs          = NSFontSlabSerifsClass         =  5 << kCTFontClassMaskShift
kCTFontClassFreeformSerifs      = NSFontFreeformSerifsClass     =  7 << kCTFontClassMaskShift
kCTFontClassSansSerif           = NSFontSansSerifClass          =  8 << kCTFontClassMaskShift
kCTFontClassOrnamentals         = NSFontOrnamentalsClass        =  9 << kCTFontClassMaskShift
kCTFontClassScripts             = NSFontScriptsClass            = 10 << kCTFontClassMaskShift
kCTFontClassSymbolic            = NSFontSymbolicClass           = 12 << kCTFontClassMaskShift
kCTFontClassMaskTrait           = NSFontClassMask               = 15 << kCTFontClassMaskShift

_csignature(libCT.CTFontCreateWithGraphicsFont, c_void_p, c_void_p, CGFloat_t, c_void_p, c_void_p)
_csignature(libCT.CTFontCopyFamilyName, c_void_p, c_void_p)
_csignature(libCT.CTFontCopyFullName, c_void_p, c_void_p)
_csignature(libCT.CTLineCreateWithAttributedString, c_void_p, c_void_p)
_csignature(libCT.CTFontCreateWithFontDescriptor, c_void_p, c_void_p, CGFloat_t, c_void_p)
_csignature(libCT.CTFontDescriptorCreateWithAttributes, c_void_p, c_void_p)
_csignature(libCT.CTFontGetBoundingRectsForGlyphs, CGRect_t, c_void_p, CTFontOrientation_t, POINTER(CGGlyph_t), POINTER(CGRect_t), CFIndex_t)
_csignature(libCT.CTFontGetAdvancesForGlyphs, c_double, c_void_p, CTFontOrientation_t, POINTER(CGGlyph_t), POINTER(CGSize_t), CFIndex_t)
_csignature(libCT.CTFontGetAscent, CGFloat_t, c_void_p)
_csignature(libCT.CTFontGetDescent, CGFloat_t, c_void_p)
_csignature(libCT.CTFontGetGlyphsForCharacters, BOOL_t, c_void_p, POINTER(UniChar_t), POINTER(CGGlyph_t), CFIndex_t)
_csignature(libCT.CTFontGetSymbolicTraits, CTFontSymbolicTraits_t, c_void_p)
_csignature(libCT.CTLineDraw, c_void, c_void_p, c_void_p)

# FOUNDATION
libFoundation = get_lib('Foundation')

_csignature_variadic(libFoundation.NSLog, c_void, c_char_p)  # ... like printf(format, ...)
_csignature(libFoundation.NSMouseInRect, BOOL_t, CGPoint_t, CGRect_t, BOOL_t)  # CORETEXT  flipped=NO

# OBJECTIVE-C
libobjc = get_lib('objc')

# BOOL class_addIvar(Class_t cls, const char *name, size_t size, uint8_t alignment, const char *types)
_csignature(libobjc.class_addIvar, BOOL_t, Class_t, c_char_p, c_size_t, c_uint8, c_char_p)
# BOOL class_addMethod(Class_t cls, SEL_t name, IMP_t imp, const char *types)
_csignature(libobjc.class_addMethod, BOOL_t, Class_t, SEL_t, IMP_t, c_char_p)
# BOOL class_addProtocol(Class_t cls, Protocol_t *protocol)
_csignature(libobjc.class_addProtocol, BOOL_t, Class_t, Protocol_t)
# BOOL class_conformsToProtocol(Class_t cls, Protocol_t *protocol)
_csignature(libobjc.class_conformsToProtocol, BOOL_t, Class_t, Protocol_t)
# Ivar_t *class_copyIvarList(Class_t cls, unsigned int *outCount)
# Returns an array of pointers of type Ivar_t describing instance variables.
# The array has *outCount pointers, NULL terminated.  You must free() the returned array!
_csignature_list(libobjc.class_copyIvarList, POINTER(Ivar_t), Class_t, POINTER(c_uint))
# Method_t *class_copyMethodList(Class_t cls, unsigned int *outCount)
# Returns an array of pointers of type Method_t describing instance methods.
# The array has *outCount pointers, NULL terminated.  You must free() the returned array!
_csignature_list(libobjc.class_copyMethodList, POINTER(Method_t), Class_t, POINTER(c_uint))
# objc_property_t *class_copyPropertyList(Class_t cls, unsigned int *outCount)
# Returns an array of pointers of type objc_property_t describing properties.
# The array has *outCount pointers, NULL terminated.  You must free() the returned array!
_csignature_list(libobjc.class_copyPropertyList, POINTER(objc_property_t), Class_t, POINTER(c_uint))
# Protocol_t **class_copyProtocolList(Class_t cls, unsigned int *outCount)
# Returns an array of pointers of type Protocol_t* describing protocols.
# The array has *outCount pointers, NULL terminated.  You must free() the returned array!
_csignature_list(libobjc.class_copyProtocolList, POINTER(Protocol_t), Class_t, POINTER(c_uint))
# Id_t class_createInstance(Class_t cls, size_t extraBytes)
_csignature(libobjc.class_createInstance, Id_t, Class_t, c_size_t)
# Method_t class_getClassMethod(Class_t aClass, SEL_t aSelector)
# Will also search superclass for implementations.
_csignature(libobjc.class_getClassMethod, Method_t, Class_t, SEL_t)
# Ivar_t class_getClassVariable(Class_t cls, const char* name)
_csignature(libobjc.class_getClassVariable, Ivar_t, Class_t, c_char_p)
# Method_t class_getInstanceMethod(Class_t aClass, SEL_t aSelector)
# Will also search superclass for implementations.
_csignature(libobjc.class_getInstanceMethod, Method_t, Class_t, SEL_t)
# size_t class_getInstanceSize(Class_t cls)
_csignature(libobjc.class_getInstanceSize, c_size_t, Class_t)
# Ivar_t class_getInstanceVariable(Class_t cls, const char* name)
_csignature(libobjc.class_getInstanceVariable, Ivar_t, Class_t, c_char_p)
# const char *class_getIvarLayout(Class_t cls)
_csignature(libobjc.class_getIvarLayout, c_char_p, Class_t)
# IMP_t class_getMethodImplementation(Class_t cls, SEL_t name)
_csignature(libobjc.class_getMethodImplementation, IMP_t, Class_t, SEL_t)
# IMP_t class_getMethodImplementation_stret(Class_t cls, SEL_t name)
_csignature(libobjc.class_getMethodImplementation_stret, IMP_t, Class_t, SEL_t)
# const char *class_getName(Class_t cls)
_csignature(libobjc.class_getName, c_char_p, Class_t)
# objc_property_t class_getProperty(Class_t cls, const char *name)
_csignature(libobjc.class_getProperty, objc_property_t, Class_t, c_char_p)
# Class_t class_getSuperclass(Class_t cls)
_csignature(libobjc.class_getSuperclass, Class_t, Class_t)
# int class_getVersion(Class_t theClass)
_csignature(libobjc.class_getVersion, c_int, Class_t)
# const char *class_getWeakIvarLayout(Class_t cls)
_csignature(libobjc.class_getWeakIvarLayout, c_char_p, Class_t)
# BOOL class_isMetaClass(Class_t cls)
_csignature(libobjc.class_isMetaClass, BOOL_t, Class_t)
# IMP_t class_replaceMethod(Class_t cls, SEL_t name, IMP_t imp, const char *types)
_csignature(libobjc.class_replaceMethod, IMP_t, Class_t, SEL_t, IMP_t, c_char_p)
# BOOL class_respondsToSelector(Class_t cls, SEL_t sel)
_csignature(libobjc.class_respondsToSelector, BOOL_t, Class_t, SEL_t)
# void class_setIvarLayout(Class_t cls, const char *layout)
_csignature(libobjc.class_setIvarLayout, c_void, Class_t, c_char_p)
# Class_t class_setSuperclass(Class_t cls, Class_t newSuper)
_csignature(libobjc.class_setSuperclass, Class_t, Class_t, Class_t)
# void class_setVersion(Class_t theClass, int version)
_csignature(libobjc.class_setVersion, c_void, Class_t, c_int)
# void class_setWeakIvarLayout(Class_t cls, const char *layout)
_csignature(libobjc.class_setWeakIvarLayout, c_void, Class_t, c_char_p)

# const char *ivar_getName(Ivar_t ivar)
_csignature(libobjc.ivar_getName, c_char_p, Ivar_t)
# ptrdiff_t ivar_getOffset(Ivar_t ivar)
_csignature(libobjc.ivar_getOffset, c_ptrdiff_t, Ivar_t)
# const char *ivar_getTypeEncoding(Ivar_t ivar)
_csignature(libobjc.ivar_getTypeEncoding, c_char_p, Ivar_t)

# char *method_copyArgumentType(Method_t method, unsigned int index).
# You must free() the returned string!
_csignature_str(libobjc.method_copyArgumentType, c_char_p, Method_t, c_uint)
# char *method_copyReturnType(Method_t method).
# You must free() the returned string, but can't despite the documentation
# http://Developer.Apple.com/documentation/objectivec/1418777-method_copyreturntype
_csignature(libobjc.method_copyReturnType, c_char_p, Method_t)
# void method_exchangeImplementations(Method_t m1, Method_t m2)
_csignature(libobjc.method_exchangeImplementations, c_void, Method_t, Method_t)
# void method_getArgumentType(Method_t method, unsigned int index, char *dst, size_t dst_len)
# Functionally similar to strncpy(dst, parameter_type, dst_len).
_csignature(libobjc.method_getArgumentType, c_void, Method_t, c_uint, c_char_p, c_size_t)
# IMP_t method_getImplementation(Method_t method)
_csignature(libobjc.method_getImplementation, IMP_t, Method_t)
# SEL_t method_getName(Method_t method)
_csignature(libobjc.method_getName, SEL_t, Method_t)
# unsigned method_getNumberOfArguments(Method_t method)
_csignature(libobjc.method_getNumberOfArguments, c_uint, Method_t)
# void method_getReturnType(Method_t method, char *dst, size_t dst_len)
# Functionally similar to strncpy(dst, return_type, dst_len)
_csignature(libobjc.method_getReturnType, c_void, Method_t, c_char_p, c_size_t)
# const char *method_getTypeEncoding(Method_t method)
_csignature(libobjc.method_getTypeEncoding, c_char_p, Method_t)
# IMP_t method_setImplementation(Method_t method, IMP_t imp)
_csignature(libobjc.method_setImplementation, IMP_t, Method_t, IMP_t)

# Class_t objc_allocateClassPair(Class_t superclass, const char *name, size_t extraBytes)
_csignature(libobjc.objc_allocateClassPair, Class_t, Class_t, c_char_p, c_size_t)
# void objc_registerClassPair(Class_t cls)
_csignature(libobjc.objc_registerClassPair, c_void, Class_t)

# Protocol_t **objc_copyProtocolList(unsigned int *outCount)
# Returns an array of *outcount pointers NULL terminated.  You must free() the array!
_csignature_list(libobjc.objc_copyProtocolList, POINTER(Protocol_t), POINTER(c_uint))

# Id_t objc_getAssociatedObject(Id_t object, void *key)
_csignature(libobjc.objc_getAssociatedObject, Id_t, Id_t, c_void_p)
# void objc_removeAssociatedObjects(Id_t object)
_csignature(libobjc.objc_removeAssociatedObjects, c_void, Id_t)
# void objc_setAssociatedObject(Id_t object, void *key, Id_t value, objc_AssociationPolicy policy)
_csignature(libobjc.objc_setAssociatedObject, c_void, Id_t, c_void_p, Id_t, c_int)

# Class_t objc_getClass(const char *name)
_csignature(libobjc.objc_getClass, Class_t, c_char_p)
# int objc_getClassList(Class_t *buffer, int bufferLen)
# Pass None for buffer to obtain just the total number of classes.
_csignature(libobjc.objc_getClassList, c_int, Class_t, c_int)
# Class_t objc_getMetaClass(const char *name)
_csignature(libobjc.objc_getMetaClass, Class_t, c_char_p)
# Protocol_t *objc_getProtocol(const char *name)
_csignature(libobjc.objc_getProtocol, Protocol_t, c_char_p)

# You should set return and argument types depending on context.
# Id_t objc_msgSend(Id_t theReceiver, SEL_t theSelector, ...)
# Id_t objc_msgSendSuper(struct objc_super_t *super, SEL_t op,  ...)
# void objc_msgSendSuper_stret(struct objc_super_t *super, SEL_t op, ...)
_csignature_variadic(libobjc.objc_msgSendSuper_stret, c_void)
# double objc_msgSend_fpret(Id_t self, SEL_t op, ...)
_csignature_variadic(libobjc.objc_msgSend_fpret, c_float)  # c_float, c_longdouble
# void objc_msgSend_stret(void * stretAddr, Id_t theReceiver, SEL_t theSelector,  ...)
_csignature_variadic(libobjc.objc_msgSend_stret, c_void)

# Id_t object_copy(Id_t obj, size_t size)
_csignature(libobjc.object_copy, Id_t, Id_t, c_size_t)
# Id_t object_dispose(Id_t obj)
_csignature(libobjc.object_dispose, Id_t, Id_t)
# Class_t object_getClass(Id_t object)
_csignature(libobjc.object_getClass, Class_t, Id_t)
# const char *object_getClassName(Id_t obj)
_csignature(libobjc.object_getClassName, c_char_p, Id_t)
# Ivar_t object_getInstanceVariable(Id_t obj, const char *name, void **outValue)
_csignature(libobjc.object_getInstanceVariable, Ivar_t, Id_t, c_char_p, c_void_p)
# Id_t object_getIvar(Id_t object, Ivar_t ivar)
_csignature(libobjc.object_getIvar, Id_t, Id_t, Ivar_t)
# Class_t object_setClass(Id_t object, Class_t cls)
_csignature(libobjc.object_setClass, c_void_p, c_void_p, c_void_p)
# Ivar_t object_setInstanceVariable(Id_t obj, const char *name, void *value)
# Set argtypes based on the data type of the instance variable.
_csignature_variadic(libobjc.object_setInstanceVariable, Ivar_t)
# void object_setIvar(Id_t object, Ivar_t ivar, Id_t value)
_csignature(libobjc.object_setIvar, c_void, Id_t, Ivar_t, Id_t)

# void objc_startCollectorThread(void)
_csignature(libobjc.objc_startCollectorThread, c_void)

# objc_property_attribute_t *property_copyAttributeList(objc_property_t property, unsigned int *outCount)
# Returns an array of pointers of type objc_property_attribute_t* describing property attributes.
# The array has *outCount pointers, NULL terminated.  You must free() the returned array!
_csignature_list(libobjc.property_copyAttributeList, POINTER(objc_property_attribute_t), objc_property_t, POINTER(c_uint))
# const char *property_getAttributes(objc_property_t property)
_csignature(libobjc.property_getAttributes, c_char_p, objc_property_t)
# const char *property_getName(objc_property_t property)
_csignature(libobjc.property_getName, c_char_p, objc_property_t)

# void protocol_addMethodDescription(Protocol_t *proto, SEL_t name, const char *types,
#                                    BOOL isRequiredMethod, BOOL isInstanceMethod)
_csignature(libobjc.protocol_addMethodDescription, c_void, Protocol_t, SEL_t, c_char_p, BOOL_t, BOOL_t)
# void protocol_addProperty(Protocol_t *proto, const char *name, const objc_property_attribute_t *attributes,
#                           unsigned int attributeCount, BOOL isRequiredProperty, BOOL isInstanceProperty)
_csignature(libobjc.protocol_addProperty, c_void, Protocol_t, c_char_p, POINTER(objc_property_attribute_t), c_uint, BOOL_t, BOOL_t)
# void protocol_addProtocol(Protocol_t *proto, Protocol_t *addition)
_csignature(libobjc.protocol_addProtocol, c_void, Protocol_t, Protocol_t)
# Protocol_t *objc_allocateProtocol(const char *name)
_csignature(libobjc.objc_allocateProtocol, Protocol_t, c_char_p)
# BOOL protocol_conformsToProtocol(Protocol_t *proto, Protocol_t *other)
_csignature(libobjc.protocol_conformsToProtocol, BOOL_t, Protocol_t, Protocol_t)
# struct objc_method_description_t *protocol_copyMethodDescriptionList(Protocol_t *p, BOOL isRequiredMethod,
#                                   BOOL isInstanceMethod, unsigned int *outCount).  You must free() the returned array!
_csignature_list(libobjc.protocol_copyMethodDescriptionList, POINTER(objc_method_description_t), Protocol_t, BOOL_t, BOOL_t, POINTER(c_uint))
# objc_property_t *protocol_copyPropertyList(Protocol_t *protocol, unsigned int *outCount)
_csignature_list(libobjc.protocol_copyPropertyList, POINTER(objc_property_t), Protocol_t, POINTER(c_uint))
# Protocol_t **protocol_copyProtocolList(Protocol_t *proto, unsigned int *outCount)
_csignature_list(libobjc.protocol_copyProtocolList, POINTER(Protocol_t), Protocol_t, POINTER(c_uint))
# struct objc_method_description_t protocol_getMethodDescription(Protocol_t *p, SEL_t aSel, BOOL isRequiredMethod, BOOL isInstanceMethod)
_csignature(libobjc.protocol_getMethodDescription, objc_method_description_t, Protocol_t, SEL_t, BOOL_t, BOOL_t)
# const char *protocol_getName(Protocol_t *p)
_csignature(libobjc.protocol_getName, c_char_p, Protocol_t)
# void objc_registerProtocol(Protocol_t *proto)
_csignature(libobjc.objc_registerProtocol, c_void, Protocol_t)

# const char *sel_getName(SEL_t aSelector)
_csignature(libobjc.sel_getName, c_char_p, SEL_t)
# BOOL sel_isEqual(SEL_t lhs, SEL_t rhs)
_csignature(libobjc.sel_isEqual, BOOL_t, SEL_t, SEL_t)
# SEL_t sel_getUid(const char *str)
# Use sel_registerName instead.
# SEL_t sel_registerName(const char *str)
_csignature(libobjc.sel_registerName, SEL_t, c_char_p)

# VLC KIT
# libVLCKit = get_lib('VLCKit')  # XXX not needed

# filter locals() for .__init__.py
__all__ = _exports(locals(), 'get_lib', 'leaked2', 'NO', 'YES',
                   starts=('lib', 'NS',
                         # 'CF', 'CG', 'ct', 'CTF',
                         # 'kCF', 'kCG', 'kCTF',
                          ))  # PYCHOK false

if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)

# MIT License <http://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2018 -- mrJean1 at Gmail dot com
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
