
# -*- coding: utf-8 -*-

# License at the end of this file.

'''ObjC classes C{NS...} and conversions from C{NS...} ObjC to Python instances.

@var NSMain: Global C{NS...} singletons (C{const} or C{property}).
@var NSMain.Application: Get the C{NSApplication.sharedApplication}.
@var NSMain.BooleanNO: Get C{NSBoolean(NO)}.
@var NSMain.BooleanYES: Get C{NSBoolean(YES)}.
@var NSMain.Bundle: Get the C{NSBundle.mainBundle}.
@var NSMain.BundleName: Get the C{NS/CFBundleName}.
@var NSMain.FontManager: Get the C{NSFontManager.sharedFontManager}.
@var NSMain.LayoutManager: Get the C{NSLayoutManager}.
@var NSMain.NO_false: Get C{NSfalse/NO}.
@var NSMain.Null: Get the C{NSNull}.
@var NSMain.PrintInfo: Get the C{NSPrintInfo}.
@var NSMain.Screen: Get the C{NSScreen.mainScreen}.
@var NSMain.ScreenBottomLeft: Get the C{NSScreen.mainScreen.frame} lower left corner as C{NSPoint_t}.
@var NSMain.ScreenBottomRight: Get the C{NSScreen.mainScreen.frame} lower right corner as C{NSPoint_t}.
@var NSMain.ScreenCenter: Get the C{NSScreen.mainScreen.frame} center as C{NSPoint_t}.
@var NSMain.ScreenFrame: Get the C{NSScreen.mainScreen.frame} as C{NSRect_t}.
@var NSMain.ScreenSize: Get the C{NSScreen.mainScreen.frame.size} as C{NSSize_t}.
@var NSMain.ScreenTopLeft: Get the C{NSScreen.mainScreen.frame} upper left corner as C{NSPoint_t}.
@var NSMain.ScreenTopRight: Get the C{NSScreen.mainScreen.frame} upper right corner as C{NSPoint_t}.
@var NSMain.TableColumn: Get a blank C{NSTableColumn}.
@var NSMain.YES_true: Get C{NStrue/YES}.
@var NSMain.nil: Get C{NSnil}.
@var NSMain.stdlog: Get the standard log file (C{stdout}, C{stderr}, other).
@var NSMain.versionstr: Get the PyCocoa, Python, macOS versions as C{str}.
'''
# all imports listed explicitly to help PyChecker
from pycocoa.getters import get_selector
from pycocoa.lazily  import _ALL_LAZY
from pycocoa.octypes import Array_t, Class_t, c_struct_t, Id_t, NSPoint_t, \
                            NSRect4_t, ObjC_t, SEL_t, Set_t
from pycocoa.oslibs  import cfNumber2bool, cfNumber2num, cfString, cfString2str, \
                            cfURLResolveAlias, libCF, libFoundation, libobjc, \
                            NO, YES
from pycocoa.runtime import isObjCInstanceOf, ObjCClass, ObjCInstance, release, \
                            retain, send_message, _Xargs
from pycocoa.utils   import _all_versionstr, bytes2str, _ByteStrs, clip, _Globals, \
                            isinstanceOf, iterbytes, lambda1, missing, property_RO, \
                            _Singletons, _Types

from ctypes import ArgumentError, byref, cast, c_byte, CFUNCTYPE, c_void_p
from datetime import datetime as _datetime
from decimal import Decimal as _Decimal
from os import linesep, path as os_path
from time import time as _timestamp

__all__ = _ALL_LAZY.nstypes
__version__ = '20.11.15'

# some commonly used Foundation and Cocoa classes, described here
# <https://OMZ-Software.com/pythonista/docs/ios/objc_util.html>

# NS... classes marked ** have Python versions, like NSStr, for
# for use by runtime.isObjCInstanceOf repectively utils.isinstanceOf
NSAlert                = ObjCClass('NSAlert')
NSApplication          = ObjCClass('NSApplication')
# NSApplicationDelegate  = ObjCClass('_NSApplicationDelegate')  # see .apps
NSArray                = ObjCClass('NSArray')  # immutable
NSAttributedString     = ObjCClass('NSAttributedString')
NSAutoreleasePool      = ObjCClass('NSAutoreleasePool')
NSBezierPath           = ObjCClass('NSBezierPath')
NSBundle               = ObjCClass('NSBundle')
NSColor                = ObjCClass('NSColor')
NSConcreteNotification = ObjCClass('NSConcreteNotification')
NSConstantString       = ObjCClass('NSConstantString')  # use NSStr
NSData                 = ObjCClass('NSData')
NSDecimalNumber        = ObjCClass('NSDecimalNumber')  # ** use NSDecimal
NSDictionary           = ObjCClass('NSDictionary')  # immutable
NSDockTile             = ObjCClass('NSDockTile')
NSEnumerator           = ObjCClass('NSEnumerator')
NSError                = ObjCClass('NSError')
NSException            = ObjCClass('NSException')
NSFont                 = ObjCClass('NSFont')
NSFontDescriptor       = ObjCClass('NSFontDescriptor')
NSFontManager          = ObjCClass('NSFontManager')
NSFontPanel            = ObjCClass('NSFontPanel')
NSImage                = ObjCClass('NSImage')
NSImageView            = ObjCClass('NSImageView')
NSLayoutManager        = ObjCClass('NSLayoutManager')
NSMenu                 = ObjCClass('NSMenu')
NSMenuItem             = ObjCClass('NSMenuItem')
NSMutableArray         = ObjCClass('NSMutableArray')
NSMutableData          = ObjCClass('NSMutableData')
NSMutableDictionary    = ObjCClass('NSMutableDictionary')
NSMutableSet           = ObjCClass('NSMutableSet')
NSMutableString        = ObjCClass('NSMutableString')
NSNotification         = ObjCClass('NSNotification')
NSNotificationCenter   = ObjCClass('NSNotificationCenter')
NSNull                 = ObjCClass('NSNull')
NSNumber               = ObjCClass('NSNumber')
NSObject               = ObjCClass('NSObject')
NSOpenPanel            = ObjCClass('NSOpenPanel')
NSPageLayout           = ObjCClass('NSPageLayout')
# NSPoint              = ObjCClass('NSPoint')  # doesn't exist, use NSPoint_t
NSPrinter              = ObjCClass('NSPrinter')
NSPrintInfo            = ObjCClass('NSPrintInfo')
NSPrintOperation       = ObjCClass('NSPrintOperation')
NSPrintPanel           = ObjCClass('NSPrintPanel')
# NSRect               = ObjCClass('NSRect')  # doesn't exist, use NSRect_t
# NSRange              = ObjCClass('NSRange')  # doesn't exist, use NSRange_t
NSSavePanel            = ObjCClass('NSSavePanel')
NSScreen               = ObjCClass('NSScreen')
NSScrollView           = ObjCClass('NSScrollView')
NSSet                  = ObjCClass('NSSet')
# NSSize               = ObjCClass('NSSize')  # doesn't exist, use NSSize_t
NSStatusBar            = ObjCClass('NSStatusBar')
NSString               = ObjCClass('NSString')  # ** use NSStr or 'at'
NSTableColumn          = ObjCClass('NSTableColumn')
NSTableView            = ObjCClass('NSTableView')
NSTextField            = ObjCClass('NSTextField')
NSTextView             = ObjCClass('NSTextView')
NSThread               = ObjCClass('NSThread')
NSURL                  = ObjCClass('NSURL')
NSView                 = ObjCClass('NSView')
NSWindow               = ObjCClass('NSWindow')

# some other NS... types
NSBoolean  = NSNumber.numberWithBool_
NSDouble   = NSNumber.numberWithDouble_
NSFloat    = NSNumber.numberWithDouble_
NSInt      = NSNumber.numberWithInt_
NSLong     = NSNumber.numberWithLong_
NSLongLong = NSNumber.numberWithLongLong_


def _ns2ctype2py(ns, ctype):
    # helper function
    if not isinstance(ns, ctype):
        ns = ctype(ns)
    return ns2py(ns)


# We need to be able to create raw NSDecimalNumber objects.  If we use
# a normal ObjCClass() wrapper, the return values of constructors will
# be auto-converted back into Python Decimals.  However, we want to
# cache class/selector/method lookups without that overhead every time.
# Originally, an older rev of .../Rubicon-ObjC/objc/core_foundation.py.
class NSDecimal(ObjCInstance):
    '''Optimized, Python C{NSDecimalNumber} class.
    '''
    _Class = NSDecimalNumber
    _IMP   = None
    _pyDec = None
    _SEL   = None

    def __new__(cls, py):
        '''New L{NSDecimal}.

           @param py: The decimal value (C{Decimal}, C{float}, C{int},
                      C{str} or L{NSDecimal}).

           @return: New L{NSDecimal} (L{ObjCInstance}).
        '''
        if isinstance(py, NSDecimal):
            return py

        if None in (cls._IMP, cls._SEL):
            cls._SEL = get_selector('decimalNumberWithString:')
            m = libobjc.class_getClassMethod(cls._Class, cls._SEL)
            m = libobjc.method_getImplementation(m)
            cls._IMP = cast(m, CFUNCTYPE(Id_t, Id_t, SEL_t, Id_t))

        py = _Decimal(py)  # from Decimal, float, int, str
        t = NSStr(py.to_eng_string())  # maintains accuracy
        d = cls._IMP(cast(cls._Class, Id_t), cls._SEL, t)
        t.release()  # PYCHOK expected
        self = super(NSDecimal, cls).__new__(cls, d)
        self._pyDec = py
        return self

    def __str__(self):
        return '%s(%s)' % (self.objc_classname, self.value)

    @property_RO
    def double(self):
        '''Get this L{NSDecimal} as a Python C{float}.
        '''
        return self.doubleValue()  # PYCHOK expected

#   @property_RO
#   def objc_classname(self):
#       return self.__class__.__name__

    @property_RO
    def value(self):
        '''Get this L{NSDecimal} as a Python C{Decimal}.
        '''
        return self._pyDec

    Decimal = value


class NSExceptionError(RuntimeError):
    '''Python Error wrapping an C{ObjC/NSexception}.

       Used for I{uncaught} C{ObjC/NSexception}, see
       L{setUncaughtExceptionHandler}.
    '''
    _dt_fmt     = '%04d-%02d-%02d %02d:%02d:%06.3f'
    NS          = None
    _timestamp  = None

    def __init__(self, nsExc=None):
        if nsExc:
            self.NS = nsExc
        self._timestamp = _timestamp()
        n = self.name or NSExceptionError.__name__
        r = self.reason or 'unknown'
        RuntimeError.__init__(self, 'ObjC/%s: %s' % (n, r))

    @property_RO
    def datetime(self):
        '''Get the time stamp as "YYYY-MM-DD HH:MM:SS.MIL" (C{str}).
        '''
        t = _datetime.fromtimestamp(self.timestamp)
        return self._dt_fmt % t.timetuple()[:6]

    @property_RO
    def name(self):
        '''Get the name of the exception (C{str}).
        '''
        return self.NS.name if self.NS else ''

    @property_RO
    def info(self):
        '''Get additional info about the exception (C{str}) or C{None}.
        '''
        return ns2py(self.NS.userInfo(), dflt=None) if self.NS else None

    @property_RO
    def reason(self):
        '''Get the reason the exception (C{str}) or C{None}.
        '''
        return ns2py(self.NS.reason(), dflt=None) if self.NS else None

    @property_RO
    def callstack(self):
        '''Get the callstack of this exception (C{iter}), most recent last.
        '''
        if self.NS:
            for s in nsIter(self.NS.callStackSymbols()):
                s = ns2py(s).rstrip()
                if s:
                    yield s

    @property_RO
    def timestamp(self):
        '''Get the time stamp of this exception (C{float}).
        '''
        return self._timestamp

    @property_RO
    def versionstr(self):
        '''Get the PyCocoa, Python, etc. versions (C{str}).
        '''
        return NSMain.versionstr


class _NSMain(_Singletons):
    '''Global C{NS...} singletons.
    '''
    _Application   =  None  # NSApplication, see .utils._Globals.App
    _BooleanNO     =  None
    _BooleanYES    =  None
    _Bundle        =  None
    _BundleName    =  None
    _FontManager   =  None
    _LayoutManager =  None
    _nil           =  None  # final
    _NO_false      =  NO  # c_byte
    _Null          =  None
    _PrintInfo     =  None
    _Screen        =  None
    _TableColumn   =  None
    _YES_true      =  YES  # c_byte
    _versionstr    = _all_versionstr()

    # all globals are properties to delay instantiation

    @property_RO
    def Application(self):
        '''Get the C{NSApplication.sharedApplication}.
        '''
        if self._Application is None:
            _NSMain._Application = retain(NSApplication.sharedApplication())
        return self._Application

    @property_RO
    def BooleanNO(self):
        '''Get C{NSBoolean(NO)}.
        '''
        if self._BooleanNO is None:
            _NSMain._BooleanNO = retain(NSBoolean(NO))
        return self._BooleanNO

    @property_RO
    def BooleanYES(self):
        '''Get C{NSBoolean(YES)}.
        '''
        if self._BooleanYES is None:
            _NSMain._BooleanYES = retain(NSBoolean(YES))
        return self._BooleanYES

    @property_RO
    def Bundle(self):
        '''Get the C{NSBundle.mainBundle}.
        '''
        if self._Bundle is None:
            _NSMain._Bundle = retain(NSBundle.mainBundle())
        return self._Bundle

    @property_RO
    def BundleName(self):
        '''Get the C{NS/CFBundleName}.
        '''
        if self._BundleName is None:
            _NSMain._BundleName = retain(NSStr('CFBundleName'))
        return self._BundleName

    @property_RO
    def FontManager(self):
        '''Get the C{NSFontManager.sharedFontManager}.
        '''
        if self._FontManager is None:
            _NSMain._FontManager = retain(NSFontManager.sharedFontManager())
        return self._FontManager

    @property_RO
    def LayoutManager(self):
        '''Get the C{NSLayoutManager}.
        '''
        if self._LayoutManager is None:
            _NSMain._LayoutManager = retain(NSLayoutManager.alloc().init())
        return self._LayoutManager

    @property_RO
    def nil(self):
        '''Get C{NSnil}.
        '''
        return self._nil

    @property_RO
    def NO_false(self):
        '''Get C{NSfalse/NO}.
        '''
        return self._NO_false

    @property_RO
    def Null(self):
        '''Get the C{NSNull}.
        '''
        if self._Null is None:
            _NSMain._Null = retain(NSNull.alloc().init())
        return self._Null

    @property_RO
    def PrintInfo(self):
        '''Get the C{NSPrintInfo}.
        '''
        if self._PrintInfo is None:
            _NSMain._PrintInfo = retain(NSPrintInfo.sharedPrintInfo())
        return self._PrintInfo

    @property_RO
    def Screen(self):
        '''Get the C{NSScreen.mainScreen}.
        '''
        if self._Screen is None:
            _NSMain._Screen = retain(NSScreen.alloc().init().mainScreen())
        return self._Screen

    @property_RO
    def ScreenBottomLeft(self):
        '''Get the C{NSScreen.mainScreen.frame} lower left corner as C{NSPoint_t}.
        '''
        return self.ScreenFrame.origin

    @property_RO
    def ScreenBottomRight(self):
        '''Get the C{NSScreen.mainScreen.frame} lower right corner as C{NSPoint_t}.
        '''
        f = self.ScreenFrame
        return NSPoint_t(f.size.width, f.origin.y)

    def ScreenCascade(self, fraction=0.1):
        '''Return a screen point off the upper left corner.

           @param fraction: Cascade off the upper left corner (C{float}).

           @return: The screen point (C{NSPoint_t}).
        '''
        p = self.ScreenTopLeft
        if 0 < fraction <= 1:
            z = self.ScreenSize
            p = NSPoint_t(p.x + fraction * z.width, p.y - fraction * z.height)
        return p

    @property_RO
    def ScreenCenter(self):
        '''Get the C{NSScreen.mainScreen.frame} center as C{NSPoint_t}.
        '''
        z = self.ScreenSize
        return NSPoint_t(z.width / 2, z.height / 2)

    @property_RO
    def ScreenFrame(self):
        '''Get the C{NSScreen.mainScreen.frame} as C{NSRect_t}.
        '''
        return self.Screen.frame()

    @property_RO
    def ScreenSize(self):
        '''Get the C{NSScreen.mainScreen.frame.size} as C{NSSize_t}.
        '''
        return self.ScreenFrame.size

    @property_RO
    def ScreenTopLeft(self):
        '''Get the C{NSScreen.mainScreen.frame} upper left corner as C{NSPoint_t}.
        '''
        f = self.ScreenFrame
        return NSPoint_t(f.origin.x, f.size.height)

    @property_RO
    def ScreenTopRight(self):
        '''Get the C{NSScreen.mainScreen.frame} upper right corner as C{NSPoint_t}.
        '''
        f = self.ScreenFrame
        return NSPoint_t(f.size.width, f.origin.y)

    @property
    def stdlog(self):
        '''Get the standard log file (C{stdout}, C{stderr}, other).
        '''
        return _Globals.stdlog

    @stdlog.setter  # PYCHOK property.setter
    def stdlog(self, file):
        '''Set the standard log file (C{file}-type).

           @raise TypeError: File B{C{file}} doesn't have callable
                             C{write} and C{flush} attributes.
        '''
        try:
            if file and callable(file.write) and callable(file.flush):
                _Globals.stdlog = file
            else:
                raise AttributeError('non-callable')
        except AttributeError as x:
            raise TypeError('%s %s: %r' % (str(x), 'file', file))

    @property_RO
    def TableColumn(self):
        '''Get a blank C{NSTableColumn}.
        '''
        if self._TableColumn is None:
            _NSMain._TableColumn = retain(NSTableColumn.alloc().init())
        return self._TableColumn

    @property_RO
    def versionstr(self):
        '''Get the PyCocoa, Python, macOS versions as C{str}.
        '''
        return self._versionstr

    @property_RO
    def YES_true(self):
        '''Get C{NStrue/YES}.
        '''
        return self._YES_true

    def items(self):  # PYCHOK signature
        '''Yield 2-tuple (name, value) for each property.
        '''
        xs = (n for n in dir(_NSMain) if n.startswith('Screen'))
        return _Singletons.items(self, 'stdlog', *xs)

NSMain = _NSMain()  # PYCHOK global C{NS...} singletons or constants


class NSStr(ObjCInstance):
    '''Python wrapper for the ObjC C{NS[Constant]String}.
    '''
    _str = None

    def __new__(cls, ustr):
        '''New L{NSStr} wrapping C{NS[Constant]String}.

           @param ustr: The string value (C{str} or C{unicode}).

           @return: The string (L{NSStr}).
        '''
        self = super(NSStr, cls).__new__(cls, cfString(ustr))
        self._str = bytes2str(ustr)
        # L{ObjCinstance} caches ObjC objects using the
        # objc_ptr.value as key, which may or may not
        # create in a singleton for each string value,
        # retaining strings seems to help singletons.
        return self if len(ustr) > 1 else retain(self)

    def __eq__(self, other):
        return isinstance(other, NSStr) and self.str == other.str

    def __hash__(self):  # XXX needed for .__eq__ and .__ne__
        return hash(self.str)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return '%s(%r)' % (self.objc_classname, clip(self.value))

#   @property_RO
#   def objc_classname(self):
#       '''Get the ObjC class name (C{str}).
#       '''
#       return self.__class__.__name__

    @property_RO
    def value(self):
        '''Get the original string value (C{str}).
        '''
        return self._str

    str = value


class at(NSStr):
    '''Acronym L{NSStr}.
    '''
    # XXX Other possible names for this method: at, ampersat, arobe,
    # apenstaartje (little monkey tail), strudel, klammeraffe (spider
    # monkey), little_mouse, arroba, sobachka (doggie), malpa (monkey),
    # snabel (trunk), papaki (small duck), afna (monkey), kukac (caterpillar).
    pass


def isAlias(path):
    '''Resolve a macOS file or folder alias.

       @param path: The alias name (C{str} or L{NSStr}).

       @return: The alias' target (C{str}) or C{None} if I{path}
                isn't a macOS alias.

       @see: U{mac-alias<https://GitHub.com/al45tair/mac_alias>} and
             U{here<https://StackOverflow.com/questions/21150169>}.
    '''
    if isinstance(path, _ByteStrs):
        path = release(NSStr(path))
    elif isinstanceOf(path, NSStr, name='path'):
        pass

    u = NSURL.alloc().initFileURLWithPath_(path)
    r = cfURLResolveAlias(u)  # URL_t
    u.release()
    if r:
        u = ObjCInstance(r)  # URL_t to NSURL
        r = cfString2str(u.path())
        u.release()
    return r


def isLink(path):
    '''Resolve a file or folder link or alias.

       @param path: The link or alias name (C{str} or L{NSStr}).

       @return: The link's or alias' target (C{str}) or
                C{None} if I{path} isn't a link or alias.
    '''
    if isinstance(path, _ByteStrs):
        p = path
    elif isinstanceOf(path, NSStr, name='path'):
        p = path.str
    r = os_path.islink(p)
    if r:
        r = os_path.realpath(p)
    else:
        r = isAlias(path)
    return r


def isNone(obj):
    '''Return True if I{obj} is C{None, NSMain.nil, NSMain.Null}, etc.

       @param obj: The object (L{ObjCInstance}).

       @return: True or False (C{bool}).
    '''
    return obj in (None, NSMain.nil, NSMain.Null)


def nsArray2listuple(ns, ctype=Array_t):  # XXX an NS*Array method?
    '''Create a Python C{list} or C{tuple} from an C{NS[Mutable]Array}.

       @param ns: The C{NS[Mutable]Array} (L{ObjCInstance}).
       @keyword ctype: The array item type (C{ctypes}).

       @return: The array (C{list} or C{tuple}).
    '''
    # XXX order is critial, NSMutableArray before NSArray
    if isObjCInstanceOf(ns, NSMutableArray, NSArray, name='ns') is NSMutableArray:
        t = list
    else:
        t = tuple
    n = libCF.CFArrayGetCount(ns)
    f = libCF.CFArrayGetValueAtIndex
    return t(_ns2ctype2py(f(ns, i), ctype) for i in range(n))


def nsBoolean2bool(ns, dflt=missing):  # XXX an NSBoolean method?
    '''Create a Python C{bool} from an C{NSBoolean}.

       @param ns: The C{NSBoolean} (L{ObjCInstance}).
       @keyword dflt: Default for a missing, unobtainable value (C{missing}).

       @return: The bool (C{bool}) of I{dlft}.

       @raise TypeError: Unexpected C{NumberType}.
    '''
    # XXX need allow c_void_p for nested booleans in lists, sets, etc.?
    isObjCInstanceOf(ns, NSNumber, c_void_p, name='ns')

    return cfNumber2bool(ns, dflt=dflt)


def nsBundleRename(ns_title, match='Python'):
    '''Change the bundle title if the current title matches.

       @param ns_title: New bundle title (L{NSStr}).
       @keyword match: Optional, previous title to match (C{str}).

       @return: The previous bundle title (C{str}) or None.

       @note: Used to mimick C{NSApplication.setTitle_(ns_title)},
              the name of an L{App} shown in the menu bar.
    '''
    t = ns_title and ns2py(ns_title)
    if t:
        _Globals.argv0 = bytes2str(t)

    # <https://Developer.Apple.com/documentation/
    #        foundation/nsbundle/1495012-bundlewithpath>
    # ns = NSBundle.bundleWithPath_(os.path.abspath(match))
    p, ns = None, NSMain.Bundle
    if ns:
        ns = ns.localizedInfoDictionary() or ns.infoDictionary()
        if ns:
            p = ns.objectForKey_(NSMain.BundleName) or None
            if p:
                p = ns2py(p, dflt='') or ''
                if t and match in (p, '', None):  # can't be empty
                    ns.setObject_forKey_(ns_title, NSMain.BundleName)
    return p


def nsData2bytes(ns, dflt=b''):  # XXX an NSData method?
    '''Create Python C{bytes} from C{NSData}.

       @param ns: The C{NSData} (L{ObjCInstance}).
       @keyword dflt: Default for empty C{NSData} (C{bytes}).

       @return: The bytes (C{bytes}) or I{dflt}.
    '''
    isObjCInstanceOf(ns, NSData, name='ns')
    n = ns.length()
    if n:
        buf = (c_byte * n)()
        ns.getBytes_length_(byref(buf), n)
        return b''.join(iterbytes(buf[:n]))
    return dflt


def nsDecimal2decimal(ns):
    '''Create a Python C{Decimal} from an C{NSDecimalNumber}.

       @param ns: The C{NSDecimalNumber} (L{ObjCInstance}).

       @return: The decimal (C{Decimal}).

       @raise ValueError: If I{ns} not an C{NSNumber}.
    '''
    if isinstance(ns, NSDecimal):
        return ns.Decimal
    return ValueError('%s not %s: %r' % ('ns', 'NSDecimal', ns))


def nsDictionary2dict(ns, ctype_keys=c_void_p, ctype_vals=c_void_p):  # XXX an NS*Dictionary method?
    '''Create a Python C{dict} from an C{NS[Mutable]Dictionary}.

       @param ns: The C{NSDictionary} instance (L{ObjCInstance}).
       @keyword ctype_keys: The dictionary keys type (C{ctypes}).
       @keyword ctype_vals: The dictionary values type (C{ctypes}).

       @return: The dict (C{dict}).
    '''
    # <https://Developer.Apple.com/documentation/corefoundation/cfdictionary-rum>
    n = libCF.CFDictionaryGetCount(ns)
    keys = (ctype_keys * n)()
    vals = (ctype_vals * n)()
    libCF.CFDictionaryGetKeysAndValues(ns, byref(keys), byref(vals))
    return dict((_ns2ctype2py(keys[i], ctype_keys),
                 _ns2ctype2py(vals[i], ctype_vals)) for i in range(n))


def nsIter(ns, reverse=False):
    '''Iterate over an C{NS..} ObjC objects's (reverse) enumerator.

       @param ns: The C{NS..} object to iterate over (L{ObjCInstance}).
       @keyword reverse: Iterate in reverse order (C{bool}), forward otherwise.

       @return: Each object (C{NS...}).
    '''
    if not isNone(ns):
        try:
            if reverse:
                it = ns.reverseObjectEnumerator()
            else:
                it = ns.objectEnumerator()
        except AttributeError:
            raise TypeError('non-iterable: %r' % (ns,))

        while True:
            ns = it.nextObject()  # nil for end
            if isNone(ns):
                break
            yield ns


def nsIter2(ns, reverse=False):
    '''Iterate over an C{NS..} ObjC objects's (reverse) enumerator.

       @param ns: The C{NS..} object to iterate over (L{ObjCInstance}).
       @keyword reverse: Iterate in reverse order (C{bool}), foward otherwise.

       @return: Each object as 2-Tuple (I{py, ns}) where I{py} is a
                Python C{Type} instance and I{ns} the ObjC object C{NS...}.
    '''
    for ns in nsIter(ns, reverse=reverse):
        yield ns2Type(ns), ns


def nsLog(ns_fmt, *ns_args):
    '''Formatted ObjC write to the console.

       @param ns_fmt: A printf-like format string (L{NSStr}).
       @param ns_args: Optional arguments to format (C{all positional}).

       @note: The I{ns_fmt} and all I{ns_args} must be C{NS...} ObjC
              instances.

       @see: Dglessus' U{nslog.py<https://gist.GitHub.com/dgelessus>}.
    '''
    if isinstanceOf(ns_fmt, NSStr, name='ns_fmt'):
        for n, ns in enumerate(ns_args):
            if not isinstance(ns, (ObjCInstance, c_void_p)):
                n = 'ns_arg[%s]' % (n,)  # raise error
                if not isinstanceOf(ns, ObjCInstance, name=n):
                    break
        else:  # XXX all ns_fmt %-types should be %@?
            libFoundation.NSLog(ns_fmt, *ns_args)  # variadic, printf-like


def nsLogf(fmt, *args):
    '''Formatted write to the console.

       @param fmt: A printf-like format string (C{str}).
       @param args: Optional arguments to format (C{all positional}).

       @see: L{nsLog}.
    '''
    if isinstanceOf(fmt, _ByteStrs, name='fmt'):
        if args:
            fmt %= args
        libFoundation.NSLog(NSStr(fmt))  # variadic, printf-like


def nsNull2none(ns):
    '''Return Python C{None} for an C{NS/CFNull} or C{nil}.

       @param ns: The C{NS...} (L{ObjCInstance}).

       @return: The singleton (C{None}).

       @raise ValueError: If I{ns} not C{isNone}.
    '''
    if isObjCInstanceOf(ns, NSNull, c_void_p, name='ns') or isNone(ns):
        return None
    return ValueError('%s not %s: %r' % ('ns', 'isNone', ns))


def nsNumber2num(ns, dflt=missing):  # XXX an NSNumber method?
    '''Create a Python C{Decimal}, C{int} or C{float} from an C{NSNumber}.

       @param ns: The C{NSNumber} (L{ObjCInstance}).
       @keyword dflt: Default for missing, unobtainable value (C{missing}).

       @return: The number (C{Decimal}, C{int} or C{float}).

       @raise TypeError: Unexpected C{NumberType}.

       @raise ValueError: If I{ns} not an C{NSNumber}.
    '''
    # special case for NSDecimal, would become a float
    # since cfType of NSDecimal is kCFNumberDoubleType
    if isinstance(ns, NSDecimal):
        return ns.Decimal
    # XXX need c_void_p for nested numbers in lists, sets, etc.?
    if isObjCInstanceOf(ns, NSNumber, c_void_p, name='ns'):
        return cfNumber2num(ns, dflt=dflt)
    return ValueError('%s not %s: %r' % ('ns', 'NSNumber', ns))


def nsOf(inst):
    '''Return the C{.NS} ObjC object of a Python wrapper or Type instance.

       @param inst: The wrapper (L{ObjCInstance} or C{Python Type}).

       @return: The C{.NS} object (C{NS...}).

       @raise TypeError: No C{.NS} for this I{inst}.
    '''
    try:
        return inst.NS
    except AttributeError:  # see also .bases.NS.setter
        if isinstance(inst, (ObjCInstance, c_struct_t, ObjC_t)):
            return inst  # XXXX ????
    raise TypeError('%s without .NS: %r' % ('inst', inst))


def nsSet2set(ns, ctype=Set_t):  # XXX NS*Set method?
    '''Create a Python C{set} or C{frozenset} from an C{NS[Mutable]Set}.

       @param ns: The C{NS[Mutable]Set} (L{ObjCInstance}).
       @keyword ctype: The set item type (C{ctypes}).

       @return: The set (C{set} or C{frozenset}).
    '''
    if isObjCInstanceOf(ns, NSMutableSet, NSSet, name='ns') is NSSet:
        s = frozenset
    else:
        s = set

    n = libCF.CFSetGetCount(ns)  # == nsSet.count()
    buf = (ctype * n)()
    libCF.CFSetGetValues(ns, byref(buf))
    return s(_ns2ctype2py(buf[i], ctype) for i in range(n))


def nsString2str(ns, dflt=None):  # XXX an NS*String method
    '''Create a Python C{str} or C{unicode} from an C{NS[Mutable]Str[ing]}.

       @param ns: The C{NS[Mutable]Str[ing]} (L{ObjCInstance}).

       @return: The string (C{str} or C{unicode}) or I{dflt}.
    '''
    # XXX need c_void_p for nested strings in lists, sets, etc.?
    if not isinstanceOf(ns, NSStr, c_void_p):
        isObjCInstanceOf(ns, NSConstantString, NSMutableString, NSString,
                             c_void_p, name='ns')

    return cfString2str(ns, dflt=dflt)


def nsTextSize3(text, ns_font=None):
    '''Return the size of a multi-line text.

       @param text: The text (C{str}), including C{linesep}arators.
       @keyword ns_font: The text font (C{NSFont}) or C{None}.

       @return: 3-Tuple (width, height, lines) in (pixels, pixels) or
                in (characters, lines, lines) if I{ns_font} is C{None}.
    '''
    w = ''
    for t in text.split(linesep):
        if len(t) > len(w):
            w = t

    h = n = text.count(linesep) + 1
    if ns_font:
        h *= NSMain.LayoutManager.defaultLineHeightForFont_(ns_font)
        w = ns_font.widthOfString_(release(NSStr(w)))
    else:
        w = len(w)
    return w, h, n


def nsTextView(text, ns_font):
    '''Return an C{NSTextView} for the given text string.
    '''
    # <https://Developer.Apple.com/documentation/appkit/
    #        nsalert/1530575-accessoryview>
    w, h, n = nsTextSize3(text, ns_font=ns_font)
    if n > 50:
        r = NSRect4_t(0, 0, max(300, w), min(800, h))
    else:  # make sure the frame is tall enough to avoid overwritten text
        r = NSRect4_t(0, 0, 300, max(20, min(800, h)))

    # XXX key NSFontAttributeName has a NSString value, no longer a Font?
    # d = NSDictionary.dictionaryWithObject_forKey_(ns_font, NSStr('NSFontAttributeName'))
    # t = NSAttributedString.alloc().initWithString_attributes_(NSStr(text), d)
    ns = NSTextView.alloc().initWithFrame_(r)
    ns.setFont_(ns_font)  # XXX set font BEFORE text
    ns.insertText_(release(NSStr(text)))
    ns.setEditable_(NO)
    ns.setDrawsBackground_(NO)
    if n > 50:  # force scroll view
        ns.setVerticallyResizable_(YES)
        ns.setHorizontallyResizable_(YES)

        r.size.width = min(600, r.size.width)
        sv = NSScrollView.alloc().initWithFrame_(r)
        sv.setHasVerticalScroller_(YES)
        sv.setHasHorizontalScroller_(YES)
        sv.setAutohidesScrollers_(YES)
        sv.setBorderType_(2)  # Border.Bezel or NSBezelBorder
        sv.setDocumentView_(ns)
        ns = sv
    else:
        ns.sizeToFit()
    return ns


def nsThrow(ns_exception):
    '''Mimick ObjC's C{@throw NSException} to raise an exception.

       @param ns_exception: The exception to raise (C{NSException}).
    '''
    # <https://Developer.Apple.com/library/archive/documentation/
    #        Cocoa/Conceptual/Exceptions/Tasks/RaisingExceptions.html>

    # can't use ns_exception.raise() since 'raise' is reserved
    # in Python; see also .runtime.ObjCInstance.__getattr__
    # substituting method name 'throw' for 'raise'.
    send_message(ns_exception, 'raise')


def nsURL2str(ns):
    '''Create a Python C{str} from C{NSURL} string.

       @param ns: The C{CFURL} (L{ObjCInstance}).

       @return: The URL as string (C{str}).
    '''
    if isObjCInstanceOf(ns, NSURL, name='ns'):
        # <https://NSHipster.com/nsurl>
        return nsString2str(ns.absoluteString())


_CFTypeID2py = {libCF.CFArrayGetTypeID():      nsArray2listuple,
                libCF.CFBooleanGetTypeID():    nsBoolean2bool,
                libCF.CFDataGetTypeID():       nsData2bytes,
                libCF.CFDictionaryGetTypeID(): nsDictionary2dict,
                libCF.CFNullGetTypeID():       nsNull2none,
                libCF.CFNumberGetTypeID():     nsNumber2num,
                libCF.CFSetGetTypeID():        nsSet2set,
                libCF.CFStringGetTypeID():     nsString2str,
                libCF.CFURLGetTypeID():        nsURL2str}


def _CFTypeID2py_items():
    for i, ns in _CFTypeID2py.items():
        yield int(i), ns.__name__


def ns2py(ns, dflt=missing):  # XXX an NSObject method?
    '''Convert (an instance of) an ObjC class to an instance of
       the equivalent Python standard type or wrapper and value.

       @param ns: The C{NS...} (L{ObjCInstance}).
       @keyword dflt: Default for unhandled, unexpected C{NS...}s (C{missing}).

       @return: The value (C{Python type}) or I{dflt} if provided.

       @raise TypeError: Unhandled, unexpected C{TypeID}.

       @note: Conversion map:

        - NSArray          -> tuple
        - NSBoolean        -> bool
        - NSConstantString -> str
        - NSData           -> bytes
        - NSDecimalNumber  -> Decimal
        - NSDictionary     -> dict
        - NSMutableArray   -> list
        - NSMutableSet     -> set
        - NSMutableString  -> str
        - NSNumber         -> int or float
        - NSNull           -> None
        - NSSet            -> frozenset
        - NSString         -> str
        - NSStr            -> str

       @see: U{Converting values between Python and Objective-C
              <https://PythonHosted.org/pyobjc/core/typemapping.html>}
    '''
    if ns is None:  # isNone(ns)
        return None

    elif isinstance(ns, NSStr):
        return ns.str

    # see Rubicon-ObjC/objc/core_foundation.py
    # if isinstance(ns, ObjCInstance):
    #     ns = ns._as_parameter_
    try:
        typeID = libCF.CFGetTypeID(ns)
        r = _CFTypeID2py[typeID](ns)
        c = {Class_t: ObjCClass,
             Id_t:    ObjCInstance}.get(type(r), lambda1)
        return c(r)

    except ArgumentError as x:
        _Xargs(x, libCF.CFGetTypeID.__name__,
                  libCF.CFGetTypeID.argtypes,
                  libCF.CFGetTypeID.restype)
        raise

    except KeyError:
        if dflt is missing:
            t = ', '.join('TypeID[%d]: %s' % t for t in
                          sorted(_CFTypeID2py_items()))
            raise TypeError('unhandled %s[%r]: %r {%s}' %
                           ('TypeID', typeID, ns, t))
        return dflt


def ns2Type(ns):
    '''Convert an C{NS...} ObjC object to an instance of
       the corresponding Python Type and value.

       @param ns: The C{NS...} (L{ObjCInstance}).

       @return: The value (C{Python Type}).
    '''
    try:
        return ns.Type(ns)
    except AttributeError:
        pass

    # XXX order is critial, NSMutableArray first
    if isObjCInstanceOf(ns, NSMutableArray) is NSMutableArray:
        _Type = _Types.List
    elif isObjCInstanceOf(ns, NSArray) is NSArray:
        _Type = _Types.Tuple

    # XXX order is critial, NSMutableDictionary first
    elif isObjCInstanceOf(ns, NSMutableDictionary) is NSMutableDictionary:
        _Type = _Types.Dict
    elif isObjCInstanceOf(ns, NSDictionary) is NSDictionary:
        _Type = _Types.FrozenDict

    # XXX order is critial, NSMutableSet first
    elif isObjCInstanceOf(ns, NSMutableSet) is NSMutableSet:
        _Type = _Types.Set
    elif isObjCInstanceOf(ns, NSSet) is NSSet:
        _Type = _Types.FrozenSet

    elif isinstanceOf(ns, NSStr):
        _Type = _Types.Str

    else:
        # printf('ns2Type(%r) -> %s', ns.objc_class, type(ns2py(ns)))
        _Type = ns2py

    # save the Python Type or ns2py convertor at the NS/Class
    # to expedite future conversions of such class instances
    ns.objc_class._Type = _Type
    return _Type(ns)


if __name__ == '__main__':

    from pycocoa.utils import _all_listing

    for n, _ in NSMain.items():
        d = getattr(_NSMain, n).__doc__ or ''
        d = d.split('\n')[0].strip()
        print('@var NSMain.%s: %s' % (n, d))

    _all_listing(__all__, locals())

# % python3 -m pycocoa.nstypes
#
# pycocoa.nstypes.__all__ = tuple(
#  pycocoa.nstypes.at is <class .at>,
#  pycocoa.nstypes.isAlias is <function .isAlias at 0x7fea94e483a0>,
#  pycocoa.nstypes.isLink is <function .isLink at 0x7fea94eec700>,
#  pycocoa.nstypes.isNone is <function .isNone at 0x7fea94eec790>,
#  pycocoa.nstypes.ns2py is <function .ns2py at 0x7fea94eee3a0>,
#  pycocoa.nstypes.ns2Type is <function .ns2Type at 0x7fea94eee430>,
#  pycocoa.nstypes.NSAlert is <ObjCClass(NSAlert of 0x7fff855d8980) at 0x7fea94a80520>,
#  pycocoa.nstypes.NSApplication is <ObjCClass(NSApplication of 0x7fff855d8ac0) at 0x7fea94a805b0>,
#  pycocoa.nstypes.NSArray is <ObjCClass(NSArray of 0x7fff85c4d2a8) at 0x7fea94abf6d0>,
#  pycocoa.nstypes.nsArray2listuple is <function .nsArray2listuple at 0x7fea94eec820>,
#  pycocoa.nstypes.NSAttributedString is <ObjCClass(NSAttributedString of 0x7fff861c2950) at 0x7fea94ad7340>,
#  pycocoa.nstypes.NSAutoreleasePool is <ObjCClass(NSAutoreleasePool of 0x7fff861c2978) at 0x7fea94aa8d60>,
#  pycocoa.nstypes.NSBezierPath is <ObjCClass(NSBezierPath of 0x7fff855d8bd8) at 0x7fea94aa8cd0>,
#  pycocoa.nstypes.NSBoolean is <ObjCBoundClassMethod(Class_t.numberWithBool_) at 0x7fea94e953a0>,
#  pycocoa.nstypes.nsBoolean2bool is <function .nsBoolean2bool at 0x7fea94eec8b0>,
#  pycocoa.nstypes.NSBundle is <ObjCClass(NSBundle of 0x7fff861c2ab8) at 0x7fea94aa8c40>,
#  pycocoa.nstypes.nsBundleRename is <function .nsBundleRename at 0x7fea94eec940>,
#  pycocoa.nstypes.NSColor is <ObjCClass(NSColor of 0x7fff855d9358) at 0x7fea94aa8910>,
#  pycocoa.nstypes.NSConcreteNotification is <ObjCClass(NSConcreteNotification of 0x7fff861bd6a8) at 0x7fea94aa88b0>,
#  pycocoa.nstypes.NSConstantString is <ObjCClass(NSConstantString of 0x7fff861c2e28) at 0x7fea94aa8850>,
#  pycocoa.nstypes.NSData is <ObjCClass(NSData of 0x7fff85c4d370) at 0x7fea94aa8760>,
#  pycocoa.nstypes.nsData2bytes is <function .nsData2bytes at 0x7fea94eec9d0>,
#  pycocoa.nstypes.NSDecimal is <class .NSDecimal>,
#  pycocoa.nstypes.nsDecimal2decimal is <function .nsDecimal2decimal at 0x7fea94eeca60>,
#  pycocoa.nstypes.NSDecimalNumber is <ObjCClass(NSDecimalNumber of 0x7fff861c3058) at 0x7fea94aa8670>,
#  pycocoa.nstypes.NSDictionary is <ObjCClass(NSDictionary of 0x7fff85c4d3e8) at 0x7fea94aa8430>,
#  pycocoa.nstypes.nsDictionary2dict is <function .nsDictionary2dict at 0x7fea94eecaf0>,
#  pycocoa.nstypes.NSDockTile is <ObjCClass(NSDockTile of 0x7fff855c8f80) at 0x7fea94aa8af0>,
#  pycocoa.nstypes.NSDouble is <ObjCBoundClassMethod(Class_t.numberWithDouble_) at 0x7fea94e95400>,
#  pycocoa.nstypes.NSEnumerator is <ObjCClass(NSEnumerator of 0x7fff85c4d410) at 0x7fea94aa8a60>,
#  pycocoa.nstypes.NSError is <ObjCClass(NSError of 0x7fff861c3350) at 0x7fea94aa89a0>,
#  pycocoa.nstypes.NSException is <ObjCClass(NSException of 0x7fff85c4d438) at 0x7fea94aa85e0>,
#  pycocoa.nstypes.NSExceptionError is <class .NSExceptionError>,
#  pycocoa.nstypes.NSFloat is <ObjCBoundClassMethod(Class_t.numberWithDouble_) at 0x7fea94e95460>,
#  pycocoa.nstypes.NSFont is <ObjCClass(NSFont of 0x7fff8d91c738) at 0x7fea94aa8550>,
#  pycocoa.nstypes.NSFontDescriptor is <ObjCClass(NSFontDescriptor of 0x7fff8d91c788) at 0x7fea94aa8310>,
#  pycocoa.nstypes.NSFontManager is <ObjCClass(NSFontManager of 0x7fff855c95e8) at 0x7fea94aa8520>,
#  pycocoa.nstypes.NSFontPanel is <ObjCClass(NSFontPanel of 0x7fff855c9638) at 0x7fea94aa9ac0>,
#  pycocoa.nstypes.NSImage is <ObjCClass(NSImage of 0x7fff855c9bb0) at 0x7fea94aa9a30>,
#  pycocoa.nstypes.NSImageView is <ObjCClass(NSImageView of 0x7fff855c9d40) at 0x7fea94aa99a0>,
#  pycocoa.nstypes.NSInt is <ObjCBoundClassMethod(Class_t.numberWithInt_) at 0x7fea94e954c0>,
#  pycocoa.nstypes.nsIter is <function .nsIter at 0x7fea94eecb80>,
#  pycocoa.nstypes.nsIter2 is <function .nsIter2 at 0x7fea94eecc10>,
#  pycocoa.nstypes.NSLayoutManager is <ObjCClass(NSLayoutManager of 0x7fff8d91c918) at 0x7fea94aa9340>,
#  pycocoa.nstypes.nsLog is <function .nsLog at 0x7fea94eecca0>,
#  pycocoa.nstypes.nsLogf is <function .nsLogf at 0x7fea94eecd30>,
#  pycocoa.nstypes.NSLong is <ObjCBoundClassMethod(Class_t.numberWithLong_) at 0x7fea94e95520>,
#  pycocoa.nstypes.NSLongLong is <ObjCBoundClassMethod(Class_t.numberWithLongLong_) at 0x7fea94e95580>,
#  pycocoa.nstypes.NSMain.Application=NSApplication(<Id_t at 0x7fea94ec5d40>) of 0x7fea9374de20,
#                        .BooleanNO=NSBoolean(<Id_t at 0x7fea94ef2240>) of 0x7fff85b15390,
#                        .BooleanYES=NSBoolean(<Id_t at 0x7fea94ef26c0>) of 0x7fff85b15380,
#                        .Bundle=NSBundle(<Id_t at 0x7fea94ef27c0>) of 0x7fea9485e9d0,
#                        .BundleName=NSConstantString('CFBundleName'),
#                        .FontManager=NSFontManager(<Id_t at 0x7fea94ef2e40>) of 0x7fea93455f90,
#                        .LayoutManager=NSLayoutManager(<Id_t at 0x7fea94ef2040>) of 0x7fea93457f90,
#                        .nil=None,
#                        .NO_false=False,
#                        .Null=NSNull(<Id_t at 0x7fea94efa340>) of 0x7fff85b15000,
#                        .PrintInfo=NSPrintInfo(<Id_t at 0x7fea94efaa40>) of 0x7fea93459350,
#                        .Screen=NSScreen(<Id_t at 0x7fea94efe240>) of 0x7fea94857fe0,
#                        .ScreenBottomLeft=NSPoint_t(x=-2560.0, y=-540.0),
#                        .ScreenBottomRight=NSPoint_t(x=2560.0, y=-540.0),
#                        .ScreenCenter=NSPoint_t(x=1280.0, y=720.0),
#                        .ScreenFrame=NSRect_t(origin=NSPoint_t(x=-2560.0, y=-540.0), size=NSSize_t(width=2560.0, height=1440.0)),
#                        .ScreenSize=NSSize_t(width=2560.0, height=1440.0),
#                        .ScreenTopLeft=NSPoint_t(x=-2560.0, y=1440.0),
#                        .ScreenTopRight=NSPoint_t(x=2560.0, y=-540.0),
#                        .stdlog=<_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>,
#                        .TableColumn=NSTableColumn(<Id_t at 0x7fea94efa7c0>) of 0x7fea93459a50,
#                        .versionstr=pycocoa.version 20.11.16, .isLazy 1, Python 3.9.0 64bit, macOS 10.15.7,
#                        .YES_true=True,
#  pycocoa.nstypes.NSMenu is <ObjCClass(NSMenu of 0x7fff855ca1f0) at 0x7fea94aa92b0>,
#  pycocoa.nstypes.NSMenuItem is <ObjCClass(NSMenuItem of 0x7fff855ca240) at 0x7fea94aa9220>,
#  pycocoa.nstypes.NSMutableArray is <ObjCClass(NSMutableArray of 0x7fff85c4d528) at 0x7fea94aa9400>,
#  pycocoa.nstypes.NSMutableData is <ObjCClass(NSMutableData of 0x7fff85c4d550) at 0x7fea94aa9490>,
#  pycocoa.nstypes.NSMutableDictionary is <ObjCClass(NSMutableDictionary of 0x7fff85c4d578) at 0x7fea94aa9fd0>,
#  pycocoa.nstypes.NSMutableSet is <ObjCClass(NSMutableSet of 0x7fff85c4d5c8) at 0x7fea94aa9f40>,
#  pycocoa.nstypes.NSMutableString is <ObjCClass(NSMutableString of 0x7fff861c4160) at 0x7fea94aa9eb0>,
#  pycocoa.nstypes.NSNotification is <ObjCClass(NSNotification of 0x7fff861c41d8) at 0x7fea94aa9e20>,
#  pycocoa.nstypes.NSNotificationCenter is <ObjCClass(NSNotificationCenter of 0x7fff861c4200) at 0x7fea94aa9dc0>,
#  pycocoa.nstypes.NSNull is <ObjCClass(NSNull of 0x7fff85c4d5f0) at 0x7fea94aa9d30>,
#  pycocoa.nstypes.nsNull2none is <function .nsNull2none at 0x7fea94eecdc0>,
#  pycocoa.nstypes.NSNumber is <ObjCClass(NSNumber of 0x7fff861c4278) at 0x7fea94aa9ca0>,
#  pycocoa.nstypes.nsNumber2num is <function .nsNumber2num at 0x7fea94eece50>,
#  pycocoa.nstypes.NSObject is <ObjCClass(NSObject of 0x7fff8e913118) at 0x7fea94aa9c10>,
#  pycocoa.nstypes.nsOf is <function .nsOf at 0x7fea94eecee0>,
#  pycocoa.nstypes.NSOpenPanel is <ObjCClass(NSOpenPanel of 0x7fff855ca948) at 0x7fea94aa9b80>,
#  pycocoa.nstypes.NSPageLayout is <ObjCClass(NSPageLayout of 0x7fff855caba0) at 0x7fea94aa90a0>,
#  pycocoa.nstypes.NSPrinter is <ObjCClass(NSPrinter of 0x7fff855cb320) at 0x7fea94aa9100>,
#  pycocoa.nstypes.NSPrintInfo is <ObjCClass(NSPrintInfo of 0x7fff855cb168) at 0x7fea94aa9190>,
#  pycocoa.nstypes.NSPrintOperation is <ObjCClass(NSPrintOperation of 0x7fff855cb1e0) at 0x7fea94aa9520>,
#  pycocoa.nstypes.NSPrintPanel is <ObjCClass(NSPrintPanel of 0x7fff855cb230) at 0x7fea94aa95b0>,
#  pycocoa.nstypes.NSSavePanel is <ObjCClass(NSSavePanel of 0x7fff855cb7d0) at 0x7fea94aa9640>,
#  pycocoa.nstypes.NSScreen is <ObjCClass(NSScreen of 0x7fff855cb848) at 0x7fea94aa96d0>,
#  pycocoa.nstypes.NSScrollView is <ObjCClass(NSScrollView of 0x7fff855cb8c0) at 0x7fea94aa9820>,
#  pycocoa.nstypes.NSSet is <ObjCClass(NSSet of 0x7fff85c4d690) at 0x7fea94aa98b0>,
#  pycocoa.nstypes.nsSet2set is <function .nsSet2set at 0x7fea94eecf70>,
#  pycocoa.nstypes.NSStatusBar is <ObjCClass(NSStatusBar of 0x7fff855cc360) at 0x7fea94aa9940>,
#  pycocoa.nstypes.NSStr is <class .NSStr>,
#  pycocoa.nstypes.NSString is <ObjCClass(NSString of 0x7fff861c5178) at 0x7fea94aab1c0>,
#  pycocoa.nstypes.nsString2str is <function .nsString2str at 0x7fea94eee040>,
#  pycocoa.nstypes.NSTableColumn is <ObjCClass(NSTableColumn of 0x7fff855cc888) at 0x7fea94aab130>,
#  pycocoa.nstypes.NSTableView is <ObjCClass(NSTableView of 0x7fff855cc9a0) at 0x7fea94aab0a0>,
#  pycocoa.nstypes.NSTextField is <ObjCClass(NSTextField of 0x7fff855ccc20) at 0x7fea94aab220>,
#  pycocoa.nstypes.nsTextSize3 is <function .nsTextSize3 at 0x7fea94eee0d0>,
#  pycocoa.nstypes.nsTextView is <function .nsTextView at 0x7fea94eee160>,
#  pycocoa.nstypes.NSTextView is <ObjCClass(NSTextView of 0x7fff855ccdd8) at 0x7fea94aab2b0>,
#  pycocoa.nstypes.NSThread is <ObjCClass(NSThread of 0x7fff861c52e0) at 0x7fea94aab340>,
#  pycocoa.nstypes.nsThrow is <function .nsThrow at 0x7fea94eee1f0>,
#  pycocoa.nstypes.NSURL is <ObjCClass(NSURL of 0x7fff85c4d7a8) at 0x7fea94aab3d0>,
#  pycocoa.nstypes.nsURL2str is <function .nsURL2str at 0x7fea94eee280>,
#  pycocoa.nstypes.NSView is <ObjCClass(NSView of 0x7fff855cda80) at 0x7fea94aab460>,
#  pycocoa.nstypes.NSWindow is <ObjCClass(NSWindow of 0x7fff855cdc88) at 0x7fea94aab4f0>,
# )[91]
# pycocoa.nstypes.version 20.11.15, .isLazy 1, Python 3.9.0 64bit, macOS 10.15.7

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2020 -- mrJean1 at Gmail -- All Rights Reserved.
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
