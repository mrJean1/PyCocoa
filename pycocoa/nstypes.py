
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
# from pycocoa.bases import _Type0  # in .nsDescription2dict ... circular!
from pycocoa.getters import get_selector
from pycocoa.internals import Adict, _bNN_, bytes2str, _ByteStrs, _COLONSPACE_, \
                             _COMMASPACE_, _Dmain_, _DOT_, frozendict, lambda1, \
                             _frozendictbase, _Globals, iterbytes, missing, \
                             _name_, _nameOf, _NN_, _no, _NSObject_, proxy_RO, \
                             _Singletons, property_RO, _SPACE_, _unhandled_
from pycocoa.lazily import _ALL_LAZY, _Types,  _fmt, _fmt_invalid, _instr
from pycocoa.octypes import Array_t, Class_t, c_struct_t, _encoding2ctype, Id_t, \
                            NSRect4_t, ObjC_t, SEL_t, Set_t  # NSPoint_t
from pycocoa.oslibs import cfNumber2bool, cfNumber2num, cfString, cfString2str, \
                           cfURLResolveAlias, _libCF, _libFoundation, _libObjC, \
                           NO, YES
from pycocoa.runtime import isObjCInstanceOf, ObjCClass, ObjCInstance, release, \
                            retain, send_message, _Xargs
from pycocoa.utils import _all_versionstr, clipstr, isinstanceOf, type2strepr

from ctypes import ArgumentError, byref, cast, c_byte, CFUNCTYPE, c_void_p
from datetime import datetime as _datetime
from decimal import Decimal as _Decimal
from os import linesep as _linesep, path as _os_path
from time import time as _timestamp

__all__ = _ALL_LAZY.nstypes
__version__ = '25.03.18'

_not_given_ = 'not given'
_raiser_ns  =  dict(raiser='ns')

# some commonly used Foundation and Cocoa classes, described here
# <https://OMZ-Software.com/pythonista/docs/ios/objc_util.html>

# NS... classes marked ** have Python versions, like NSStr, for
# for use by runtime.isObjCInstanceOf repectively utils.isinstanceOf
NSAlert                = ObjCClass('NSAlert')
NSApplication          = ObjCClass('NSApplication')
# NSApplicationDelegate defined in .apps
NSArray                = ObjCClass('NSArray')  # immutable
_NSArrayI              = ObjCClass('__NSArrayI')  # DUNDER, immutable
_NSArrayM              = ObjCClass('__NSArrayM')  # DUNDER, mutable
_NS0ArrayI             = ObjCClass('__NSArray0')  # DUNDER, immutable
_NS1ArrayI             = ObjCClass('__NSSingleObjectArrayI')  # DUNDER, immutable
NSAttributedString     = ObjCClass('NSAttributedString')
NSAutoreleasePool      = ObjCClass('NSAutoreleasePool')
NSAutoreleasePools     = 0  # PYCHOK in .nstypes
NSBezierPath           = ObjCClass('NSBezierPath')
NSBundle               = ObjCClass('NSBundle')
NSColor                = ObjCClass('NSColor')
NSConcreteNotification = ObjCClass('NSConcreteNotification')
NSConcreteValue        = ObjCClass('NSConcreteValue')
NSConstantString       = ObjCClass('NSConstantString')  # use NSStr
_NSCFConstantString    = ObjCClass('__NSCFConstantString')  # DUNDER, immutable
NSData                 = ObjCClass('NSData')
NSDate                 = ObjCClass('NSDate')
NSDecimalNumber        = ObjCClass('NSDecimalNumber')  # ** use NSDecimal
NSDictionary           = ObjCClass('NSDictionary')  # immutable
_NSDictionaryI         = ObjCClass('__NSDictionaryI')  # DUNDER, immutable
_NSDictionaryM         = ObjCClass('__NSDictionaryM')  # DUNDER, mutable
_NS0DictionaryI        = ObjCClass('__NSDictionary0')  # DUNDER, mutable
_NS1DictionaryI        = ObjCClass('__NSSingleEntryDictionaryI')
NSDockTile             = ObjCClass('NSDockTile')
NSEnumerator           = ObjCClass('NSEnumerator')
NSError                = ObjCClass('NSError')
NSException            = ObjCClass('NSException')
NSFont                 = ObjCClass('NSFont')
NSFontDescriptor       = ObjCClass('NSFontDescriptor')
NSFontManager          = ObjCClass('NSFontManager')
NSFontPanel            = ObjCClass('NSFontPanel')
_NSFrozenArrayM        = ObjCClass('__NSFrozenArrayM')  # DUNDER, immutable!
_NSFrozenDictionaryM   = ObjCClass('__NSFrozenDictionaryM')  # DUNDER, immutable!
_NSFrozenSetM          = ObjCClass('__NSFrozenSetM')  # DUNDER, immutable!
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
NSObject               = ObjCClass(_NSObject_)  # in .runtime.isObjCinstanceOf
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
_NSSetI                = ObjCClass('__NSSetI')  # DUNDER, immutable
_NSSetM                = ObjCClass('__NSSetM')  # DUNDER, mutable
# NSSize               = ObjCClass('NSSize')  # doesn't exist, use NSSize_t
NSStatusBar            = ObjCClass('NSStatusBar')
NSString               = ObjCClass('NSString')  # ** use NSStr or 'at'
_NSCFString            = ObjCClass('__NSCFString')  # DUNDER, immutable?
NSTableColumn          = ObjCClass('NSTableColumn')
NSTableView            = ObjCClass('NSTableView')
_NSTaggedPointerString = ObjCClass('NSTaggedPointerString')  # == NSString?
NSTextField            = ObjCClass('NSTextField')
NSTextView             = ObjCClass('NSTextView')
NSThread               = ObjCClass('NSThread')
NSURL                  = ObjCClass('NSURL')
NSValue                = ObjCClass('NSValue')
NSView                 = ObjCClass('NSView')
NSWindow               = ObjCClass('NSWindow')

# some other NS... types
NSBoolean  = NSNumber.numberWithBool_
NSDouble   = NSNumber.numberWithDouble_
NSFloat    = NSNumber.numberWithDouble_
NSInt      = NSNumber.numberWithInt_
NSLong     = NSNumber.numberWithLong_
NSLongLong = NSNumber.numberWithLongLong_


class _NSImms(tuple):  # all immutable NS... ObjCClasses
    ArrayI01 = _NSArrayI, _NS0ArrayI, _NS1ArrayI  # in .nsArray2listuple
    Arrays   = (NSArray, _NSFrozenArrayM) + ArrayI01  # in .tuples
    DictI01  = _NSDictionaryI, _NS0DictionaryI, _NS1DictionaryI
    Dicts    = (NSDictionary, _NSFrozenDictionaryM) + DictI01  # in .dicts
    Sets     =  NSSet, _NSSetI, _NSFrozenSetM  # in .sets
    Strs     =  NSString, NSConstantString, _NSCFConstantString, _NSTaggedPointerString  # in .strs

_NSImms = _NSImms(_NSImms.Arrays + _NSImms.Dicts +  # PYCHOK singleton, in .runtime
                  _NSImms.Sets   + _NSImms.Strs)
assert len(_NSImms) == 17


class _NSMtbs(tuple):  # all mutable NS... ObjCClasses
    Arrays = NSMutableArray, _NSArrayM  # in .lists
    Dicts  = NSMutableDictionary, _NSDictionaryM  # in .dicts
#   Notifs = NSNotification, NSConcreteNotification
    Sets   = NSMutableSet, _NSSetM  # in .sets
    Strs   = NSMutableString, _NSCFString  # in .strs
    Values = NSValue, NSConcreteValue

_NSMtbs = _NSMtbs(_NSMtbs.Arrays + _NSMtbs.Dicts +  # PYCHOK singleton, in .runtime
                  _NSMtbs.Sets   + _NSMtbs.Strs  + _NSMtbs.Values)
assert len(_NSMtbs) == 10


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
            m = _libObjC.class_getClassMethod(cls._Class, cls._SEL)
            m = _libObjC.method_getImplementation(m)
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
    _dt_fmt    = '%04d-%02d-%02d %02d:%02d:%06.3f'
    NS         =  None
    _timestamp =  None

    def __init__(self, nsExc):
        '''New L{NSExceptionError} wrapper.

           @param nsExc: The C{ObjC/NSException} instance to wrap.

           @raise TypeError: Invalid I{nsExc}.
        '''
        isObjCInstanceOf(nsExc, NSException, raiser='nsExc')
        self.NS = nsExc
        self._timestamp = _timestamp()
        n =  self.name or NSExceptionError.__name__
        r =  self.reason or _not_given_
        t = 'ObjC/' + _COLONSPACE_(n, r)
        RuntimeError.__init__(self, t)

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
        ns = self.NS
        return ns.name if ns else _NN_

    @property_RO
    def info(self):
        '''Get additional info about the exception (L{Adict}) or C{None}.
        '''
        ns = self.NS
        return ns2py(ns.userInfo(), dflt=None) if ns else None

    @property_RO
    def reason(self):
        '''Get the reason for the exception (C{str}) or C{None}.
        '''
        ns = self.NS
        return ns2py(ns.reason(), dflt=None) if ns else None

    @property_RO
    def callstack(self):
        '''Get the callstack of this exception (C{iter}), most recent last.
        '''
        ns = self.NS
        if ns:
            for s in nsIter(ns.callStackSymbols()):
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
        # see .utils._Globals.App
        return self._set_retain(Application=NSApplication.sharedApplication())

    @property_RO
    def BooleanNO(self):
        '''Get C{NSBoolean(NO)}.
        '''
        return self._set_retain(BooleanNO=NSBoolean(NO))

    @property_RO
    def BooleanYES(self):
        '''Get C{NSBoolean(YES)}.
        '''
        return self._set_retain(BooleanYES=NSBoolean(YES))

    @property_RO
    def Bundle(self):
        '''Get the C{NSBundle.mainBundle}.
        '''
        return self._set_retain(Bundle=NSBundle.mainBundle())

    @property_RO
    def BundleName(self):
        '''Get the C{NS/CFBundleName}.
        '''
        return self._set_retain(BundleName=NSStr('CFBundleName'))

    @property_RO
    def FontManager(self):
        '''Get the C{NSFontManager.sharedFontManager}.
        '''
        return self._set_retain(FontManager=NSFontManager.sharedFontManager())

    @property_RO
    def LayoutManager(self):
        '''Get the C{NSLayoutManager}.
        '''
        return self._set_retain(LayoutManager=NSLayoutManager.alloc().init())

    @property_RO
    def nil(self):  # in .runtime
        '''Get C{NSnil}.
        '''
        return self._set(nil=None)

    @property_RO
    def NO_false(self):
        '''Get C{NSfalse/NO}.
        '''
        return self._set(NO_false=NO)  # c_byte

    @property_RO
    def Nones(self):
        return self._set(Nones=(None, NSMain.Null))  # NSMain.nil

    @property_RO
    def Null(self):
        '''Get C{NSNull}.
        '''
        return self._set_retain(Null=NSNull.alloc().init())

    @property_RO
    def PrintInfo(self):
        '''Get the C{NSPrintInfo}.
        '''
        return self._set_retain(PrintInfo=NSPrintInfo.sharedPrintInfo())

    @property_RO
    def Screen(self):
        '''Get the C{NSScreen.mainScreen}, once.
        '''
        from pycocoa.screens import Screens  # circular
        return self._set_retain(Screen=Screens.NS.mainScreen())

    def _set_retain(self, **name_NS):
        name, NS = name_NS.popitem()
        return self._set(**{name: retain(NS)})

    @property
    def stdlog(self):
        '''Get the standard log file (C{stdout}, C{stderr}, other).
        '''
        return _Globals.stdlog

    @stdlog.setter  # PYCHOK property.setter
    def stdlog(self, file):
        '''Set the standard log file (C{file}-type).

           @raise TypeError: File I{file} doesn't have callable
                             C{write} and C{flush} attributes.
        '''
        try:
            if not (file and callable(file.write)
                         and callable(file.flush)):
                raise AttributeError(_no('.write, .flush'))
            _Globals.stdlog = file
        except AttributeError as x:
            t = _fmt_invalid(file=repr(file))
            raise TypeError(_COMMASPACE_(t, x))

    @property_RO
    def TableColumn(self):
        '''Get a blank C{NSTableColumn}.
        '''
        return self._set_retain(TableColumn=NSTableColumn.alloc().init())

    @property_RO
    def versionstr(self):
        '''Get the PyCocoa, Python, macOS versions as C{str}.
        '''
        return self._set(versionstr=_all_versionstr())

    @property_RO
    def YES_true(self):
        '''Get C{NStrue/YES}.
        '''
        return self._set(YES_true=YES)  # c_byte

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


def _NSStr(ustr):
    '''(INTERNAL) Return a C{released NSStr(ustr)}.
    '''
    return release(NSStr(ustr))


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

       @raise TypeError: Invalid I{path}.

       @see: U{mac-alias<https://GitHub.com/al45tair/mac_alias>} and
             U{here<https://StackOverflow.com/questions/21150169>}.
    '''
    if isinstance(path, _ByteStrs):
        path = _NSStr(path)
    elif isinstanceOf(path, NSStr, *_ByteStrs, raiser='path'):
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

       @raise TypeError: Invalid I{path}.
    '''
    if isinstance(path, _ByteStrs):
        p = path
    elif isinstanceOf(path, NSStr, *_ByteStrs, raiser='path'):
        p = path.str
    r = _os_path.islink(p)
    return _os_path.realpath(p) if r else isAlias(path)


def isNone(obj):
    '''Return True if I{obj} is C{None, NSMain.nil, NSMain.Null}, etc.

       @param obj: The object (L{ObjCInstance}).

       @return: True or False (C{bool}).
    '''
    return obj in NSMain.Nones


def _nsArray2items(ns):  # helper for nsArray2..., in .printers
    I_ = _libCF.CFArrayGetValueAtIndex
    for i in range(_libCF.CFArrayGetCount(ns)):
        yield I_(ns, i)


def nsArray2listuple(ns, ctype=Array_t, typy=None):  # XXX an NS*Array method?
    '''Create a Python C{list} or C{tuple} from an C{NS[Mutable]Array}.

       @param ns: The C{NS[Mutable]Array} instance (L{ObjCInstance}).
       @keyword ctype: The array item type (C{ctypes}).
       @keyword typy: Use C{B{typy}=list}, C{B{typy}=tuple} or
                      C{B{typy}=any_callable} to override the Python type.

       @return: The array (C{list} or C{tuple} or C{typy}).

       @raise TypeError: Invalid I{ns}.
    '''
    if isObjCInstanceOf(ns, *_NSImms.ArrayI01) and not ns.from_py2NS:  # NSScreen.screens()
        return nsArray2tuple(ns, typy=typy)
    _, py = _ns2Tpy2(ns, typy, list, tuple, **_raiser_ns)
    return py(_ns2ctype2py(c, ctype) for c in _nsArray2items(ns))


def nsArray2tuple(ns, ctype=ObjCInstance, typy=tuple):
    '''Create a Python C{tuple} from an I{immutable} C{NSArray}.

       @param ns: The C{NSArray} instance (L{ObjCInstance}).
       @keyword ctype: The array item type (C{ObjCInstance}).
       @keyword typy: Use C{B{typy}=any_callable} to override
                      the Python C{tuple} type.

       @return: The array (C{tuple} or C{typy}).

       @raise TypeError: Invalid I{ns}.
    '''
    isObjCInstanceOf(ns, *_NSImms.Arrays, **_raiser_ns)
    py = typy if typy and callable(typy) else tuple
    return py(ctype(c) for c in _nsArray2items(ns))


def nsBoolean2bool(ns, dflt=missing):  # XXX an NSBoolean method?
    '''Create a Python C{bool} from an C{NSBoolean}.

       @param ns: The C{NSBoolean} instance (L{ObjCInstance}).
       @keyword dflt: Default for a missing, unobtainable value (C{missing}).

       @return: The bool (C{bool}) of I{dlft}.

       @raise TypeError: Invalid I{ns}.
    '''
    # XXX need allow c_void_p for nested booleans in lists, sets, etc.?
    isObjCInstanceOf(ns, NSNumber, c_void_p, **_raiser_ns)
    return cfNumber2bool(ns, dflt=dflt)


def nsBundleRename(ns_title, match='Python'):
    '''Change the bundle title if the current title matches.

       @param ns_title: New bundle title (L{NSStr}).
       @keyword match: Optional, previous title to match (C{str}).

       @return: The previous bundle title (C{str}) or None.

       @raise TypeError: Invalid I{ns}.

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


def _ns2ctype2py(ns, ctype):  # in .screens
    # return C{ns} as a C{ctype} instance
    return ns2py(ns if isinstance(ns, ctype) else ctype(ns))


def nsData2bytes(ns, dflt=_bNN_):  # XXX an NSData method?
    '''Create Python C{bytes} from C{NSData}.

       @param ns: The C{NSData} instance (L{ObjCInstance}).
       @keyword dflt: Default for empty C{NSData} (C{bytes}).

       @return: The bytes (C{bytes}) or I{dflt}.

       @raise TypeError: Invalid I{ns}.
    '''
    isObjCInstanceOf(ns, NSData, **_raiser_ns)
    n = ns.length()
    if n:
        bs = (c_byte * n)()
        ns.getBytes_length_(byref(bs), n)
        bs = _bNN_.join(iterbytes(bs[:n]))
    else:
        bs =  dflt
    return bs


def nsDate2time(ns, since=1970):
    '''Create Python C{float} from C{NSDate}.

       @param ns: The C{NSDate} instance (L{ObjCInstance}).
       @keyword since: Epoch start date (1970, 2001) otherwise now.

       @return: The time in seconds (C{float}).

       @raise TypeError: Invalid I{ns}.
    '''
    isObjCInstanceOf(ns, NSDate, **_raiser_ns)
    t = ns.timeIntervalSince1970() if since == 1970 else (
        ns.timeIntervalSinceNow()  if since != 2001 else
        ns.timeIntervalSinceReferenceDate())  # CFDateGetAbsoluteTime(ns)
    return float(t)  # cfNumber2num(t)


def nsDecimal2decimal(ns):
    '''Create a Python C{Decimal} from an C{NSDecimal}.

       @param ns: The C{NSDecimal} instance (L{ObjCInstance}).

       @return: The decimal (C{Decimal}).

       @raise TypeError: If I{ns} not C{NSDecimal}.
    '''
    if isinstance(ns, NSDecimal):
        return ns.Decimal
    t = NSDecimal.__name__
    raise TypeError(_fmt_invalid(t, ns=repr(ns)))


def nsDescription2dict(ns, **defaults):
    '''Create an I{immutable} C{dict} object with key I{and} attribute access to items by name.

       @param ns: The C{NS...} instance (L{ObjCInstance}).
       @keyword defaults: Optional defaults items (Any kwds).
    '''
    from pycocoa.bases import _Type0  # avoid circular import

    class Description(_Type0, _frozendictbase):
        '''Immutable C{dict} typically used to wrap an I{immutable} C{Dictionary},
           like an C{NSScreen.} or C{NSPrinter.deviceDescription}.

           @note: Items are loaded from the C{Dictionary} on-demand I{only}.
        '''
        def __init__(self, ns, **defaults):
            self.NS = ns  # _NSImms.Dicts
            if defaults:
                _frozendictbase.__init__(self, defaults)

        def __getattr__(self, name):
            '''Get the value of an attribute or item by I{name}.
            '''
            v = self.get(name, missing)
            if v is missing:
                n = NSStr(name)
                v = c_void_p(None)
                t = _libCF.CFDictionaryGetValueIfPresent(self.NS, n, byref(v))
                if not t or isNone(v):
                    t = _DOT_(self.name, name)
                    t = _fmt('%s (%r)', t, n)
                    raise AttributeError(_fmt_invalid(item=t))
                v = _ns2ctype2py(v, c_void_p)
                dict.__setitem__(self, name, v)  # NOT _frozendictbase
            return v

        @property_RO
        def name(self):
            return dict.get(self, _name_, Description.__name__)

        def __repr__(self):
            return _SPACE_(self.typename, self)

#       def __setitem__(self, key, value):
#           t = _fmt('%s[%r] = %r', self.name, key, value)
#           raise TypeError(_COMMASPACE(t, 'immutable'))

        def __str__(self):
            '''Return this C{Description} as C{str}.
            '''
            return type2strepr(self, **self)

#       def copy(self):
#           '''Return a shallow copy.
#           '''
#           return type(self)(self.NS, **self)

    return Description(ns, **defaults)


def nsDictionary2dict(ns, ctype_keys=c_void_p, ctype_vals=c_void_p, typy=None):  # XXX an NS*Dictionary method?
    '''Create a Python C{dict} or C{frozendict} from an C{NS[Mutable|Frozen]Dictionary}.

       @param ns: The C{NSDictionary} instance (L{ObjCInstance}).
       @keyword ctype_keys: The dictionary keys type (C{ctypes}).
       @keyword ctype_vals: The dictionary values type (C{ctypes}).
       @keyword typy: Use C{B{typy}=dict}, C{B{typy}=Adict}, C{B{typy}=frozendict}
                      or C{B{typy}=any_callable} to override the Python type.

       @return: The dict (L{Adict} or C{frozendict} or C{typy}).

       @raise TypeError: Invalid I{ns}.
    '''
#   if isObjCInstanceOf(ns, *_NSImms.Dicts) and not ns.from_py2NS:  # NSScreen.deviceDescription()
#       return nsDescription2dict(ns)  # XXX Adict(map(ns2py, t) for t in nsDictionary2items(ns))
    _, py = _ns2Tpy2(ns, typy, Adict, dict, frozendict, **_raiser_ns)
    ts = _nsDictionary2items(ns, ctype_keys, ctype_vals)
    return py((_ns2ctype2py(k, ctype_keys),
               _ns2ctype2py(v, ctype_vals)) for k, v in ts)


def _nsDictionary2items(ns, ctype_keys, ctype_vals):  # helper for nsDictionary2...
    # <https://Developer.Apple.com/documentation/corefoundation/cfdictionary-rum>
    n  = _libCF.CFDictionaryGetCount(ns)
    ks = (ctype_keys * n)()
    vs = (ctype_vals * n)()
    _libCF.CFDictionaryGetKeysAndValues(ns, byref(ks), byref(vs))
    return zip(ks, vs)


def nsDictionary2items(ns):  # XXX an NS*Dictionary method?
    '''Yield the C{(key, value)} items from an C{NSDictionary}.

       @param ns: The C{NSDictionary} instance (L{ObjCInstance}).

       @return: A 2-tuple C{(key, value)} for each item, where
                each C{key} and C{value} is an L{ObjCInstance}.

       @raise TypeError: Invalid I{ns}.
    '''
    _ = _ns2Tpy2(ns, None, Adict, dict, frozendict, **_raiser_ns)
    for t in _nsDictionary2items(ns, c_void_p, c_void_p):
        yield tuple(map(ObjCInstance, t))


def nsException(name=None, reason=_not_given_, **info):
    '''Create an C{ObjC/NSException} instance.

       @keyword name: Ignored (U{NSExceptionName<https://Developer.Apple.com/
                      documentation/foundation/nsexceptionname>}).
       @keyword reason: The reason for the exception (C{str}).
       @keyword info: Other, caller-defined information (C{all keywords}).

       @return: The exception (C{ObjC/NSException}).

       @see: L{nsRaise}, L{nsThrow} and L{NSExceptionError}.

       @note: Use L{NSExceptionError}C{(nsExc)} to wrap a Python
              exception around an C{ObjC/NSException} instance and
              get access to the attributes of the latter.

       @note: Raised and thrown C{NSException}s can I{not be caught} and
              result in I{fatal} L{exiting}.

    '''
    from pycocoa.pytypes import dict2NS
    # <https://Developer.Apple.com/library/archive/documentation/
    #        Cocoa/Conceptual/Exceptions/Tasks/RaisingExceptions.html>
    # XXX use NSExceptionName inlieu of NSStr(name) since the latter
    # seems to always become 'NSException' instead of the _name_
    n = NSStr(name or nsException.__name__)
    r = NSStr(str(reason))
    d = dict2NS(info)
    return NSException.alloc().initWithName_reason_userInfo_(n, r, d)


def nsIter(ns, reverse=False, keys=False):
    '''Iterate over an C{NS..} ObjC objects's keys, values or reverse values.

       @param ns: The C{NS..} instance to iterate over (L{ObjCInstance}).
       @keyword reverse: If C{True}, iterate in reverse otherwise forward order
                         over C{B{ns}}' values (C{bool}).
       @keyword keys: If C{True}, iterate over C{B{ns}}' keys, provided C{B{ns}}
                      is an C{NS[Mutable]Dictionary} and ignoring C{B{reverse}}.

       @return: Yield each object or key (C{NS...}).

       @raise TypeError: Invalid I{ns}.

       @note: If C{B{ns}} is an C{NS[Mutable]Dictionary} and C{B{keys}=False}, the
              values of C{B{ns}} are enumerated in forward or  C{reverse} order.
    '''
    if ns and not isNone(ns):
        try:
            E = ns.keyEnumerator           if keys else (
                ns.reverseObjectEnumerator if reverse else
                ns.objectEnumerator)
            e = E().nextObject
        except AttributeError:
            t = _fmt_invalid('iterable', ns=repr(ns))
            raise TypeError(t)

        while True:
            ns = e()  # nil for end
            if isNone(ns):
                break
            yield ns


def nsIter2(ns, reverse=False, keys=False):
    '''Iterate over an C{NS..} ObjC objects's keys or (reverse) values.

       @see: Function L{nsIter} for C{B{ns}}, C{B{reverse}} and C{B{key}}
             details and function L{ns2Type} for Python C{Type}s.

       @return: Yield each object as 2-Tuple (I{py, ns}) where I{py} is a
                Python C{Type} instance and I{ns} the object C{NS...}.

       @raise TypeError: Invalid I{ns}.
    '''
    for ns in nsIter(ns, reverse=reverse, keys=keys):
        yield ns2Type(ns), ns


def nsLog(ns_fmt, *ns_args):
    '''Formatted ObjC write to the console.

       @param ns_fmt: A printf-like format string (L{NSStr}).
       @param ns_args: Optional arguments to format (C{all positional}).

       @raise TypeError: Invalid I{ns_fmt}.

       @note: The I{ns_fmt} and all I{ns_args} must be C{NS...} ObjC
              instances.

       @see: Dglessus' U{nslog.py<https://gist.GitHub.com/dgelessus>}.
    '''
    isinstanceOf(ns_fmt, NSStr, raiser='ns_fmt')
    for i, ns in enumerate(ns_args):
        if not isinstanceOf(ns, ObjCInstance, c_void_p):
            n = _fmt('%s[%s]', 'ns_args', i)  # raise error
            isinstanceOf(ns, ObjCInstance, raiser=n)
            break  # never reached
    else:  # XXX all ns_fmt %-types should be %@?
        _libFoundation.NSLog(ns_fmt, *ns_args)  # variadic, printf-like


def nsLogf(fmtxt, *args):
    '''Formatted write to the console.

       @param fmtxt: A printf-like format string (C{str}).
       @param args: Optional arguments to format (C{all positional}).

       @raise TypeError: Invalid I{fmtxt}.

       @see: L{nsLog}.
    '''
    isinstanceOf(fmtxt, *_ByteStrs, raiser='fmtxt')
    ns = NSStr(_fmt(fmtxt, *args))
    _libFoundation.NSLog(ns)  # variadic, printf-like


def ns2NSType2(ns):
    '''Get the main C{NS[Mutable]...} class and Python Type.

       @param ns: The C{NS...} instance (L{ObjCInstance}).

       @return: 2-Tuple C{(NS, Type)} with the C{NS[Mutable]...}
                class and Python Type, either may be C{None}.

       @raise TypeError: Invalid I{ns}.

       @see: Functions L{ns2Type} and L{ns2TypeID2}.
    '''
    T, py = _ns2Tpy2(ns, None, **_raiser_ns)
    if py is str and ns.objc_class in _NSMtbs.Strs:
        NS =  NSMutableString
    else:
        NS = _py2NS_get(py, None)
    if T is ns2py:
        T = type(ns2py(ns))
    return NS, T


def nsNull2none(ns):
    '''Return Python C{None} for an C{NS/CFNull} or C{nil}.

       @param ns: The C{NS...} instance (L{ObjCInstance}).

       @return: The singleton (C{None}).

       @raise TypeError: Invalid I{ns}.

       @raise ValueError: If I{ns} not C{isNone}.
    '''
    if isNone(ns) or isObjCInstanceOf(ns, NSNull, c_void_p):  # **_raiser_ns
        return None
    t = _fmt_invalid(isNone.__name__, ns=repr(ns))
    raise ValueError(t)


def nsNumber2num(ns, dflt=missing):  # XXX an NSNumber method?
    '''Create a Python C{Decimal}, C{int} or C{float} from an C{NSNumber}.

       @param ns: The C{NSNumber} instance (L{ObjCInstance}).
       @keyword dflt: Default for missing, unobtainable value (C{missing}).

       @return: The number (C{Decimal}, C{int} or C{float}).

       @raise TypeError: Invalid I{ns}.

       @raise ValueError: If I{ns} not an C{NSNumber}.
    '''
    # special case for NSDecimal, would become a float
    # since cfType of NSDecimal is kCFNumberDoubleType
    if isinstance(ns, NSDecimal):
        return ns.Decimal
    # XXX need c_void_p for nested numbers in lists, sets, etc.?
    isObjCInstanceOf(ns, NSNumber, c_void_p, **_raiser_ns)
    return cfNumber2num(ns, dflt=dflt)
#   raise ValueError(_fmt_invalid(NSNumber.name, ns=repr(ns)))


def nsOf(inst):
    '''Return the C{.NS} ObjC object of a Python wrapper or Type instance.

       @param inst: The wrapper (L{ObjCInstance} or C{Python Type}).

       @return: The C{.NS} object (C{NS...}).

       @raise TypeError: No C{.NS} for this I{inst}.
    '''
    try:
        return inst.NS
    except AttributeError:  # see also .bases.NS.setter
        pass
    if isinstanceOf(inst, ObjCInstance, c_struct_t, ObjC_t):
        return inst  # XXXX ????
    t = _fmt_invalid(_no('.NS'), inst=repr(inst))
    raise TypeError(t)


def ns2py(ns, dflt=missing):  # XXX an NSObject method?
    '''Convert an ObjC class' instance to the equivalent
       Python standard type's instance or wrapper and value.

       @param ns: The C{NS...} instance (L{ObjCInstance}).
       @keyword dflt: Default for unhandled, unexpected C{NS...}s (C{missing}).

       @return: The value (C{Python type}) or I{dflt} if provided.

       @raise TypeError: Invalid I{ns} or unhandled C{TypeID}.

       @note: Conversion map:

        - NSArray             -> tuple
        - NSBoolean           -> bool
        - NSConstantString    -> str
        - NSData              -> bytes
        - NSDecimalNumber     -> Decimal
        - NSDictionary        -> frozendict
        - NSMutableArray      -> list
        - NSMutableDictionary -> dict
        - NSMutableSet        -> set
        - NSMutableString     -> str
        - NSNumber            -> int or float
        - NSNull              -> None
        - NSSet               -> frozenset
        - NSStr               -> str
        - NSString            -> str

       @see: U{Converting values between Python and Objective-C
              <https://PythonHosted.org/pyobjc/core/typemapping.html>}
    '''
    if ns is None:  # or isNone(ns)
        r = None
    elif isinstance(ns, NSStr):
        r = ns.str
    else:  # see Rubicon-ObjC/objc/core_foundation.py
        # if isinstance(ns, ObjCInstance):
        #     ns = ns._as_parameter_
        _,  _ns = ns2TypeID2(ns, dflt=dflt)
        r = _ns(ns)
        C = {Id_t:    ObjCInstance,
             Class_t: ObjCClass}.get(type(r), lambda1)
        r = C(r)
    return r


def nsRaise(name=None, reason=_not_given_, **info):
    '''Create an C{NSException} and mimick C{@throw NSException}.

       @keyword name: Ignored (U{NSExceptionName<https://Developer.Apple.com/
                      documentation/foundation/nsexceptionname>}).
       @keyword reason: The reason for the exception (C{str}).
       @keyword info: Other, caller-defined information (C{all keywords}).

       @note: Raised C{NSException}s can I{not be caught} and result in
              I{fatal} L{exiting}.

       @see: L{NSException} and L{nsThrow}.
    '''
    # XXX use NSExceptionName, see nsException above
    nsThrow(nsException(name=name, reason=reason, **info))


def nsSet2set(ns, ctype=Set_t, typy=None):  # XXX NS*Set method?
    '''Create a Python C{set} or C{frozenset} from an C{NS[Mutable]Set}.

       @param ns: The C{NS[Mutable]Set} instance (L{ObjCInstance}).
       @keyword ctype: The set item type (C{ctypes}).
       @keyword typy: Use C{B{typy}=set}, C{B{typy}=frozenset} or
                      C{B{typy}=any_callable} to override the Python type.

       @return: The set (C{set} or C{frozenset} or C{typy}).

       @raise TypeError: Invalid I{ns}.
    '''
    _, py = _ns2Tpy2(ns, typy, set, frozenset, **_raiser_ns)
    n  = _libCF.CFSetGetCount(ns)  # == nsSet.count()
    cs = (ctype * n)()
    _libCF.CFSetGetValues(ns, byref(cs))
    return py(_ns2ctype2py(c, ctype) for c in cs)


def nsString2str(ns, dflt=None):  # XXX an NS*String method
    '''Create a Python C{str} or C{unicode} from an C{NS[Mutable]Str[ing]}.

       @param ns: The C{NS[Mutable]Str[ing]} instance (L{ObjCInstance}).

       @return: The string (C{str} or C{unicode}) or I{dflt}.
    '''
    # XXX need c_void_p for nested strings in lists, sets, etc.?
    if isinstanceOf(ns, NSStr, c_void_p) or \
           _ns2Tpy2(ns, None, str, **_raiser_ns):
        return cfString2str(ns, dflt=dflt)


def nsTextSize3(text, ns_font=None):
    '''Return the size of a multi-line text.

       @param text: The text (C{str}), including C{linesep}arators.
       @keyword ns_font: The text font (C{NSFont}) or C{None}.

       @return: 3-Tuple (width, height, lines) in (pixels, pixels) or
                in (characters, lines, lines) if I{ns_font} is C{None}.
    '''
    w = _NN_
    for t in text.split(_linesep):
        if len(t) > len(w):
            w = t

    h = n = text.count(_linesep) + 1
    if ns_font:
        h *= NSMain.LayoutManager.defaultLineHeightForFont_(ns_font)
        w = ns_font.widthOfString_(_NSStr(w))
    else:
        w = len(w)
    return w, h, n


def nsTextView(text, ns_font, scroll=50):
    '''Return an C{NSTextView} for the given text string.

       @keyword scroll: Make the C{NSTextView} scrollable
                        if the number of text lines exceeds
                        C{scroll} (C{int}).
    '''
    # <https://Developer.Apple.com/documentation/appkit/
    #        nsalert/1530575-accessoryview>
    w, h, n = nsTextSize3(text, ns_font=ns_font)
    if n > scroll:
        w, h = max(300, w), min(800, h)
    else:  # make the frame tall enough to avoid overwritten text
        w, h = 300, max(20, min(800, h))
    r = s = NSRect4_t(0, 0, w,   h)
    if w > 600:  # min(600, w)
        s = NSRect4_t(0, 0, 600, h)

    # XXX key NSFontAttributeName has a NSString value, no longer a Font?
    # d = NSDictionary.dictionaryWithObject_forKey_(ns_font, NSStr('NSFontAttributeName'))
    # t = NSAttributedString.alloc().initWithString_attributes_(NSStr(text), d)
    ns = NSTextView.alloc().initWithFrame_(r)
    ns.setFont_(ns_font)  # XXX set font BEFORE text
    ns.insertText_(_NSStr(text))
    ns.setEditable_(NO)
    ns.setDrawsBackground_(NO)
    if n > scroll:  # scrollable
        ns.setVerticallyResizable_(YES)
        ns.setHorizontallyResizable_(YES)

        sv = NSScrollView.alloc().initWithFrame_(s)
        sv.setHasVerticalScroller_(YES)
        sv.setHasHorizontalScroller_(YES)
        sv.setAutohidesScrollers_(YES)
        sv.setBorderType_(2)  # Border.Bezel or NSBezelBorder
        sv.setDocumentView_(ns)
        ns = sv
    else:
        ns.sizeToFit()
    return ns


@proxy_RO
def _NS2Tpy2s():
    # lazily build the C{_NS2Tpy2s} dict
    from pycocoa.dicts import Dict, FrozenDict
    from pycocoa.lists import List,  Tuple
    from pycocoa.sets import Set, FrozenSet
    from pycocoa.strs import Str  # PYCHOK fill _Types...
#   from pycocoa.tuples import Tuple  # from .lists
    # _Types.Attrs, validate with test/test_Dicts, -_Fonts, -_Lazily
    d = {}
    for Tpy2, NSs in (((List,       list),       _NSMtbs.Arrays),
                      ((Tuple,      tuple),      _NSImms.Arrays),
                      ((Dict,      Adict),       _NSMtbs.Dicts),
                      ((FrozenDict, frozendict), _NSImms.Dicts),
                      ((Set,        set),        _NSMtbs.Sets),
                      ((FrozenSet,  frozenset),  _NSImms.Sets),
                      ((ns2py,      str),        _NSMtbs.Strs + _NSImms.Strs)):
        for NS in NSs:
            # assert all(map(callable, Tpy2))
            d[NS] = Tpy2
    return d


def _ns2Tpy2(ns, typy, *pys, **raiser):
    # XXX order is critial, check NSMutual...s first,
    # NSMutual... may be a sub-class of the immutable
    NS = isObjCInstanceOf(ns, *_NSMtbs) or \
         isObjCInstanceOf(ns, *_NSImms, **raiser)
    try:
        T, py = _NS2Tpy2s[NS]
        if (pys and py not in pys) or not callable(T):
            t = _instr(_ns2Tpy2, ns, typy, *map(_nameOf, pys))
            r = _fmt('[%r]%s', NS, (T, py))
            raise AssertionError(_COLONSPACE_(t, r))
    except KeyError:
        T, py =  ns2py, None  # (pys[0] if pys else lambda1)
#       printf('ns2Type(%r) -> %s', ns.objc_class, type(ns2py(ns)))
    if typy and callable(typy):
        py = typy  # override
    return T, py


def nsThrow(nsExc):
    '''Mimick ObjC's C{@throw NSException} to raise an exception.

       @param nsExc: The exception to raise (C{NSException}).

       @see: L{NSException} and L{nsRaise}.

       @note: Thrown C{NSException}s can I{not be caught} and result
              in I{fatal} L{exiting}.

       @raise TypeError: Invalid I{nsExc}.
    '''
    # can't use ns_exception.raise() since 'raise' is reserved
    # in Python; see also .runtime.ObjCInstance.__getattr__
    # substituting method name 'throw' for 'raise'.
    if isObjCInstanceOf(nsExc, NSException, raiser='nsExc'):
        send_message(nsExc, 'raise')


def ns2Type(ns):
    '''Convert an C{NS...} ObjC object to an instance of the
       corresponding Python Type, I{capital T!}.

       @param ns: The C{NS...} instance (L{ObjCInstance}).

       @return: The instance (C{Python Type}).
    '''
    try:
        r =  ns.Type(ns)
    except AttributeError:
        T = _Types.Str if isinstance(ns, NSStr) else \
            _ns2Tpy2(ns, None)[0]
        # save the Python Type or ns2py convertor at the NS/Class
        # to expedite future conversions of such ObjC instances
        ns.objc_class._Type = T
        r = T(ns)
    return r


def ns2TypeID2(ns, dflt=None):
    '''Get the C{NS...} ObjC C{TypeID}.

       @param ns: The C{NS...} instance (L{ObjCInstance}).
       @keyword dflt: Default for unhandled, unexpected C{NS...}s (C{missing}).

       @return: 2-Tuple C{(TypeID, ns...2py)} of an C{int}NS
                and the type conversion C{callable}.

       @raise TypeError: Invalid I{ns}.
    '''
    # see Rubicon-ObjC/objc/core_foundation.py
    # if isinstance(ns, ObjCInstance):
    #     ns = ns._as_parameter_
    try:
        iD = _libCF.CFGetTypeID(ns)
    except ArgumentError as x:
        _Xargs(x, _libCF.CFGetTypeID.__name__,
                  _libCF.CFGetTypeID.argtypes,
                  _libCF.CFGetTypeID.restype)
        raise
    try:
        _ns2 = _CFTypeID2ns[iD]
    except KeyError:
        _ns2 =  dflt
        if dflt is missing:
            raise _CFTypeID2ns._Error(ns, iD, _unhandled_)
    return iD, _ns2


def nsURL2str(ns):
    '''Create a Python C{str} from C{NSURL} string.

       @param ns: The C{CFURL} instance (L{ObjCInstance}).

       @return: The URL as string (C{str}).

       @raise TypeError: Invalid I{ns}.
    '''
    isObjCInstanceOf(ns, NSURL, **_raiser_ns)
    # <https://NSHipster.com/nsurl>
    return nsString2str(ns.absoluteString())


def nsValue2py(ns, dflt=missing):
    '''Create a Python instance from an C{NS[Concrete]Value}.

       @param ns: The C{NS[Concrete]Value} instance (L{ObjCInstance}).
       @keyword dflt: Default for missing, unobtainable value.

       @raise TypeError: Invalid I{ns} or unhandled C{ns.objCType}.

       @return: The value (C{NSPoint_t}, C{NSRange_t}, C{NSRect_t},
                C{NSSize_t} or C{tuple}) or I{dflt}.

       @raise TypeError: Invalid I{ns}.
    '''
    if isObjCInstanceOf(ns, *_NSMtbs.Values):
        objCType = ns.objCType()
        try:
            ctype = _encoding2ctype[objCType]
            py = ctype()
            ns.getValue_(byref(py))
            return py
        except KeyError:
            T = repr(objCType)
    elif isObjCInstanceOf(ns, *_NSImms.Arrays):
        return nsArray2tuple(ns)  # _NS1Array!
    else:
        T = _NN_
    try:
        py = ObjCInstance(ns)
    except (TypeError, ValueError):
        py = dflt
        if dflt is missing:
            t = _instr(nsValue2py, repr(ns))
            t = _SPACE_(_unhandled_, t, T)
            raise TypeError(t)
    return py


_py2NS_get = {list:       NSMutableArray,  # function-like
              tuple:      NSArray,
              dict:       NSMutableDictionary,
              frozendict: NSDictionary,
              set:        NSMutableSet,
              frozenset:  NSSet,
#            _mtbstr:     NSMutableString,
              str:        NSString}.get


class _CFTypeID2ns(dict):  # singleton last
    '''ObjC TypeID to ns to Python converter.
    '''
    def _Error(self, ns, iD, why):
        t = _COMMASPACE_.join(self.itemstrs())
        t = _fmt('TypeID[%r]: %r {%s}', iD, ns, t)
        return TypeError(_SPACE_(why, t))

    def items(self):
        for iD, ns2 in dict.items(self):
            yield int(iD), ns2.__name__

    def itemstrs(self):
        for t in sorted(self.items()):
            yield _COLONSPACE_(*t)

_CFTypeID2ns = _CFTypeID2ns({1:          nsValue2py,  # PYCHOK _NSImms.Arrays
         _libCF.CFArrayGetTypeID():      nsArray2listuple,   # 19
         _libCF.CFBooleanGetTypeID():    nsBoolean2bool,     # 21
         _libCF.CFDataGetTypeID():       nsData2bytes,       # 20
         _libCF.CFDateGetTypeID():       nsDate2time,        # 42
         _libCF.CFDictionaryGetTypeID(): nsDictionary2dict,  # 18
         _libCF.CFNullGetTypeID():       nsNull2none,        # 16
         _libCF.CFNumberGetTypeID():     nsNumber2num,       # 22
         _libCF.CFSetGetTypeID():        nsSet2set,          # 17
         _libCF.CFStringGetTypeID():     nsString2str,       # 7
         _libCF.CFURLGetTypeID():        nsURL2str})         # 29

if __name__ == _Dmain_:

    from pycocoa.utils import _all_listing, _varstr

    print(_varstr(NSMain))

    _all_listing(__all__, locals())

    # XXX to shut up PyChecker
    del (_NSArrayI, _NSArrayM, _NS0ArrayI, _NS1ArrayI,
         _NSDictionaryI, _NSDictionaryM, _NS0DictionaryI, _NS1DictionaryI,
         _NSFrozenArrayM, _NSFrozenDictionaryM, _NSFrozenSetM,
         _NSCFConstantString, _NSCFString, _NSTaggedPointerString,
         _NSSetI, _NSSetM)

# % python3 -m pycocoa.nstypes
#
# pycocoa.nstypes.__all__ = tuple(
#  pycocoa.nstypes.at is <class .at>,
#  pycocoa.nstypes.isAlias is <function .isAlias at 0x103529b20>,
#  pycocoa.nstypes.isLink is <function .isLink at 0x103529c60>,
#  pycocoa.nstypes.isNone is <function .isNone at 0x103529d00>,
#  pycocoa.nstypes.ns2NSType2 is <function .ns2NSType2 at 0x10352a8e0>,
#  pycocoa.nstypes.ns2py is <function .ns2py at 0x10352ab60>,
#  pycocoa.nstypes.ns2Type is <function .ns2Type at 0x10352b100>,
#  pycocoa.nstypes.ns2TypeID2 is <function .ns2TypeID2 at 0x10352b1a0>,
#  pycocoa.nstypes.NSAlert is <ObjCClass(NSAlert of 0x203d32a68) at 0x1032027b0>,
#  pycocoa.nstypes.NSApplication is <ObjCClass(NSApplication of 0x203d32b80) at 0x103133ed0>,
#  pycocoa.nstypes.NSArray is <ObjCClass(NSArray of 0x203d0d438) at 0x103534050>,
#  pycocoa.nstypes.nsArray2listuple is <function .nsArray2listuple at 0x103529e40>,
#  pycocoa.nstypes.nsArray2tuple is <function .nsArray2tuple at 0x103529ee0>,
#  pycocoa.nstypes.NSAttributedString is <ObjCClass(NSAttributedString of 0x203d139c8) at 0x1032405a0>,
#  pycocoa.nstypes.NSAutoreleasePool is <ObjCClass(NSAutoreleasePool of 0x203d139f0) at 0x1031df650>,
#  pycocoa.nstypes.NSBezierPath is <ObjCClass(NSBezierPath of 0x203d32c98) at 0x1031df850>,
#  pycocoa.nstypes.NSBoolean is <ObjCBoundClassMethod(Class_t.numberWithBool_) at 0x103202cf0>,
#  pycocoa.nstypes.nsBoolean2bool is <function .nsBoolean2bool at 0x103529f80>,
#  pycocoa.nstypes.NSBundle is <ObjCClass(NSBundle of 0x203d13ab8) at 0x10312bc50>,
#  pycocoa.nstypes.nsBundleRename is <function .nsBundleRename at 0x10352a020>,
#  pycocoa.nstypes.NSColor is <ObjCClass(NSColor of 0x203d333c8) at 0x10355c320>,
#  pycocoa.nstypes.NSConcreteNotification is <ObjCClass(NSConcreteNotification of 0x203d126e0) at 0x10356bcb0>,
#  pycocoa.nstypes.NSConcreteValue is <ObjCClass(NSConcreteValue of 0x203d13c70) at 0x10356bbd0>,
#  pycocoa.nstypes.NSConstantString is <ObjCClass(NSConstantString of 0x203d13ce8) at 0x10319dcc0>,
#  pycocoa.nstypes.NSData is <ObjCClass(NSData of 0x203d0d500) at 0x103282510>,
#  pycocoa.nstypes.nsData2bytes is <function .nsData2bytes at 0x10352a160>,
#  pycocoa.nstypes.NSDate is <ObjCClass(NSDate of 0x203d0d528) at 0x1032825d0>,
#  pycocoa.nstypes.NSDecimal is <class .NSDecimal>,
#  pycocoa.nstypes.nsDecimal2decimal is <function .nsDecimal2decimal at 0x10352a2a0>,
#  pycocoa.nstypes.NSDecimalNumber is <ObjCClass(NSDecimalNumber of 0x203d13db0) at 0x103578680>,
#  pycocoa.nstypes.nsDescription2dict is <function .nsDescription2dict at 0x10352a340>,
#  pycocoa.nstypes.NSDictionary is <ObjCClass(NSDictionary of 0x203d0d578) at 0x1035787e0>,
#  pycocoa.nstypes.nsDictionary2dict is <function .nsDictionary2dict at 0x10352a3e0>,
#  pycocoa.nstypes.nsDictionary2items is <function .nsDictionary2items at 0x10352a520>,
#  pycocoa.nstypes.NSDockTile is <ObjCClass(NSDockTile of 0x203d236d0) at 0x1035837d0>,
#  pycocoa.nstypes.NSDouble is <ObjCBoundClassMethod(Class_t.numberWithDouble_) at 0x1035342d0>,
#  pycocoa.nstypes.NSEnumerator is <ObjCClass(NSEnumerator of 0x203d0d5a0) at 0x1030af9a0>,
#  pycocoa.nstypes.NSError is <ObjCClass(NSError of 0x203d13e50) at 0x1031d7a10>,
#  pycocoa.nstypes.NSException is <ObjCClass(NSException of 0x203d0d5c8) at 0x1031d78c0>,
#  pycocoa.nstypes.nsException is <function .nsException at 0x10352a5c0>,
#  pycocoa.nstypes.NSExceptionError is <class .NSExceptionError>,
#  pycocoa.nstypes.NSFloat is <ObjCBoundClassMethod(Class_t.numberWithDouble_) at 0x103534410>,
#  pycocoa.nstypes.NSFont is <ObjCClass(NSFont of 0x203d4bed0) at 0x1031d7850>,
#  pycocoa.nstypes.NSFontDescriptor is <ObjCClass(NSFontDescriptor of 0x203d4bf20) at 0x1031d74d0>,
#  pycocoa.nstypes.NSFontManager is <ObjCClass(NSFontManager of 0x203d23d38) at 0x1031d7380>,
#  pycocoa.nstypes.NSFontPanel is <ObjCClass(NSFontPanel of 0x203d23d88) at 0x1031d6f20>,
#  pycocoa.nstypes.NSImage is <ObjCClass(NSImage of 0x203d242d8) at 0x103550440>,
#  pycocoa.nstypes.NSImageView is <ObjCClass(NSImageView of 0x203d24440) at 0x1035504b0>,
#  pycocoa.nstypes.NSInt is <ObjCBoundClassMethod(Class_t.numberWithInt_) at 0x103227ce0>,
#  pycocoa.nstypes.nsIter is <function .nsIter at 0x10352a660>,
#  pycocoa.nstypes.nsIter2 is <function .nsIter2 at 0x10352a700>,
#  pycocoa.nstypes.NSLayoutManager is <ObjCClass(NSLayoutManager of 0x203d4c0b0) at 0x103550520>,
#  pycocoa.nstypes.nsLog is <function .nsLog at 0x10352a7a0>,
#  pycocoa.nstypes.nsLogf is <function .nsLogf at 0x10352a840>,
#  pycocoa.nstypes.NSLong is <ObjCBoundClassMethod(Class_t.numberWithLong_) at 0x103227950>,
#  pycocoa.nstypes.NSLongLong is <ObjCBoundClassMethod(Class_t.numberWithLongLong_) at 0x103289eb0>,
#  pycocoa.nstypes.NSMain.Application=NSApplication(<Id_t at 0x103531bd0>) of 0x12069e270,
#                        .BooleanNO=NSBoolean(<Id_t at 0x1035320d0>) of 0x208ea0890,
#                        .BooleanYES=NSBoolean(<Id_t at 0x103532750>) of 0x208ea0880,
#                        .Bundle=NSBundle(<Id_t at 0x103532950>) of 0x600001be40a0,
#                        .BundleName=NSConstantString('CFBundleName'),
#                        .FontManager=NSFontManager(<Id_t at 0x103533350>) of 0x600001be4af0,
#                        .LayoutManager=NSLayoutManager(<Id_t at 0x1035337d0>) of 0x120735e10,
#                        .nil=None,
#                        .NO_false=False,
#                        .Null=NSNull(<Id_t at 0x103533dd0>) of 0x208ea0c00,
#                        .PrintInfo=NSPrintInfo(<Id_t at 0x10350c450>) of 0x6000038c24a0,
#                        .Screen=NSScreen(<Id_t at 0x10350e5d0>) of 0x600001ce4f60,
#                        .stdlog=<_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>,
#                        .TableColumn=NSTableColumn(<Id_t at 0x10350ea50>) of 0x6000013ec380,
#                        .versionstr=pycocoa.version 25.2.22, .isLazy 1, Python 3.13.1 64bit arm64, macOS 14.7.3,
#                        .YES_true=True,
#  pycocoa.nstypes.NSMenu is <ObjCClass(NSMenu of 0x203d248f0) at 0x103550590>,
#  pycocoa.nstypes.NSMenuItem is <ObjCClass(NSMenuItem of 0x203d24940) at 0x103550600>,
#  pycocoa.nstypes.NSMutableArray is <ObjCClass(NSMutableArray of 0x203d0d690) at 0x103550670>,
#  pycocoa.nstypes.NSMutableData is <ObjCClass(NSMutableData of 0x203d0d6b8) at 0x1035506e0>,
#  pycocoa.nstypes.NSMutableDictionary is <ObjCClass(NSMutableDictionary of 0x203d0d6e0) at 0x103550750>,
#  pycocoa.nstypes.NSMutableSet is <ObjCClass(NSMutableSet of 0x203d0d730) at 0x1035507c0>,
#  pycocoa.nstypes.NSMutableString is <ObjCClass(NSMutableString of 0x203d14350) at 0x103550830>,
#  pycocoa.nstypes.NSNotification is <ObjCClass(NSNotification of 0x203d14378) at 0x1035508a0>,
#  pycocoa.nstypes.NSNotificationCenter is <ObjCClass(NSNotificationCenter of 0x203d143a0) at 0x103550910>,
#  pycocoa.nstypes.NSNull is <ObjCClass(NSNull of 0x203d0d758) at 0x103550980>,
#  pycocoa.nstypes.nsNull2none is <function .nsNull2none at 0x10352a980>,
#  pycocoa.nstypes.NSNumber is <ObjCClass(NSNumber of 0x203d143c8) at 0x1035509f0>,
#  pycocoa.nstypes.nsNumber2num is <function .nsNumber2num at 0x10352aa20>,
#  pycocoa.nstypes.NSObject is <ObjCClass(NSObject of 0x203cf1ff0) at 0x103550a60>,
#  pycocoa.nstypes.nsOf is <function .nsOf at 0x10352aac0>,
#  pycocoa.nstypes.NSOpenPanel is <ObjCClass(NSOpenPanel of 0x203d25020) at 0x103550ad0>,
#  pycocoa.nstypes.NSPageLayout is <ObjCClass(NSPageLayout of 0x203d25278) at 0x103550b40>,
#  pycocoa.nstypes.NSPrinter is <ObjCClass(NSPrinter of 0x203d25980) at 0x103550bb0>,
#  pycocoa.nstypes.NSPrintInfo is <ObjCClass(NSPrintInfo of 0x203d25818) at 0x103550c20>,
#  pycocoa.nstypes.NSPrintOperation is <ObjCClass(NSPrintOperation of 0x203d25890) at 0x103550c90>,
#  pycocoa.nstypes.NSPrintPanel is <ObjCClass(NSPrintPanel of 0x203d258e0) at 0x103550d00>,
#  pycocoa.nstypes.nsRaise is <function .nsRaise at 0x10352ac00>,
#  pycocoa.nstypes.NSSavePanel is <ObjCClass(NSSavePanel of 0x203d25fc0) at 0x103550d70>,
#  pycocoa.nstypes.NSScreen is <ObjCClass(NSScreen of 0x203d26010) at 0x103550de0>,
#  pycocoa.nstypes.NSScrollView is <ObjCClass(NSScrollView of 0x203d26088) at 0x103550e50>,
#  pycocoa.nstypes.NSSet is <ObjCClass(NSSet of 0x203d0d7f8) at 0x103550ec0>,
#  pycocoa.nstypes.nsSet2set is <function .nsSet2set at 0x10352aca0>,
#  pycocoa.nstypes.NSStatusBar is <ObjCClass(NSStatusBar of 0x203d26b00) at 0x103551010>,
#  pycocoa.nstypes.NSStr is <class .NSStr>,
#  pycocoa.nstypes.NSString is <ObjCClass(NSString of 0x203d148c8) at 0x103551080>,
#  pycocoa.nstypes.nsString2str is <function .nsString2str at 0x10352ad40>,
#  pycocoa.nstypes.NSTableColumn is <ObjCClass(NSTableColumn of 0x203d27000) at 0x1035510f0>,
#  pycocoa.nstypes.NSTableView is <ObjCClass(NSTableView of 0x203d27118) at 0x103551160>,
#  pycocoa.nstypes.NSTextField is <ObjCClass(NSTextField of 0x203d27370) at 0x1035511d0>,
#  pycocoa.nstypes.nsTextSize3 is <function .nsTextSize3 at 0x10352ade0>,
#  pycocoa.nstypes.nsTextView is <function .nsTextView at 0x10352ae80>,
#  pycocoa.nstypes.NSTextView is <ObjCClass(NSTextView of 0x203d27528) at 0x103551240>,
#  pycocoa.nstypes.NSThread is <ObjCClass(NSThread of 0x203d149b8) at 0x1035512b0>,
#  pycocoa.nstypes.nsThrow is <function .nsThrow at 0x10352b060>,
#  pycocoa.nstypes.NSURL is <ObjCClass(NSURL of 0x203d0d910) at 0x103551320>,
#  pycocoa.nstypes.nsURL2str is <function .nsURL2str at 0x10352b240>,
#  pycocoa.nstypes.NSValue is <ObjCClass(NSValue of 0x203d14b70) at 0x103551390>,
#  pycocoa.nstypes.nsValue2py is <function .nsValue2py at 0x10352b2e0>,
#  pycocoa.nstypes.NSView is <ObjCClass(NSView of 0x203d281a8) at 0x103551400>,
#  pycocoa.nstypes.NSWindow is <ObjCClass(NSWindow of 0x203d283b0) at 0x103551470>,
# )[102]
# pycocoa.nstypes.version 25.3.18, .isLazy 1, Python 3.13.2 64bit arm64, macOS 15.3.2

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
