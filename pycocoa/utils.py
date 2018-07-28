
# -*- coding: utf-8 -*-

# License at the end of this file.

'''(INTERNAL) Utility functions, constants, etc.

@var missing: Missing keyword argument value.
'''
__version__ = '18.07.27'

try:  # all imports listed explicitly to help PyChecker
    from math import gcd  # Python 3+
except ImportError:
    try:
        from fractions import gcd  # Python 2-
    except ImportError:
        def gcd(a, b):
            while b:
                a, b = b, (a % b)
            return a


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
        t = j.join(fmt(*t) for t in sorted(self.items()))
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

    def items(self):
        '''Yield 2-tuple (name, value) for each constant.
        '''
        for n in dir(self):
            if n[:1].isupper():
                yield n, getattr(self, n)


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
    App      = None  # set by .apps.App.__init__, not an NSApplication!
    argv0    = 'PyCocoa'  # set by .nstypes.nsBundleRename and _allisting
    Items    = {}  # set by .menus.Item.__init__, gotten by .menus.ns2Item
    raiser   = False  # set by .apps.App.__init__
    Tables   = []  # set by .tables.TableWindow.__init__
    Windows  = {}  # set by .windows.Window.__init__
    Xhandler = None  # set by .nstype.nsUncaughtExceptionHandler


class _Singletons(_MutableConstants):
    '''(INTERNAL) Global, single instances.
    '''
    def __repr__(self):
        def _fmt(n, v):
            return '%s=%s' % (n, v)
        return self._strepr(_fmt)

    def items(self):
        '''Yield 2-tuple (name, value) for each singleton.
        '''
        c = self.__class__
        for n in dir(self):
            if not n.startswith('_'):
                g, _ = property2(self, n)
                if g and hasattr(c, '_' + n):
                    # XXX resolves the property
                    yield n, g(self)


class _Types(_MutableConstants):
    '''Python Types, to avoid circular imports.
    '''
    AlertPanel  = None  # set by .panels.py
    App         = None  # set by .apps.py
    Dict        = None  # set by .dicts.py
    ErrorPanel  = None  # set by .panels.py
    Font        = None  # sef by .fonts.py
    FrozenDict  = None  # set by .dicts.py
    FrozenSet   = None  # set by .sets.py
    Item        = None  # set by .menus.py
    List        = None  # set by .lists.py
    MediaWindow = None  # set by .windows.py
    Menu        = None  # set by .menus.py
    MenuBar     = None  # set by .menus.py
    OpenPanel   = None  # set by .panels.py
    SavePanel   = None  # set by .panels.py
    Set         = None  # set by .sets.py
    Separator   = None  # set by .menus.py
    Str         = None  # set by .strs.py
    StrAttd     = None  # set by .strs.py
    Table       = None  # set by .tables.py
    TableWindow = None  # set by .tables.py
    TextPanel   = None  # set by .panels.py
    TextWindow  = None  # set by .windows.py
    Tuple       = None  # set by .tuples.py
    Window      = None  # set by .windows.py


_Types = _Types()  # freeze


class Cache2(dict):
    '''Two-level cache implemented by two C{dict}s, a primary
       level-1 C{dict} and a secondary level-2 C{dict}.

       Frequently gotten key-value items are elevated into this,
       the primary level-1 C{dict}.  Newly created key-value pairs
       are entered into the secondary level-2 C{dict}.

       The secondary level-2 C{dict} can optionally be limited in
       size to avoid excessive growth.
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

    @property
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

    @property
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

    def __str__(self):
        return 'missing'


DEFAULT_UNICODE = 'utf-8'    # default Python encoding
missing         = missing()  # private, singleton


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

    def bytes2str(bytestr, dflt=missing):
        '''Convert C{bytes}/C{unicode} to C{str} if needed.

           @param bytestr: C{bytes}, C{str} or C{unicode}.
           @keyword dflt: Optional, default return value.

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
            raise TypeError('%s: %r' % ('bytes2str', bytestr))
        return dflt

    # iter(bytes) yields a 1-char str/byte in Python 2-
    iterbytes = iter

    def str2bytes(bytestr, dflt=missing):
        '''Convert C{str} to C{bytes}/C{unicode} if needed.

           @param bytestr: C{bytes}, C{str} or C{unicode}.
           @keyword dflt: Optional, default return value.

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
            raise TypeError('%s: %r' % ('str2bytes', bytestr))
        return dflt

except NameError:  # Python 3+
    _Bytes = bytes, bytearray
    _Ints  = int,
    _Strs  = str,

    bytes2repr = repr  # produces always b'...'

    def bytes2str(bytestr, dflt=missing):  # PYCHOK expected
        '''Convert C{bytes} to C{str} if needed.

           @param bytestr: C{str} or C{bytes}.
           @keyword dflt: Optional, default return value.

           @return: C{str} or I{dflt}.

           @raise TypeError: If neither C{str} nor C{bytes}, but
                             only if no I{dflt} is provided.
        '''
        if isinstance(bytestr, _Strs):
            return bytestr
        elif isinstance(bytestr, _Bytes):
            return bytestr.decode(DEFAULT_UNICODE)
        elif dflt is missing:
            raise TypeError('%s: %r' % ('bytes2str', bytestr))
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

    def str2bytes(bytestr, dflt=missing):  # PYCHOK expected
        '''Convert C{str} to C{bytes} if needed.

           @param bytestr: Original C{bytes} or C{str}.
           @keyword dflt: Optional, default return value.

           @return: C{bytes} or I{dflt}.

           @raise TypeError: If neither C{bytes} nor C{str}, but
                             only if no I{dflt} is provided.
        '''
        if isinstance(bytestr, _Bytes):
            return bytestr
        elif isinstance(bytestr, _Strs):
            return bytes(bytestr, DEFAULT_UNICODE)
        elif dflt is missing:
            raise TypeError('%s: %r' % ('str2bytes', bytestr))
        return dflt

_ByteStrs = _Bytes + _Strs  # bytes and/or str types


def _allisting(alls, localls, version, filename, argv0=''):
    '''(INTERNAL) Print sorted __all__ names and values.
    '''
    import os

    _Globals.argv0 = argv0

    m = os.path.basename(os.path.splitext(filename)[0])
    printf('%s.%s = %s(', m, '__all__', alls.__class__.__name__, nl=1)

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
            r = r.replace(' ' * len(n), ' ' * (len(n) + len(m) + 4))
            printf('  %s.%s,', m, r)
        else:
            printf('  %s.%s is %s,', m, n, r)
        i += 1
    if d:
        d = ' %s%s%s' % (d, ' DUPLICATE', 's' if d > 1 else '')
    else:
        d = ''
    printf(')[%d]%s', i, d)
    printf('%s.%s = %r', m, '__version__', version)


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


def _exports(localls, *names, **starts_ends):  # starts=(), ends=(), not_starts=())
    '''(INTERNAL) Return a tuple of __all__ exported names.
    '''
    s = starts_ends.pop('starts', ()) or ()
    e = starts_ends.pop('ends', ()) or ()
    n = starts_ends.pop('not_starts', ()) or ()
    if starts_ends:
        t = localls['__file__']
        raise ValueError('%s(..., %s) in %s' % ('_exports', ', '.join(
                         '%s=%r' % t for t in sorted(starts_ends.items())),
                          t))
    t = tuple(_ for _ in localls.keys() if (s and _.startswith(s))
                                        or (e and _.endswith(e)
                                              and not _.startswith('_'))
                                        or (n and not _.startswith(n)))
    for n in names:
        if n not in localls:
            raise NameError('no %r in %s' % (n, 'locals'))

    return t + names


def flint(f):
    '''Return C{int} for integer C{float}.
    '''
    try:
        if f.is_integer():
            return int(f)
    except AttributeError:
        pass
    return f


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

       @see: Function L{isInstanceOf} for checking ObjC instances.
    '''
    if isinstance(inst, classes):
        return inst.__class__

    name = name_missing.get('name', missing)
    if name is missing:
        return None

    t = ', '.join(getattr(c, '__name__', str(c)) for c in classes)
    raise TypeError('%s not %s: %r' % (name, t, inst))


def lambda1(arg):
    '''Inlieu of using M{lambda arg: arg}.
    '''
    return arg


def name2objc(name_):
    '''Convert a (selector) name to bytes and ObjC naming rules.

       @param name_: Name to convert (C{str} or C{bytes}).

       @return: Converted name (C{bytes}).
    '''
    return str2bytes(name_).replace(b'_', b':')


def name2py(name_):
    '''Convert a (selector) name to str and Python naming conventions.

       @param name_: Name to convert (C{str} or C{bytes}).

       @return: Converted name (C{str}).
    '''
    return bytes2str(name_).replace(':', '_')


def name2pymethod(name_):
    '''Convert a (selector) name to a valid Python callback method.

       @param name_: Name to convert (C{str} or C{bytes}).

       @return: Converted name (C{str}).

       @raise ValueError: Invalid, non-alphanumeric I{name_}.
    '''
    m = name2py(name_)
    if not (m and m.replace('_', '').isalnum()):
        raise ValueError('%s invalid: %r' % ('name_', name_))
    return m


def printf(fmt, *args, **kwds):  # argv0='', nl=0, nt=0
    '''Formatted print I{fmt % args} with optional keywords.

       @param fmt: Print-like format (C{str}).
       @param args: Optional arguments to include (I{all positional}).
       @keyword argv0: Optional prefix (C{str}).
       @keyword nl: Number of leading blank lines (C{int}).
       @keyword nt: Number of trailing blank lines (C{int}).
    '''
    a = kwds.get('argv0', _Globals.argv0)
    t = (fmt % args) if args else fmt
    nl = '\n' * kwds.get('nl', 0)
    nt = '\n' * kwds.get('nt', 0)
    print('%s%s %s%s' % (nl, a, t, nt))


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


def zSIstr(size, B='B', K=1024):
    '''Convert a size to string with SI-units suffix.

       @param size: Value to convert (C{float} or C{int}).
       @keyword B: The unit (C{str}).
       @keyword K: 1024 or 1000 (C{int}).

       @return: "<Size> <SI>[i]<B>" (C{str}).
    '''
    z, si, k = float(size), '', float(K)
    if z > k:
        for si in iter('KMGTPE'):
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


__all__ = _exports(locals(), 'aspect_ratio', 'Cache2', 'clip',
                             'DEFAULT_UNICODE', 'flint', 'isinstanceOf',
                             'gcd', 'iterbytes', 'lambda1', 'missing',
                             'printf', 'property2', 'type2strepr',
                   starts=('bytes', 'inst', 'name2', 'str', 'z'))

if __name__ == '__main__':

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
