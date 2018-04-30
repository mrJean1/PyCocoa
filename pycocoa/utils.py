
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

# MIT License <http://opensource.org/licenses/MIT>
#
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

'''(INTERNAL) Utility functions, constants, etc.
'''
# all imports listed explicitly to help PyChecker
__version__ = '18.04.27'

try:
    from math import gcd  # Python 3+
except ImportError:
    try:
        from fractions import gcd  # Python 2-
    except ImportError:
        def gcd(a, b):
            while b:
                a, b = b, (a % b)
            return a


class _Constants(object):
    '''Only constant, readable attributes.
    '''
    def __init__(self, *unused):
        raise AssertionError('%s is constant' % (self.__class__.__name__,))

    __setattr__ = __init__


class _Globals(object):  # some PyCocoa-internal globals
    App     = None  # XXX single instance only
    argv0   = 'PyCocoa'  # set by .nstypes.nsBundleRename
    Items   = {}
    raiser  = False
    Tables  = []
    Windows = {}


class _Types(_Constants):
    '''Holder of the Python Types, to avoid circular imports.
    '''
    Dict        = None  # set by .dicts.py
    FrozenDict  = None  # set by .dicts.py
    FrozenSet   = None  # set by .sets.py
    Item        = None  # set by .menus.py
    List        = None  # set by .lists.py
    MediaWindow = None  # set by .windows.py
    Menu        = None  # set by .menus.py
    MenuBar     = None  # set by .menus.py
    OpenPanel   = None  # set be .panels.py
    SavePanel   = None  # set be .panels.py
    Set         = None  # set by .sets.py
    Separator   = None  # set by .menus.py
    Str         = None  # set by .strs.py
    Table       = None  # set by .tables.py
    TableWindow = None  # set by .tables.py
    Tuple       = None  # set by .tuples.py
    Window      = None  # set by .windows.py

    @staticmethod
    def listypes():
        for a, v in sorted(_Types.__dict__.items()):
            if not a.startswith('_'):
                printf('_Types.%-11s %r', a + ':', v)


class missing(object):  # singleton class, lost on purpose

    def __eq__(self, unused):  # avoid assignment '=='
        raise SyntaxError("use 'is %s' or 'is not %s'" % (self, self))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'missing'


DEFAULT_UNICODE = 'utf-8'    # default Python encoding
missing         = missing()  # private, singleton


def aspect_ratio(width, height):
    '''Compute the smallest, int aspect ratio.

       @param width: The width (float or int).
       @param height: The height (float or int).

       @return: 2-Tuple (width, height) or None.

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


try:  # MCCABE 22

    # in Python 2- bytes *is* str and bytes.__name__ == 'str'
    _Bytes = unicode, bytearray
    _Ints  = int, long  # PYCHOK for export
    _Strs  = basestring

    def bytes2repr(bytestr):
        '''Represent bytes like C{repr(bytestr)}.

           @param bytestr: Str or bytes.
           @return: Representation C{b'...'} (str).
        '''
        return 'b%r' % (bytestr,)

    def bytes2str(bytestr, dflt=missing):
        '''Convert bytes/unicode to str if needed.

           @param bytestr: Str or bytes.
           @keyword dflt: Optional, default return value.

           @return: Str or I{dflt}.

           @raise TypeError: If neither str nor bytes, but
                             iff no I{dflt} is provided.
        '''
        if isinstance(bytestr, _Strs):
            return bytestr
        elif isinstance(bytestr, _Bytes):
            return bytestr.decode(DEFAULT_UNICODE)
        elif dflt is missing:
            raise TypeError('%s: %r' % ('bytes/str', bytestr))
        return dflt

    # iter(bytes) yields a 1-char str/byte in Python 2-
    iterbytes = iter

    def str2bytes(bytestr, dflt=missing):
        '''Convert str to bytes/unicode if needed.

           @param bytestr: Bytes or str.
           @keyword dflt: Optional, default return value.

           @return: Bytes or I{dflt}.

           @raise TypeError: If neither bytes nor str, but
                             iff no I{dflt} is provided.
        '''
        if isinstance(bytestr, _Strs):
            return bytestr
        elif isinstance(bytestr, _Bytes):
            return bytestr.encode(DEFAULT_UNICODE)
        elif dflt is missing:
            raise TypeError('%s: %r' % ('str/bytes', bytestr))
        return dflt

except NameError:  # Python 3+
    _Bytes = bytes, bytearray
    _Ints  = int
    _Strs  = str

    bytes2repr = repr  # always b'...'

    def bytes2str(bytestr, dflt=missing):  # PYCHOK expected
        '''Convert bytes to str if needed.

           @param bytestr: Str or bytes.
           @keyword dflt: Optional, default return value.

           @return: Str or I{dflt}.

           @raise TypeError: If neither str nor bytes, but
                             iff no I{dflt} is provided.
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
        '''Iterate bytes, yielding each as C{byte}.
        '''
        for b in bytestr:  # convert int to bytes
            yield bytes([b])

    # double check iterbytes
    for b in iterbytes(b'a0'):
        assert(isinstance(b, bytes))
    del b

    def str2bytes(bytestr, dflt=missing):  # PYCHOK expected
        '''Convert str to bytes if needed.

           @param bytestr: Bytes or str.
           @keyword dflt: Optional, default return value.

           @return: Bytes or I{dflt}.

           @raise TypeError: If neither bytes nor str, but
                             iff no I{dflt} is provided.
        '''
        if isinstance(bytestr, _Bytes):
            return bytestr
        elif isinstance(bytestr, _Strs):
            return bytes(bytestr, DEFAULT_UNICODE)
        elif dflt is missing:
            raise TypeError('%s: %r' % ('str2bytes', bytestr))
        return dflt

_ByteStrs = _Bytes + (_Strs,)  # bytes and/or str types


def _allisting(alls, localls, version, filename):
    '''(INTERNAL) Print sorted __all__ names and values.
    '''
    import os

    m = os.path.basename(os.path.splitext(filename)[0])
    printf('%s.%s = %s(', m, '__all__', alls.__class__.__name__, nl=1)

    d = i = 0
    p = ''
    for n in sorted(alls, key=str.lower):
        v = localls[n]
        r = repr(v)
        if r.startswith('<class '):
            r = r.replace("'", '')
        elif r.startswith('<function '):
            r = r[:10] + v.__module__ + '.' + r[10:]
        r = r.replace('__main__', '')  # .replace('__main__', m)
        if n == p:
            d += 1
            r += ' DUPLICATE'
        else:
            p = n
        printf('  %s.%s is %s,', m, n, r)
        i += 1
    if d:
        d = ' %s%s%s' % (d, ' DUPLICATE', 's' if d > 1 else '')
    else:
        d = ''
    printf(')[%d]%s', i, d)
    printf('%s.%s = %r', m, '__version__', version)


def clip(bytestr, limit=50):
    '''Clip a string or bytes to the given length limit.

       @param bytestr: Bytes or str.
       @keyword limit: Length limit (int).

       @return: Bytes or str.
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
    '''(INTYERNAL) Return a tuple of __all__ exported names.
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


def inst2strepr(inst, strepr, *attrs):
    '''Convert an instance's attributes, maintaining the order.

       @param inst: Instance (any).
       @param strepr: Conversion (C{repr} or C{str}).
       @param attrs: Instance attribute names (I{all positional}).

       @return: Instance representation (str).
    '''
    def _strepr(v):
        return repr(v) if isinstance(v, _ByteStrs) else strepr(v)

    t = ['%s=%s' % (a, _strepr(getattr(inst, a))) for a in attrs]
    return '%s(%s)' % (inst.__class__.__name__, ', '.join(t))


def instanceof(inst, *classes, **name_missing):
    '''Check whether a Python object is an instance of some Python class.

       @param inst: The instance to check (I{any}).
       @param classes: One or several classes (I{all positional}).
       @keyword name: The name of the instance (str).

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


def name2objc(name):
    '''Convert a (selector) name to bytes and ObjC naming rules.

       @param name: Name to convert (str).

       @return: Converted name (str).
    '''
    return str2bytes(name).replace(b'_', b':')


def name2py(name):
    '''Convert a (selector) name to str and Python naming conventions.

       @param name: Name to convert (str).

       @return: Converted name (str).
    '''
    return bytes2str(name).replace(':', '_')


def name2pymethod(name):
    '''Convert a (selector) name to a valid Python callback method.

       @param name: Name to convert (str).

       @return: Converted name (str).

       @raise ValueError: Invalid, non-alphanumeric I{name}.
    '''
    m = name2py(name)
    if not (m and m.replace('_', '').isalnum()):
        raise ValueError('%s invalid: %r' % ('name', name))
    return m


def printf(fmt, *args, **kwds):  # argv0='', nl=0, nt=0
    '''Formatted print I{fmt % args} with optional keywords.

       @param fmt: Print-like format (str).
       @param args: Optional arguments to include (I{all positional}).
       @keyword argv0: Optional prefix (str).
       @keyword nl: Number of leading blank lines (int).
       @keyword nt: Number of trailing blank lines (int).
    '''
    a = kwds.get('argv0', _Globals.argv0)
    t = (fmt % args) if args else fmt
    nl = '\n' * kwds.get('nl', 0)
    nt = '\n' * kwds.get('nt', 0)
    print('%s%s %s%s' % (nl, a, t, nt))


def type2strepr(inst, strepr=str):
    '''Return a Python Type instance as L{str} or L{repr}.

       @param inst: Instance (any).
       @keyword strepr: Conversion (C{repr} or C{str}).

       @return: Instance representation (str).
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
    '''Convert a size value to string with 1_000's seperator.

       @param size: Value to convert (float or int).

       @return: "<1or2digits><sep><3digits>..." or "-" if I{size}
                is negative (str).
   '''
    z = int(size)
    if z < 0:
        return '-'
    try:  # '_' only in Python 3.6+
        t = '{0:_}'.format(z)
        if sep != '_':
            t = t.replace('_', sep)
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


def zSIstr(size, B='B'):
    '''Convert a size value to string with SI-units.

       @param size: Value to convert (float or int).

       @return: "<Size> <B><SI>" (str).
    '''
    z, si = float(size), ''
    if z > 1024.0:
        for si in iter('KMGTPE'):
            z /= 1024.0
            if z < 1024.0:
                si = '%.1f %si%s' % (z, si, B)
                break
        else:
            si = '%.3e %s' % (float(size), B)
    else:
        si = '%d %s' % (int(size), B)
    return si


__all__ = _exports(locals(), 'aspect_ratio', 'clip', 'DEFAULT_UNICODE',
                             'gcd', 'iterbytes', 'missing', 'printf',
                             'type2strepr',
                   starts=('bytes', 'inst', 'str', 'z'))


if __name__ == '__main__':

    _allisting(__all__, locals(), __version__, __file__)
