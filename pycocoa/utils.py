
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Utility functions, constants, internals, etc.

@var missing: Missing keyword argument value.
'''

from pycocoa.lazily import _ALL_LAZY, _COLON_, _COMMASPACE_, \
                           _DOT_, _EQUALS_, _lazy_import, \
                           _NL_, _NN_, _SPACE_, _UNDER_, isLazy

import os
import platform as _platform
import sys  # in pycocoa.oslibs.py
_Python_ = sys.version.split()[0]  # PYCHOK internal
_Python2 = sys.version_info.major < 3  # PYCHOK internal
_Python3 = sys.version_info.major > 2  # PYCHOK internal

__all__ = _ALL_LAZY.utils
__version__ = '21.11.04'

_bCOLON_ = b':'
_bUNDER_ = b'_'
_COMMA_  =  ','


class module_property_RO(object):
    '''Decorator for a C{Read-Only} module property.

       @example:

         >>> @module_property_RO
         >>> def mp():  # no args
         >>>     return ro  # singleton or other

       @see: U{Module Properties | the Proxy Pattern
             <https://JTushman.GitHub.io/blog/2014/05/02/module-properties/>}.
    '''
    def __init__(self, func):
        '''New L{module_property_RO}.

           @param func: Function to be decorated as C{property}
                        (C{callable, invoked without args}).
        '''
        self._func = func

    def __getattr__(self, name):
        return getattr(self._func(), name)


def property_RO(method):
    '''Decorator for C{Read_Only} class/instance property.

       @param method: The callable to be decorated as C{property}.

       @note: Like standard Python C{property} without a C{property.setter}
              with a more descriptive error message when set.
    '''
    def Read_Only(self, ignored):
        '''Throws an C{AttributeError}, always.
        '''
        raise AttributeError('Read_Only property: %s = %r' %
                             (_DOT_(self, method.__name__), ignored))

    return property(method, Read_Only, None, method.__doc__ or 'N/A')


class _MutableConstants(object):
    '''(INTERNAL) Enum-like, settable "constants".
    '''
    def __setattr__(self, name, value):
        if not hasattr(self, name):
            raise NameError('no such %s' % (_DOT_(self.__class__.__name__, name),))
        super(_MutableConstants, self).__setattr__(name, value)

    def _strepr(self, fmt):
        c = self.__class__.__name__.lstrip(_UNDER_)
        j = _NN_(',', _NL_, _SPACE_ * len(c), _DOT_)
        t = j.join(fmt(*t) for t in sortuples(self.items()))
        return _DOT_(c, t)

    def __repr__(self):
        def _fmt(n, v):
            return '%s=%s' % (n, _intstr(v))
        return self._strepr(_fmt)

    def __str__(self):
        def _fmt(n, unused):
            return n
        return self._strepr(_fmt)

    def get(self, name, *dflt):
        return getattr(self, name, *dflt)

    def items(self):
        '''Yield 2-tuple (name, value) for each constant.
        '''
        for n in self.keys():
            yield n, getattr(self, n)

    def items_(self, *classes):
        '''Yield 2-tuple (name, value) for each constant,
           if an instance of one of the B{C{classes}}.
        '''
        if classes:
            for n, v in self.items():
                if isinstance(v, classes):
                    yield n, v

    def keys(self):
        '''Yield each constant name.
        '''
        for n in dir(self):
            if n[:1].isupper():
                yield n

    def values(self):
        '''Yield each constant value.
        '''
        for n in self.keys():
            yield getattr(self, n)


class _Constants(_MutableConstants):
    '''(INTERNAL) Enum-like, read-only constants.
    '''
    def __setattr__(self, name, value):
        raise TypeError('%s = %r' % (_DOT_(self.__class__.__name__, name), value))

    def _masks(self, *names):
        ns = []
        for n in names:
            ns.extend(n.strip().lower().split())

        ns, c = set(ns), 0
        for n, m in self.items():
            n = n.lower()
            if n in ns:
                c |= m
                ns.remove(n)

        if ns:  # some invalid names
            return c, _SPACE_.join(map(repr, ns))
        else:
            return c, None

    def astrs(self, mask):
        '''Return constants mask as names (C{str}s).
        '''
        return _SPACE_.join(n for n, m in self.items() if mask & m)


class Adict(dict):
    '''A C{dict} with key I{and} attribute access to the items
       and callable to add items.
    '''
    def __call__(self, **kwds):
        '''Equivalent to C{self.update(B{kwds})}.
        '''
        dict.update(self, kwds)
        return self

    def __getattr__(self, name):
        '''Get the value of an attribute or item by B{C{name}}.
        '''
        try:
            return self[name]
        except KeyError:
            return dict.__getattr__(self, name)

    def __str__(self):
        '''Return this C{Adict} as C{str}.
        '''
        return '{%s}' % (_COMMASPACE_.join('%s=%r' % t
                         for t in sorted(self.items())),)

    def copy(self):
        '''Return a shallow copy.
        '''
        return self.__class__(self)


class _Globals(object):
    '''(INTERNAL) Some PyCocoa globals
    '''
    App       = None        # set by .apps.App.__init__, not an NSApplication!
    argv0     = 'pycocoa'   # set by .nstypes.nsBundleRename, _allisting, test/simple_VLCplayer
    Items     = {}          # set by .menus.Item.__init__, gotten by .menus.ns2Item
    MenuBar   = None        # set by .menus.MenuBar.__init__
#   Menus     = {}          # set by .menus._Menu_Type2._initM
    raiser    = False       # set by .apps.App.__init__
    stdlog    = sys.stdout  # set by .faults
    Tables    = []          # set by .tables.TableWindow.__init__
    Windows   = {}          # set by .windows.Window.__init__
    Xhandler2 = None        # set by .faults.setUncaughtExceptionHandler


class _Singletons(_MutableConstants):
    '''(INTERNAL) Global, single instances.
    '''
    def __repr__(self):
        def _fmt(n, v):
            return '%s=%s' % (n, v)
        return self._strepr(_fmt)

    def items(self, *extra):  # PYCHOK signature
        '''Yield 2-tuple (name, value) for each singleton.
        '''
        c = self.__class__
        for n in dir(self):
            if not n.startswith(_UNDER_):
                g, _ = property2(self, n)
                if g and (n in extra or hasattr(c, _UNDER_(_NN_, n))):
                    # XXX resolves the property
                    yield n, g(self)


class _Types(_MutableConstants):
    '''Python Types, to avoid circular imports.
    '''
    AlertPanel    = None  # set by .panels.py
    App           = None  # set by .apps.py
    Color         = None  # set by .colors.py
    Dict          = None  # set by .dicts.py
    ErrorPanel    = None  # set by .panels.py
    Font          = None  # sef by .fonts.py
    FrozenDict    = None  # set by .dicts.py
    FrozenSet     = None  # set by .sets.py
    Item          = None  # set by .menus.py
    ItemSeparator = None  # set by .menus.py
    List          = None  # set by .lists.py
    MediaWindow   = None  # set by .windows.py
    Menu          = None  # set by .menus.py
    MenuBar       = None  # set by .menus.py
    OpenPanel     = None  # set by .panels.py
    Paper         = None  # set by .printer.py
    PaperCustom   = None  # set by .printer.py
    PaperMargins  = None  # set by .printer.py
    Printer       = None  # set by .printer.py
    SavePanel     = None  # set by .panels.py
    Screen        = None  # set by .screens.py
    Set           = None  # set by .sets.py
    Str           = None  # set by .strs.py
    StrAttd       = None  # set by .strs.py
    Table         = None  # set by .tables.py
    TableWindow   = None  # set by .tables.py
    TextPanel     = None  # set by .panels.py
    TextWindow    = None  # set by .windows.py
    Tuple         = None  # set by .tuples.py
    Window        = None  # set by .windows.py

    if _Python3 and isLazy:
        def __getattribute__(self, name):
            '''(INTERNAL) Lazily import any missing _Types.
            '''
            return _MutableConstants.__getattribute__(self, name) or _lazy_import(name)

_Types = _Types()  # PYCHOK singleton


def _TypeError(name, inst, func, classes=()):
    '''(INTERNAL) Format a TypeError for func(inst, *classes).
    '''
    if classes:
        c = [getattr(c, '__name__', str(c)) for c in classes]
        c = _COMMASPACE_.join([_NN_] + c)
    else:
        c = _NN_

    if name:
        t = 'not %s(%s%s): %r' % (func.__name__, name, c, inst)
    else:
        t = 'invalid %s(%r, %s)' % (func.__name__, inst, c)
    return TypeError(t)


class Cache2(dict):
    '''Two-level cache implemented by two C{dict}s, a primary
       level-1 C{dict} and a secondary level-2 C{dict}.

       Newly created key-value pairs are entered into the
       secondary C{dict}.  Repeatedly gotten key-value items
       are elevated from the secondadry to the primary C{dict}.

       The secondary C{dict} can optionally be limited in size
       to avoid excessive growth.
    '''
    def __init__(self, limit2=None):
        '''New L{Cache2}, optionally limited in size.

           @keyword limit2: Size limit for the secondary level-2
                            C{dict} (C{int} or C{None}).
        '''
        self._limit2 = limit2
        self._dict2 = {}

    def __contains__(self, key):
        return dict.__contains__(key) or key in self._dict2

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            # .pop raises KeyError
            value = self._dict2.pop(key)
            # elevate to primary
            dict.__setitem__(self, key, value)
            return value

    def __setitem__(self, key, value):
        try:  # replace item if in primary
            if dict.__getitem__(self, key) != value:
                dict.__setitem__(self, key, value)
        except KeyError:
            if self._limit2:
                n = len(self._dict2)
                if n > max(4, self._limit2):
                    for k in list(self._dict2.keys())[:n//4]:
                        self._dict2.pop(k)
            self._dict2[key] = value
            # print(len(self), len(self._dict2))

    @property_RO
    def dict2(self):
        '''Get the secondary level-2 C{dict}.
        '''
        return self._dict2

    def get(self, key, default=None):
        '''Return the specified item's value.

           @param key: The item's key (C{any}).
           @keyword default: Default value for missing item (C{any}).

           @return: C{Cache2}I{[key]} if I{key} in C{Cache2}
                    else I{default} or C{None} if no I{default}
                    specified.
        '''
        try:
            return self.__getitem__(key)  # self[key]
        except KeyError:
            return default

    @property_RO
    def limit2(self):
        '''Get the secondary level-2 C{dict} size limit (C{int} or C{None}).
        '''
        return self._limit2

    def pop(self, key, *default):
        '''Remove the specified item.

           @param key: The item's key (C{any}).
           @param default: Value for missing item (C{any}).

           @return: C{Cache2}I{[key]} if I{key} in C{Cache2} else
                    I{default}, provided I{default} was specified.

           @raise KeyError: No such item I{key} and no I{default} given.

           @note: If I{key} is not in the primary level-1 C{dict}, the
                  secondary level-2 C{dict} is checked.
        '''
        try:
            return dict.pop(self, key)
        except KeyError:
            return self._dict2.pop(key, *default)

    def popitem(self):
        '''Remove the item most recently elevated into the primary
           level-1 C{dict}.

           @return: The removed item as 2-Tuple (key, value).

           @raise KeyError: The secondary level-2 C{dict} is empty.

           @note: Use C{Cache2.dict2.popitem()} to remove the most
                  recently entered item to the secondary level-2 C{dict}.
        '''
        return dict.popitem(self)

    def update(self, *other, **kwds):
        '''Update this cache with one or more additional items.

           @param other: Items specified as an iterable of 2-tuples
                         C{(key, value)} or as a C{dict}.
           @keyword kwds: Items given as C{key=value} pairs, with
                          priority over B{C{other}}.
        '''
        if other:
            dict.update(self, other[0])
        if kwds:
            dict.update(self, kwds)


class missing(object):
    '''Singleton class (named like instance, to be lost on purpose)
    '''
    def __eq__(self, unused):  # avoid '==' comparison
        raise SyntaxError("use 'is %s'" % (self,))

    def __ne__(self, unused):  # avoid '!=' comparison
        raise SyntaxError("use 'is not %s'" % (self,))

    def __repr__(self):
        return missing.__class__.__name__

    def __str__(self):
        return missing.__class__.__name__


DEFAULT_UNICODE = 'utf-8'    # default Python encoding
missing         = missing()  # private, singleton

try:  # MCCABE 23

    # in Python 2- bytes *is* str and bytes.__name__ == 'str'
    _Bytes = unicode, bytearray
    _Ints  = int, long  # PYCHOK for export
    _Strs  = basestring,

    def bytes2repr(bytestr):
        '''Represent C{bytes} or C{str} as C{b"..."}.

           @param bytestr: C{bytes} or C{str}..
           @return: Representation C{b'...'} (C{str}).
        '''
        return 'b%r' % (bytestr,)

    def bytes2str(bytestr, dflt=missing, name=_NN_):
        '''Convert C{bytes}/C{unicode} to C{str} if needed.

           @param bytestr: C{bytes}, C{str} or C{unicode}.
           @keyword dflt: Optional, default return value.
           @keyword name: Optional name of I{bytestr} argument.

           @return: C{str} or I{dflt}.

           @raise TypeError: If neither C{str} nor C{bytes}, but
                             only if no I{dflt} is provided.
        '''
        # XXX see Python-Vlc's vlc.py
        if isinstance(bytestr, _Strs):
            return bytestr
        elif isinstance(bytestr, _Bytes):
            # return str(bytestr, DEFAULT_UNICODE)
            return bytestr.decode(DEFAULT_UNICODE)
        elif dflt is missing:
            raise _TypeError(name, bytestr, bytes2str)
        return dflt

    # iter(bytes) yields a 1-charsstr/byte in Python 2-
    iterbytes = iter

    def str2bytes(bytestr, dflt=missing, name=_NN_):
        '''Convert C{str} to C{bytes}/C{unicode} if needed.

           @param bytestr: C{bytes}, C{str} or C{unicode}.
           @keyword dflt: Optional, default return value.
           @keyword name: Optional name of I{bytestr} argument.

           @return: C{bytes} or I{dflt}.

           @raise TypeError: If neither C{bytes} nor C{str}, but
                             only if no I{dflt} is provided.
        '''
        # XXX see Python-Vlc's vlc.py
        if isinstance(bytestr, _Strs):
            return bytestr
        elif isinstance(bytestr, _Bytes):
            return bytestr.encode(DEFAULT_UNICODE)
        elif dflt is missing:
            raise _TypeError(name, bytestr, str2bytes)
        return dflt

except NameError:  # Python 3+
    _Bytes = bytes, bytearray
    _Ints  = int,
    _Strs  = str,

    bytes2repr = repr  # produces always b'...'

    def bytes2str(bytestr, dflt=missing, name=_NN_):  # PYCHOK expected
        '''Convert C{bytes} to C{str} if needed.

           @param bytestr: C{str} or C{bytes}.
           @keyword dflt: Optional, default return value.
           @keyword name: Optional name of I{bytestr} argument.

           @return: C{str} or I{dflt}.

           @raise TypeError: If neither C{str} nor C{bytes}, but
                             only if no I{dflt} is provided.
        '''
        if isinstance(bytestr, _Strs):
            return bytestr
        elif isinstance(bytestr, _Bytes):
            return bytestr.decode(DEFAULT_UNICODE)
        elif dflt is missing:
            raise _TypeError(name, bytestr, bytes2str)
        return dflt

    # iter(bytes) yields an int in Python 3+
    def iterbytes(bytestr):
        '''Iterate C{bytes}, yielding each as C{byte}.
        '''
        for b in bytestr:  # convert int to bytes
            yield bytes([b])

    # double check iterbytes
    for b in iterbytes(b'a0'):
        assert isinstance(b, bytes), 'iterbytes failed'
    del b

    def str2bytes(bytestr, dflt=missing, name=_NN_):  # PYCHOK expected
        '''Convert C{str} to C{bytes} if needed.

           @param bytestr: Original C{bytes} or C{str}.
           @keyword dflt: Optional, default return value.
           @keyword name: Optional name of I{bytestr} argument.

           @return: C{bytes} or I{dflt}.

           @raise TypeError: If neither C{bytes} nor C{str}, but
                             only if no I{dflt} is provided.
        '''
        if isinstance(bytestr, _Bytes):
            return bytestr
        elif isinstance(bytestr, _Strs):
            return bytes(bytestr, DEFAULT_UNICODE)
        elif dflt is missing:
            raise _TypeError(name, bytestr, str2bytes)
        return dflt

_ByteStrs = _Bytes + _Strs  # bytes and/or str types


def _all_listing(alls, localls, libs=False, _file_=_NN_, argv0='#'):
    '''(INTERNAL) Print sorted __all__ names and values.
    '''
    def _all_in(alls, inns, m, n):
        t = tuple(a for a in alls if a not in inns)
        if t:
            t = _COMMASPACE_.join(t)
            raise NameError('missing %s: %s' % (_DOT_(m, n), t))

    f = _file_ or localls.get('__file__', _NN_)
    m, n = _dirbasename2(f)
    printf('%s = %s(', _DOT_(m, '__all__'), alls.__class__.__name__, argv0=argv0, nl=1)

    lazy = _ALL_LAZY.get(n, ())
    if lazy:
        _all_in(alls, lazy,   'lazily', n)
        _all_in(lazy, alls,    m, '__all__')
        _all_in(lazy, localls, m, 'locals()')

    d = i = 0
    p = _NN_
    for n in sorted(alls, key=str.lower):
        v = localls[n]
        r = repr(v)
        if isinstance(v, _Ints):
            r = '%s or 0x%X' % (r, v)
            v, s = _int2(v)
            if s > 2:
                r = '%s or %d << %s' % (r, v, s)
        elif r.startswith('<class '):
            r = r.replace("'", _NN_)
        elif r.startswith('<function '):
            r = r[:10] + _DOT_(v.__module__, r[10:])
        r = r.replace('__main__', _NN_)  # .replace('__main__', m)
        if n == p:
            d += 1
            r += ' DUPLICATE'
        else:
            p = n
        if r.startswith(_DOT_(n, _NN_)):
            # increase indentation to align enums, constants, etc.
            r = r.replace(_SPACE_ * len(n), _SPACE_ * (len(n) + len(m) + 2))
        else:
            r = '%s is %s' % (n, r)
        printf(' %s,', _DOT_(m, r), argv0=argv0)
        i += 1
    if d:
        d = _NN_(_SPACE_, d, ' DUPLICATE', 's' if d > 1 else _NN_)
    else:
        d = _NN_
    printf(')[%d]%s', i, d, argv0=argv0)
    _all_versions(libs=libs, _file_=f, _version_=localls.get('__version__', _NN_), argv0=argv0)  # PYCHOK kwargs


def _all_versions(libs=False, _file_=_NN_, _version_=_NN_, argv0=_NN_):
    '''(INTERNAL) Print PyCocao, Python, macOS.
    '''
    printf(_all_versionstr(libs=libs, _file_=_file_, _version_=_version_), argv0=argv0)


def _all_versionstr(libs=False, _file_=_NN_, _version_=_NN_):
    '''(INTERNAL) PyCocao, Python, macOS, etc. versions as C{str}.
    '''
    from pycocoa import oslibs, _pycocoa, version as _version

    t = (('version', _version_ or _version),  # PYCHOK shadow
         ('.isLazy',  str(isLazy)),
         ('Python',  _Python_, _platform.architecture()[0], machine()),
         ('macOS',   _macOSver()))
    if libs:
        t += ('oslibs', str(sorted(oslibs.get_libs().keys())).replace("'", _NN_)),

    m, _ = _dirbasename2(_file_ or _pycocoa)
    return _DOT_(m, _COMMASPACE_.join(_SPACE_.join(v) for v in t))


def aspect_ratio(width, *height, **Error_kwds):
    '''Compute the smallest, integer aspect ratio.

       @param width: The width (C{float}, C{int}, L{Size}, 2-tuple
                     (width, height), str("w:h") or C{NSSize_t}).
       @param height: The height (C{float} or C{int}).

       @return: 2-Tuple (width, height) as (C{int}, C{int}) or C{None}.

       @example:

       >>> aspect_ratio(10, 15)
       (2, 3)
       >>> aspect_ratio(10.0, 15)
       (2, 3)
       >>> aspect_ratio(10, -15)
       (-2, 3)
       >>> aspect_ratio(-10, -15)
       (2, 3)
       >>> aspect_ratio(10.5, 15)
       (7, 10)
       >>> aspect_ratio(0, 15)
       ()
    '''

    if height:
        r = (width,) + height
    else:
        r =  width
    try:
        s = bytes2str(r, dflt=None)
        if s is not None:
            w, h = map(int, s.split(_COLON_))
        elif isinstance(r, (tuple, list)) and len(r) == 2:
            w, h = map(flint, r)
        else:  # NSSize_t
            w, h = flint(r.width), flint(r.height)

        # video 4:3, 16:9, 21:9 [14:10, 19:10]
        # photo 1:1, 3:2, 4:3, 5:3, 5:4, 7:5, 16:9,
        #            2:3  3:4  3:5  4:5  5:7  9:16
        r = gcd(w, h)
        if r and w and h:
            r = float(r)
            return int(w / r), int(h / r)
        else:
            return None

    except (AttributeError, ValueError):
        pass  # to avoid chaining
    Error = Error_kwds.get('Error', ValueError)
    raise Error('invalid %s: %r' % ('ratio', r))


def clipstr(bytestr, limit=50):
    '''Clip a string to the given length limit.

       @param bytestr: String (C{bytes} or C{str}).
       @keyword limit: Length limit (C{int}).

       @return: Clipped C{bytes} or C{str}.
    '''
    if bytestr and limit > 10:
        n = len(bytestr)
        if n > limit:
            h = limit // 2
            t = type(bytestr)
            bytestr = bytestr[:h] + t('....') + bytestr[-h:]
        #   if XXX:
        #       bytestr += t('[' + str(n) + ']')
    return bytestr


def _dirbasename2(filename, sep=_DOT_):
    '''(INTERNAL) get the dir and base name of a C{filename} without extension.
    '''
    f = os.path.splitext(filename)[0]
    d, b = os.path.split(f.strip())
    while d and not b:  # ended with '/'
        d, b = os.path.split(d)
    _, d = os.path.split(d)
    if d and b:
        m = sep.join((d, b)) if sep else os.path.join(d, b)
        n = b
    else:
        m = n = d or b
    return m, n


def flint(f):
    '''Return C{int} for integer C{float}.
    '''
    try:
        if f.is_integer():
            return int(f)
    except AttributeError:
        if not isinstance(f, _Ints):
            raise
    return f


try:  # all imports listed explicitly to help PyChecker
    from math import gcd  # Python 3+
except ImportError:
    try:
        from fractions import gcd  # Python 2-
    except ImportError:

        def gcd(a, b):
            a, b = abs(a), abs(b)
            if a < b:
                a, b = b, a
            while b:
                a, b = b, (a % b)
            return a


def inst2strepr(inst, strepr, *attrs):
    '''Convert an instance's attributes, maintaining the order.

       @param inst: Instance (C{any}).
       @param strepr: Conversion (C{repr} or C{str}).
       @param attrs: Instance attribute names (I{all positional}).

       @return: Instance representation (C{str}).
    '''
    def _strepr(v):
        return repr(v) if isinstance(v, _ByteStrs) else strepr(v)

    t = ('%s=%s' % (a, _strepr(getattr(inst, a))) for a in attrs)
    return '%s(%s)' % (inst.__class__.__name__, _COMMASPACE_.join(t))


def _int2(i):
    '''(INTERNAL) Split an C{int} into 2-tuple (int, shift).
    '''
    s = 0
    if isinstance(i, _Ints) and i > 0:
        for m, n in ((255, 8), (15, 4), (1, 1)):
            while not (i & m):
                i >>= n
                s  += n
    return i, s


def _intstr(i):  # .windows
    '''(INTERNAL) Return C{int} as C{str}.
    '''
    b, s = _int2(i)
    return ('%s<<%s' % (b, s)) if s > 1 else str(i)


def isinstanceOf(inst, *classes, **name_missing):
    '''Check a Python instance' class.

       @param inst: The instance to check (I{any}).
       @param classes: One or several classes (I{all positional}).
       @keyword name: The name of the instance (C{str}).

       @return: The matching I{class} from I{classes}, None otherwise.

       @raise TypeError: If I{inst} does not match any of the I{classes},
                         but iff keyword I{name='...'} is provided.

       @see: Function L{isObjCInstanceOf} for checking ObjC instances.
    '''
    if isinstance(inst, classes):
        return inst.__class__

    name = name_missing.get('name', missing)
    if name is missing:
        return None

    raise _TypeError(name, inst, isinstanceOf, classes)


def lambda1(arg):
    '''Inlieu of using M{lambda arg: arg}.
    '''
    return arg


def logf(fmt, *args, **kwds):
    '''Formatted log I{fmt % args} with optional keywords.

       @param fmt: Print-like format or plain string (C{str}).
       @param args: Optional arguments to format (I{all positional}).
       @keyword argv0: Optional prefix (C{str}).
       @keyword file: Alternate file to write to (C{file}-type),
                      default C{NSMain.stdlog}.
       @keyword flush: Flush B{C{file}} after writing (C{bool}),
                       default C(True).
       @keyword nl: Number of leading blank lines (C{int}).
       @keyword nt: Number of trailing blank lines (C{int}).
    '''
    opts = dict(file=_Globals.stdlog, flush=True)
    if kwds:
        opts.update(kwds)
    _writestr(fmt, args, **opts)


def machine():
    '''Return the C{platform.machine} string, distinguishing Intel from
       I{emulating} Intel on Apple Silicon (on macOS).

       @return: Machine C{'arm64'} for Apple Silicon, C{"arm64_x86_64"} for
                Intel I{emulated}, C{'x86_64'} for Intel, etc. (C{str} with
                any C{comma}s by C{underscore}).
    '''
    m = _platform.machine().replace(_COMMA_, _UNDER_)  # arm64 Apple Si, x86_64, other?
    if m == 'x86_64':  # only on Intel or Rosetta2
        # <https://Developer.Apple.com/forums/thread/659846>
        if _sysctl_uint('sysctl.proc_translated') == 1:  # and \
#          _sysctl_uint('hw.optional.arm64') == 1:  # PYCHOK indent
            m = _UNDER_('arm64', m)  # Apple Silicon emulating Intel x86
    return m


def _macOSver():
    '''(INTERNAL) Return the macOS release as C{str}.

       @note: C{macOS 11 Big Sur} is C{'10.16'} before Python 3.9.6.
    '''
    return _platform.mac_ver()[0]


def _macOSver2(n=2):
    '''(INTERNAL) Return the macOS release as 1-, 2- or 3-tuple of C{int}s.

       @note: C{macOS 11 Big Sur} is C{(10, 16)} before Python 3.9.6.
    '''
    v = _macOSver()
    t = (tuple(map(int, v.split(_DOT_)[:n])) if v else ()) + (0, 0, 0)
    return t[:n]


def name2objc(name_):
    '''Convert a (selector) name to C{bytes} and ObjC naming rules.

       @param name_: Name to convert (C{str} or C{bytes}).

       @return: Converted name (C{bytes}).

       @note: A I{name_} starting with an underscore is returned as-is.
    '''
    b = str2bytes(name_)
    if not b.startswith(_bUNDER_):
        b = b.replace(_bUNDER_, _bCOLON_)
    return b


def name2py(name_):
    '''Convert a (selector) name C{str} and Python naming conventions.

       @param name_: Name to convert (C{str} or C{bytes}).

       @return: Converted name (C{str}).

       @note: A I{name_} starting with an underscore is returned as-is.
    '''
    s = bytes2str(name_)
    if not s.startswith(_UNDER_):
        s = s.replace(_COLON_, _UNDER_)
    return s


def name2pymethod(name_):
    '''Convert a (selector) name to a valid Python callback method.

       @param name_: Name to convert (C{str} or C{bytes}).

       @return: Converted name (C{str}).

       @raise ValueError: Invalid, non-alphanumeric I{name_}.
    '''
    m = name2py(name_)
    if m and m.replace(_UNDER_, _NN_).isalnum() and not m[:1].isdigit():
        return m
    raise ValueError('invalid %s: %r' % ('name_', name_))


def printf(fmt, *args, **kwds):
    '''Formatted print I{fmt % args} with optional keywords.

       @param fmt: Print-like format or plain string (C{str}).
       @param args: Optional arguments to format (I{all positional}).
       @keyword argv0: Optional prefix (C{str}).
       @keyword file: Alternate file to write to (C{file}-type),
                      default C{sys.stdout}.
       @keyword flush: Flush B{C{file}} after writing (C{bool}),
                       default C{False}.
       @keyword nl: Number of leading blank lines (C{int}).
       @keyword nt: Number of trailing blank lines (C{int}).
    '''
    _writestr(fmt, args, **kwds)


def properties(inst):
    '''All property names and values.

       @param inst: An instance (C{any}).

       @return: The properties (C{dict}).
    '''
    pd = {}
    for a in dir(inst):
        if type(getattr(inst.__class__, a)) is property:
            try:
                pd[a] = getattr(inst, a)
            except Exception as x:
                pd[a] = repr(x)
    return pd


def property2(inst, name):
    '''Return the property C{get} and C{set} method.

       @param inst: An instance (C{any}).
       @param name: Property name (C{str}).

       @return: 2-Tuple (get, set) as C{callable}s, (C{callable}, C{None})
                or (C{None}, C{None}) if I{inst.name} is not a property.
    '''
    try:
        p = getattr(inst.__class__, name)
        if isinstance(p, property):
            g = p.fget
            if callable(g):
                return g, p.fset
    except (AttributeError, TypeError, ValueError):
        pass
    return None, None


def sortuples(iterable):  # sort tuples
    '''Sort tuples alphabetically, case-insensitive.
    '''
    def _tup(tup):
        return tup[0].upper()
    return sorted(iterable, key=_tup)


def _sysctl_uint(name):
    '''(INTERNAL) Get an unsigned int sysctl item by name (on macOS).
    '''
    from pycocoa.oslibs import byref, c_char_p, c_size_t, c_uint, Libs, sizeof
    C = Libs.C
    if C:  # <https://StackOverflow.com/questions/759892/python-ctypes-and-sysctl>
        n = name if str is bytes else bytes(name, 'utf_8')  # PYCHOK isPython2 = str is bytes
        u = c_uint(0)
        z = c_size_t(sizeof(u))
        r = C.sysctlbyname(c_char_p(n), byref(u), byref(z), None, c_size_t(0))
    else:  # could find or load 'libc'
        r = -2
    return int(r if r else u.value)  # -1 ENOENT error, -2 no libc


def terminating(app, timeout=None):
    '''Set up a separate thread to terminate an NSApplication
       by calling the C{.terminate_} method after the given
       timeout has elapsed.

       @return: Timeout in seconds (C{float}) or C{None}.

       @note: Similarly, the NSWindow could be closed, provided
              the NSWindow or NSApplication C{Delegate} instance
              includes the C{.windowWillClose_} method which in
              turn terminates the NSApplication's C{.terminate_}
              method.
    '''
    try:
        s = float(timeout)
        t = app.terminate_
    except AttributeError:
        raise ValueError('invalid %s: %r' % ('app', app))
    except (TypeError, ValueError):
        return None

    def _t():
        from time import sleep
        sleep(s + 0.5)
        # <https://Developer.Apple.com/documentation/appkit/nsapplication/1428417-terminate>
        t(app)

    from threading import Thread
    Thread(target=_t).start()

    return s


def _text_title2(text_or_file, title=_NN_):
    '''(INTERNAL) Return 2-tuple (title, text).
    '''
    if isinstance(text_or_file, _ByteStrs):
        text, t = text_or_file, title
    else:
        try:
            text = text_or_file.read()
        except (AttributeError, IOError, OSError) as x:
            text = str(x)
        t = 'File %r' % (getattr(text_or_file, 'name', None),)
    return text, t


def type2strepr(inst, strepr=str, **kwds):
    '''Represent a Python Type instance as L{str} or L{repr}.

       @param inst: Instance (C{any}).
       @keyword strepr: Representation function (C{repr} or C{str}).

       @return: Instance representation (C{str}).
    '''
    try:
        t = getattr(inst.NS, 'objc_classname', _NN_)  # PYCHOK expected
    except AttributeError:
        t = _NN_
    try:
        t += '[%s]' % (len(inst),)
    except TypeError:
        pass
    try:
        d = dict(name=repr(inst.name))
        d.update(kwds)
    except AttributeError:
        d = kwds
    d = tuple(_EQUALS_(n, v) for n, v in d.items())
    if t and d:
        t = _COMMASPACE_(strepr(t), *d)
    elif d:
        t = _COMMASPACE_.join(d)
    else:
        t = strepr(t)
    return '%s(%s)' % (inst.__class__.__name__, t)


def _varstr(constants, strepr=None):
    '''(INTERNAL) Return all C{@var Class.<name>: <doc>} lines as C{str}.
    '''
    def _doc1(c, n, f):
        # get class c's 1st __doc__ line or value from f(c)
        d = f(c) if callable(f) else (
            getattr(c, '__doc__') or _NN_)  # PYCHOK getattr
        t = d.split(_NL_)[0].strip().rstrip(_DOT_)
        return '@var %s: %s.' % (n, t)

    C = constants.__class__
    N = C.__name__.lstrip(_UNDER_)
    v = [_NN_, _doc1(C, N, None)]
    for n, _ in constants.items():
        v.append(_doc1(getattr(C, n), _DOT_(N, n), strepr))
    return _NL_.join(v)


def _writestr(fmtxt, args=(), file=sys.stdout, flush=False,
                              nl=0, nt=0, **argv0):
    '''(INTERNAL) Write C{text} to C{file}.
    '''
    if args:
        try:
            fmtxt %= args
        except TypeError:
            fmtxt += str(map(str, args))
    a = argv0.get('argv0', _Globals.argv0)
    if a:
        s = _SPACE_
        fmtxt = fmtxt.replace(_NL_, _NN_(_NL_ + a + s))
    else:
        s = _NN_
    t = _NL_ * nl, a, s, fmtxt, _NL_ * (nt + 1)
    n = file.write(_NN_.join(t))
    if flush:
        file.flush()
    return n


def z1000str(size, sep=_UNDER_):
    '''Convert a size to string with 1_000's seperator.

       @param size: Value to convert (C{float} or C{int}).
       @keyword sep: 1_000's separator (C{str}),

       @return: "<1or2digits><sep><3digits>..." or "-" if
                I{size} is negative (C{str}).
   '''
    z = int(size)
    if z < 0:
        return '-'
    try:  # '_' only in Python 3.6+
        t = '{0:_}'.format(z).replace(_UNDER_, sep)
    except ValueError:
        try:  # ',' only in Python 3.1+
            t = '{0:,}'.format(z).replace(',', sep)
        except ValueError:
            t = str(z)
            n = len(t)
            while n > 3:
                n -= 3
                t = t[:n] + sep + t[n:]
    return t


def zfstr(flt, prec=3):
    '''Format a C{float} and strip trailing zero decimals.

       @param flt: Value (C{float}).
       @keyword prec: Number of decimals (C{int}).

       @return: Value (C{str}).
    '''
    fstr = '%.*f' % (prec, float(flt))
    if prec > 0:
        fstr = fstr.rstrip('0').rstrip(_DOT_)
    return fstr


def zSIstr(size, B='B', K=1024):
    '''Convert a size to string with SI-units suffix.

       @param size: Value to convert (C{float} or C{int}).
       @keyword B: The unit (C{str}).
       @keyword K: 1024 or 1000 (C{int}).

       @return: "<Size> <SI>[i]<B>" (C{str}).
    '''
    z, si, k = float(size), _NN_, float(K)
    if z > k:
        # Science Mag, vol 363, issue 6428, p 681, Feb 15, 2019
        # "Metric prefixes sought for extremely large numbers",
        # Ronna 10^27 and Quecca 10^30
        for si in iter('KMGTPEZYRQ'):
            z /= k
            if z < k:
                if k == 1024.0:
                    si += 'i'
                si = '%.1f %s%s' % (z, si, B)
                break
        else:
            si = '%.3e %s' % (float(size), B)
    else:
        si = '%d %s' % (int(size), B)
    return si


if __name__ == '__main__':

    _all_listing(__all__, locals())

# % python3 -m pycocoa.utils
#
# pycocoa.utils.__all__ = tuple(
#  pycocoa.utils.Adict is <class .Adict>,
#  pycocoa.utils.aspect_ratio is <function .aspect_ratio at 0x1050ad000>,
#  pycocoa.utils.bytes2repr is <built-in function repr>,
#  pycocoa.utils.bytes2str is <function .bytes2str at 0x1050ac3a0>,
#  pycocoa.utils.Cache2 is <class .Cache2>,
#  pycocoa.utils.clipstr is <function .clipstr at 0x1050ad090>,
#  pycocoa.utils.DEFAULT_UNICODE is 'utf-8',
#  pycocoa.utils.flint is <function .flint at 0x1050ad1b0>,
#  pycocoa.utils.gcd is <built-in function gcd>,
#  pycocoa.utils.inst2strepr is <function .inst2strepr at 0x1050ad240>,
#  pycocoa.utils.isinstanceOf is <function .isinstanceOf at 0x1050ad3f0>,
#  pycocoa.utils.iterbytes is <function .iterbytes at 0x1050acd30>,
#  pycocoa.utils.lambda1 is <function .lambda1 at 0x1050ad480>,
#  pycocoa.utils.logf is <function .logf at 0x1050ad510>,
#  pycocoa.utils.machine is <function .machine at 0x1050ad5a0>,
#  pycocoa.utils.missing is missing,
#  pycocoa.utils.module_property_RO is <class .module_property_RO>,
#  pycocoa.utils.name2objc is <function .name2objc at 0x1050ad750>,
#  pycocoa.utils.name2py is <function .name2py at 0x1050ad7e0>,
#  pycocoa.utils.name2pymethod is <function .name2pymethod at 0x1050ad870>,
#  pycocoa.utils.printf is <function .printf at 0x1050ad900>,
#  pycocoa.utils.properties is <function .properties at 0x1050ad990>,
#  pycocoa.utils.property2 is <function .property2 at 0x1050ada20>,
#  pycocoa.utils.property_RO is <function .property_RO at 0x104fb5bd0>,
#  pycocoa.utils.sortuples is <function .sortuples at 0x1050adab0>,
#  pycocoa.utils.str2bytes is <function .str2bytes at 0x1050acdc0>,
#  pycocoa.utils.terminating is <function .terminating at 0x1050adbd0>,
#  pycocoa.utils.type2strepr is <function .type2strepr at 0x1050adcf0>,
#  pycocoa.utils.z1000str is <function .z1000str at 0x1050adea0>,
#  pycocoa.utils.zfstr is <function .zfstr at 0x1050adf30>,
#  pycocoa.utils.zSIstr is <function .zSIstr at 0x1050adfc0>,
# )[31]
# pycocoa.utils.version 21.11.04, .isLazy 1, Python 3.11.0 64bit arm64, macOS 13.0.1

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
