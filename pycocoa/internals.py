
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Mostly INTERNAL, private classes, functions, constants, etc.

@var missing: Missing keyword argument value.
'''

import inspect as _inspect
try:
    _getargspec = _inspect.getfullargspec  # Python 3+
except AttributeError:
    _getargspec = _inspect.getargspec  # Python 2
import os
import sys  # PYCHOK used!

from platform import machine as _m
_m = _m()  # see .utils.machine
__arm64__  = _m == 'arm64'   # PYCHOK see .oslibs._isAppleSi
__i386__   = _m == 'i386'    # PYCHOK expected
__x86_64__ = _m == 'x86_64'  # PYCHOK also Intel emulation
del _m


class _Str(str):
    '''(INTERNAL) Callable C{_Str(*args)} == C{_Str.join(map(str, args))}.
    '''
    def __call__(self, *args):
        '''Join C{args} as C{self.join(args)}.
        '''
        return self.join(map(str, args))

_alloc_          = 'alloc'     # PYCHOK .printers, .runtime
_bNN_            = b''         # PYCHOK bytes(_NN_)
_COLON_          = _Str(':')   # PYCHOK expected
_COLONSPACE_     = _Str(': ')
_COMMA_          = _Str(',')   # in .getters, .utils
_COMMASPACE_     = _Str(', ')
_Dall_           = '__all__'   # PYCHOK _DUNDER_all_
_Ddoc_           = '__doc__'   # PYCHOK _DUNDER_doc_
_DEFAULT_UNICODE = 'utf-8'     # default Python encoding
_Dfile_          = '__file__'  # PYCHOK _DUNDER_file_
_Dmain_          = '__main__'  # _DUNDER_main_
_Dname_          = '__name__'  # PYCHOK _DUNDER_name_
_Dpackage_       = '__package__'  # PYCHOK _DUNDER_package_
_Dversion_       = '__version__'  # PYCHOK _DUNDER_version_
_DOT_            = _Str('.')
_EQUALS_         = _Str('=')
_invalid_        = 'invalid'
_NN_             = _Str('')     # empty string, I{Nomen Nescio}
_NA_             = 'N/A'
_name_           = 'name'       # PYCHOK .nstypes, ...
_NL_             =  os.linesep  # PYCHOK ...
_not_            = 'not'
_NSObject_       = 'NSObject'   # PYCHOK NSObject.name
_pycocoa_        = 'pycocoa'    # PYCHOK pycocoa._pycocoa_package
_SPACE_          = _Str(' ')
_UNDER_          = _Str('_')
_unhandled_      = 'unhandled'  # PYCHOK .nstypes, .pytypes


def property_RO(method):
    '''Decorator for C{Read_Only} class/instance property.

       @param method: The callable to be decorated as C{Read_Only property}.

       @note: Like standard Python C{property} without a C{property.setter}
              and with an error message when trying to set.
    '''
    def Read_Only(inst, value):
        '''Throws an C{AttributeError}, always.
        '''
        t = _DOT_(inst, method.__name__)
        t = _fmt('%s %s: %s = %r', Read_Only.__name__, 'property', t, value)
        raise AttributeError(t)

    return property(method, Read_Only, None, method.__doc__ or _NA_)


class proxy_RO(object):
    '''Decorator for a lazy module C{dict} or C{Read-Only} module property.

       @see: U{Module Properties | the Proxy Pattern
             <https://JTushman.GitHub.io/blog/2014/05/02/module-properties/>}.
    '''
    _dict = None

    def __init__(self, func):
        '''New L{proxy_RO}.

           @param func: Function to be decorated as C{property}
                        (C{callable, invoked without args}).

           @example:

             >>> @proxy_RO
             >>> def mattr():  # no args
             >>>     return ro  # singleton

             >>> x = [module.]mattr

             >>> @proxy_RO
             >>> def mdict():  # no args
             >>>     d = dict(...)
             >>>     return d # singleton

             >>> x = [module.]mdict[k]
        '''
        # assert callable(func) and not _nargs(func)
        self._func = func

    def __getattr__(self, name):
        return getattr(self._func(), name)

    def __getitem__(self, key):
        d = self._dict
        if d is None:  # build lazily
            self._dict = d = self._func()
        return d[key]


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
        '''Get C{value} for case-insensitive I{name} or I{dflt} or C{AttributeError}.
        '''
        try:
            return self.get(name)
        except AttributeError:
            pass
        n = name.lower()
        for k in self.keys():
            if k.lower() == n:
                return getattr(self, k)
        if dflt:
            return dflt[0]
        raise AttributeError(self._invalid(name))

    def _invalid(self, name):
        n = _DOT_(self.typename, name)
        return _COLONSPACE_(n, _invalid_)

    def rget(self, value, *dflt):  # in _MutableConstants.rget
        '''Get the C{name} for I{value} or I{dflt} or C{ValueError}.
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
        return type(self).__name__


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
#       return _instr(frozendict.__name__, dict.__repr__(self))


class _Globals(object):
    '''(INTERNAL) Some PyCocoa globals
    '''
    App       =  None       # set by .apps.App.__init__, not an NSApplication!
    argv0     = _pycocoa_   # set by .nstypes.nsBundleRename, _allisting, test/simple_VLCplayer
    exiting   = -9          # set by .faults.exiting, default _exit and status
    Items     = {}          # set by .menus.Item.__init__, gotten by .menus.ns2Item
    MenuBar   =  None       # set by .menus.MenuBar.__init__
#   Menus     = {}          # set by .menus._Menu_Type2._initM
    raiser    =  False      # set by .apps.App.__init__
#  _Segfaulty =  None       # see property
    stdlog    = sys.stdout  # set by .faults
    Tables    = []          # set by .tables.TableWindow.__init__
    Windows   = {}          # set by .windows.Window.__init__
    Xhandler2 =  None       # set by .faults.setUncaughtExceptionHandler

    def __setattr__(self, name, value):
        if not hasattr(type(self), name):
            raise AttributeError(_fmt_invalid(name=repr(name)))
        setattr(type(self), name, value)

    @property
    def Segfaulty(self):
        try:
            S = self._Segfaulty
        except AttributeError:
            from pycocoa.faults import _Segfaulty
            type(self)._Segfaulty = S = _Segfaulty()
        return S

    @Segfaulty.setter  # PYCHOK property.setter
    def Segfaulty(self, S):
        from pycocoa.faults import SegfaultError
        if S not in (None, False) and not isinstance(S, SegfaultError):
            raise AssertionError(_fmt_invalid(S=repr(S)))
        type(self)._Segfaulty = S

_Globals = _Globals()  # PYCHOK singleton


class missing(object):
    '''Singleton class (named like instance, lost on purpose)
    '''
    def __eq__(self, unused):  # avoid '==' comparison
        raise SyntaxError(self._use('is', '=='))

    def __ne__(self, unused):  # avoid '!=' comparison
        raise SyntaxError(self._use('is not', '!='))

    def __repr__(self):
        return self.typename

    def __str__(self):
        return self.typename

    @property_RO
    def typename(self):
        '''Get this instance' Python class name (C{str}).
        '''
        return type(self).__name__

    def _use(self, is_not, neq):
        return _fmt("use '%s %s', not '%s'", is_not, self, neq)

missing = missing()  # PYCHOK private, singleton


class _MutableConstants(object):  # in .lazily
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
        return _fmt_invalid(constant=n)

    def _isAlnum(self, name):
        return isinstance(name, str) and name.isalnum() \
                                     and name[:1].isupper() \
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

    @property_RO
    def typename(self):
        '''Get this instance' Python class name (C{str}).
        '''
        return type(self).__name__

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


def _TypeError(name, inst, func, *classes):  # in .runtime
    '''(INTERNAL) Format a TypeError for func(inst, *classes).
    '''
    c = _COMMASPACE_(name, *map(_nameOf, classes))
    n = _nameOf(func)
    t = _fmt('%s %s(%s): %r', _not_, n, c, inst) if name else \
        _fmt('%s %s(%r%s)', _invalid_, n, inst, c)
    return TypeError(t)


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
        return _fmt('b%r', bytestr)

    def bytes2str(bytestr, dflt=missing, **name):
        '''Convert C{bytes}/C{unicode} to C{str} if needed.

           @param bytestr: Original C{bytes}, C{str} or C{unicode}.
           @keyword dflt: Optional, default return value.
           @keyword name: Optional name of I{bytestr} argument.

           @return: The C{str} or I{dflt}.

           @raise TypeError: If neither C{str} nor C{bytes}, but
                             only if no I{dflt} is specified.
        '''
        # XXX see Python-Vlc's vlc.py
        if isinstance(bytestr, _Strs):
            return bytestr
        elif isinstance(bytestr, _Bytes):
            # return str(bytestr, _DEFAULT_UNICODE)
            return bytestr.decode(_DEFAULT_UNICODE)
        return _dflt(dflt, bytes2str, bytestr, **name)

    # iter(bytes) yields a 1-charsstr/byte in Python 2-
    def iterbytes(bytestr):
        '''Iterate C{bytes}, yielding each as C{byte}.
        '''
        return iter(bytestr)

    def str2bytes(strbytes, dflt=missing, **name):
        '''Convert C{strbytes} to C{bytes}/C{unicode} if needed.

           @param strbytes: Original C{str}, C{bytes} or C{unicode}.
           @keyword dflt: Optional, default return value.
           @keyword name: Optional name of I{bytestr} argument.

           @return: The C{bytes} or I{dflt}.

           @raise TypeError: If neither C{bytes} nor C{str}, but
                             only if no I{dflt} is specified.
        '''
        # XXX see Python-Vlc's vlc.py
        if isinstance(strbytes, _Strs):
            return strbytes
        elif isinstance(strbytes, _Bytes):
            return strbytes.encode(_DEFAULT_UNICODE)
        return _dflt(dflt, str2bytes, strbytes, **name)

except NameError:  # Python 3+
    _Bytes = bytes, bytearray
    _Ints  = int,
    _Strs  = str,

    def bytes2repr(bytestr):  # PYCHOK redef
        '''Represent C{bytes} or C{str} as C{b"..."}.

           @param bytestr: C{bytes} or C{str}..
           @return: Representation C{b'...'} (C{str}).
        '''
        return repr(bytestr)  # produces always b'...'

    def bytes2str(bytestr, dflt=missing, **name):  # PYCHOK redef
        '''Convert C{bytes} to C{str} if needed.

           @param bytestr: Original C{bytes}, C{str} or C{unicode}.
           @keyword dflt: Optional, default return value.
           @keyword name: Optional name of I{bytestr} argument.

           @return: The C{str} or I{dflt}.

           @raise TypeError: If neither C{str} nor C{bytes}, but
                             only if no I{dflt} is specified.
        '''
        if isinstance(bytestr, _Strs):
            return bytestr
        elif isinstance(bytestr, _Bytes):
            return bytestr.decode(_DEFAULT_UNICODE)
        return _dflt(dflt, bytes2str, bytestr, **name)

    # iter(bytes) yields an int in Python 3+
    def iterbytes(bytestr):  # PYCHOK redef
        '''Iterate C{bytes}, yielding each as C{byte}.
        '''
        for b in bytestr:  # convert int to bytes
            yield bytes([b])

    # double check iterbytes
    for b in iterbytes(b'a0'):
        assert isinstance(b, bytes), 'iterbytes failed'
    del b

    def str2bytes(strbytes, dflt=missing, **name):  # PYCHOK redef
        '''Convert C{strbytes} to C{bytes} if needed.

           @param strbytes: Original C{str}, C{bytes} or C{unicode}.
           @keyword dflt: Optional, default return value.
           @keyword name: Optional name of I{bytestr} argument.

           @return: The C{bytes} or I{dflt}.

           @raise TypeError: If neither C{bytes} nor C{str}, but
                             only if no I{dflt} is specified.
        '''
        if isinstance(strbytes, _Bytes):
            return strbytes
        elif isinstance(strbytes, _Strs):
            return bytes(strbytes, _DEFAULT_UNICODE)
        return _dflt(dflt, str2bytes, strbytes, **name)

_ByteStrs = _Bytes + _Strs  # PYCHOK bytes and/or str types

def _dflt(dflt, func, arg, name=_NN_):  # PYCHOK helper above
    if dflt is missing:
        raise _TypeError(name, arg, func)
    return dflt


def _caller3(up):
    '''(INTERNAL) Get 3-tuple C{(caller name, file name, line number)}
       for the caller B{C{up}} frames back in the Python call stack.
    '''
    f = None
    try:
        f =  sys._getframe(up + 1)  # == _inspect.stack()[up + 1][0]
        t = _inspect.getframeinfo(f)
        t =  t.function, t.filename, t.lineno
# or ...
#       t = _inspect.stack()[up + 1]  # (frame, filename, lineno, function, ...)
#       t =  t[3], t[1], t[2]
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


def _c_tstr(*c_ts):
    '''(INTERNAL) Simplify names of C{c_..._t} result or argument types.
    '''
    return _COMMASPACE_.join(map(_nameOf, c_ts))


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
    '''(INTERNAL) Format an "<inst>[<arg>] = <value>, immutable" string.
    '''
    return _fmt('%s[%r] = %r, immutable', *inst_arg_value)


def _fmt_invalid(*nots, **kwd1):
    '''(INTERNAL) Format an "invalid <name>: <value>" string.
    '''
    t = _SPACE_(_invalid_, _COLONSPACE_(*kwd1.popitem()))
    if nots:
        t = _COMMASPACE_(t, _not_)
        t = _SPACE_(t, _COMMASPACE_(*nots))
    return t


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
    if isinstance(i, _Ints) and i > 0 and not (i & 1):
        for n in (8, 4, 2, 1):
            m = 2**n - 1
            while not (i & m):
                i >>= n
                s  += n
    return i, s


def _int2str(i):
    '''(INTERNAL) Return C{int} as C{str}.
    '''
    b, s = _int2(i)
    return _fmt('%s or %s<<%s', i, b, s) if s > 1 else str(i)


def _isgenerator(obj):
    '''(INTERNAL) Is I{obj} a gnerator/=functions?
    '''
    return _inspect.isgenerator(obj) or \
           _inspect.isgeneratorfunction(obj)


def _isiterable(obj):
    '''(INTERNAL) Is I{obj} iterable?
    '''
    # XXX function pygeodesy.bsics.isiterabletype?
    return hasattr(obj, '__iter__') or (hasattr(obj, '__len__')
                                    and hasattr(obj, '__getitem__'))


def _kwdstr(kwds, strepr=str, sep=_COMMASPACE_):
    '''(INTERNAL) Format I{kwds} as a comma-separated C{str}ing or
       as an iterable of C{str}ings .
    '''
    t = (_EQUALS_(k, strepr(v)) for k, v in sorted(kwds.items()))
    return sep.join(t) if sep else t


def lambda1(arg):
    '''Inlieu of using M{lambda arg: arg}.
    '''
    return arg


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
    '''(INTERNAL) Return a callable's number of args or C{none} if not callable.
    '''
    if callable(typy):
        try:
            n = len(_getargspec(typy).args)
            if _inspect.isclass(typy) or _inspect.ismethod(typy):
                n -= 1  # self
            return n
        except (AttributeError, TypeError):
            pass
    return none


def _no(*args):
    '''(INTERNAL) Return C{" ".join(("no",) + args)}.
    '''
    return _SPACE_('no', *args)


def _presegfaulty(S=None):  # in .__init__, .__main__
    '''(INTERNAL) Print and set C{Segfaulty}, return previous setting.
    '''
    s = _Globals.Segfaulty
    if s:
        _writef('%s may raise %rs', (_Globals.argv0, s), flush=True)
        _Globals.Segfaulty = S
    return s


def _property2(inst, name):
    '''(INTERNAL) Return the property C{get} and C{set} method.

       @param inst: An instance (C{any}).
       @param name: Property name (C{str}).

       @return: 2-Tuple (get, set) as C{callable}s, (C{callable}, C{None})
                or (C{None}, C{None}) if I{inst.name} is not a property.
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


def _sortuples(iterable):  # in .deprecated
    '''(INTERNAL) Sort tuples alphabetically, case-insensitive.
    '''
    def _tup(tup):
        return tup[0].upper()
    return sorted(iterable, key=_tup)


def _writef(fmtxt, args, file=sys.stdout, flush=False,
                         nl=0, nt=1, argv0=missing):
    '''(INTERNAL) Write a formatted string to C{file}.
    '''
    t = _fmt(fmtxt, *args)
    a = _Globals.argv0 if argv0 is missing else argv0
    if a:
        t =  t.replace(_NL_, _NN_(_NL_, a, _SPACE_))
        t = _SPACE_(a, t)
    t = _NN_(_NL_ * nl, t, _NL_ * nt)
    n =  file.write(t)
    if flush:
        file.flush()
    return n


__all__ = tuple(_.__name__ for _ in (Adict, bytes2repr, bytes2str,
                                     frozendict, iterbytes,
                                     lambda1, missing.__class__,
                                     property_RO, proxy_RO, str2bytes))
__version__ = '25.03.24'

if __name__ == _Dmain_:

    from pycocoa.utils import _all_listing

    _all_listing(__all__, locals())

# % python3 -m pycocoa.internals
#
# pycocoa.internals.__all__ = tuple(
#  pycocoa.internals.Adict is <class .Adict>,
#  pycocoa.internals.bytes2repr is <function .bytes2repr at 0x102883a60>,
#  pycocoa.internals.bytes2str is <function .bytes2str at 0x1028907c0>,
#  pycocoa.internals.frozendict is <class .frozendict>,
#  pycocoa.internals.iterbytes is <function .iterbytes at 0x102890860>,
#  pycocoa.internals.lambda1 is <function .lambda1 at 0x102890cc0>,
#  pycocoa.internals.missing is missing,
#  pycocoa.internals.properties is <function .properties at 0x102890ea0>,
#  pycocoa.internals.proxy_RO is <class .proxy_RO>,
#  pycocoa.internals.str2bytes is <function .str2bytes at 0x102890900>,
# )[10]
# pycocoa.internals.version 25.3.24, .isLazy 1, Python 3.13.2 64bit arm64, macOS 15.3.2

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
