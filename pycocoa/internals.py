
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Decorator L{property_RO}, functions L{bytes2repr}, L{bytes2str},
L{iterbytes}, L{lambda1}, L{str2bytes} and L{unicodec}, singleton
L{missing} and private (INTERNAL) constants.

@var missing: Missing keyword argument value, singleton.
'''
import inspect
import os
import sys  # PYCHOK used!p

_env_get = os.environ.get  # in .basics, .faults, .lazily, .runtime


class _CallableStr(str):
    '''(INTERNAL) C{_CallableStr(*args)} == C{_CallableStr.join(map(str, args))}.
    '''
    def __call__(self, *args):
        '''Join C{args} as C{self.join(args)}.
        '''
        return self.join(map(str, args))

_alloc_      = 'alloc'            # PYCHOK .printers, .runtime
_arm64_      = 'arm64'            # PYCHOK .faults, .utils
_bNN_        = b''                # PYCHOK bytes(_NN_)
_COLON_      = _CallableStr(':')  # PYCHOK expected
_COLONSPACE_ = _CallableStr(': ')
_COMMA_      = _CallableStr(',')  # PYCHOK in .basics, ...
_COMMASPACE_ = _CallableStr(', ')
_Dall_       = '__all__'          # PYCHOK _DUNDER_all_
# _Ddoc_     = '__doc__'          # PYCHOK _DUNDER_doc_
_Dfile_      = '__file__'         # PYCHOK _DUNDER_file_
_Dmain_      = '__main__'         # _DUNDER_main_
# _Dname_    = '__name__'         # PYCHOK _DUNDER_name_
_Dpackage_   = '__package__'      # PYCHOK _DUNDER_package_
_Dversion_   = '__version__'      # PYCHOK _DUNDER_version_
_DOT_        = _CallableStr('.')
_EQUALS_     = _CallableStr('=')
_invalid_    = 'invalid'
_NN_         = _CallableStr('')   # empty string, I{Nomen Nescio}
_NA_         = 'N/A'
_name_       = 'name'             # PYCHOK .nstypes, ...
_NL_         =  os.linesep        # PYCHOK ...
_not_        = 'not'
_NSObject_   = 'NSObject'         # PYCHOK NSObject.name
_pycocoa_    = 'pycocoa'          # PYCHOK pycocoa._pycocoa_package
_SPACE_      = _CallableStr(' ')
_UNDER_      = _CallableStr('_')  # PYCHOK in .basics, ...
_unhandled_  = 'unhandled'        # PYCHOK .nstypes, .pytypes
_UNICODEC    = _env_get('PYCOCOA_UNICODEC', _NN_) or 'utf-8'  # in .oslibs, .pytypes


def _docOf(obj, dflt=_NN_, line=None):
    '''(INTERNAL) Get the C{obj}'s __doc__ string (C{str}).
    '''
    # inspect.getdoc(obj)  # cleandoc()
    d = getattr(obj, '__doc__', None) or dflt
    if line is not None:
        d = d.lstrip().split(_NL_)[line].strip()
    return d


def property_RO(method):
    '''Decorator for C{Read_Only} class/instance property.

       @param method: The callable to be decorated as C{Read_Only property}.

       @note: Like standard Python C{property} without a C{property.setter}
              and with an error message when trying to set.
    '''
    def Read_Only(inst, value):
        '''Throws an C{AttributeError}, always.
        '''
        t = _DOT_(inst, _nameOf(method))
        t = _SPACE_(_nameOf(property_RO), t)
        t = _fmt('%s = %r: %s', t, value, _nameOf(Read_Only))
        raise AttributeError(t)

    return property(method, Read_Only, None, _docOf(method, _NA_))


class _Objectype(object):
    '''Base class with C{typename}.
    '''
    @property_RO
    def typename(self):
        '''Get this instance' Python class name (C{str}).
        '''
        return _nameOf(type(self))


class missing(_Objectype):
    '''Singleton class (named like instance, lost on purpose)
    '''
    def __eq__(self, unused):  # avoid '==' comparison
        raise self._Error('is', '==')

    def __ne__(self, unused):  # avoid '!=' comparison
        raise self._Error('is not', '!=')

    def __repr__(self):
        return self.typename

    def __str__(self):
        return self.typename

    def _Error(self, is_not, neq):
        t = _fmt("use '%s %s', instead of '%s'", is_not, self, neq)
        return SyntaxError(t)

missing = missing()  # PYCHOK private, singleton


try:  # MCCABE 23

    # in Python 2- bytes *is* str and _nameOf(bytes) == 'str'
    _Bytes = unicode, bytearray
    _Ints  = int, long  # PYCHOK for export
    _Strs  = basestring,

    def bytes2repr(bytestr):
        '''Represent C{bytes} or C{str} as C{b"..."}.

           @param bytestr: C{bytes} or C{str}..
           @return: Representation C{b'...'} (C{str}).
        '''
        return _fmt('b%r', bytestr)

    def bytes2str(bytestr, dflt=missing, **name):
        '''Convert C{bytes}/C{unicode} to C{str} if needed.

           @param bytestr: Original C{bytes}, C{str} or C{unicode}.
           @keyword dflt: Optional, default return value.
           @keyword name: Optional name of I{bytestr} argument, used
                          for errors and missing C{dflt} only.

           @return: The C{str} or I{dflt}.

           @raise TypeError: If C{bytestr} is not C{bytes}, C{str} or
                             C{unicode} and if I{dflt} is missing.
        '''
        # XXX see Python-Vlc's vlc.py
        if isinstance(bytestr, _Strs):
            r =  bytestr
        elif isinstance(bytestr, _Bytes):
            r =  bytestr.decode(_UNICODEC)
        else:
            r = _dflt(dflt, bytes2str, bytestr, **name)
        return r

    def iterbytes(bytestr):
        '''Iterate C{bytes}, yielding each as C{1-str/byte}.
        '''
        return iter(bytestr)

    def str2bytes(strbytes, dflt=missing, **name):
        '''Convert C{strbytes} to C{bytes}/C{unicode} if needed.

           @param strbytes: Original C{str}, C{bytes} or C{unicode}.
           @keyword dflt: Optional, default return value.
           @keyword name: Optional name of I{bytestr} argument, used
                          for errors and missing C{dflt} only.

           @return: The C{bytes} or I{dflt}.

           @raise TypeError: If C{strbytes} is not C{str}, C{bytes} or
                             C{unicode} and if I{dflt} is missing.
       '''
        # XXX see Python-Vlc's vlc.py
        if isinstance(strbytes, _Strs):
            r =  strbytes
        elif isinstance(strbytes, _Bytes):
            r =  strbytes.encode(_UNICODEC)
        else:
            r = _dflt(dflt, str2bytes, strbytes, **name)
        return r

except NameError:  # Python 3+
    _Bytes = bytes, bytearray
    _Ints  = int,
    _Strs  = str,

    def bytes2repr(bytestr):  # PYCHOK redef
        '''Represent C{bytes} or C{str} as C{b"..."}.

           @param bytestr: C{bytes} or C{str}.

           @return: Representation C{b'...'} (C{str}).
        '''
        return repr(bytestr)  # produces always b'...'

    def bytes2str(bytestr, dflt=missing, **name):  # PYCHOK redef
        '''Convert C{bytes} to C{str} if needed.

           @param bytestr: Original C{bytes}, C{str} or C{unicode}.
           @keyword dflt: Optional, default return value.
           @keyword name: Optional name of I{bytestr} argument, used
                          for errors and missing C{dflt} only.

           @return: The C{str} or I{dflt}.

           @raise TypeError: If C{bytestr} is not C{bytes}, C{str} or
                             C{unicode} and if I{dflt} is missing.
        '''
        if isinstance(bytestr, _Strs):
            r =  bytestr
        elif isinstance(bytestr, _Bytes):
            r =  bytestr.decode(_UNICODEC)
        else:
            r = _dflt(dflt, bytes2str, bytestr, **name)
        return r

    def iterbytes(bytestr):  # PYCHOK redef
        '''Iterate C{bytes}, returning each as C{byte}.

           @note: C{iter(bytes)} yields an C{int} in Python 3+.
        '''
        def _i2b(b):  # convert int/byte to bytes[1]
            # assert 0 <= b <= 255
            return bytes([b])

        return map(_i2b, bytestr)

    # double check iterbytes
    for b in iterbytes(b'a0'):
        assert isinstance(b, bytes), 'iterbytes failed'
    del b

    def str2bytes(strbytes, dflt=missing, **name):  # PYCHOK redef
        '''Convert C{strbytes} to C{bytes} if needed.

           @param strbytes: Original C{str}, C{bytes} or C{unicode}.
           @keyword dflt: Optional, default return value.
           @keyword name: Optional name of I{bytestr} argument, used
                          for errors and missing C{dflt} only.

           @return: The C{bytes} or I{dflt}.

           @raise TypeError: If C{strbytes} is not C{str}, C{bytes} or
                             C{unicode} and if I{dflt} is missing.
        '''
        if isinstance(strbytes, _Bytes):
            r =  strbytes
        elif isinstance(strbytes, _Strs):
            r =  bytes(strbytes, _UNICODEC)
        else:
            r = _dflt(dflt, str2bytes, strbytes, **name)
        return r

_ByteStrs = _Bytes + _Strs  # PYCHOK bytes and/or str types


def _c_tstr(*c_ts):
    '''(INTERNAL) Simplify names of C{c_..._t} result or argument types.
    '''
    return _COMMASPACE_.join(map(_nameOf, c_ts))


def _dflt(dflt, func, arg, name=_NN_):  # helper above
    if dflt is missing:
        raise _TypeError(name, arg, func)
    return dflt


def _filexists(name):
    '''(INTERNAL) Does file I{name} exist?
    '''
    return os.access(name, os.F_OK)


def _fmt(fmtxt, *args):
    '''(INTERNAL) Format a string.
    '''
    if args:
        try:
            t =  fmtxt % args
        except TypeError:
            t = _NN_(fmtxt, map(str, args))
    else:
        t = str(fmtxt)
    return t


def _fmt_frozen(*inst_arg_value):
    '''(INTERNAL) Format an "<inst>([<arg>]) = <value>, not mutable" string.
    '''
    return _fmt('%s[%r] = %r, not mutable', *inst_arg_value)


def _fmt_invalid(*nots, **kwd1):
    '''(INTERNAL) Format an "invalid <name>: <value>" string.
    '''
    t = _SPACE_(_invalid_, _COLONSPACE_(*kwd1.popitem()))
    if nots:
        t = _COMMASPACE_(t, _not_)
        t = _SPACE_(t, _COMMASPACE_(*nots))
    return t


try:
    _getargspec = inspect.getfullargspec  # PYCHOK Python 3+
except AttributeError:
    _getargspec = inspect.getargspec  # Python 2


def _instr(name, *args, **kwds):
    '''(INTERNAL) Format an instance "<name>(*<args>)" string.
    '''
    if kwds:
        args += tuple(_kwdstr(kwds, sep=None))
    return _fmt('%s(%s)', _nameOf(name), _COMMASPACE_(*args))


def _int2(i):  # in .utils
    '''(INTERNAL) Split an C{int} into 2-tuple C{(int, shift)}.
    '''
    s = 0
    if isinstance(i, _Ints) and i > 0:  # and not (i & 1):
        for n, m in ((8, 255), (4, 15), (2, 3)):
            while (i & m) == 0:
                i >>= n
                s  += n
    return i, s


def _int2str(i):
    '''(INTERNAL) Return C{int} as C{str}.
    '''
    b, s = _int2(i)
    return _fmt('%s or %s<<%s', i, b, s) if s > 1 else str(i)


try:  # for case-less compare
    _istr = str.casefold
except AttributeError:
    _istr = str.lower


def _kwdstr(kwds, strepr=str, sep=_COMMASPACE_):
    '''(INTERNAL) Format I{kwds} as a comma-separated C{str}ing or
       as an iterable of C{str}ings .
    '''
    t = (_EQUALS_(k, strepr(v)) for k, v in sorted(kwds.items()))
    return sep.join(t) if sep else t


def _nameOf(cC):
    '''(INTERNAL) Get the name of a class, type ObjC... or NS... Class.
    '''
    try:
        return cC.__name__
    except AttributeError:
        try:  # NS...
            return cC.name
        except AttributeError:
            return str(cC)


def _nargs(typy, none=0):
    '''(INTERNAL) Return C{typy}'s' number of args and kwds or C{none}
       if C{typy} is not callable.
    '''
    n = none
    if callable(typy):
        try:
            s = _getargspec(typy)  # inspect.signature(obj)
            n =  len(s.args)
            if inspect.isclass(typy) or inspect.ismethod(typy):
                n -= 1  # self
            n += len(s.kwonlyargs)  # if _isPython3 else 0
        except (AttributeError, TypeError, ValueError):
            pass
    return n


def _no(*args):
    '''(INTERNAL) Return C{" ".join(("no",) + args)}.
    '''
    return _SPACE_('no', *args)


def _property2(inst, name):
    '''(INTERNAL) Return the property C{get} and C{set} method.

       @param inst: An instance (C{any}).
       @param name: Property name (C{str}).

       @return: 2-Tuple (get, set), each a C{callable} or C{None}.
    '''
    try:
        p = getattr(type(inst), name)  # XXX __mro__?
        if isinstance(p, property):
            g = p.fget
            if callable(g):
                return g, p.fset
    except (AttributeError, TypeError, ValueError):
        pass
    return None, None


def _raiser_name(raiser=None, name=None):  # PYCHOK in .runtime, .utils
    return raiser or name


def _sortuples(iterable):  # in .deprecated
    '''(INTERNAL) Sort tuples alphabetically, case-insensitive.
    '''
    def _ituple(t):
        return _istr(t[0])

    return sorted(iterable, key=_ituple)


def _TypeError(name, inst, func, *classes):  # in .runtime
    '''(INTERNAL) Format a TypeError for func(inst, *classes).
    '''
    c = _COMMASPACE_(name, *map(_nameOf, classes))
    n = _nameOf(func)
    t = _fmt('%s %s(%s): %r', _not_, n, c, inst) if name else \
        _fmt('%s %s(%r%s)', _invalid_, n, inst, c)
    return TypeError(t)


def unicodec(codec=None):
    '''Get/set the unicode encoding, default C{"utf-8"}.

       @param codec: A encoding (C{str} or C{None}).

       @return: The previous encoding (C{str}).

       @see: U{Codecs<https://docs.Python.org/3/library/codecs.html#standard-encodings>}.
    '''
    global _UNICODEC
    c = _UNICODEC
    if codec:  # is not None:
        _UNICODEC = str(codec)
    return c


__all__ = tuple(map(_nameOf, (bytes2repr, bytes2str, iterbytes,
                              type(missing), property_RO,
                              str2bytes, unicodec)))
__version__ = '25.04.07'

if __name__ == _Dmain_:

    from pycocoa.utils import _all_listing

    _all_listing(__all__, locals())

# % python3 -m pycocoa.internals
#
# pycocoa.internals.__all__ = tuple(
#  pycocoa.internals.bytes2repr is <function .bytes2repr at 0x1046a6e80>,
#  pycocoa.internals.bytes2str is <function .bytes2str at 0x1046a7a60>,
#  pycocoa.internals.iterbytes is <function .iterbytes at 0x1046a7b00>,
#  pycocoa.internals.missing is missing,
#  pycocoa.internals.property_RO is <function .property_RO at 0x1046a6200>,
#  pycocoa.internals.str2bytes is <function .str2bytes at 0x1046a7ba0>,
#  pycocoa.internals.unicodec is <function .unicodec at 0x1046b4720>,
# )[7]
# pycocoa.internals.version 25.4.7, .isLazy 1, Python 3.13.2 64bit arm64, macOS 15.4

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
