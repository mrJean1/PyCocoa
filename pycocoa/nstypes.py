
# -*- coding: utf-8 -*-

# License at the end of this file.

'''ObjC classes C{NS...} and conversions from C{NS...} ObjC to Python instances.

@var NSMain: Global C{ObjC/NS/CF...} singletons.
@var NSMain.Application: Get the C{NSApplication.sharedApplication}.
@var NSMain.BooleanNO: Get C{NSBoolean(NO)}.
@var NSMain.BooleanYES: Get C{NSBoolean(YES)}.
@var NSMain.Bundle: Get the C{NSBundle.mainBundle}.
@var NSMain.BundleName: Get the C{NS/CFBundleName}.
@var NSMain.FontManager: Get the C{NSFontManager.sharedFontManager}.
@var NSMain.LayoutManager: Get the C{NSLayoutManager}.
@var NSMain.NO_false: Get C{NSfalse/NO}.
@var NSMain.Null: Get C{NSNull}.
@var NSMain.PrintInfo: Get the C{NSPrintInfo}.
@var NSMain.Screen: Get the C{NSScreen.mainScreen}, once.
@var NSMain.TableColumn: Get a blank C{NSTableColumn}.
@var NSMain.YES_true: Get C{NStrue/YES}.
@var NSMain.nil: Get C{NSnil}.
@var NSMain.stdlog: Get the standard log file (C{stdout}, C{stderr}, other).
@var NSMain.versionstr: Get the PyCocoa, Python, macOS versions as C{str}.
'''
# all imports listed explicitly to help PyChecker
from pycocoa.getters import get_selector
from pycocoa.lazily import _ALL_LAZY, _bNN_, _COMMASPACE_, _Dmain_, _DOT_, _fmt, \
                           _fmt_invalid, _instr, _NN_, _no, _SPACE_
from pycocoa.octypes import Array_t, Class_t, c_struct_t, _encoding2ctype, Id_t, \
                            NSRect4_t, ObjC_t, SEL_t, Set_t  # NSPoint_t
from pycocoa.oslibs import cfNumber2bool, cfNumber2num, cfString, cfString2str, \
                           cfURLResolveAlias, libCF, libFoundation, libobjc, \
                           NO, YES
from pycocoa.runtime import isObjCInstanceOf, ObjCClass, ObjCInstance, release, \
                            retain, send_message, _NSAutorelease, _NSnil, _Xargs
from pycocoa.utils import Adict, _all_versionstr, bytes2str, _ByteStrs, clipstr, \
                         _Globals, isinstanceOf, iterbytes, lambda1, missing, \
                         _Singletons, _Types, type2strepr, property_RO

from ctypes import ArgumentError, byref, cast, c_byte, CFUNCTYPE, c_void_p
from datetime import datetime as _datetime
from decimal import Decimal as _Decimal
from os import linesep, path as os_path
from time import time as _timestamp

__all__ = _ALL_LAZY.nstypes
__version__ = '25.02.04'

_not_given_ = 'not given'

# some commonly used Foundation and Cocoa classes, described here
# <https://OMZ-Software.com/pythonista/docs/ios/objc_util.html>

# NS... classes marked ** have Python versions, like NSStr, for
# for use by runtime.isObjCInstanceOf repectively utils.isinstanceOf
NSAlert                 = ObjCClass('NSAlert')
NSApplication           = ObjCClass('NSApplication')
# NSApplicationDelegate defined in .apps
NSArray                 = ObjCClass('NSArray')  # immutable
_NSArrayI               = ObjCClass('__NSArrayI')  # DUNDER, immutable
_NS1ArrayI              = ObjCClass('__NSSingleObjectArrayI')  # DUNDER, immutable
NSAttributedString      = ObjCClass('NSAttributedString')
_NSAutorelease.Pool     = \
NSAutoreleasePool       = ObjCClass('NSAutoreleasePool')
NSBezierPath            = ObjCClass('NSBezierPath')
NSBundle                = ObjCClass('NSBundle')
NSColor                 = ObjCClass('NSColor')
NSConcreteNotification  = ObjCClass('NSConcreteNotification')
NSConcreteValue         = ObjCClass('NSConcreteValue')
NSConstantString        = ObjCClass('NSConstantString')  # use NSStr
NSData                  = ObjCClass('NSData')
NSDate                  = ObjCClass('NSDate')
NSDecimalNumber         = ObjCClass('NSDecimalNumber')  # ** use NSDecimal
NSDictionary            = ObjCClass('NSDictionary')  # immutable
_NSDictionaryI          = ObjCClass('__NSDictionaryI')  # DUNDER, immutable
_NSDictionaryM          = ObjCClass('__NSDictionaryM')  # DUNDER, mutable
NSDockTile              = ObjCClass('NSDockTile')
NSEnumerator            = ObjCClass('NSEnumerator')
NSError                 = ObjCClass('NSError')
NSException             = ObjCClass('NSException')
NSFont                  = ObjCClass('NSFont')
NSFontDescriptor        = ObjCClass('NSFontDescriptor')
NSFontManager           = ObjCClass('NSFontManager')
NSFontPanel             = ObjCClass('NSFontPanel')
NSImage                 = ObjCClass('NSImage')
NSImageView             = ObjCClass('NSImageView')
NSLayoutManager         = ObjCClass('NSLayoutManager')
NSMenu                  = ObjCClass('NSMenu')
NSMenuItem              = ObjCClass('NSMenuItem')
NSMutableArray          = ObjCClass('NSMutableArray')
NSMutableData           = ObjCClass('NSMutableData')
NSMutableDictionary     = ObjCClass('NSMutableDictionary')
NSMutableSet            = ObjCClass('NSMutableSet')
NSMutableString         = ObjCClass('NSMutableString')
NSNotification          = ObjCClass('NSNotification')
NSNotificationCenter    = ObjCClass('NSNotificationCenter')
NSNull                  = ObjCClass('NSNull')
NSNumber                = ObjCClass('NSNumber')
NSObject                = ObjCClass('NSObject')
NSOpenPanel             = ObjCClass('NSOpenPanel')
NSPageLayout            = ObjCClass('NSPageLayout')
# NSPoint               = ObjCClass('NSPoint')  # doesn't exist, use NSPoint_t
NSPrinter               = ObjCClass('NSPrinter')
NSPrintInfo             = ObjCClass('NSPrintInfo')
NSPrintOperation        = ObjCClass('NSPrintOperation')
NSPrintPanel            = ObjCClass('NSPrintPanel')
# NSRect                = ObjCClass('NSRect')  # doesn't exist, use NSRect_t
# NSRange               = ObjCClass('NSRange')  # doesn't exist, use NSRange_t
NSSavePanel             = ObjCClass('NSSavePanel')
NSScreen                = ObjCClass('NSScreen')
NSScrollView            = ObjCClass('NSScrollView')
NSSet                   = ObjCClass('NSSet')
# NSSize                = ObjCClass('NSSize')  # doesn't exist, use NSSize_t
NSStatusBar             = ObjCClass('NSStatusBar')
NSString                = ObjCClass('NSString')  # ** use NSStr or 'at'
NSTableColumn           = ObjCClass('NSTableColumn')
NSTableView             = ObjCClass('NSTableView')
NSTextField             = ObjCClass('NSTextField')
NSTextView              = ObjCClass('NSTextView')
NSThread                = ObjCClass('NSThread')
NSURL                   = ObjCClass('NSURL')
NSValue                 = ObjCClass('NSValue')
NSView                  = ObjCClass('NSView')
NSWindow                = ObjCClass('NSWindow')

# some other NS... types
NSBoolean  = NSNumber.numberWithBool_
NSDouble   = NSNumber.numberWithDouble_
NSFloat    = NSNumber.numberWithDouble_
NSInt      = NSNumber.numberWithInt_
NSLong     = NSNumber.numberWithLong_
NSLongLong = NSNumber.numberWithLongLong_


def _ns2ctype2py(ns, ctype):  # in .screens
    return ns2py(ns if isinstance(ns, ctype) else ctype(ns))


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
        return _instr(self.objc_classname, self.value)

    @property_RO
    def double(self):
        '''Get this L{NSDecimal} as a Python C{float}.
        '''
        return self.doubleValue()  # PYCHOK expected

    @property_RO
    def value(self):
        '''Get this L{NSDecimal} as a Python C{Decimal}.
        '''
        return self._pyDec

    Decimal = value


class NSExceptionError(RuntimeError):
    '''Python Error wrapping an C{ObjC/NSException}.

       Used to wrap I{uncaught} C{ObjC/NSException}s, see
       L{setUncaughtExceptionHandler}.
    '''
    _dt_fmt     = '%04d-%02d-%02d %02d:%02d:%06.3f'
    NS          =  None
    _timestamp  =  None

    def __init__(self, nsExc):
        '''New L{NSExceptionError} wrapper.

           @param nsExc: The C{ObjC/NSException} instance to wrap.
        '''
        if isObjCInstanceOf(nsExc, NSException, name='nsExc'):
            self.NS = nsExc
        self._timestamp = _timestamp()
        n = self.name or NSExceptionError.__name__
        r = self.reason or 'not given'
        RuntimeError.__init__(self, _fmt('ObjC/%s: %s', n, r))

    @property_RO
    def datetime(self):
        '''Get the time stamp as "YYYY-MM-DD HH:MM:SS.MIL" (C{str}).
        '''
        t = _datetime.fromtimestamp(self.timestamp)
        return self._dt_fmt % t.timetuple()[:6]

    @property_RO
    def name(self):
        '''Get the name of the exception (C{str}).

           @see: U{NSExceptionName<https://Developer.Apple.com/
                 documentation/foundation/nsexceptionname>}.
        '''
        return self.NS.name if self.NS else _NN_

    @property_RO
    def info(self):
        '''Get additional info about the exception (L{Adict}) or C{None}.
        '''
        return ns2py(self.NS.userInfo(), dflt=None) if self.NS else None

    @property_RO
    def reason(self):
        '''Get the reason for the exception (C{str}) or C{None}.
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
    '''Global C{ObjC/NS/CF...} singletons.
    '''
    _Application   =  None  # NSApplication, see .utils._Globals.App
    _BooleanNO     =  None
    _BooleanYES    =  None
    _Bundle        =  None
    _BundleName    =  None
    _FontManager   =  None
    _LayoutManager =  None
    _nil           = _NSnil  # final
    _NO_false      =  NO  # c_byte
    _Null          =  None
    _PrintInfo     =  None
    _Screen        =  None
    _TableColumn   =  None
    _YES_true      =  YES  # c_byte
    _versionstr    = _all_versionstr()

    # all globals are properties to delay instantiation

    def __getattr__(self, name):
        if len(name) > 6 and name.startswith('Screen'):
            t = _DOT_('.Screens.Main', name[6:].lower())
            t = _fmt('.%s obsolete, see %s', name, t)
            raise AttributeError(t)
        return super(_NSMain, self).__getattr__(name)

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
        '''Get C{NSNull}.
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
        '''Get the C{NSScreen.mainScreen}, once.
        '''
        if self._Screen is None:
            from pycocoa.screens import Screens
            _NSMain._Screen = retain(Screens.NS.mainScreen())
        return self._Screen

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
                raise AttributeError('not callable')
        except AttributeError as x:
            t = _fmt_invalid(file=repr(file))
            raise TypeError(_COMMASPACE_(t, x))

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
        return _Singletons.items(self, _NSMain.stdlog.fget.__name__)

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
        return _instr(self.objc_classname, repr(clipstr(self.value)))

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
    if isObjCInstanceOf(ns, _NS1ArrayI, _NSArrayI) and not ns.from_py2NS:  # NSScreen.screens()
        return nsArray2tuple(ns)
    # XXX order is critial, NSMutableArray before NSArray
    elif isObjCInstanceOf(ns, NSMutableArray, NSArray, name='ns') is NSMutableArray:
        t = list
    else:
        t = tuple
    n = libCF.CFArrayGetCount(ns)
    f = libCF.CFArrayGetValueAtIndex
    return t(_ns2ctype2py(f(ns, i), ctype) for i in range(n))


def nsArray2tuple(ns, ctype=ObjCInstance):
    '''Create a Python C{tuple} from an I{immutable} C{NSArray}.

       @param ns: The C{NSArray} (L{ObjCInstance}).
       @keyword ctype: The array item type (C{ObjCInstance}).

       @return: The array (C{tuple}).
    '''
    if isObjCInstanceOf(ns, _NS1ArrayI, _NSArrayI, name='ns'):
        n = libCF.CFArrayGetCount(ns)
        f = libCF.CFArrayGetValueAtIndex
        return tuple(ctype(f(ns, i)) for i in range(n))


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
                p = ns2py(p, dflt=_NN_) or _NN_
                if t and match in (p, _NN_, None):  # can't be empty
                    ns.setObject_forKey_(ns_title, NSMain.BundleName)
    return p


def nsData2bytes(ns, dflt=_bNN_):  # XXX an NSData method?
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
        return _bNN_.join(iterbytes(buf[:n]))
    return dflt


def nsDate2time(ns, since=1970):
    '''Create Python C{float} from C{NSDate}.

       @param ns: The C{NSDate} (L{ObjCInstance}).
       @keyword since: Epoch start date (1970, 2001) otherwise now.

       @return: The time in seconds (C{float}).
    '''
    isObjCInstanceOf(ns, NSDate, name='ns')
    if since == 1970:
        t = ns.timeIntervalSince1970()
    elif since == 2001:
        t = ns.timeIntervalSinceReferenceDate()  # CFDateGetAbsoluteTime(ns)
    else:
        t = ns.timeIntervalSinceNow()
    return float(t)  # cfNumber2num(t)


def nsDecimal2decimal(ns):
    '''Create a Python C{Decimal} from an C{NSDecimal}.

       @param ns: The C{NSDecimal} (L{ObjCInstance}).

       @return: The decimal (C{Decimal}).

       @raise ValueError: If I{ns} not an C{NSDecimal}.
    '''
    if isinstance(ns, NSDecimal):
        return ns.Decimal
    raise ValueError(_fmt_invalid(NSDecimal.__name__, ns=repr(ns)))


def nsDescription2dict(ns, **defaults):
    '''Create an I{immutable} C{dict} object with key I{and} attribute access to items by name.
    '''
    from pycocoa.bases import _Type0

    class Description(_Type0, dict):
        '''Immutable C{dict} typically used to wrap an I{immutable} C{Dictionary},
           like an C{NSScreen.} or C{NSPrinter.deviceDescription}.

           @note: Items are loaded from the C{Dictionary} on-demand I{only}.
        '''
        def __init__(self, ns, **defaults):
            self.NS = ns  # NSDictionary, __NSDictionaryI
            if defaults:
                self.update(defaults)

        def __getattr__(self, name):
            '''Get the value of an attribute or item by B{C{name}}.
            '''
            v = self.get(name, missing)
            if v is missing:
                n = NSStr(name)
                v = c_void_p(None)
                t = libCF.CFDictionaryGetValueIfPresent(self.NS, n, byref(v))
                if not t or isNone(v):
                    t = _fmt('%s (%r)', _DOT_(self.name, name), n)
                    raise KeyError(_fmt_invalid(item=t))
                v = _ns2ctype2py(v, c_void_p)
                dict.__setitem__(self, name, v)
            return v

        @property_RO
        def name(self):
            return dict.get(self, 'name', Description.__name__)

        def __repr__(self):
            return _SPACE_(self.typename, self)

        def __setitem__(self, key, value):
            raise TypeError(_fmt('%s[%r] = %r', self.name, key, value))

        def __str__(self):
            '''Return this C{Description} as C{str}.
            '''
            return type2strepr(self, **self)

#       def copy(self):
#           '''Return a shallow copy.
#           '''
#           return type(self)(self.NS, **self)

    return Description(ns, **defaults)


def nsDictionary2dict(ns, ctype_keys=c_void_p, ctype_vals=c_void_p):  # XXX an NS*Dictionary method?
    '''Create a Python C{dict} from an C{NS[Mutable]Dictionary}.

       @param ns: The C{NSDictionary} instance (L{ObjCInstance}).
       @keyword ctype_keys: The dictionary keys type (C{ctypes}).
       @keyword ctype_vals: The dictionary values type (C{ctypes}).

       @return: The dict (L{Adict}).
    '''
#   if isObjCInstanceOf(ns, _NSDictionaryI) and not ns.from_py2NS:  # NSScreen.deviceDescription()
#       return nsDescription2dict(ns)  # XXX Adict(map(ns2py, t) for t in nsDictionary2items(ns))

    # <https://Developer.Apple.com/documentation/corefoundation/cfdictionary-rum>
    n = libCF.CFDictionaryGetCount(ns)
    keys = (ctype_keys * n)()
    vals = (ctype_vals * n)()
    libCF.CFDictionaryGetKeysAndValues(ns, byref(keys), byref(vals))
    return Adict((_ns2ctype2py(keys[i], ctype_keys),
                  _ns2ctype2py(vals[i], ctype_vals)) for i in range(n))


def nsDictionary2items(ns):  # XXX an NS*Dictionary method?
    '''Yield the C{(key, value)} items from an C{NSDictionary}.

       @param ns: The C{NSDictionary} instance (L{ObjCInstance}).

       @return: A 2-tuple C{(key, value)} for each item, each
                a separate L{ObjCInstance}
    '''
    # <https://Developer.Apple.com/documentation/corefoundation/cfdictionary-rum>
    n = libCF.CFDictionaryGetCount(ns)
    keys = (c_void_p * n)()
    vals = (c_void_p * n)()
    libCF.CFDictionaryGetKeysAndValues(ns, byref(keys), byref(vals))
    for i in range(n):
        yield tuple(map(ObjCInstance, (keys[i], vals[i])))


def nsException(name=None, reason=_not_given_, **info):
    '''Create an C{ObjC/NSException} instance.

       @keyword name: Ignored (U{NSExceptionName<https://Developer.Apple.com/
                      documentation/foundation/nsexceptionname>}).
       @keyword reason: The reason for the exception (C{str}).
       @keyword info: Other, caller-defined information (C{all keywords}).

       @see: L{nsRaise}, L{nsThrow} and L{NSExceptionError}.

       @note: Use L{NSExceptionError}C{(nsExc)} to wrap a Python
              exception around an C{ObjC/NSException} instance and
              get access to the attributes of the latter.

       @note: Raised and thrown C{NSException}s can not be caught and
              result in I{fatal} L{exiting}.

    '''
    from pycocoa.pytypes import dict2NS
    # <https://Developer.Apple.com/library/archive/documentation/
    #        Cocoa/Conceptual/Exceptions/Tasks/RaisingExceptions.html>
    # XXX use NSExceptionName inlieu of NSStr(name) since the latter
    # seems to always become 'NSException' instead of the 'name'
    return NSException.alloc().initWithName_reason_userInfo_(
                                   NSStr(name or nsException.__name__),
                                   NSStr(str(reason)), dict2NS(info))


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
            raise TypeError(_fmt_invalid('iterable', ns=repr(ns)))

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
                n = _fmt('ns_arg[%s]', n)  # raise error
                if not isinstanceOf(ns, ObjCInstance, name=n):
                    break
        else:  # XXX all ns_fmt %-types should be %@?
            libFoundation.NSLog(ns_fmt, *ns_args)  # variadic, printf-like


def nsLogf(fmtxt, *args):
    '''Formatted write to the console.

       @param fmtxt: A printf-like format string (C{str}).
       @param args: Optional arguments to format (C{all positional}).

       @see: L{nsLog}.
    '''
    if isinstanceOf(fmtxt, _ByteStrs, name='fmtxt'):
        ns = NSStr(_fmt(fmtxt, *args))
        libFoundation.NSLog(ns)  # variadic, printf-like


def nsNull2none(ns):
    '''Return Python C{None} for an C{NS/CFNull} or C{nil}.

       @param ns: The C{NS...} (L{ObjCInstance}).

       @return: The singleton (C{None}).

       @raise ValueError: If I{ns} not C{isNone}.
    '''
    if isObjCInstanceOf(ns, NSNull, c_void_p, name='ns') or isNone(ns):
        return None
    raise ValueError(_fmt_invalid(isNone.__name__, ns=repr(ns)))


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
    raise ValueError(_fmt_invalid(NSNumber.name, ns=repr(ns)))


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
    raise TypeError(_fmt_invalid(_no('.NS'), inst=repr(inst)))


def nsRaise(name=None, reason=_not_given_, **info):
    '''Create an C{NSException} and mimick C{@throw NSException}.

       @keyword name: Ignored (U{NSExceptionName<https://Developer.Apple.com/
                      documentation/foundation/nsexceptionname>}).
       @keyword reason: The reason for the exception (C{str}).
       @keyword info: Other, caller-defined information (C{all keywords}).

       @note: Raised C{NSException}s can not be caught and result
              in I{fatal} L{exiting}.

       @see: L{NSException} and L{nsThrow}.
    '''
    # XXX use NSExceptionName, see nsException above
    nsThrow(nsException(name=name, reason=reason, **info))


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
    w = _NN_
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


def nsThrow(nsExc):
    '''Mimick ObjC's C{@throw NSException} to raise an exception.

       @param nsExc: The exception to raise (C{NSException}).

       @see: L{NSException} and L{nsRaise}.

       @note: Thrown C{NSException}s can not be caught and result
              in I{fatal} L{exiting}.

       @raise TypeError: Invalid B{C{nsExc}}.
    '''
    # can't use ns_exception.raise() since 'raise' is reserved
    # in Python; see also .runtime.ObjCInstance.__getattr__
    # substituting method name 'throw' for 'raise'.
    if isObjCInstanceOf(nsExc, NSException, name='nsExc'):
        send_message(nsExc, 'raise')


def nsURL2str(ns):
    '''Create a Python C{str} from C{NSURL} string.

       @param ns: The C{CFURL} (L{ObjCInstance}).

       @return: The URL as string (C{str}).
    '''
    if isObjCInstanceOf(ns, NSURL, name='ns'):
        # <https://NSHipster.com/nsurl>
        return nsString2str(ns.absoluteString())


def nsValue2py(ns, dflt=missing):
    '''Create a Python instance from an C{NS[Concrete]Value}.

       @param ns: The C{NS[Concrete]Value} (L{ObjCInstance}).
       @keyword dflt: Default for missing, unobtainable value.

       @raise TypeError: Invalid B{C{ns}} or unexpected C{ns.objCType}.

       @return: The value (C{NSPoint_t}, C{NSRange_t}, C{NSRect_t},
                C{NSSize_t} or C{tuple}) or B{C{dflt}}.
    '''
    if isObjCInstanceOf(ns, NSConcreteValue, NSValue):
        objCType = ns.objCType()
        try:
            ctype = _encoding2ctype[objCType]
            py = ctype()
            ns.getValue_(byref(py))
            return py
        except KeyError:
            pass
    elif isObjCInstanceOf(ns, _NSArrayI, _NS1ArrayI):
        return nsArray2tuple(ns)
    else:
        objCType = None

    try:
        return ObjCInstance(ns)
    except (TypeError, ValueError):
        pass

    if dflt is missing:
        t = _instr('NSValue', repr(ns))
        raise TypeError(_fmt('unhandled %s: %r', t, objCType))
    return dflt


_CFTypeID2py = {1:                             nsValue2py,  # __NSArrayI
                libCF.CFArrayGetTypeID():      nsArray2listuple,   # 19
                libCF.CFBooleanGetTypeID():    nsBoolean2bool,     # 21
                libCF.CFDataGetTypeID():       nsData2bytes,       # 20
                libCF.CFDateGetTypeID():       nsDate2time,        # 42
                libCF.CFDictionaryGetTypeID(): nsDictionary2dict,  # 18
                libCF.CFNullGetTypeID():       nsNull2none,        # 16
                libCF.CFNumberGetTypeID():     nsNumber2num,       # 22
                libCF.CFSetGetTypeID():        nsSet2set,          # 17
                libCF.CFStringGetTypeID():     nsString2str,       # 7
                libCF.CFURLGetTypeID():        nsURL2str}          # 29


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
    _, t = ns2TypeID2(ns, dflt=dflt)
    r = t(ns)
    c = {Class_t: ObjCClass,
         Id_t:    ObjCInstance}.get(type(r), lambda1)
    return c(r)


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

    # XXX order is critial, check for NSMutableArray first
    if isObjCInstanceOf(ns, NSMutableArray) is NSMutableArray:
        _Type = _Types.List
    elif isObjCInstanceOf(ns, NSArray) is NSArray:
        _Type = _Types.Tuple

    # XXX order is critial, check for NSMutableDictionary first
    elif isObjCInstanceOf(ns, NSMutableDictionary, _NSDictionaryM) in (
                              NSMutableDictionary, _NSDictionaryM):
        _Type = _Types.Dict
    elif isObjCInstanceOf(ns, NSDictionary, _NSDictionaryI) in (
                              NSDictionary, _NSDictionaryI):
        _Type = _Types.FrozenDict

    # XXX order is critial, check for NSMutableSet first
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


def ns2TypeID2(ns, dflt=None):
    '''Get the C{NS...} ObjC C{TypeID}.

       @param ns: The C{NS...} (L{ObjCInstance}).
       @keyword dflt: Default for unhandled, unexpected C{NS...}s (C{missing}).

       @return: 2-Tuple C{(TypeID, ns...2py)} of an C{int}NS
                and the type conversion C{callable}.
    '''
    # see Rubicon-ObjC/objc/core_foundation.py
    # if isinstance(ns, ObjCInstance):
    #     ns = ns._as_parameter_
    try:
        i = libCF.CFGetTypeID(ns)
        return i, _CFTypeID2py[i]

    except ArgumentError as x:
        _Xargs(x, libCF.CFGetTypeID.__name__,
                  libCF.CFGetTypeID.argtypes,
                  libCF.CFGetTypeID.restype)
        raise

    except KeyError:
        if dflt is missing:
            t = (_fmt('TypeID[%d]: %s', *t) for t in sorted(_CFTypeID2py_items()))
            t =  _fmt('TypeID[%r] unhandled: %r {%s}', i, ns, _COMMASPACE_.join(t))
            raise TypeError(t)
        return i, dflt


if __name__ == _Dmain_:

    from pycocoa.utils import _all_listing, _varstr

    print(_varstr(NSMain))

    _all_listing(__all__, locals())

# % python3 -m pycocoa.nstypes
#
# pycocoa.nstypes.__all__ = tuple(
#  pycocoa.nstypes.at is <class .at>,
#  pycocoa.nstypes.isAlias is <function .isAlias at 0x102ff4900>,
#  pycocoa.nstypes.isLink is <function .isLink at 0x1036b8180>,
#  pycocoa.nstypes.isNone is <function .isNone at 0x1036b8220>,
#  pycocoa.nstypes.ns2py is <function .ns2py at 0x1036b93a0>,
#  pycocoa.nstypes.ns2Type is <function .ns2Type at 0x1036b9440>,
#  pycocoa.nstypes.ns2TypeID2 is <function .ns2TypeID2 at 0x1036b94e0>,
#  pycocoa.nstypes.NSAlert is <ObjCClass(NSAlert of 0x1f90b6a68) at 0x103680050>,
#  pycocoa.nstypes.NSApplication is <ObjCClass(NSApplication of 0x1f90b6b80) at 0x103521a90>,
#  pycocoa.nstypes.NSArray is <ObjCClass(NSArray of 0x1f9091438) at 0x103521bd0>,
#  pycocoa.nstypes.nsArray2listuple is <function .nsArray2listuple at 0x1036b82c0>,
#  pycocoa.nstypes.nsArray2tuple is <function .nsArray2tuple at 0x1036b8360>,
#  pycocoa.nstypes.NSAttributedString is <ObjCClass(NSAttributedString of 0x1f90979c8) at 0x103666690>,
#  pycocoa.nstypes.NSAutoreleasePool is <ObjCClass(NSAutoreleasePool of 0x1f90979f0) at 0x103535150>,
#  pycocoa.nstypes.NSBezierPath is <ObjCClass(NSBezierPath of 0x1f90b6c98) at 0x103535260>,
#  pycocoa.nstypes.NSBoolean is <ObjCBoundClassMethod(Class_t.numberWithBool_) at 0x103680ad0>,
#  pycocoa.nstypes.nsBoolean2bool is <function .nsBoolean2bool at 0x1036b8400>,
#  pycocoa.nstypes.NSBundle is <ObjCClass(NSBundle of 0x1f9097ab8) at 0x1034faa50>,
#  pycocoa.nstypes.nsBundleRename is <function .nsBundleRename at 0x1036b84a0>,
#  pycocoa.nstypes.NSColor is <ObjCClass(NSColor of 0x1f90b73c8) at 0x1034fb550>,
#  pycocoa.nstypes.NSConcreteNotification is <ObjCClass(NSConcreteNotification of 0x1f90966e0) at 0x103549040>,
#  pycocoa.nstypes.NSConcreteValue is <ObjCClass(NSConcreteValue of 0x1f9097c70) at 0x103549130>,
#  pycocoa.nstypes.NSConstantString is <ObjCClass(NSConstantString of 0x1f9097ce8) at 0x103677d90>,
#  pycocoa.nstypes.NSData is <ObjCClass(NSData of 0x1f9091500) at 0x103677cb0>,
#  pycocoa.nstypes.nsData2bytes is <function .nsData2bytes at 0x1036b8540>,
#  pycocoa.nstypes.NSDate is <ObjCClass(NSDate of 0x1f9091528) at 0x10347d160>,
#  pycocoa.nstypes.NSDecimal is <class .NSDecimal>,
#  pycocoa.nstypes.nsDecimal2decimal is <function .nsDecimal2decimal at 0x1036b8680>,
#  pycocoa.nstypes.NSDecimalNumber is <ObjCClass(NSDecimalNumber of 0x1f9097db0) at 0x10365fe90>,
#  pycocoa.nstypes.nsDescription2dict is <function .nsDescription2dict at 0x1036b8720>,
#  pycocoa.nstypes.NSDictionary is <ObjCClass(NSDictionary of 0x1f9091578) at 0x10365ff50>,
#  pycocoa.nstypes.nsDictionary2dict is <function .nsDictionary2dict at 0x1036b87c0>,
#  pycocoa.nstypes.nsDictionary2items is <function .nsDictionary2items at 0x1036b8860>,
#  pycocoa.nstypes.NSDockTile is <ObjCClass(NSDockTile of 0x1f90a76d0) at 0x1036a7750>,
#  pycocoa.nstypes.NSDouble is <ObjCBoundClassMethod(Class_t.numberWithDouble_) at 0x103521e50>,
#  pycocoa.nstypes.NSEnumerator is <ObjCClass(NSEnumerator of 0x1f90915a0) at 0x1036a7890>,
#  pycocoa.nstypes.NSError is <ObjCClass(NSError of 0x1f9097e50) at 0x1034edeb0>,
#  pycocoa.nstypes.NSException is <ObjCClass(NSException of 0x1f90915c8) at 0x1036a96d0>,
#  pycocoa.nstypes.nsException is <function .nsException at 0x1036b8900>,
#  pycocoa.nstypes.NSExceptionError is <class .NSExceptionError>,
#  pycocoa.nstypes.NSFloat is <ObjCBoundClassMethod(Class_t.numberWithDouble_) at 0x103521f90>,
#  pycocoa.nstypes.NSFont is <ObjCClass(NSFont of 0x1f90cfed0) at 0x1036aa1d0>,
#  pycocoa.nstypes.NSFontDescriptor is <ObjCClass(NSFontDescriptor of 0x1f90cff20) at 0x103554ad0>,
#  pycocoa.nstypes.NSFontManager is <ObjCClass(NSFontManager of 0x1f90a7d38) at 0x103555780>,
#  pycocoa.nstypes.NSFontPanel is <ObjCClass(NSFontPanel of 0x1f90a7d88) at 0x1035557f0>,
#  pycocoa.nstypes.NSImage is <ObjCClass(NSImage of 0x1f90a82d8) at 0x103555860>,
#  pycocoa.nstypes.NSImageView is <ObjCClass(NSImageView of 0x1f90a8440) at 0x1035558d0>,
#  pycocoa.nstypes.NSInt is <ObjCBoundClassMethod(Class_t.numberWithInt_) at 0x103551350>,
#  pycocoa.nstypes.nsIter is <function .nsIter at 0x1036b89a0>,
#  pycocoa.nstypes.nsIter2 is <function .nsIter2 at 0x1036b8a40>,
#  pycocoa.nstypes.NSLayoutManager is <ObjCClass(NSLayoutManager of 0x1f90d00b0) at 0x103555940>,
#  pycocoa.nstypes.nsLog is <function .nsLog at 0x1036b8ae0>,
#  pycocoa.nstypes.nsLogf is <function .nsLogf at 0x1036b8b80>,
#  pycocoa.nstypes.NSLong is <ObjCBoundClassMethod(Class_t.numberWithLong_) at 0x1035515b0>,
#  pycocoa.nstypes.NSLongLong is <ObjCBoundClassMethod(Class_t.numberWithLongLong_) at 0x103667ad0>,
#  pycocoa.nstypes.NSMain.Application=NSApplication(<Id_t at 0x1036bc150>) of 0x122ea3d80,
#                        .BooleanNO=NSBoolean(<Id_t at 0x1036bc650>) of 0x1fe228890,
#                        .BooleanYES=NSBoolean(<Id_t at 0x1036bccd0>) of 0x1fe228880,
#                        .Bundle=NSBundle(<Id_t at 0x1036bced0>) of 0x600001278000,
#                        .BundleName=NSConstantString('CFBundleName'),
#                        .FontManager=NSFontManager(<Id_t at 0x1036bdcd0>) of 0x600001279900,
#                        .LayoutManager=NSLayoutManager(<Id_t at 0x1036be3d0>) of 0x122f8da90,
#                        .nil=None,
#                        .NO_false=False,
#                        .Null=NSNull(<Id_t at 0x1036bec50>) of 0x1fe228c00,
#                        .PrintInfo=NSPrintInfo(<Id_t at 0x1036bf4d0>) of 0x60000317dc00,
#                        .Screen=NSScreen(<Id_t at 0x1036bcbd0>) of 0x600001579d40,
#                        .stdlog=<_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>,
#                        .TableColumn=NSTableColumn(<Id_t at 0x1036edb50>) of 0x600001a78930,
#                        .versionstr=pycocoa.version 25.1.31, .isLazy 1, Python 3.13.1 64bit arm64, macOS 14.6.1,
#                        .YES_true=True,
#  pycocoa.nstypes.NSMenu is <ObjCClass(NSMenu of 0x1f90a88f0) at 0x1035559b0>,
#  pycocoa.nstypes.NSMenuItem is <ObjCClass(NSMenuItem of 0x1f90a8940) at 0x103555a20>,
#  pycocoa.nstypes.NSMutableArray is <ObjCClass(NSMutableArray of 0x1f9091690) at 0x103555a90>,
#  pycocoa.nstypes.NSMutableData is <ObjCClass(NSMutableData of 0x1f90916b8) at 0x103555b00>,
#  pycocoa.nstypes.NSMutableDictionary is <ObjCClass(NSMutableDictionary of 0x1f90916e0) at 0x103555b70>,
#  pycocoa.nstypes.NSMutableSet is <ObjCClass(NSMutableSet of 0x1f9091730) at 0x103555be0>,
#  pycocoa.nstypes.NSMutableString is <ObjCClass(NSMutableString of 0x1f9098350) at 0x103555c50>,
#  pycocoa.nstypes.NSNotification is <ObjCClass(NSNotification of 0x1f9098378) at 0x103555cc0>,
#  pycocoa.nstypes.NSNotificationCenter is <ObjCClass(NSNotificationCenter of 0x1f90983a0) at 0x103555d30>,
#  pycocoa.nstypes.NSNull is <ObjCClass(NSNull of 0x1f9091758) at 0x103555da0>,
#  pycocoa.nstypes.nsNull2none is <function .nsNull2none at 0x1036b8c20>,
#  pycocoa.nstypes.NSNumber is <ObjCClass(NSNumber of 0x1f90983c8) at 0x103555e10>,
#  pycocoa.nstypes.nsNumber2num is <function .nsNumber2num at 0x1036b8cc0>,
#  pycocoa.nstypes.NSObject is <ObjCClass(NSObject of 0x1f9075fb0) at 0x103555e80>,
#  pycocoa.nstypes.nsOf is <function .nsOf at 0x1036b8d60>,
#  pycocoa.nstypes.NSOpenPanel is <ObjCClass(NSOpenPanel of 0x1f90a9020) at 0x103555ef0>,
#  pycocoa.nstypes.NSPageLayout is <ObjCClass(NSPageLayout of 0x1f90a9278) at 0x103555f60>,
#  pycocoa.nstypes.NSPrinter is <ObjCClass(NSPrinter of 0x1f90a9980) at 0x103555fd0>,
#  pycocoa.nstypes.NSPrintInfo is <ObjCClass(NSPrintInfo of 0x1f90a9818) at 0x103556040>,
#  pycocoa.nstypes.NSPrintOperation is <ObjCClass(NSPrintOperation of 0x1f90a9890) at 0x1035560b0>,
#  pycocoa.nstypes.NSPrintPanel is <ObjCClass(NSPrintPanel of 0x1f90a98e0) at 0x103556120>,
#  pycocoa.nstypes.nsRaise is <function .nsRaise at 0x1036b8e00>,
#  pycocoa.nstypes.NSSavePanel is <ObjCClass(NSSavePanel of 0x1f90a9fc0) at 0x103556190>,
#  pycocoa.nstypes.NSScreen is <ObjCClass(NSScreen of 0x1f90aa010) at 0x103556200>,
#  pycocoa.nstypes.NSScrollView is <ObjCClass(NSScrollView of 0x1f90aa088) at 0x103556270>,
#  pycocoa.nstypes.NSSet is <ObjCClass(NSSet of 0x1f90917f8) at 0x1035562e0>,
#  pycocoa.nstypes.nsSet2set is <function .nsSet2set at 0x1036b8ea0>,
#  pycocoa.nstypes.NSStatusBar is <ObjCClass(NSStatusBar of 0x1f90aab00) at 0x103556350>,
#  pycocoa.nstypes.NSStr is <class .NSStr>,
#  pycocoa.nstypes.NSString is <ObjCClass(NSString of 0x1f90988c8) at 0x1035563c0>,
#  pycocoa.nstypes.nsString2str is <function .nsString2str at 0x1036b8f40>,
#  pycocoa.nstypes.NSTableColumn is <ObjCClass(NSTableColumn of 0x1f90ab000) at 0x103556430>,
#  pycocoa.nstypes.NSTableView is <ObjCClass(NSTableView of 0x1f90ab118) at 0x1035564a0>,
#  pycocoa.nstypes.NSTextField is <ObjCClass(NSTextField of 0x1f90ab370) at 0x103556510>,
#  pycocoa.nstypes.nsTextSize3 is <function .nsTextSize3 at 0x1036b8fe0>,
#  pycocoa.nstypes.nsTextView is <function .nsTextView at 0x1036b9080>,
#  pycocoa.nstypes.NSTextView is <ObjCClass(NSTextView of 0x1f90ab528) at 0x103556580>,
#  pycocoa.nstypes.NSThread is <ObjCClass(NSThread of 0x1f90989b8) at 0x1035565f0>,
#  pycocoa.nstypes.nsThrow is <function .nsThrow at 0x1036b9120>,
#  pycocoa.nstypes.NSURL is <ObjCClass(NSURL of 0x1f9091910) at 0x103556660>,
#  pycocoa.nstypes.nsURL2str is <function .nsURL2str at 0x1036b91c0>,
#  pycocoa.nstypes.NSValue is <ObjCClass(NSValue of 0x1f9098b70) at 0x1035566d0>,
#  pycocoa.nstypes.nsValue2py is <function .nsValue2py at 0x1036b9260>,
#  pycocoa.nstypes.NSView is <ObjCClass(NSView of 0x1f90ac1a8) at 0x103556740>,
#  pycocoa.nstypes.NSWindow is <ObjCClass(NSWindow of 0x1f90ac3b0) at 0x1035567b0>,
# )[101]
# pycocoa.nstypes.version 25.2.4, .isLazy 1, Python 3.13.1 64bit arm64, macOS 14.6.1

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
