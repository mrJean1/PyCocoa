
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

__version__ = '18.04.18'

DEFAULT_UNICODE = 'utf-8'  # default Python encoding


class _Globals(object):
    # some PyCocoa-internal globals
    App     = None
    argv0   = 'PyCocoa'  # set by .nstypes.nsBundleRename
    Items   = {}
    raiser  = False
    Tables  = []
    Windows = {}


class missing(object):  # singleton class, lost on purpose

    def __eq__(self, unused):
        raise SyntaxError("use 'is %s' or 'is not %s'" % (self, self))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'missing'


missing = missing()  # private, singleton


try:  # MCCABE 22
    # in Python 2- bytes *is* str and bytes.__name__ == 'str'
    _Bytes = unicode, bytearray
    _Ints  = int, long  # PYCHOK for export
    _Strs  = basestring

    def bytes2repr(bytestr):
        '''Like repr(bytestr) for bytes:  b'...'.
        '''
        return 'b%r' % (bytestr,)

    def bytes2str(bytestr, dflt=missing):
        '''Convert bytes/unicode to str if needed.

           @param bytestr: Str or bytes.
           @keyword dflt: Optional, default return value.

           @return: Str or I{dflt}.

           @raise TypeError: If neither str nor bytes, but
                             only I{dflt} is not provided.
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
                             only I{dflt} is not provided.
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

    bytes2repr = repr

    def bytes2str(bytestr, dflt=missing):  # PYCHOK expected
        '''Convert bytes to str if needed.

           @param bytestr: Str or bytes.
           @keyword dflt: Optional, default return value.

           @return: Str or I{dflt}.

           @raise TypeError: If neither str nor bytes, but
                             only if I{dflt} is not provided.
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
                             only if I{dflt} is not provided.
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
    '''Print sorted __all__ names and values.
    '''
    import os

    m = os.path.basename(os.path.splitext(filename)[0])
    print('\n%s.%s = %s(' % (m, '__all__', alls.__class__.__name__))

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
        print('  %s.%s is %s,' % (m, n, r))
        i += 1
    if d:
        d = ' %s%s%s' % (d, ' DUPLICATE', 's' if d > 1 else '')
    else:
        d = ''
    print(')[%d]%s' % (i, d))
    print('%s.%s = %r' % (m, '__version__', version))


def clip(bytestr, limit=50):
    '''Clip a string or bytes to the given length limit.
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
    '''Return a tuple of __all__ exported names.
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
    '''Convert an instance's attributes to str or repr,
    maintaining the order of the attributes.
    '''
    def _strepr(v):
        return repr(v) if isinstance(v, _ByteStrs) else strepr(v)

    t = ['%s=%s' % (a, _strepr(getattr(inst, a))) for a in attrs]
    return '%s(%s)' % (inst.__class__.__name__, ', '.join(t))


def instanceof(inst, *classes, **name_missing):
    '''Check whether a Python object is an instance of some Python class.

    @param inst: The instance to check (I{any}).
    @param classes: One or several classes (I{all positional}).
    @keyword name: The name of the instance (string).

    @return: The matching I{class} from I{classes}, None otherwise.

    @raise TypeError: If I{inst} does not match any of the I{classes},
                      and only if keyword I{name='...'} is provided.

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
    '''Convert a (selector) name to bytes and ObjC rules.
    '''
    return str2bytes(name).replace(b'_', b':')


def name2py(name):
    '''Convert a (selector) name to str and Python conventions.
    '''
    return bytes2str(name).replace(':', '_')


def name2pymethod(name):
    '''Convert a (selector) name to Python callback method.
    '''
    m = name2py(name)
    if not m.replace('_', '').isalnum():
        raise ValueError('%s invalid: %r' % ('name', name))
    return m


def printf(fmt, *args, **kwds):  # nl=0, nt=0
    '''Formatted print.
    '''
    t = (fmt % args) if args else fmt
    nl = '\n' * kwds.get('nl', 0)
    nt = '\n' * kwds.get('nt', 0)
    print('%s%s %s%s' % (nl, _Globals.argv0, t, nt))


def type2strepr(inst, strepr=str):
    '''Return a Python Type instance as string.
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


def zSIstr(size):
    '''Convert a size to string with SI-units.
    '''
    z, si = float(size), ''
    if z > 1024.0:
        for si in iter('KMGTPE'):
            z /= 1024.0
            if z < 1024.0:
                si = '%.1f %siB' % (z, si)
                break
        else:
            si = '%.3e B' % (float(size),)
    else:
        si = '%d B' % (int(size),)
    return si


__all__ = _exports(locals(), 'clip', 'DEFAULT_UNICODE', 'iterbytes',
                             'missing', 'printf', 'type2strepr',
                   starts=('bytes', 'inst', 'str', 'z'))


if __name__ == '__main__':

    _allisting(__all__, locals(), __version__, __file__)
