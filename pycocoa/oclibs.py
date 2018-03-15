
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
from ctypes  import POINTER, cdll, sizeof, util, \
                    c_bool, c_byte, c_char_p, c_double, c_float, \
                    c_int, c_int32, c_size_t, c_ubyte, c_uint, \
                    c_uint8, c_uint32, c_void_p  # string_at
from octypes import c_ptrdiff_t, CFArray, CFIndex, CFNumberType, \
                    CFTypeID, CFRange, CGFloat, CGGlyph, CGPoint, \
                    CGRect, CGSize,  Class, Id, IMP, Ivar, Method, \
                    NSPoint, NSRect, objc_method_description, \
                    objc_property_t, Protocol, SEL, UniChar  # DEFAULT_UNICODE

__version__ = '18.03.14'

c_void = None


def _csignature(libfunc, restype, *argtypes):
    # set the result and argument ctypes
    libfunc.restype = restype
    if argtypes:
        libfunc.argtypes = argtypes


def _csignature_list(libfunc, restype, *argtypes):
    # set the list result and argument ctypes and
    # install a handler to duplicate the result and
    # and leak the memory of the original list
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
    # set the String result and argument ctypes and
    # install a handler to duplicate the result and
    # and leak the memory of the original string
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
    # duplicate a NULL- or nul-terminated array of
    # pointers or string of bytes, leak the original
    n = 0
    while result[n]:
        n += 1
    dup = [result[i] for i in range(n)]

    # leak the original memory, only temporarily
    _leaked.append((result, (n + 1) * sizeof(ctype)))
    # free several, previously leaked memory but
    # this may segfault or produce erratic results,
    # especially if the memory is freed immediately
    if _libc_free and len(_leaked) > 4:
        result, _ = _leaked.pop(0)
        _libc_free(result)

    return dup


_leaked = []  # leaked memory, 2-tuples (ptr, size)


def leaked2():
    '''Return the number of memory leaks and
    the total number of bytes leaked.
    '''
    return len(_leaked), sum(t[1] for t in _leaked)


def _listdup(result, *unused):  # func, args
    # copy the NULL-terminated list
    # and free the original memory
    return _dup(result, c_void_p) if result else []


def _strdup(result, *unused):  # func, args
    # copy the nul-terminated string
    # and free the original memory
    return b''.join(_dup(result, c_byte)) if result else b''


_libs_cache = {}  # loaded libraries


def get_lib(name):
    '''Find and load the C{.dylib} library.
    '''
    try:
        lib = _libs_cache[name]
    except KeyError:
        lib = cdll.LoadLibrary(util.find_library(name))
        _libs_cache[name] = lib
    return lib


# get the free(void *ptr) function from the C runtime
# (see <http://GitHub.com/oaubert/python-vlc>, the
# Python binding for VLC in folder generated/*/vlc.py)
_libc = get_lib('c')
if _libc:  # macOS, linux, etc.
    _libc_free = _libc.free
    _csignature(_libc_free, c_void, c_void_p)
else:  # ignore free, leaking some memory
    _libc_free = None
del _libc


# CORE FOUNDATION

libCF = get_lib('CoreFoundation')

kCFAllocatorDefault   = c_void_p.in_dll(libCF, 'kCFAllocatorDefault')  # XXX or NULL
kCFRunLoopDefaultMode = c_void_p.in_dll(libCF, 'kCFRunLoopDefaultMode')

# <http://Developer.Apple.com/documentation/corefoundation/
#         cfstringbuiltinencodings?language=objc>
kCFStringEncodingISOLatin1     = 0x0201
kCFStringEncodingMacRoman      = 0
kCFStringEncodingASCII         = 0x0600
kCFStringEncodingNonLossyASCII = 0x0BFF
kCFStringEncodingUnicode       = 0x0100
kCFStringEncodingUTF8          = 0x08000100  # shared with .runtime.py
kCFStringEncodingUTF16         = 0x0100
kCFStringEncodingUTF16BE       = 0x10000100
kCFStringEncodingUTF16LE       = 0x14000100
kCFStringEncodingUTF32         = 0x0c000100
kCFStringEncodingUTF32BE       = 0x18000100
kCFStringEncodingUTF32LE       = 0x1c000100
kCFStringEncodingWindowsLatin1 = 0x0500

CFAllocatorRef   = c_void_p  # a ctype
CFStringEncoding = c_uint32  # a ctype

_csignature(libCF.CFArrayAppendValue, CFArray, c_void_p)
# <http://Developer.Apple.com/documentation/corefoundation/1388741-cfarraycreate?language=objc>
_csignature(libCF.CFArrayCreate, CFArray, CFAllocatorRef, c_void_p, CFIndex, c_void_p)
# <http://Developer.Apple.com/library/content/documentation/CoreFoundation/
#         Conceptual/CFStrings/Articles/ComparingAndSearching.html>
_csignature(libCF.CFArrayCreateMutable, CFArray, CFAllocatorRef, CFIndex, c_void_p)
_csignature(libCF.CFArrayGetCount, CFIndex, c_void_p)
_csignature(libCF.CFArrayGetTypeID, CFTypeID)
_csignature(libCF.CFArrayGetValueAtIndex, c_void_p, c_void_p, CFIndex)

_csignature(libCF.CFAttributedStringCreate, c_void_p, CFAllocatorRef, c_void_p, c_void_p)

_csignature(libCF.CFBooleanGetTypeID, CFTypeID)

_csignature(libCF.CFDataCreate, c_void_p, c_void_p, c_void_p, CFIndex)
_csignature(libCF.CFDataGetBytes, c_void, c_void_p, CFRange, c_void_p)
_csignature(libCF.CFDataGetLength, CFIndex, c_void_p)
_csignature(libCF.CFDataGetTypeID, CFTypeID)

_csignature(libCF.CFDictionaryAddValue, c_void, c_void_p, c_void_p, c_void_p)
_csignature(libCF.CFDictionaryCreateMutable, c_void_p, CFAllocatorRef, CFIndex, c_void_p, c_void_p)
_csignature(libCF.CFDictionaryGetCount, CFIndex, c_void_p)
_csignature(libCF.CFDictionaryGetKeysAndValues, c_void, c_void_p, c_void_p)
_csignature(libCF.CFDictionaryGetTypeID, CFTypeID)
_csignature(libCF.CFDictionaryGetValue, c_void_p, c_void_p, c_void_p)

_csignature(libCF.CFGetTypeID, CFTypeID, c_void_p)

_csignature(libCF.CFNullGetTypeID, CFTypeID)

_csignature(libCF.CFNumberCreate, c_void_p, CFAllocatorRef, CFNumberType, c_void_p)
_csignature(libCF.CFNumberGetType, CFNumberType, c_void_p)
_csignature(libCF.CFNumberGetTypeID, CFTypeID)
_csignature(libCF.CFNumberGetValue, c_ubyte, c_void_p, CFNumberType, c_void_p)

_csignature(libCF.CFRelease, c_void_p, c_void_p)

_csignature(libCF.CFRunLoopGetCurrent, c_void_p)
_csignature(libCF.CFRunLoopGetMain, c_void_p)

_csignature(libCF.CFSetGetCount, CFIndex, c_void_p)
# PyPy 1.7 is fine with the 2nd arg as POINTER(c_void_p),
# but CPython ctypes 1.1.0 complains, so just use c_void_p.
_csignature(libCF.CFSetGetValues, c_void, c_void_p, c_void_p)

_csignature(libCF.CFStringCreateWithCString, c_void_p, CFAllocatorRef, c_char_p, CFStringEncoding)
_csignature(libCF.CFStringGetCString, c_bool, c_void_p, c_char_p, CFIndex, CFStringEncoding)
_csignature(libCF.CFStringGetLength, CFIndex, c_void_p)
_csignature(libCF.CFStringGetMaximumSizeForEncoding, CFIndex, CFIndex, CFStringEncoding)
_csignature(libCF.CFStringGetTypeID, CFTypeID)

# APPLICATION KIT
# Even though we don't use this directly, it must be loaded so that
# we can find the NSApplication, NSWindow, and NSView classes.
libAppKit = get_lib('AppKit')

NSApplicationDidHideNotification   = c_void_p.in_dll(libAppKit, 'NSApplicationDidHideNotification')
NSApplicationDidUnhideNotification = c_void_p.in_dll(libAppKit, 'NSApplicationDidUnhideNotification')
NSDefaultRunLoopMode               = c_void_p.in_dll(libAppKit, 'NSDefaultRunLoopMode')
NSEventTrackingRunLoopMode         = c_void_p.in_dll(libAppKit, 'NSEventTrackingRunLoopMode')

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

# /System/Library/Frameworks/AppKit.framework/Headers/NSWindow.h
NSBorderlessWindowMask     = 0
NSTitledWindowMask         = 1 << 0
NSClosableWindowMask       = 1 << 1
NSMiniaturizableWindowMask = 1 << 2
NSResizableWindowMask      = 1 << 3

# /System/Library/Frameworks/AppKit.framework/Headers/NSPanel.h
NSUtilityWindowMask = 1 << 4

# /System/Library/Frameworks/AppKit.framework/Headers/NSGraphics.h
NSBackingStoreRetained    = 0
NSBackingStoreNonretained = 1
NSBackingStoreBuffered    = 2

# /System/Library/Frameworks/AppKit.framework/Headers/NSTrackingArea.h
NSTrackingMouseEnteredAndExited = 0x01
NSTrackingMouseMoved            = 0x02
NSTrackingCursorUpdate          = 0x04
NSTrackingActiveInActiveApp     = 0x40

# /System/Library/Frameworks/AppKit.framework/Headers/NSOpenGL.h
NSOpenGLPFAAllRenderers          =   1  # choose from all available renderers
NSOpenGLPFADoubleBuffer          =   5  # choose a double buffered pixel format
NSOpenGLPFAStereo                =   6  # stereo buffering supported
NSOpenGLPFAAuxBuffers            =   7  # number of aux buffers
NSOpenGLPFAColorSize             =   8  # number of color buffer bits
NSOpenGLPFAAlphaSize             =  11  # number of alpha component bits
NSOpenGLPFADepthSize             =  12  # number of depth buffer bits
NSOpenGLPFAStencilSize           =  13  # number of stencil buffer bits
NSOpenGLPFAAccumSize             =  14  # number of accum buffer bits
NSOpenGLPFAMinimumPolicy         =  51  # never choose smaller buffers than requested
NSOpenGLPFAMaximumPolicy         =  52  # choose largest buffers of type requested
NSOpenGLPFAOffScreen             =  53  # choose an off-screen capable renderer
NSOpenGLPFAFullScreen            =  54  # choose a full-screen capable renderer
NSOpenGLPFASampleBuffers         =  55  # number of multi sample buffers
NSOpenGLPFASamples               =  56  # number of samples per multi sample buffer
NSOpenGLPFAAuxDepthStencil       =  57  # each aux buffer has its own depth stencil
NSOpenGLPFAColorFloat            =  58  # color buffers store floating point pixels
NSOpenGLPFAMultisample           =  59  # choose multisampling
NSOpenGLPFASupersample           =  60  # choose supersampling
NSOpenGLPFASampleAlpha           =  61  # request alpha filtering
NSOpenGLPFARendererID            =  70  # request renderer by ID
NSOpenGLPFASingleRenderer        =  71  # choose a single renderer for all screens
NSOpenGLPFANoRecovery            =  72  # disable all failure recovery systems
NSOpenGLPFAAccelerated           =  73  # choose a hardware accelerated renderer
NSOpenGLPFAClosestPolicy         =  74  # choose the closest color buffer to request
NSOpenGLPFARobust                =  75  # renderer does not need failure recovery
NSOpenGLPFABackingStore          =  76  # back buffer contents are valid after swap
NSOpenGLPFAMPSafe                =  78  # renderer is multi-processor safe
NSOpenGLPFAWindow                =  80  # can be used to render to an onscreen window
NSOpenGLPFAMultiScreen           =  81  # single window can span multiple screens
NSOpenGLPFACompliant             =  83  # renderer is opengl compliant
NSOpenGLPFAScreenMask            =  84  # bit mask of supported physical screens
NSOpenGLPFAPixelBuffer           =  90  # can be used to render to a pbuffer
NSOpenGLPFARemotePixelBuffer     =  91  # can be used to render offline to a pbuffer
NSOpenGLPFAAllowOfflineRenderers =  96  # allow use of offline renderers
NSOpenGLPFAAcceleratedCompute    =  97  # choose a hardware accelerated compute device
NSOpenGLPFAVirtualScreenCount    = 128  # number of virtual screens in this format

NSOpenGLCPSwapInterval           = 222

# /System/Library/Frameworks/ApplicationServices.framework/Frameworks/...
#     CoreGraphics.framework/Headers/CGImage.h
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

kCGBitmapByteOrderMask     = 0x7000
kCGBitmapByteOrderDefault  = 0 << 12
kCGBitmapByteOrder16Little = 1 << 12
kCGBitmapByteOrder32Little = 2 << 12
kCGBitmapByteOrder16Big    = 3 << 12
kCGBitmapByteOrder32Big    = 4 << 12

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

# <http://StackOverflow.com/questions/24024723/swift-using-
#  nsstatusbar-statusitemwithlength-and-nsvariablestatusitemlength>
NSSquareStatusItemLength   = -2
NSVariableStatusItemLength = -1

# <http://Developer.Apple.com/documentation/appkit/1473652-nsrectfill>
_csignature(libAppKit.NSRectFill, c_void, POINTER(NSRect))

# QUARTZ / COREGRAPHICS
libquartz = get_lib('quartz')

CGDirectDisplayID = c_uint32  # CGDirectDisplay.h
CGError           = c_int32   # CGError.h
CGBitmapInfo      = c_uint32  # CGImage.h

# /System/Library/Frameworks/ApplicationServices.framework/Frameworks/...
#  ImageIO.framework/Headers/CGImageProperties.h
kCGImagePropertyGIFDictionary = c_void_p.in_dll(libquartz, 'kCGImagePropertyGIFDictionary')
kCGImagePropertyGIFDelayTime  = c_void_p.in_dll(libquartz, 'kCGImagePropertyGIFDelayTime')

# /System/Library/Frameworks/ApplicationServices.framework/Frameworks/...
#  CoreGraphics.framework/Headers/CGColorSpace.h
kCGRenderingIntentDefault = 0

_csignature(libquartz.CGAssociateMouseAndMouseCursorPosition, CGError, c_bool)
_csignature(libquartz.CGBitmapContextCreate, c_void_p, c_void_p, c_size_t, c_size_t, c_size_t, c_size_t, c_void_p, CGBitmapInfo)
_csignature(libquartz.CGBitmapContextCreateImage, c_void_p, c_void_p)
_csignature(libquartz.CGColorSpaceCreateDeviceRGB, c_void_p)
_csignature(libquartz.CGColorSpaceRelease, c_void, c_void_p)
_csignature(libquartz.CGContextDrawImage, c_void, c_void_p, CGRect, c_void_p)
_csignature(libquartz.CGContextRelease, c_void, c_void_p)
_csignature(libquartz.CGContextSetShouldAntialias, c_void,c_void_p, c_bool)
_csignature(libquartz.CGContextSetTextPosition, c_void, c_void_p, CGFloat, CGFloat)
_csignature(libquartz.CGCursorIsVisible, c_bool)
_csignature(libquartz.CGDataProviderCopyData, c_void_p, c_void_p)
_csignature(libquartz.CGDataProviderCreateWithCFData, c_void_p, c_void_p)
_csignature(libquartz.CGDataProviderRelease, c_void, c_void_p)
_csignature(libquartz.CGDisplayBounds, CGRect, CGDirectDisplayID)
_csignature(libquartz.CGDisplayCapture, CGError, CGDirectDisplayID)
_csignature(libquartz.CGDisplayCopyAllDisplayModes, c_void_p, CGDirectDisplayID, c_void_p)
_csignature(libquartz.CGDisplayCopyDisplayMode, c_void_p, CGDirectDisplayID)
_csignature(libquartz.CGDisplayIDToOpenGLDisplayMask, c_uint32, c_uint32)
_csignature(libquartz.CGDisplayModeCopyPixelEncoding, c_void_p, c_void_p)
_csignature(libquartz.CGDisplayModeGetHeight, c_size_t, c_void_p)
_csignature(libquartz.CGDisplayModeGetRefreshRate, c_double, c_void_p)
_csignature(libquartz.CGDisplayModeGetWidth, c_size_t, c_void_p)
_csignature(libquartz.CGDisplayModeRelease, c_void, c_void_p)
_csignature(libquartz.CGDisplayModeRetain, c_void_p, c_void_p)
_csignature(libquartz.CGDisplayMoveCursorToPoint, CGError, CGDirectDisplayID, CGPoint)
_csignature(libquartz.CGDisplayRelease, CGError, CGDirectDisplayID)
_csignature(libquartz.CGDisplaySetDisplayMode, CGError, CGDirectDisplayID, c_void_p, c_void_p)
_csignature(libquartz.CGFontCreateWithDataProvider, c_void_p, c_void_p)
_csignature(libquartz.CGFontCreateWithFontName, c_void_p, c_void_p)
_csignature(libquartz.CGGetActiveDisplayList, CGError, c_uint32, POINTER(CGDirectDisplayID), POINTER(c_uint32))
_csignature(libquartz.CGImageCreate, c_void_p, c_size_t, c_size_t, c_size_t, c_size_t, c_size_t, c_void_p, c_uint32, c_void_p, c_void_p, c_bool, c_int)
_csignature(libquartz.CGImageGetBitmapInfo, CGBitmapInfo, c_void_p)
_csignature(libquartz.CGImageGetBitsPerPixel, c_size_t, c_void_p)
_csignature(libquartz.CGImageGetBytesPerRow, c_size_t, c_void_p)
_csignature(libquartz.CGImageGetDataProvider, c_void_p, c_void_p)
_csignature(libquartz.CGImageGetHeight, c_size_t, c_void_p)
_csignature(libquartz.CGImageGetWidth, c_size_t, c_void_p)
_csignature(libquartz.CGImageRelease, c_void, c_void_p)
_csignature(libquartz.CGImageSourceCopyPropertiesAtIndex, c_void_p, c_void_p, c_size_t, c_void_p)
_csignature(libquartz.CGImageSourceCreateImageAtIndex, c_void_p, c_void_p, c_size_t, c_void_p)
_csignature(libquartz.CGImageSourceCreateWithData, c_void_p, c_void_p, c_void_p)
_csignature(libquartz.CGMainDisplayID, CGDirectDisplayID)
_csignature(libquartz.CGShieldingWindowLevel, c_int32)
_csignature(libquartz.CGWarpMouseCursorPosition, CGError, CGPoint)

# CORETEXT
libCT = get_lib('CoreText')

# Types
CTFontOrientation    = c_uint32  # CTFontDescriptor.h
CTFontSymbolicTraits = c_uint32  # CTFontTraits.h

# CoreText constants
kCTFontAttributeName       = c_void_p.in_dll(libCT, 'kCTFontAttributeName')
kCTFontFamilyNameAttribute = c_void_p.in_dll(libCT, 'kCTFontFamilyNameAttribute')
kCTFontSymbolicTrait       = c_void_p.in_dll(libCT, 'kCTFontSymbolicTrait')
kCTFontWeightTrait         = c_void_p.in_dll(libCT, 'kCTFontWeightTrait')
kCTFontTraitsAttribute     = c_void_p.in_dll(libCT, 'kCTFontTraitsAttribute')

# constants from CTFontTraits.h
kCTFontItalicTrait = (1 << 0)
kCTFontBoldTrait   = (1 << 1)

_csignature(libCT.CTFontCreateWithGraphicsFont, c_void_p, c_void_p, CGFloat, c_void_p, c_void_p)
_csignature(libCT.CTFontCopyFamilyName, c_void_p, c_void_p)
_csignature(libCT.CTFontCopyFullName, c_void_p, c_void_p)
_csignature(libCT.CTLineCreateWithAttributedString, c_void_p, c_void_p)
_csignature(libCT.CTFontCreateWithFontDescriptor, c_void_p, c_void_p, CGFloat, c_void_p)
_csignature(libCT.CTFontDescriptorCreateWithAttributes, c_void_p, c_void_p)
_csignature(libCT.CTFontGetBoundingRectsForGlyphs, CGRect, c_void_p, CTFontOrientation, POINTER(CGGlyph), POINTER(CGRect), CFIndex)
_csignature(libCT.CTFontGetAdvancesForGlyphs, c_double, c_void_p, CTFontOrientation, POINTER(CGGlyph), POINTER(CGSize), CFIndex)
_csignature(libCT.CTFontGetAscent, CGFloat, c_void_p)
_csignature(libCT.CTFontGetDescent, CGFloat, c_void_p)
_csignature(libCT.CTFontGetGlyphsForCharacters, c_bool, c_void_p, POINTER(UniChar), POINTER(CGGlyph), CFIndex)
_csignature(libCT.CTFontGetSymbolicTraits, CTFontSymbolicTraits, c_void_p)
_csignature(libCT.CTLineDraw, c_void, c_void_p, c_void_p)

# FOUNDATION
libF = get_lib('Foundation')

_csignature_variadic(libF.NSLog, c_void, c_char_p)  # ... like printf(format, ...)
_csignature(libF.NSMouseInRect, c_bool, NSPoint, NSRect, c_bool)  # CORETEXT

# VLC KIT
libVLCKit = get_lib('VLCKit')

# objC
libobjc = get_lib('objc')

# BOOL class_addIvar(Class cls, const char *name, size_t size, uint8_t alignment, const char *types)
_csignature(libobjc.class_addIvar, c_bool, Class, c_char_p, c_size_t, c_uint8, c_char_p)
# BOOL class_addMethod(Class cls, SEL name, IMP imp, const char *types)
_csignature(libobjc.class_addMethod, c_bool, Class, SEL, IMP, c_char_p)
# BOOL class_addProtocol(Class cls, Protocol *protocol)
_csignature(libobjc.class_addProtocol, c_bool, Class, Protocol)
# BOOL class_conformsToProtocol(Class cls, Protocol *protocol)
_csignature(libobjc.class_conformsToProtocol, c_bool, Class, Protocol)
# Ivar * class_copyIvarList(Class cls, unsigned int *outCount)
# Returns an array of pointers of type Ivar describing instance variables.
# The array has *outCount pointers, NULL terminated.  You must free() the returned array!
_csignature_list(libobjc.class_copyIvarList, POINTER(Ivar), Class, POINTER(c_uint))
# Method * class_copyMethodList(Class cls, unsigned int *outCount)
# Returns an array of pointers of type Method describing instance methods.
# The array has *outCount pointers, NULL terminated.  You must free() the returned array!
_csignature_list(libobjc.class_copyMethodList, POINTER(Method), Class, POINTER(c_uint))
# objc_property_t *class_copyPropertyList(Class cls, unsigned int *outCount)
# Returns an array of pointers of type objc_property_t describing properties.
# The array has *outCount pointers, NULL terminated.  You must free() the returned array!
_csignature_list(libobjc.class_copyPropertyList, POINTER(objc_property_t), Class, POINTER(c_uint))
# Protocol ** class_copyProtocolList(Class cls, unsigned int *outCount)
# Returns an array of pointers of type Protocol* describing protocols.
# The array has *outCount pointers, NULL terminated.  You must free() the returned array!
_csignature_list(libobjc.class_copyProtocolList, POINTER(Protocol), Class, POINTER(c_uint))
# id class_createInstance(Class cls, size_t extraBytes)
_csignature(libobjc.class_createInstance, Id, Class, c_size_t)
# Method class_getClassMethod(Class aClass, SEL aSelector)
# Will also search superclass for implementations.
_csignature(libobjc.class_getClassMethod, Method, Class, SEL)
# Ivar class_getClassVariable(Class cls, const char* name)
_csignature(libobjc.class_getClassVariable, Ivar, Class, c_char_p)
# Method class_getInstanceMethod(Class aClass, SEL aSelector)
# Will also search superclass for implementations.
_csignature(libobjc.class_getInstanceMethod, Method, Class, SEL)
# size_t class_getInstanceSize(Class cls)
_csignature(libobjc.class_getInstanceSize, c_size_t, Class)
# Ivar class_getInstanceVariable(Class cls, const char* name)
_csignature(libobjc.class_getInstanceVariable, Ivar, Class, c_char_p)
# const char *class_getIvarLayout(Class cls)
_csignature(libobjc.class_getIvarLayout, c_char_p, Class)
# IMP class_getMethodImplementation(Class cls, SEL name)
_csignature(libobjc.class_getMethodImplementation, IMP, Class, SEL)
# IMP class_getMethodImplementation_stret(Class cls, SEL name)
_csignature(libobjc.class_getMethodImplementation_stret, IMP, Class, SEL)
# const char * class_getName(Class cls)
_csignature(libobjc.class_getName, c_char_p, Class)
# objc_property_t class_getProperty(Class cls, const char *name)
_csignature(libobjc.class_getProperty, objc_property_t, Class, c_char_p)
# Class class_getSuperclass(Class cls)
_csignature(libobjc.class_getSuperclass, Class, Class)
# int class_getVersion(Class theClass)
_csignature(libobjc.class_getVersion, c_int, Class)
# const char *class_getWeakIvarLayout(Class cls)
_csignature(libobjc.class_getWeakIvarLayout, c_char_p, Class)
# BOOL class_isMetaClass(Class cls)
_csignature(libobjc.class_isMetaClass, c_bool, Class)
# IMP class_replaceMethod(Class cls, SEL name, IMP imp, const char *types)
_csignature(libobjc.class_replaceMethod, IMP, Class, SEL, IMP, c_char_p)
# BOOL class_respondsToSelector(Class cls, SEL sel)
_csignature(libobjc.class_respondsToSelector, c_bool, Class, SEL)
# void class_setIvarLayout(Class cls, const char *layout)
_csignature(libobjc.class_setIvarLayout, c_void, Class, c_char_p)
# Class class_setSuperclass(Class cls, Class newSuper)
_csignature(libobjc.class_setSuperclass, Class, Class, Class)
# void class_setVersion(Class theClass, int version)
_csignature(libobjc.class_setVersion, c_void, Class, c_int)
# void class_setWeakIvarLayout(Class cls, const char *layout)
_csignature(libobjc.class_setWeakIvarLayout, c_void, Class, c_char_p)

# const char * ivar_getName(Ivar ivar)
_csignature(libobjc.ivar_getName, c_char_p, Ivar)
# ptrdiff_t ivar_getOffset(Ivar ivar)
_csignature(libobjc.ivar_getOffset, c_ptrdiff_t, Ivar)
# const char * ivar_getTypeEncoding(Ivar ivar)
_csignature(libobjc.ivar_getTypeEncoding, c_char_p, Ivar)

# char * method_copyArgumentType(Method method, unsigned int index).
# You must free() the returned string!
_csignature_str(libobjc.method_copyArgumentType, c_char_p, Method, c_uint)
# char * method_copyReturnType(Method method).
# You must free() the returned string, but can't despite the documentation
# http://Developer.Apple.com/documentation/objectivec/1418777-method_copyreturntype
_csignature(libobjc.method_copyReturnType, c_char_p, Method)
# void method_exchangeImplementations(Method m1, Method m2)
_csignature(libobjc.method_exchangeImplementations, c_void, Method, Method)
# void method_getArgumentType(Method method, unsigned int index, char *dst, size_t dst_len)
# Functionally similar to strncpy(dst, parameter_type, dst_len).
_csignature(libobjc.method_getArgumentType, c_void, Method, c_uint, c_char_p, c_size_t)
# IMP method_getImplementation(Method method)
_csignature(libobjc.method_getImplementation, IMP, Method)
# SEL method_getName(Method method)
_csignature(libobjc.method_getName, SEL, Method)
# unsigned method_getNumberOfArguments(Method method)
_csignature(libobjc.method_getNumberOfArguments, c_uint, Method)
# void method_getReturnType(Method method, char *dst, size_t dst_len)
# Functionally similar to strncpy(dst, return_type, dst_len)
_csignature(libobjc.method_getReturnType, c_void, Method, c_char_p, c_size_t)
# const char * method_getTypeEncoding(Method method)
_csignature(libobjc.method_getTypeEncoding, c_char_p, Method)
# IMP method_setImplementation(Method method, IMP imp)
_csignature(libobjc.method_setImplementation, IMP, Method, IMP)

# Class objc_allocateClassPair(Class superclass, const char *name, size_t extraBytes)
_csignature(libobjc.objc_allocateClassPair, Class, Class, c_char_p, c_size_t)
# Protocol **objc_copyProtocolList(unsigned int *outCount)
# Returns an array of *outcount pointers NULL terminated.  You must free() the array!
_csignature_list(libobjc.objc_copyProtocolList, POINTER(Protocol), POINTER(c_uint))
# id objc_getAssociatedObject(id object, void *key)
_csignature(libobjc.objc_getAssociatedObject, Id, Id, c_void_p)
# Class objc_getClass(const char *name)
_csignature(libobjc.objc_getClass, Class, c_char_p)
# int objc_getClassList(Class *buffer, int bufferLen)
# Pass None for buffer to obtain just the total number of classes.
_csignature(libobjc.objc_getClassList, c_int, Class, c_int)
# Class objc_getMetaClass(const char *name)
_csignature(libobjc.objc_getMetaClass, Class, c_char_p)
# Protocol *objc_getProtocol(const char *name)
_csignature(libobjc.objc_getProtocol, Protocol, c_char_p)
# You should set return and argument types depending on context.
# id objc_msgSend(id theReceiver, SEL theSelector, ...)
# id objc_msgSendSuper(struct objc_super *super, SEL op,  ...)
# void objc_msgSendSuper_stret(struct objc_super *super, SEL op, ...)
_csignature_variadic(libobjc.objc_msgSendSuper_stret, c_void)
# double objc_msgSend_fpret(id self, SEL op, ...)
_csignature_variadic(libobjc.objc_msgSend_fpret, c_float)  # c_float, c_longdouble
# void objc_msgSend_stret(void * stretAddr, id theReceiver, SEL theSelector,  ...)
_csignature_variadic(libobjc.objc_msgSend_stret, c_void)
# void objc_registerClassPair(Class cls)
_csignature(libobjc.objc_registerClassPair, c_void, Class)
# void objc_removeAssociatedObjects(id object)
_csignature(libobjc.objc_removeAssociatedObjects, c_void, Id)
# void objc_setAssociatedObject(id object, void *key, id value, objc_AssociationPolicy policy)
_csignature(libobjc.objc_setAssociatedObject, c_void, Id, c_void_p, Id, c_int)

# id object_copy(id obj, size_t size)
_csignature(libobjc.object_copy, Id, Id, c_size_t)
# id object_dispose(id obj)
_csignature(libobjc.object_dispose, Id, Id)
# Class object_getClass(id object)
_csignature(libobjc.object_getClass, Class, Id)
# const char *object_getClassName(id obj)
_csignature(libobjc.object_getClassName, c_char_p, Id)
# Ivar object_getInstanceVariable(id obj, const char *name, void **outValue)
_csignature(libobjc.object_getInstanceVariable, Ivar, Id, c_char_p, c_void_p)
# id object_getIvar(id object, Ivar ivar)
_csignature(libobjc.object_getIvar, Id, Id, Ivar)
# Class object_setClass(id object, Class cls)
_csignature(libobjc.object_setClass, c_void_p, c_void_p, c_void_p)
# Ivar object_setInstanceVariable(id obj, const char *name, void *value)
# Set argtypes based on the data type of the instance variable.
_csignature_variadic(libobjc.object_setInstanceVariable, Ivar)
# void object_setIvar(id object, Ivar ivar, id value)
_csignature(libobjc.object_setIvar, c_void, Id, Ivar, Id)

# const char *property_getAttributes(objc_property_t property)
_csignature(libobjc.property_getAttributes, c_char_p, objc_property_t)
# const char *property_getName(objc_property_t property)
_csignature(libobjc.property_getName, c_char_p, objc_property_t)

# BOOL protocol_conformsToProtocol(Protocol *proto, Protocol *other)
_csignature(libobjc.protocol_conformsToProtocol, c_bool, Protocol, Protocol)
# struct objc_method_description protocol_getMethodDescription(Protocol *p, SEL aSel, BOOL isRequiredMethod, BOOL isInstanceMethod)
_csignature(libobjc.protocol_getMethodDescription, objc_method_description, c_void_p, c_void_p, c_bool, c_bool)
# struct objc_method_description *protocol_copyMethodDescriptionList(Protocol *p, BOOL isRequiredMethod,
#                                 BOOL isInstanceMethod, unsigned int *outCount).  You must free() the returned array!
_csignature_list(libobjc.protocol_copyMethodDescriptionList, POINTER(objc_method_description), Protocol, c_bool, c_bool, POINTER(c_uint))
# objc_property_t * protocol_copyPropertyList(Protocol *protocol, unsigned int *outCount)
_csignature_list(libobjc.protocol_copyPropertyList, POINTER(objc_property_t), Protocol, POINTER(c_uint))
# Protocol **protocol_copyProtocolList(Protocol *proto, unsigned int *outCount)
_csignature_list(libobjc.protocol_copyProtocolList, POINTER(Protocol), Protocol, POINTER(c_uint))
# const char *protocol_getName(Protocol *p)
_csignature(libobjc.protocol_getName, c_char_p, Protocol)

# const char* sel_getName(SEL aSelector)
_csignature(libobjc.sel_getName, c_char_p, SEL)
# SEL sel_getUid(const char *str)
# Use sel_registerName instead.
# BOOL sel_isEqual(SEL lhs, SEL rhs)
_csignature(libobjc.sel_isEqual, c_bool, SEL, SEL)
# SEL sel_registerName(const char *str)
_csignature(libobjc.sel_registerName, SEL, c_char_p)

# filter locals() for .__init__.py
__all__ = tuple(_ for _ in locals().keys() if _.startswith((
          'CF', 'CG', 'ct', 'CTF', 'kCF', 'kCG', 'kCTF', 'NS'  # 'lib'
          ))) + ('get_lib', 'leaked2')

if __name__ == '__main__':

    from octypes import _allist

    _allist(__all__, locals(), __version__, __file__)
