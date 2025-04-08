
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Classes L{Adict}, L{frozendict}, decorator L{Proxy1ce} and
private (INTERNAL) functions and singletons.
'''
from pycocoa.internals import _COLONSPACE_, _COMMA_, _COMMASPACE_, _Dmain_, _docOf, \
                              _DOT_, _EQUALS_, _fmt, _fmt_invalid, _instr, _int2str, \
                              _istr, _invalid_, _kwdstr, missing, _nameOf, _NL_, _NN_, \
                              _not_, _Objectype, property_RO, _pycocoa_, _sortuples, \
                              _SPACE_, _TypeError, _UNDER_,  sys  # PYCHOK used
import inspect
# import sys  # from .internals

_TypeErrorX = TypeError()  # _NN_


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
        '''Get the value of an item by B{C{name}}.
        '''
        try:
            return self[name]
        except KeyError:
            raise AttributeError(self._invalid(name))

    def __setattr__(self, name, value):
        '''Set the value of a I{known} item by B{C{name}}.
        '''
        if self[name] != value:
            self[name] = value

    def __str__(self):
        '''Return this C{Adict} as C{str}.
        '''
        return _fmt('{%s}', _kwdstr(self, repr))

    def copy(self):
        '''Return a shallow copy.
        '''
        return dict.copy(self)

    def iget(self, name, *dflt):  # in _MutableConstants.iget
        '''Get C{value} for case-insensitive I{name} or I{dflt}, otherwise C{AttributeError}.
        '''
        try:
            return self.get(name)
        except AttributeError:
            pass
        n = _istr(name)
        for k in self.keys():
            if _istr(k) == n:
                return getattr(self, k)
        if dflt:
            return dflt[0]
        raise AttributeError(self._invalid(name))

    def _invalid(self, name):
        n = _DOT_(self.typename, name)
        return _COLONSPACE_(n, _invalid_)

    def rget(self, value, *dflt):  # in _MutableConstants.rget
        '''Get the C{name} for I{value} or I{dflt}, otherwise C{ValueError}.
        '''
        for n, v in self.items():
            if v == value:
                return n
        if dflt:
            return dflt[0]
        t = _fmt_invalid(self.typename, value=value)
        raise ValueError(t)

    @property_RO
    def typename(self):
        '''Get this instance' Python class name (C{str}).
        '''
        return _nameOf(type(self))


class _frozendictbase(dict):  # in nstypes.nsDescription2dict
    '''(INTERNAL) Base class for immutable C{dict} types.
    '''
    def _immutable(self):
        t = _fmt('immutable: %r', self)
        raise TypeError(t)

    __call__    = \
    __delitem__ = \
    __setitem__ = \
    clear       = \
    pop         = \
    popitem     = \
    setdefault  = \
    update      = property(_immutable)

    def __hash__(self):
        try:
            h = self._cached_hash
        except AttributeError:
            # was h = hash(tuple(sorted(self.items())))
            h = hash(frozenset(self.items()))
            self._cached_hash = h
        return h

    @property_RO
    def typename(self):
        '''Get this instance' Python class name (C{str}).
        '''
        return _nameOf(type(self))


class frozendict(_frozendictbase):
    '''An immutable Python C{dict} with key I{and} attribute access to the items.

       @see: U{Frozen Dictionaries
             <https://code.ActiveState.com/recipes/414283-frozen-dictionaries/>}
    '''
    def __new__(cls, *args, **kwds):
        '''I{Ero Carrera}'s extended version of C{frozendict}.
        '''
        def _de(v):
            for e in v:
                yield frozendict(e) if isinstance(e, dict) else e

        def _dt(v):
            return frozendict(v) if isinstance(v, dict) else (
                   tuple(_de(v)) if isinstance(v, list) else v)

        def _da(a):
            if isinstance(a, dict):
                a = dict((k, _dt(v)) for k, v in a.items())
            return a

        args = map(_da, args)
        new  = dict.__new__(cls)
        dict.__init__(new, *args, **kwds)
        return new

    def __init__(self, *args, **kwds):  # PYCHOK unused
        '''New C{frozendict}.
        '''
        pass

    def __getattr__(self, name):
        '''Get the value of an attribute or item by B{C{name}}.
        '''
        try:
            return self[name]
        except KeyError as x:
            raise AttributeError(str(x))

#   def __repr__(self):
#       '''Return this C{frozendict} as C{repr}.
#       '''
#       return _instr(self.typename, dict.__repr__(self))


class _Globals(_Objectype):
    '''(INTERNAL) Some pycocoa-wide globals.
    '''
    App       =  None        # set by .apps.App.__init__, not an NSApplication!
    argv0     = _pycocoa_    # set by .nstypes.nsBundleRename, _allisting, test/simple_VLCplayer
    exiting   = -9           # set by .faults.exiting, default _exit and status
    Items     = {}           # set by .menus.Item.__init__, gotten by .menus.ns2Item
    MenuBar   =  None        # set by .menus.MenuBar.__init__
#   Menus     = {}           # set by .menus._Menu_Type2._initM
#   pycocoa   =  None        # see property
    raiser    =  False       # set by .apps.App.__init__
#  _Segfaulty =  None        # see property
    stdlog    =  sys.stdout  # set by .faults
    Tables    = []           # set by .tables.TableWindow.__init__
    Windows   = {}           # set by .windows.Window.__init__
    Xhandler2 =  None        # set by .faults.setUncaughtExceptionHandler

    def __setattr__(self, name, value):
        if not hasattr(type(self), name):
            raise AttributeError(_fmt_invalid(name=repr(name)))
        setattr(type(self), name, value)

    @property_RO
    def pycocoa(self):  # get pycocoa, I{once}
        pycocoa = _sys_module(_pycocoa_)
        setattr(type(self), _pycocoa_, pycocoa)  # overwrite property_RO
# . or. type(self).pycocoa = pycocoa  # overwrite property_RO
        return pycocoa

    @property
    def Segfaulty(self):
        try:
            S =  self._Segfaulty
        except AttributeError:
            S = _faults._Segfaulty()
            self.Segfaulty = S  # overwrite property
        return S

    @Segfaulty.setter  # PYCHOK property.setter
    def Segfaulty(self, S):
        E = _faults.SegfaultError
        if isinstance(S, E) or S in (None, False):
            type(self)._Segfaulty = S  # overwrite property
        else:
            t = _fmt_invalid(_nameOf(E), S=repr(S))
            raise AssertionError(t)

_Globals = _Globals()  # PYCHOK singleton


class _MutableConstants(_Objectype):  # in .lazily
    '''(INTERNAL) Enum-like, settable "constants".
    '''
    def __contains__(self, name):
        return self._isAlnum(name) and name in type(self).__dict__

    def __repr__(self):
        def _fmt2(n, v):
            return _EQUALS_(n, _int2str(v))
        return self._strepr(_fmt2)

    def __setattr__(self, name, value):
        if not self._isAlnum(name):
            raise AttributeError(self._invalid(name))
        super(_MutableConstants, self).__setattr__(name, value)

    def __str__(self):
        def _fmt2(n, unused):
            return n
        return self._strepr(_fmt2)

    def get(self, name, *dflt):
        '''Get C{value} for I{name} or I{dflt} or C{AttributeError}.
        '''
        if self._isAlnum(name):
            try:
                return getattr(self, name, *dflt)
            except AttributeError:
                if dflt:
                    return dflt[0]
        raise AttributeError(self._invalid(name))

    def iget(self, name, *dflt):
        '''Get C{value} for case-insensitive I{name} or I{dflt} or C{AttributeError}.
        '''
        return Adict.iget(self, name, *dflt)

    def _invalid(self, name):
        n = _DOT_(self.typename, name)
        return _fmt_invalid(name=n)

    def _isAlnum(self, name):
        return isinstance(name, str) and name[:1].isupper() \
                                     and (hasattr(self, name) or
                                          hasattr(type(self), name))

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
        '''Yield each Constant's name.
        '''
        for n in type(self).__dict__.keys():
            if self._isAlnum(n):
                yield n

    def rget(self, value, *dflt):
        '''Get the C{name} for I{value} or I{dflt} or C{ValueError}.
        '''
        return Adict.rget(self, value, *dflt)

    def _strepr(self, _fmt2=_EQUALS_):  # helper for __repr__ and __str__
        n =  self.typename.lstrip(_UNDER_)
        j = _NN_(_COMMA_, _NL_, _SPACE_ * len(n), _DOT_)
        t = (_fmt2(*t) for t in _sortuples(self.items()))
        return _DOT_(n, j.join(t))

    def values(self):
        '''Yield each constant value.
        '''
        for n in self.keys():
            yield getattr(self, n)


class _Constants(_MutableConstants):  # _ImmutableConstants
    '''(INTERNAL) Enum-like, read-only constants.
    '''
    def __setattr__(self, name, value):
        t = _DOT_(self.typename, name)
        t = _fmt('%s = %r', t, value)
        t = _COLONSPACE_(t, 'immutable')
        raise TypeError(t)

    def _masks(self, *names):  # in .windows
        ns = []
        for n in names:
            ns.extend(n.strip().lower().split())
        M, ms, ns = 0, [], list(set(ns))
        while ns:
            n = ns.pop()
            try:
                M |= getattr(self, n)
            except AttributeError:
                ms.append(n)
        ms = _COMMASPACE_(*map(repr, ms)) if ms else None
        return M, ms  # some invalid names or None


class Proxy1ce(object):
    '''Decorator for a lazily evaluated dict or lazily imported module or
       singleton, I{avoiding circular imports} and providing access to the
       dict's items or the singleton's or module's attributes.

       @see: U{Module Properties | the Proxy Pattern
             <https://JTushman.GitHub.io/blog/2014/05/02/module-properties/>}.
    '''
    _mlf0 = None

    def __init__(self, mlf0):
        '''New L{Proxy1ce}.

           @param mlf0: Module-level function representing the dict, module or
                        singleton to be decorated (C{callable}, I{invoked lazily,
                        only once and without parameters}).

           @note: The first key or attribute access of the I{decorated} C{mlf0}
                  invokes C{mlf0} I{and} replaces C{mlf0}'s module-level Proxy1ce
                  with C{mlf0}'s returned result.

           @example:

             >>> @Proxy1ce
             >>> def _dict():  # no args
             >>>     d = dict(...)  # compute once
             >>>     return d  # singleton
             >>>
             >>> s = type(_dict)  # Proxy1ce
             >>> x = _dict[k]
             >>> t = type(_dict)  # type(d)

             >>> @Proxy1ce
             >>> def _singleton():  # no args
             >>>     from somewhere import singleton
             >>>     return singleton
             >>>
             >>> s = type(_singleton)  # Proxy1ce
             >>> x = _singleton.attr
             >>> t = type(_singleton)  # type(singleton)

             >>> @Proxy1ce
             >>> def _module():  # no args
             >>>     import module as mod
             >>>     return mod
             >>>
             >>> s = type(_module)  # Proxy1ce
             >>> x = _module.attr
             >>> t = type(_module)  # type(mod)
        '''
        try:
            r = inspect.isfunction
            if not (r(mlf0) and _sys_module(mlf0.__module__)):
                raise _TypeErrorX  # PYCHOK Exception!
        except Exception as x:
            raise _AssertX(x, r, mlf0=repr(mlf0))
        self._mlf0 = mlf0

    def __getattr__(self, name):
        r = self._once()
        return getattr(r, name)

    def __getitem__(self, key):
        d = self._once()
        return d[key]

    def _once(self):  # get C{mlf0} result, I{once}
        f = self._mlf0
        m = f.__module__
        n = f.__name__
        r = f()
        if inspect.ismodule(r) and not _isDEPRECATED(f):
            s = n.strip(_UNDER_)
            if not _nameOf(r).endswith(_DOT_ + s):
                raise _AssertX(_TypeErrorX, r, mlf0=s)
        s = sys.modules.get(m, None)
        if s is None:
            raise _AssertX(_TypeErrorX, f, mlf0=m)
        setattr(s, n, r)  # overwrite @Proxy1ce mlf0
        return r


class _Singletons(_MutableConstants):
    '''(INTERNAL) Global, single instances.
    '''
    def _isAlnum(self, name):  # overloading
        try:  # non-Camelized, alnum property
            p = type(self).__dict__[name]
            return isinstance(p, property) and name.isalnum()
        except KeyError:
            return False

    def reset(self):
        '''Rest all cached attributes.
        '''
        d = self.__dict__
        u = len(d)
        for n in d:
            if self._isAlnum(n):
                _ = d.pop(n)
        return u - len(d)

    def _set(self, **name_value):
        n, v = name_value.popitem()
        self.__dict__[n] = v  # cached
        return v


def _AssertX(x, r, **name):
    '''(INTERNAL) Format an C{AssertionError}.
    '''
    t, x = _nameOf(r), str(x)
    if x:
        t = _COLONSPACE_(t, x)
    return AssertionError(_fmt_invalid(t, **name))


def _caller3(up):
    '''(INTERNAL) Get 3-tuple C{(caller name, file name, line number)}
       for the caller B{C{up}} frames back in the Python call stack.
    '''
    f = None
    try:
        f = sys._getframe(up + 1)  # == inspect.stack()[up + 1][0]
        t = inspect.getframeinfo(f)
        t = t.function, t.filename, t.lineno
# or ...
#       t = inspect.stack()[up + 1]  # (frame, filename, lineno, function, ...)
#       t = t[3], t[1], t[2]
# or ...
#       f =  sys._getframe(up + 1)
#       c =  f.f_code
#       t = (c.co_name,      # caller name
#            c.co_filename,  # file name .py
#            f.f_lineno)     # line number
    except (AttributeError, IndexError, ValueError):
        # sys._getframe(1) ... 'importlib._bootstrap' line 1032,
        # may throw a ValueError('call stack not deep enough')
        t = _NN_, _NN_, 0
    finally:
        del f  # break ref cycle
    return t


def _isDEPRECATED(obj, outer=1):
    '''(INTERNAL) Is C{obj} or its outer C{type} DEPRECATED?
    '''
    for _ in range(max(0, outer) + 1):
        if 'DEPRECATED' in _docOf(obj):
            return True
        obj = type(obj)
    return False


def _isEpydoc():
    '''(INTERNAL) Is C{Epydoc} running?
    '''
    return bool(_lazily._FOR_DOCS)


def _isgenerator(obj):
    '''(INTERNAL) Is I{obj} a generator/function?
    '''
    return inspect.isgenerator(obj) or \
           inspect.isgeneratorfunction(obj)


def _isiterable(obj):
    '''(INTERNAL) Is I{obj} iterable?
    '''
    # XXX function pygeodesy.basics.isiterabletype?
    return hasattr(obj, '__iter__') or (hasattr(obj, '__len__')
                                    and hasattr(obj, '__getitem__'))


def _isPyChOK():
    '''(INTERNAL) Is C{PyChecker} running?
    '''
    # .../pychecker/checker.py --limit 0 --stdlib pycocoa/<name>.py
    return sys.argv[0].endswith('/pychecker/checker.py')  # or
    #      bool(internals._env_get('PYCOCOA_PYCHOK', None))


def lambda1(arg):
    '''Inlieu of M{lambda arg: arg}.
    '''
    return arg


def _presegfaulty(S=None):  # in .__init__, .__main__
    '''(INTERNAL) Print and set C{Segfaulty}, return previous setting.
    '''
    s = _Globals.Segfaulty
    if s:
        _writef('may raise a %r', (s,), flush=True)
        _Globals.Segfaulty = S
    return s


def _sys_module(name):  # in .Proxy1ce
    '''(INTERNAL) Get module by C{name}.
    '''
    try:
        m = sys.modules[name]  # without re-import, isLazy=0
        if inspect.ismodule(m):
            return m
    except KeyError as x:  # MUST exist
        m = str(x)
    raise _AssertX(m, _sys_module, name=repr(name))


def _writef(fmtxt, args=(), file=sys.stdout, flush=False,
                            nl=0, nt=1, argv0=missing):  # in .lazily, .utils
    '''(INTERNAL) Write a formatted string to C{file}, C{flush}
       and return the number of bytes written.
    '''
    t = _fmt(fmtxt, *args) if args else fmtxt
    a = _Globals.argv0 if argv0 is missing else argv0
    if a:
        t =  t.replace(_NL_, _NN_(_NL_, a, _SPACE_))
        t = _SPACE_(a, t)
    t = _NN_(_NL_ * nl, t, _NL_ * nt)
    n =  file.write(t)
    if flush:
        file.flush()
    return n


@Proxy1ce  # PYCHOK _faults used!
def _faults():  # lazily import faults, I{once}
    from pycocoa import faults
    return faults


@Proxy1ce
def _lazily():  # lazily import lazily, I{once}
    from pycocoa import lazily
    return lazily


__all__ = tuple(map(_nameOf, (Adict, frozendict, lambda1, Proxy1ce)))
__version__ = '25.04.08'

if __name__ == _Dmain_:

    from pycocoa.utils import _all_listing

    _all_listing(__all__, locals())

# % python3 -m pycocoa.basics
#
# pycocoa.basics.__all__ = tuple(
#  pycocoa.basics.Adict is <class .Adict>,
#  pycocoa.basics.frozendict is <class .frozendict>,
#  pycocoa.basics.lambda1 is <function .lambda1 at 0x10149d8a0>,
#  pycocoa.basics.Proxy1ce is <class .Proxy1ce>,
# )[4]
# pycocoa.basics.version 25.4.8, .isLazy 1, Python 3.13.2 64bit arm64, macOS 15.4

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
