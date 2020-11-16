
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Utility functions, constants, internals, etc.

@var missing: Missing keyword argument value.
'''

from pycocoa.lazily import _ALL_LAZY, isLazy, _lazy_import

import os
import sys
_Python_ = sys.version.split()[0]  # PYCHOK internal
_Python2 = sys.version_info.major < 3  # PYCHOK internal
_Python3 = sys.version_info.major > 2  # PYCHOK internal

__all__ = _ALL_LAZY.utils
__version__ = '20.11.15'


class module_property_RO(object):
    '''Decorator for a C{Read-Only} module property.

       @example:

         >>> @module_property_RO
         >>> def mp():  # no args
         >>>     return ro  # singleton or other

       @see: U{Module Properties | the Proxy Pattern
             <https://jtushman.GitHub.io/blog/2014/05/02/module-properties/>}.
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
        raise AttributeError('Read_Only property: %s.%s = %r' %
                             (self, method.__name__, ignored))

    return property(method, Read_Only, None, method.__doc__ or 'N/A')


class _MutableConstants(object):
    '''(INTERNAL) Enum-like, settable "constants".
    '''
    def __setattr__(self, name, value):
        if not hasattr(self, name):
            raise NameError('no such %s.%s' % (self.__class__.__name__, name))
        super(_MutableConstants, self).__setattr__(name, value)

    def _strepr(self, fmt):
        c = self.__class__.__name__.lstrip('_')
        j = ',\n%s.' % (' ' * len(c),)
        t = j.join(fmt(*t) for t in sortuples(self.items()))
        return '%s.%s' % (c, t)

    def __repr__(self):
        def _fmt(n, v):
            b, s = _int2(v)
            if s > 0:
                v = '%s<<%s' % (b, s)
            return '%s=%s' % (n, v)
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
        raise TypeError('%s.%s = %r' % (self.__class__.__name__, name, value))

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
            return c, ' '.join(map(repr, ns))
        else:
            return c, None

    def astrs(self, mask):
        '''Return constants mask as names (C{str}s).
        '''
        return ' '.join(n for n, m in self.items() if mask & m)


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
            if not n.startswith('_'):
                g, _ = property2(self, n)
                if g and (n in extra or hasattr(c, '_' + n)):
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
    Set           = None  # set by .sets.py
    ItemSeparator = None  # set by .menus.py
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
        c = ', '.join([''] + c)
    else:
        c = ''

    if name:
        t = 'not %s(%s%s): %r' % (func.__name__, name, c, inst)
    else:
        t = 'invalid %s(%r, %s)' % (func.__name__, inst, c)
    return TypeError(t)


# class Adict(dict):
#     '''A C{dict} with key I{and} attribute access to the items.
#     '''
#     _name = ''
#
#     def __init__(self, *args, **kwds):
#         if args:  # args override kwds
#             kwds = kwds.copy()
#             kwds.update(dict(args))
#         if 'name' in kwds:
#             self._name = kwds.pop('name'))  # see _Named.name
#         dict.__init__(self, kwds)
#
#     def __delattr__(self, name):
#         '''Delete an attribute or item by B{C{name}}.
#         '''
#         if name in ('name', '_name')):
#             dict.__setattr__(self, '_name', '')
#         elif dict.__contains__(self, name):
#             dict.pop(name)
#         else:
#             dict.__delattr__(self, name)
#
#     def __getattr__(self, name):
#         '''Get the value of an attribute or item by B{C{name}}.
#         '''
#         try:
#             return self[name]
#         except KeyError:
#             if name in ('name', '_name')
#                 return dict.__getattr__(self, '_name')
#             else:
#                 return dict.__getattr__(self, name)
#
#     def __getitem__(self, key):
#         '''Get the value of an item by B{C{key}}.
#         '''
#         return dict.__getitem__(self, key)
#
#     def __setattr__(self, name, value):
#         '''Set attribute or item B{C{name}} to B{C{value}}.
#         '''
#         if name in ('name', '_name'):
#             dict.__setattr__(self, '_name', value)
#         elif dict.__contains__(self, name):
#             dict.__setitem__(self, name, value)  # self[name] = value
#         else:
#             dict.__setattr__(self, name, value)
#
#     def __setitem__(self, key, value):
#         '''Set item B{C{key}} to B{C{value}}.
#         '''
#         if key in ('name', '_name'):
#             dict.__setattr__(self, '_name', value)
#         else:
#             dict.__setitem__(self, key, value)


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

           @param other: Items specified as an terable of 2-tuples
                         (key, value) or a C{dict}.
           @keyword kwds: Items given as C{key=value} pairs.
        '''
        d = {}
        if other:
            d.update(other[0])
        if kwds:
            d.update(kwds)
        for k, v in d.items():
            self.__setitem__(k, v)


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

    def bytes2str(bytestr, dflt=missing, name=''):
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

    def str2bytes(bytestr, dflt=missing, name=''):
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

    def bytes2str(bytestr, dflt=missing, name=''):  # PYCHOK expected
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

    def str2bytes(bytestr, dflt=missing, name=''):  # PYCHOK expected
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


def _all_listing(alls, localls, libs=False, _file_=''):
    '''(INTERNAL) Print sorted __all__ names and values.
    '''
    def _all_in(alls, inns, m, n):
        t = tuple(a for a in alls if a not in inns)
        if t:
            t = ', '.join(t)
            raise NameError('missing %s.%s: %s' % (m, n, t))

    f = _file_ or localls.get('__file__', '')
    m, n = _dirbasename2(f)
    printf('%s.%s = %s(', m, '__all__', alls.__class__.__name__, argv0='', nl=1)

    lazy = _ALL_LAZY.get(n, ())
    if lazy:
        _all_in(alls, lazy,   'lazily', n)
        _all_in(lazy, alls,    m, '__all__')
        _all_in(lazy, localls, m, 'locals()')

    d = i = 0
    p = ''
    for n in sorted(alls, key=str.lower):
        v = localls[n]
        r = repr(v)
        if isinstance(v, _Ints):
            r = '%s or 0x%X' % (r, v)
            v, s = _int2(v)
            if s > 2:
                r = '%s or %d << %s' % (r, v, s)
        elif r.startswith('<class '):
            r = r.replace("'", '')
        elif r.startswith('<function '):
            r = r[:10] + v.__module__ + '.' + r[10:]
        r = r.replace('__main__', '')  # .replace('__main__', m)
        if n == p:
            d += 1
            r += ' DUPLICATE'
        else:
            p = n
        if r.startswith(n + '.'):
            # increase indentation to align enums, constants, etc.
            r = r.replace(' ' * len(n), ' ' * (len(n) + len(m) + 2))
        else:
            r = '%s is %s' % (n, r)
        printf(' %s.%s,', m, r, argv0='')
        i += 1
    if d:
        d = ' %s%s%s' % (d, ' DUPLICATE', 's' if d > 1 else '')
    else:
        d = ''
    printf(')[%d]%s', i, d, argv0='')
    _all_versions(libs=libs, _file_=f, _version_=localls.get('__version__', ''))  # PYCHOK kwargs


def _all_versions(libs=False, _file_='', _version_=''):
    '''(INTERNAL) Print PyCocao, Python, macOS.
    '''
    printf(_all_versionstr(libs=libs, _file_=_file_, _version_=_version_), argv0='')


def _all_versionstr(libs=False, _file_='', _version_=''):
    '''(INTERNAL) PyCocao, Python, macOS, etc. versions as C{str}.
    '''
    from pycocoa import oslibs, _pycocoa, version as _version
    import platform

    t = (('version', _version_ or _version),  # PYCHOK shadow
         ('.isLazy',  str(isLazy)),
         ('Python',  _Python_, platform.architecture()[0]),
         ('macOS',    platform.mac_ver()[0]))
    if libs:
        t += ('oslibs', str(sorted(oslibs.get_libs().keys())).replace("'", '')),

    m, _ = _dirbasename2(_file_ or _pycocoa)
    return '%s.%s' % (m, ', '.join(' '.join(v) for v in t))


def aspect_ratio(width, height):
    '''Compute the smallest, integer aspect ratio.

       @param width: The width (C{float} or C{int}).
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
    # video 4:3, 16:9, 21:9 [14:10, 19:10]
    # photo 1:1, 3:2, 4:3, 5:3, 5:4, 7:5, 16:9,
    #            2:3  3:4  3:5  4:5  5:7  9:16
    r = gcd(width, height)
    if r and width and height:
        return int(width / r), int(height / r)
    else:
        return None


def clip(bytestr, limit=50):
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


def _dirbasename2(filename, sep='.'):
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
        pass
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

    t = ['%s=%s' % (a, _strepr(getattr(inst, a))) for a in attrs]
    return '%s(%s)' % (inst.__class__.__name__, ', '.join(t))


def _int2(i):
    '''(INTERNAL) Split an C{int} into 2-tuple (int, shift).
    '''
    s = 0
    if isinstance(i, _Ints) and i > 0:
        while not (i & 255):
            i >>= 8
            s += 8
        while not (i & 15):
            i >>= 4
            s += 4
        while not (i & 1):
            i >>= 1
            s += 1
    return i, s


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


def name2objc(name_):
    '''Convert a (selector) name to C{bytes} and ObjC naming rules.

       @param name_: Name to convert (C{str} or C{bytes}).

       @return: Converted name (C{bytes}).

       @note: A I{name_} starting with an underscore is returned as-is.
    '''
    b = str2bytes(name_)
    if not b.startswith(b'_'):
        b = b.replace(b'_', b':')
    return b


def name2py(name_):
    '''Convert a (selector) name C{str} and Python naming conventions.

       @param name_: Name to convert (C{str} or C{bytes}).

       @return: Converted name (C{str}).

       @note: A I{name_} starting with an underscore is returned as-is.
    '''
    s = bytes2str(name_)
    if not s.startswith('_'):
        s = s.replace(':', '_')
    return s


def name2pymethod(name_):
    '''Convert a (selector) name to a valid Python callback method.

       @param name_: Name to convert (C{str} or C{bytes}).

       @return: Converted name (C{str}).

       @raise ValueError: Invalid, non-alphanumeric I{name_}.
    '''
    m = name2py(name_)
    if not (m and m.replace('_', '').isalnum()):
        raise ValueError('invalid %s: %r' % ('name_', name_))
    return m


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


def _text_title2(text_or_file, title=''):
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


def type2strepr(inst, strepr=str):
    '''Represent a Python Type instance as L{str} or L{repr}.

       @param inst: Instance (C{any}).
       @keyword strepr: Representation function (C{repr} or C{str}).

       @return: Instance representation (C{str}).
    '''
    try:
        t = getattr(inst.NS, 'objc_classname', '')  # PYCHOK expected
    except AttributeError:
        t = ''
    try:
        t += '[%s]' % (len(inst),)
    except TypeError:
        pass
    return '%s(%s)' % (inst.__class__.__name__, strepr(t))


def _writestr(fmtxt, args=(), argv0=_Globals.argv0, nl=0, nt=0,
                               file=sys.stdout, flush=False):
    '''(INTERNAL) Write C{text} to C{file}.
    '''
    if args:
        try:
            fmtxt %= args
        except TypeError:
            fmtxt += str(map(str, args))
    s = ' ' if argv0 else ''
    t = '\n' * nl, argv0, s, fmtxt, '\n' * (nt + 1)
    n = file.write(''.join(t))
    if flush:
        file.flush()
    return n


def z1000str(size, sep='_'):
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
        t = '{0:_}'.format(z).replace('_', sep)
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
        fstr = fstr.rstrip('0').rstrip('.')
    return fstr


def zSIstr(size, B='B', K=1024):
    '''Convert a size to string with SI-units suffix.

       @param size: Value to convert (C{float} or C{int}).
       @keyword B: The unit (C{str}).
       @keyword K: 1024 or 1000 (C{int}).

       @return: "<Size> <SI>[i]<B>" (C{str}).
    '''
    z, si, k = float(size), '', float(K)
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
#  pycocoa.utils.aspect_ratio is <function .aspect_ratio at 0x7f8967a840d0>,
#  pycocoa.utils.bytes2repr is <built-in function repr>,
#  pycocoa.utils.bytes2str is <function .bytes2str at 0x7f8967a813a0>,
#  pycocoa.utils.Cache2 is <class .Cache2>,
#  pycocoa.utils.clip is <function .clip at 0x7f8967a84160>,
#  pycocoa.utils.DEFAULT_UNICODE is 'utf-8',
#  pycocoa.utils.flint is <function .flint at 0x7f8967a84280>,
#  pycocoa.utils.gcd is <built-in function gcd>,
#  pycocoa.utils.inst2strepr is <function .inst2strepr at 0x7f8967a84310>,
#  pycocoa.utils.isinstanceOf is <function .isinstanceOf at 0x7f8967a844c0>,
#  pycocoa.utils.iterbytes is <function .iterbytes at 0x7f8967a81d30>,
#  pycocoa.utils.lambda1 is <function .lambda1 at 0x7f8967a84550>,
#  pycocoa.utils.missing is missing,
#  pycocoa.utils.module_property_RO is <class .module_property_RO>,
#  pycocoa.utils.name2objc is <function .name2objc at 0x7f8967a845e0>,
#  pycocoa.utils.name2py is <function .name2py at 0x7f8967a84670>,
#  pycocoa.utils.name2pymethod is <function .name2pymethod at 0x7f8967a84700>,
#  pycocoa.utils.printf is <function .printf at 0x7f8967a84790>,
#  pycocoa.utils.properties is <function .properties at 0x7f8967a84820>,
#  pycocoa.utils.property2 is <function .property2 at 0x7f8967a848b0>,
#  pycocoa.utils.property_RO is <function .property_RO at 0x7f8967a708b0>,
#  pycocoa.utils.sortuples is <function .sortuples at 0x7f8967a84940>,
#  pycocoa.utils.str2bytes is <function .str2bytes at 0x7f8967a81dc0>,
#  pycocoa.utils.terminating is <function .terminating at 0x7f8967a849d0>,
#  pycocoa.utils.type2strepr is <function .type2strepr at 0x7f8967a84af0>,
#  pycocoa.utils.z1000str is <function .z1000str at 0x7f8967a84b80>,
#  pycocoa.utils.zfstr is <function .zfstr at 0x7f8967a84c10>,
#  pycocoa.utils.zSIstr is <function .zSIstr at 0x7f8967a84ca0>,
# )[28]
# pycocoa.utils.version 20.11.14, .isLazy 1, Python 3.9.0 64bit, macOS 10.15.7

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
