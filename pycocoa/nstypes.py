
# -*- coding: utf-8 -*-

# License at the end of this file.

'''ObjC classes C{NS...} and conversions from C{NS...} ObjC to Python instances.

@var NSMain: Global C{NS...} singletons (C{const}).
'''
# all imports listed explicitly to help PyChecker
from decimal import Decimal as _Decimal
from ctypes  import ArgumentError, byref, cast, c_byte, CFUNCTYPE, c_void_p
from getters import get_selector
from octypes import Array_t, Class_t, c_struct_t, Id_t, NSRect4_t, \
                    ObjC_t, SEL_t, Set_t
from oslibs  import cfNumber2bool, cfNumber2num, cfString, cfString2str, \
                    cfURLResolveAlias, libAppKit, libCF, libFoundation, \
                    libobjc, NO, NSExceptionHandler_t, YES
from runtime import isInstanceOf, ObjCClass, ObjCInstance, release, \
                    retain, send_message, _Xargs
from utils   import bytes2str, _ByteStrs, clip, _exports, _Globals, \
                    isinstanceOf, iterbytes, lambda1, missing, \
                    _Singletons, _Types  # printf

from os import linesep, path as os_path

__version__ = '18.06.28'

# some commonly used Foundation and Cocoa classes, described here
# <http://OMZ-Software.com/pythonista/docs/ios/objc_util.html>

# NS... classes marked ** have Python versions, like NSStr, for
# for use by runtime.isInstanceOf repectively utils.isinstanceOf
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
    '''Optimized, Python L{NSDecimalNumber} class.
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

    @property
    def double(self):
        '''Get this L{NSDecimal} as a Python C{float}.
        '''
        return self.doubleValue()  # PYCHOK expected

#   @property
#   def objc_classname(self):
#       return self.__class__.__name__

    @property
    def value(self):
        '''Get this L{NSDecimal} as a Python C{Decimal}.
        '''
        return self._pyDec

    Decimal = value


class _NSMain(_Singletons):
    '''Global C{NS...} singletons.
    '''
    _Application   = None  # NSApplication, see .utils._Globals.App
    _BooleanNO     = None
    _BooleanYES    = None
    _Bundle        = None
    _BundleName    = None
    _FontManager   = None
    _LayoutManager = None
    _nil           = None  # final
    _NO_false      = NO  # c_byte
    _Null          = None
    _Screen        = None
    _ScreenFrame   = None
    _ScreenSize    = None
    _TableColumn   = None
    _YES_true      = YES  # c_byte

    # all globals are properties to delay instantiation

    @property
    def Application(self):
        '''Get the C{NSApplication.sharedApplication}.
        '''
        if self._Application is None:
            _NSMain._Application = retain(NSApplication.sharedApplication())
        return self._Application

    @property
    def BooleanNO(self):
        '''Get C{NSBoolean(NO)}.
        '''
        if self._BooleanNO is None:
            _NSMain._BooleanNO = retain(NSBoolean(NO))
        return self._BooleanNO

    @property
    def BooleanYES(self):
        '''Get C{NSBoolean(YES)}.
        '''
        if self._BooleanYES is None:
            _NSMain._BooleanYES = retain(NSBoolean(YES))
        return self._BooleanYES

    @property
    def Bundle(self):
        '''Get the C{NSBundle.mainBundle}.
        '''
        if self._Bundle is None:
            _NSMain._Bundle = retain(NSBundle.mainBundle())
        return self._Bundle

    @property
    def BundleName(self):
        '''Get the C{NS/CFBundleName}.
        '''
        if self._BundleName is None:
            _NSMain._BundleName = retain(NSStr('CFBundleName'))
        return self._BundleName

    @property
    def FontManager(self):
        '''Get the C{NSFontManager.sharedFontManager}.
        '''
        if self._FontManager is None:
            _NSMain._FontManager = retain(NSFontManager.sharedFontManager())
        return self._FontManager

    @property
    def LayoutManager(self):
        '''Get the L{NSLayoutManager}.
        '''
        if self._LayoutManager is None:
            _NSMain._LayoutManager = retain(NSLayoutManager.alloc().init())
        return self._LayoutManager

    @property
    def nil(self):
        '''Get C{NSnil}.
        '''
        return self._nil

    @property
    def NO_false(self):
        '''Get C{NSfalse/NO}.
        '''
        return self._NO_false

    @property
    def Null(self):
        '''Get the C{NSNull}.
        '''
        if self._Null is None:
            _NSMain._Null = retain(NSNull.alloc().init())
        return self._Null

    @property
    def Screen(self):
        '''Get the C{NSScreen.mainScreen}.
        '''
        if self._Screen is None:
            _NSMain._Screen = retain(NSScreen.alloc().init().mainScreen())
        return self._Screen

    @property
    def ScreenFrame(self):
        '''Get the C{NSScreen.mainScreen.frame}.
        '''
        if self._ScreenFrame is None:
            _NSMain._ScreenFrame = self.Screen.frame()  # NSRect_t
        return self._ScreenFrame

    @property
    def ScreenSize(self):
        '''Get the C{NSScreen.mainScreen.frame.size}.
        '''
        if self._ScreenSize is None:
            _NSMain._ScreenSize = self.ScreenFrame.size  # NSSize_t
        return self._ScreenSize

    @property
    def TableColumn(self):
        '''Get a blank L{NSTableColumn}.
        '''
        if self._TableColumn is None:
            _NSMain._TableColumn = retain(NSTableColumn.alloc().init())
        return self._TableColumn

    @property
    def YES_true(self):
        '''Get C{NStrue/YES}.
        '''
        return self._YES_true


NSMain  = _NSMain()  # global C{NS...} singletons


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

    def __str__(self):
        return '%s(%r)' % (self.objc_classname, clip(self.value))

#   @property
#   def objc_classname(self):
#       '''Get the ObjC class name (C{str}).
#       '''
#       return self.__class__.__name__

    @property
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

       @see: U{mac-alias<http://GitHub.com/al45tair/mac_alias>} and
             U{here<http://StackOverflow.com/questions/21150169/>}.
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
    if isInstanceOf(ns, NSMutableArray, NSArray, name='ns') is NSMutableArray:
        t = list
    else:
        t = tuple
    n = libCF.CFArrayGetCount(ns)
    f = libCF.CFArrayGetValueAtIndex
    return t(_ns2ctype2py(f(ns, i), ctype) for i in range(n))


def nsBoolean2bool(ns, dflt=missing):  # XXX an NSBoolean method?
    '''Create a Python C{bool} from an L{NSBoolean}.

       @param ns: The L{NSBoolean} (L{ObjCInstance}).
       @keyword dflt: Default for a missing, unobtainable value (C{missing}).

       @return: The bool (C{bool}) of I{dlft}.

       @raise TypeError: Unexpected C{NumberType}.
    '''
    # XXX need allow c_void_p for nested booleans in lists, sets, etc.?
    isInstanceOf(ns, NSNumber, c_void_p, name='ns')

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

    # <http://Developer.Apple.com/documentation/
    #       foundation/nsbundle/1495012-bundlewithpath>
    # ns = NSBundle.bundleWithPath_(os.path.abspath(match))
    p, ns = None, NSMain.Bundle
    if ns:
        ns = ns.localizedInfoDictionary() or ns.infoDictionary()
        if ns:
            p = ns.objectForKey_(NSMain.BundleName) or None
            if p:
                p = ns2py(p, dflt='') or ''
                if t and match in ('', None, p):  # can't be empty
                    ns.setObject_forKey_(ns_title, NSMain.BundleName)
    return p


def nsData2bytes(ns, dflt=b''):  # XXX an NSData method?
    '''Create Python C{bytes} from L{NSData}.

       @param ns: The L{NSData} (L{ObjCInstance}).
       @keyword dflt: Default for empty L{NSData} (C{bytes}).

       @return: The bytes (C{bytes}) or I{dflt}.
    '''
    isInstanceOf(ns, NSData, name='ns')
    n = ns.length()
    if n:
        buf = (c_byte * n)()
        ns.getBytes_length_(byref(buf), n)
        return b''.join(iterbytes(buf[:n]))
    return dflt


def nsDecimal2decimal(ns):
    '''Create a Python C{Decimal} from an L{NSDecimalNumber}.

       @param ns: The L{NSDecimalNumber} (L{ObjCInstance}).

       @return: The decimal (C{Decimal}).

       @raise ValueError: If I{ns} not an L{NSNumber}.
    '''
    if isinstance(ns, NSDecimal):
        return ns.Decimal
    return ValueError('%s not %s: %r' % ('ns', 'NSDecimal', ns))


def nsDictionary2dict(ns, ctype_keys=c_void_p, ctype_vals=c_void_p):  # XXX an NS*Dictionary method?
    '''Create a Python C{dict} from an C{NS[Mutable]Dictionary}.

       @param ns: The L{NSDictionary} instance (L{ObjCInstance}).
       @keyword ctype_keys: The dictionary keys type (C{ctypes}).
       @keyword ctype_vals: The dictionary values type (C{ctypes}).

       @return: The dict (C{dict}).
    '''
    # <http://Developer.Apple.com/documentation/corefoundation/cfdictionary-rum>
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
    if isInstanceOf(ns, NSNull, c_void_p, name='ns') or isNone(ns):
        return None
    return ValueError('%s not %s: %r' % ('ns', 'isNone', ns))


def nsNumber2num(ns, dflt=missing):  # XXX an NSNumber method?
    '''Create a Python C{Decimal}, C{int} or C{float} from an L{NSNumber}.

       @param ns: The L{NSNumber} (L{ObjCInstance}).
       @keyword dflt: Default for missing, unobtainable value (C{missing}).

       @return: The number (C{Decimal}, C{int} or C{float}).

       @raise TypeError: Unexpected C{NumberType}.

       @raise ValueError: If I{ns} not an L{NSNumber}.
    '''
    # special case for NSDecimal, would become a float
    # since cfType of NSDecimal is kCFNumberDoubleType
    if isinstance(ns, NSDecimal):
        return ns.Decimal
    # XXX need c_void_p for nested numbers in lists, sets, etc.?
    if isInstanceOf(ns, NSNumber, c_void_p, name='ns'):
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
    if isInstanceOf(ns, NSMutableSet, NSSet, name='ns') is NSSet:
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
        isInstanceOf(ns, NSConstantString, NSMutableString, NSString,
                         c_void_p, name='ns')

    return cfString2str(ns, dflt=dflt)


def nsTextSize3(text, ns_font=None):
    '''Return the size of a multi-line text.

       @param text: The text (C{str}), including C{linesep}arators.
       @keyword ns_font: The text font (L{NSFont}) or C{None}.

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
    '''Return an L{NSTextView} for the given text string.
    '''
    # <http://Developer.Apple.com/documentation/appkit/
    #       nsalert/1530575-accessoryview>
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

       @param ns_exception: The exception to raise (L{NSException}).
    '''
    # <http://Developer.Apple.com/library/archive/documentation/
    #       Cocoa/Conceptual/Exceptions/Tasks/RaisingExceptions.html>

    # can't use ns_exception.raise() since 'raise' is reserved
    # in Python; see also .runtime.ObjCInstance.__getattr__
    # substituting method name 'throw' for 'raise'.
    send_message(ns_exception, 'raise')


def nsUncaughtExceptionHandler(handler):
    '''Install an ObjC L{NSException} handler, the handler signature
       must match L{NSExceptionHandler_t} C{def handler(ns_exc): ...}.

       @param handler: A callable (L{NSExceptionHandler_t}).

       @return: Previously installed handler (L{NSExceptionHandler_t}).

       @note: Faults like C{SIGILL}, C{SIGSEGV}, etc. do
              not throw uncaught L{NSException}s and will
              not invoke this I{handler}.
    '''
    libAppKit.NSSetUncaughtExceptionHandler(NSExceptionHandler_t(handler))
    h, _Globals.Xhandler = _Globals.Xhandler, handler
    return h


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
    '''Convert (an instance of) an ObjC class to an instance of
       the equivalent Python standard type or wrapper and value.

       @param ns: The C{NS...} (L{ObjCInstance}).
       @keyword dflt: Default for unhandled, unexpected C{NS...}s (C{None}).

       @return: The value (C{Python type}) or I{dflt}.

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
    '''
    if isinstance(ns, NSStr):
        return ns.str

    elif ns is not None:  # not isNone(ns)
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
            if dflt is None:
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

    elif isinstanceOf(ns, NSStr):
        _Type = _Types.Str

    else:
        # printf('ns2Type(%r) -> %s', ns.objc_class, type(ns2py(ns)))
        _Type = ns2py

    # save the Python Type or ns2py convertor at the NS/Class
    # to expedite future conversions of such class instances
    ns.objc_class._Type = _Type
    return _Type(ns)


# filter locals() for .__init__.py
__all__ = _exports(locals(), 'at', 'isAlias', 'isLink', 'isNone',
                   starts=('NS', 'ns'),
                   ends='2NS')

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
