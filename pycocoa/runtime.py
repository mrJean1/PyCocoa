
# -*- coding: utf-8 -*-

# License at the end of this file.

# Some Objective-C references and introductions:
#
# 1. <https://Developer.Apple.com/library/content/documentation/Cocoa/Conceptual/
# ProgrammingWithObjectiveC/Introduction/Introduction.html#//apple_ref/doc/uid/TP40011210>
#
# 2. <https://Developer.Apple.com/library/content/documentation/Cocoa/Conceptual/
# ObjCRuntimeGuide/Introduction/Introduction.html#//apple_ref/doc/uid/TP40008048-CH1-SW1>
#
# 3. <https://Developer.Apple.com/library/content/documentation/Cocoa/Conceptual/
# MemoryMgmt/Articles/MemoryMgmt.html#//apple_ref/doc/uid/10000011i>
#
# 4. Several Objective-C/C header files are also available at
# <https://GitHub.com/gnustep/libs-gui/tree/master/Headers>

'''Classes C{ObjCClass}, C{ObjCInstance}, C{ObjCMethod}, C{ObjCSubclass}, etc.

For debugging purposes, enable logging to the console by setting env variable
C{PYCOCOA_OBJC_LOG} to a string of one or more of the following letters:

C{% env  PYCOCOA_OBJC_LOG=ICSMBDPX  python3  ...}

where C{I} logs __new__ and __del__ Instance calls, C{C} new Classes, C{S}
new Subclasses, C{M} new Methods, C{B} new BoundMethods, C{D} draining of,
C{P} printing of C{NSAutoreleasePool}s and C{X} I{send_message}, I{send_super},
(rather C{libobjc.objc_msgSend} and C{libobjc.objc_msgSendSuper}) calls.

Use env variable C{PYCOCOA_LIBOBJC_NONATOMIC=on} to detect I{non-atomic} calls
of certain C{libobjc} functions.

@var OBJC_ASSOCIATION: C{Libs,ObjC.objc_setAssociatedObject} associations (C{mask}).
@var OBJC_ASSOCIATION.ASSIGN: 0x0
@var OBJC_ASSOCIATION.COPY: 0x303
@var OBJC_ASSOCIATION.COPY_NONATOMIC: 0x3
@var OBJC_ASSOCIATION.RETAIN: 0x301
@var OBJC_ASSOCIATION.RETAIN_NONATOMIC: 0x1
'''
from pycocoa.getters import _ivar_ctype, get_c_func_t, get_class, \
                             get_classname, get_classof, get_ivar, \
                             get_metaclass, get_protocol, get_selector, \
                             get_superclassof
from pycocoa.internals import Adict, _alloc_, _bNN_, _ByteStrs, bytes2str, \
                             _COLONSPACE_, _COMMASPACE_, _Constants, _c_tstr, \
                             _Dmain_, _DOT_, _fmt, _fmt_invalid, __i386__, \
                             _instr, _kwdstr, lambda1, missing, _NA_, _name_, \
                             _NL_, _NN_, _no, _NSObject_, property_RO, \
                             _property2, proxy_RO, _SPACE_, str2bytes, \
                             _TypeError,  _Ddoc_, sys  # PYCHOK used!
from pycocoa.lazily import _ALL_LAZY, _environ
# from pycocoa import nstypes as _nstypes  # circular, see proxy_RO
from pycocoa.octypes import _bAT, _bHASH  # PYCHOK used!
from pycocoa.octypes import c_struct_t, c_void, ctype2encoding, emcoding2ctype, \
                            encoding2ctype, Class_t, Id_t, IMP_t, objc_super_t, \
                            objc_super_t_ptr, ObjC_t, SEL_t, split_emcoding2, \
                            TypeCodeError
from pycocoa.oslibs import cfString2str, _csignature, _dllattr, _libObjC
from pycocoa.utils import isinstanceOf, logf, name2py, _raiser_name

from ctypes import alignment, ArgumentError, byref, cast, c_buffer, \
                   c_char_p, c_double, c_float, CFUNCTYPE, c_longdouble, \
                   c_void_p, POINTER  # XXX c_uint, sizeof removed
#                  # to avoid segfault in PyChecker, by forcing an
#                  # NameError in function add_ivar below and class
#                  # _ObjCDeallocObserver.  sizeof is imported at the
#                  # very end of this module.
# from os import environ as _environ  # from .lazily
# import sys  # from .internals

__all__ = _ALL_LAZY.runtime
__version__ = '25.03.24'

_OBJC_ENV = 'PYCOCOA_OBJC_LOG'
_OBJC_LOG =  dict((_, 0) for _ in _environ.get(_OBJC_ENV, _NN_).upper()
                          if _ in 'ICSMBDPX')  # _.isalpha()
_OBJC_NON = 'PYCOCOA_LIBOBJC_NONATOMIC' in _environ
del _environ


@proxy_RO
def _nstypes():  # lazily import nstypes, I{once}
    from pycocoa import nstypes
    sys.modules[__name__]._nstypes = nstypes  # overwrite proxy_RO _thismodule
    return nstypes  # .NSAutoReleasePool, .NSMain, ._NSImms, ._NSMtbs


class _Ivar1(_Constants):
    # the _ObjCDeallocObserver ivar
    name = '_ObjCPtrValue'
    c_t  =   Id_t

    @staticmethod
    def akwd():
        return {_Ivar1.name: _Ivar1.c_t}

    @staticmethod
    def astr(*n_v):
        t = n_v or (_Ivar1.name, _Ivar1.c_t)
        return _fmt('%r %s', *t)


# <https://Developer.Apple.com/documentation/objectivec/
#        objc_associationpolicy?language=objc>
class OBJC_ASSOCIATION(_Constants):
    '''C{libObjC.objc_setAssociatedObject} associations (C{mask}).
    '''
    ASSIGN           = 0      # weak reference
    COPY             = 0x303  # 01403
    COPY_NONATOMIC   = 3
    RETAIN           = 0x301  # 01401
    RETAIN_NONATOMIC = 1

OBJC_ASSOCIATION = OBJC_ASSOCIATION()  # PYCHOK singleton


class _ObjCBase(object):
    '''(INTERNAL) Base class for C{runtime.ObjC...} classes.
    '''
    _as_parameter_ =  None  # for ctypes
    _name          = _bNN_  # shut PyChecker up

    def __repr__(self):
        t = _instr(self.typename, self)
        return _fmt('<%s at %#x>', t, id(self))

    def _AttributeError(self, name, _or_other):
        # no classmethod, method or property attr
        t = _DOT_(self, name)
        t = _COLONSPACE_(_or_other, t)
        t = _no('[class]method%' + t)
        return AttributeError(t)

    @property_RO
    def description(self):
        '''Return this ObjC's description, first line of C{__doc__}.
        '''
        n = getattr(self, _name_, self.typename)
        d = getattr(self, _Ddoc_, _NA_).lstrip()
        d = d.split(_NL_, 1)[0]
        return _COLONSPACE_(n, d.strip())

    @property_RO
    def typename(self):
        '''Get this instance' Python class name (C{str}).
        '''
        return type(self).__name__


class ObjCBoundMethod(_ObjCBase):
    '''Python wrapper for a bound ObjC instance method, an L{IMP_t}.

       @note: Each ObjC method invocation requires creation of another,
              new C{ObjCBound[Class]Method} instance which is discarded
              immediately thereafter.
    '''
    # if _isPython2:
    #     __slots__ = ('_inst', '_method', '_objc_id')

    def __init__(self, method, objc_id, inst):
        '''Initialize with an ObjC instance or class method.

           @param method: The ObjC method (C{ObjC[Class]Method}).
           @param objc_id: The ObjC instance (L{ObjCInstance}) or
                           class (C{Class_t}).
           @param inst: The instance C{ObjCInstance} or C{ObjCClass},
                        used only to report invokation errors.
        '''
        self._inst = inst
        self._method = method
        self._objc_id = objc_id

    def __str__(self):
        return _DOT_(self._objc_id, self._method.name)

    def __call__(self, *args):
        '''Call the method with the given arguments.
        '''
        _ObjC_log(self, 'call', 'B', *args)
        return self._method(self._inst, self._objc_id, *args)

    @property_RO
    def inst(self):
        '''Get the C{ObjCInstance} or C{ObjCClass}.
        '''
        return self._inst

    @property_RO
    def method(self):
        '''Get the method (C{ObjC[Class]Method}).
        '''
        return self._method

    @property_RO
    def name(self):
        '''Get the method's name (C{str}).
        '''
        return self._method.name

    @property_RO
    def objc_id(self):
        '''Get the ObjC instance (C{Class_t} or L{ObjCSubclass}).
        '''
        return self._objc_id


class ObjCBoundClassMethod(ObjCBoundMethod):
    '''Python wrapper for a bound ObjC class method, only
       to distinguish bound class from bound instance methods.
    '''
    # __slots__ must be repeated in sub-classes, see "Problems with
    # __slots__" in Luciano Ramalho, "Fluent Python", page 276+,
    # O'Reilly, 2016, also at <https://Books.Google.ie/books?
    # id=bIZHCgAAQBAJ&lpg=PP1&dq=fluent%20python&pg=PT364#
    # v=onepage&q=“Problems%20with%20__slots__”&f=false>
    # if _isPython2:
    #     __slots__ = ObjCBoundMethod.__slots__
    pass


class ObjCClass(_ObjCBase):
    '''Python wrapper for an ObjC class.
    '''
    _classmethods_cache = {}  # local cache per class
    _methods_cache      = {}  # local cache per class
    _ObjCClasses_cache  = {}  # global cache **)
    _ptr                =  None
    _Type               =  None  # Python Type, e.g. Dict, List, Tuple, etc.

    # **) Only one ObjCClass instance is created for each ObjC class.
    # Any future calls with the same class will return the previously
    # created ObjCClass instance.  Note, these aren't weak references,
    # each ObjCClass created will exist till the end of the process.

    def __new__(cls, name_or_ptr, *protocols):
        '''Create a new L{ObjCClass} instance or return a previously
           created instance for the given ObjC class name or ptr.

           @param name_or_ptr: Either the name of or a pointer to the
                               class to retrieve (C{str} or L{Class_t}).
           @param protocols: C{None}, one or more protocol to add (C{str}s
                             or L{Protocol_t} instances).
        '''
        # Determine name and ptr values from C{name_or_ptr}.
        ptr, name = _objc_name2(name_or_ptr, get_class)
        if name is None:
            if not ptr:
                raise RuntimeError(_fmt_invalid(name_ptr=repr(ptr)))
            # Make sure that ptr is wrapped in a Class_t,
            # for safety when passing as ctypes argument.
            ptr = cast(name_or_ptr, Class_t)
            name = str2bytes(get_classname(ptr, dflt='nil'))

        if ptr is None or ptr.value is None:
            raise ValueError(_fmt_invalid(Class=bytes2str(name)))

        # Check if we've already created a Python object for this class
        # and if so, return it rather than making a new one.
        try:
            return cls._ObjCClasses_cache[name]
        except KeyError:
            pass

        # Otherwise create a new Python object and initialize it.
        self = super(ObjCClass, cls).__new__(cls)  # objc_class
        self._name = name
        self._ptr = self._as_parameter_ = ptr  # for ctypes

        _ObjC_log(self, 'new', 'C')

        # Cache the Python version of all instance methods of
        # this class (doesn't include methods of superclass).
        self._methods_cache = self._cache_methods(ptr, ObjCMethod)
        # Cache the Python version of all class methods of this
        # class (doesn't include class methods of superclass).
        p = get_classof(ptr)
        self._classmethods_cache = self._cache_methods(p, ObjCClassMethod)

        # add any protocols
        for p in protocols:
            add_protocol(ptr, p)

        # Add the class to the (registered) classes cache.
        cls._ObjCClasses_cache[name] = self

        return self

    def __getattr__(self, name):
        '''Returns a callable method object with the given name.
        '''
        # If name refers to a class method, then return a callable object
        # for the class method with self.ptr as hidden first parameter.
        method = self.get_classmethod(name)
        if method:
            return ObjCBoundClassMethod(method, self.ptr, self)

        # If name refers to an instance method, then simply return the method.
        # The caller will need to supply an instance as the first parameter.
        method = self.get_method(name)
        if method:
            return method

        # Otherwise, throw an error.
        raise self._AttributeError(name, _NN_)

    def __str__(self):
        return _fmt('%s of %#x', self.name, self.ptr.value)

    def _cache_method(self, name, Class, cache, getter):
        # get and cache a class or instance method
        # XXX get_selector_permutations(name2py(name))?
        m = getter(self._ptr, get_selector(name))
        # XXX add a check that .alloc() was called
        # before .init() for any I{NSDelegate} class
        # logf('%s.%s', self.name, name)
        if m and m.value:
            m = Class(m)
            cache[m.name] = m
            _ObjC_log(m, 'new', 'M')
            return m
        return None

    def _cache_methods(self, which, Class):  # PYCHOK unused
        # build a cache of all class or instance methods
        # def _n_m2(which, Class):
        #     n = c_uint()
        #     for m in _libObjC.class_copyMethodList(which, byref(n)):
        #         m = Class(m)
        #         _ObjC_log(m, 'new', 'M')
        #         yield m.name, m
        return {}  # dict(_n_m2(which, Class))

    def add_protocol(self, protocol):
        '''Add a protocol to this class.

           @param protocol: The protocol to add (str or L{Protocol_t}).

           @return: True if the protocol was added, False otherwise.
        '''
        return add_protocol(self._ptr, protocol)

    def get_classmethod(self, name):
        '''Find a class method.

           @param name: Name of the method (C{str}).

           @return: The class method wrapper (L{ObjCClassMethod}) or None.
        '''
        try:
            return self._classmethods_cache[name2py(name)]
        except KeyError:
            return self._cache_method(name, ObjCClassMethod,
                   self._classmethods_cache, _libObjC.class_getClassMethod)

    def get_method(self, name):
        '''Find an instance method.

           @param name: Name of the method (C{str}).

           @return: The instance method wrapper (L{ObjCMethod}) or None.
        '''
        try:
            return self._methods_cache[name2py(name)]
        except KeyError:
            return self._cache_method(name, ObjCMethod,
                   self._methods_cache, _libObjC.class_getInstanceMethod)

    @property_RO
    def name(self):
        '''Get the ObjC class name (C{str}).
        '''
        return bytes2str(self._name)

    @property_RO
    def ptr(self):
        '''Get the ObjC class (L{Class_t}).
        '''
        return self._ptr

    NS = ptr

    @property_RO
    def Type(self):
        '''Get the Python Type for this ObjC class (C{class} or C{None}).
        '''
        return self._Type


class ObjCDelegate(ObjCClass):
    '''Register the C{_NS_Delegate._ObjC} (sub)class and
       create an L{ObjCClass}C{(_NS_Delegate.__name__)}.

       @note: L{ObjCDelegate} instances are singletons,
              I{intentionally}.
    '''
    def __new__(cls, _NS_Delegate, *protocols):
        '''New L{ObjCDelegate} for class B{C{_NS_Delegate}}.

           @param _NS_Delegate: A private Python class intended as an
                                L{ObjCDelegate} with class attribute
                                C{._ObjC}, an I{un-}registered
                                L{ObjCSubclass}.
           @param protocols: C{None}, one or more protocol to add
                             (C{str}s or L{Protocol_t} instances).

           @raise TypeError: Attribute C{B{_NS_Delegate}._ObjC} is not
                             a sub-class of L{ObjCSubclass} or the name
                             of C{B{_NS_Delegate}} does not start with
                             private C{_NS} or end with C{Delegate}.
        '''
        name = _NS_Delegate.__name__
        # ObjCDelegate classes cached in parent _objc_cache
        if name not in ObjCClass._ObjCClasses_cache:
            _ObjC = _NS_Delegate._ObjC
            if not isinstance(_ObjC, ObjCSubclass):
                n = _DOT_(name, '_ObjC')
                raise _ObjCDelegateError(n, ObjCSubclass.__name__)
            if not _ObjC.isregistered:
                _ObjC.register()
                # catch class and naming mistakes
                if not name.startswith('_NS'):
                    raise _ObjCDelegateError(name, 'private _NS')
                elif not name.endswith('Delegate'):
                    raise _ObjCDelegateError(name, 'Delegate')
        return ObjCClass.__new__(cls, name, *protocols)


def _ObjCDelegate(name, register=False):  # get an C{_NSDelegate._ObjC} attribute.
    return ObjCSubclass(_NSObject_, name, register=register)  # defer


def _ObjCDelegateError(name, why):  # helper for __new__ above
    return TypeError(_fmt_invalid(why, **{ObjCDelegate.__name__: name}))


class ObjCInstance(_ObjCBase):
    '''Python wrapper for an ObjC instance.
    '''
    _autoPool   =  0  # pool id, see property .inPool
    _dealloc_d  =  False
    _from_py2NS =  False
    _objc_cache = {}  # see _ObjCDeallocObserver, example class_wrapper4.py
    _objc_class =  None
    _objc_ptr   =  None  # shut PyChecker up
    _retained   =  None  # False or True

    def __new__(cls, objc_ptr, cached=True):
        '''New L{ObjCInstance} or a previously created, cached one.

           @param objc_ptr: The ObjC instance (L{Id_t} or C{c_void_p}).
           @keyword cached: Cache the new instance (C{bool}), required
                            for most objects.

           @raise RuntimeError: An L{NSAutoreleasePool} ObjC instance
                                is created with C{B{cached}=False}.
        '''
        # Make sure that obj_ptr is wrapped in an Id_t.
        if not isinstance(objc_ptr, Id_t):
            objc_ptr = cast(objc_ptr, Id_t)

        ptr = objc_ptr.value  # actual ObjC address
        if not ptr:
            return None  # nil pointer

        if cached:
            # Check whether an ObjCInstance was already for the C{Id_t}
            # and if so, return it.  Otherwise, create an ObjCInstance
            # for the C{Id_t} and that will persist until the object is
            # de-allocated by ObjC (see C{_ns/NSDeallocObserver} below)
            # or C{drain}ed from the pool it was allocated in (see
            # method C{_cache_clear} below).
            try:
                # cls._objc_cache == ObjCInstance._objc_cache
                return cls._objc_cache[ptr]
            except KeyError:
                pass

        # Otherwise, create a new ObjCInstance.
        self = super(ObjCInstance, cls).__new__(cls)  # objc_instance
        self._objc_ptr = self._as_parameter_ = objc_ptr  # for ctypes

        # Determine and hold the class of this object.
        self._objc_class = NS_ = ObjCClass(get_classof(objc_ptr))

        if cached:
            # store the object in the cached objects dict, keyed
            # by the (integer) memory address pointed to by the
            # obj_ptr (cls._objc_cache == ObjCInstance._objc_cache)
            cls._objc_cache[ptr] = self

            auto = _nstypes.NSAutoreleasePools
            if NS_ is _nstypes.NSAutoreleasePool:  # new pool instance
                # i.e. isObjCInstanceOf(self, _NSAutoreleasePool)
                _ObjCDeallocObserver._new(ptr)  # needed for _cache_clear
                self._autoPool = _nstypes.NSAutoreleasePools = auto + 1
            elif auto:  # hold current, non-zero pool identifier
                self._autoPool = auto
            elif not isClass(self):
                # observe the C{objc_ptr.value}, the key into the
                # C{cls._objc_cache} dict, but only for objects not
                # allocated in an C{NSAutoreleasePool} since those
                # never receive a C{dealloc} or C{finalize} message
                # anyway (courtesy caffeinepills in U{issue #6
                # <https://GitHub.com/mrJean1/PyCocoa/issues/6>})
                _ObjCDeallocObserver._new(ptr)

        elif NS_ is _nstypes.NSAutoreleasePool:  # must be cached!
            raise RuntimeError(_fmt('not cached: %r', self))

        _ObjC_log(self, 'new', 'I', auto=self.inPool, cached=cached)
        return self

    def __del__(self):
        # remove from _objc_cache
        # if self.retained():  # or self.inPool < _nstypes.NSAutoreleasePools
        #     raise RuntimeError(_fmt("%r is retained, can't be deleted", self))
        objc = self._objc_cache.pop(self.ptr.value, None)
        _ObjC_log(self, 'del', 'I', auto=self.inPool, cached=objc is self)
        # self._cache_clear()

#   def __eq__(self, other):
#       return bool(isinstance(other, ObjCInstance) and
#                   self.isEqualTo_(other))
#
#   def __ne__(self, other):
#       return not self.__eq__(other)

    def __getattr__(self, name):
        '''Return a callable ObjC method or Python property
           with the given name.

           @param name: The method or property name (C{str}).

           @return: A bound class or instance method (C{ObjCBound[Class]Method})
                    or this instance's Python property C{get} function.

           @raise AttributeError: No I{name} method or property.

           @raise RuntimeError: This instance' ObjC object has been
                                deallocated and no longer exists.
        '''
        if self._dealloc_d:
            t = _fmt('longer exists: %r', self)
            raise RuntimeError(_no(t))

        clas = self._objc_class
        # Get the named instance method in the class object and if it
        # exists, return callable object (with self as hidden argument).
        method = clas.get_method(name)
        if method:
            # @note: pass self and NOT self.ptr to ObjCBoundMethod, so
            # that it will be able to keep the ObjCInstance alive for
            # chained calls like Class.alloc().init() where the object
            # created by alloc() isn't assigned to a variable.
            return ObjCBoundMethod(method, self, self)

        # Otherwise, get the class method with given name in the class
        # object.  If that exists, return callable object (with a
        # pointer to the class as the hidden argument).
        method = clas.get_classmethod(name)
        if method:
            return ObjCBoundClassMethod(method, clas.ptr, self)

        # ... handle substitutes for ObjC method names conflicting
        # with Python reserved words, like 'throw' for 'raise' or
        # ObjC attributes conflicting with Python properties, like
        # NSPrinter.name()
#       subst = {_name_:  'objc_classname',  # self.isKindOf(NSPrinter)
#                'throw': 'raise',  # self.isKindOf(NSException)
#               }.get(name, None)  # PYCHOK expected
#       if subst:
#           return self.__getattr__(subst)

        # Try this class' property.
        get, _ = _property2(self, bytes2str(name))
        if get:
            return get(self)

        # Otherwise, throw an error.
        raise self._AttributeError(name, ' or property')

#   def __repr__(self):
#       return _fmt('<%s %#x: %s>', ObjCInstance.__name__, id(self), self)

    def __str__(self):
        t = _instr(self.objc_classname, repr(self.ptr))
        return _fmt('%s of %#x', t, self.ptr.value)

    def _cache_clear(self):
        # clear the _objc_cache and return the number of cleared C{ObjcInstance}s
        if self._objc_class is _nstypes.NSAutoreleasePool:
            # i.e. isObjCInstanceOf(self, NSAutoreleasePool)
            cache, auto, keep = self._objc_cache, self.inPool, {}
            self._cache_print('cached')
            n, _popitem = len(cache), cache.popitem
            while cache:
                ptr, objc = _popitem()
                if objc.retained() or objc.inPool < auto:
                    keep[ptr] = objc
            cache.update(keep)
            n -= len(cache)
            self._cache_print('retained')
            _nstypes.NSAutoreleasePools = max(0, auto - 1)
            _ObjC_log(self, 'drain', 'D', auto=auto, cleared=n)
        else:
            n  = 0
        return n

    def _cache_print(self, label):
        if 'P' in _OBJC_LOG:
            _rc = sys.getrefcount
            c   = self._objc_cache
            t   = (_fmt('%r %d', v, _rc(v)) for v in c.values())
            _ObjC_log(self, label, 'P', len(c), _COMMASPACE_.join(t))

    @property_RO
    def from_py2NS(self):
        '''Get this instance' origin (C{bool}).
        '''
        return self._from_py2NS

    @property_RO
    def inPool(self):
        '''Get this instance' C{NSAutoreleasePool} identifier (C{int} or C{0} iff global).
        '''
        return self._autoPool

    @property_RO
    def objc_class(self):
        '''Get this instance' ObjC class (L{ObjCClass}).
        '''
        return self._objc_class

    @property_RO
    def objc_classname(self):
        '''Get this instance' ObjC class name (C{str}).
        '''
        return self._objc_class.name.replace('__NSCF', 'NS')  # .lstrip(_UNDER_)

    # XXX name property clashes with NSPrinter.NS.name()
    name = objc_classname  # for C{ObjCMethod.__call__}

    @property_RO
    def objc_description(self):
        '''Get this instance' ObjC description (C{str}).
        '''
        # XXX conflicts with NSPrinter.description()
        d = send_message(self.ptr, 'description', restype=Id_t)
        s = cfString2str(d, dflt=_NA_)
        # d.release()
        return s

    @property_RO
    def ptr(self):
        '''Get this instance' ObjC object (L{Id_t}).
        '''
        return self._objc_ptr

    def retained(self, *retain):
        '''Get/set this instance' cache retention (C{bool}).

           @arg retain: If C{True} retain, if C{False} I{do not}
                        retain this instance.

           @return: The previous value (C{bool}).

           @note: Use sel/method C{retain}, to retain this
                  instance in L{NSAutoreleasePool}s.
        '''
        r = self._retained
        if retain:
            self._retained = b = bool(retain[0])
            if b and self.ptr.value not in self._objc_cache:
                t = _fmt("can't be retained: %r, not cached", self)
                raise RuntimeError(t)
        return r

    def set_ivar(self, name, value, ctype=None):
        '''Set an instance variable (ivar) to the given value.

           @param name: Name of the ivar (C{str}).
           @param value: Value for the ivar (C{any}).
           @keyword ctype: The type code of the ivar (C{ctypes}).

           @return: The ivar (L{Ivar_t}).

           @raise ArgumentError: Invalid I{name}, I{value} or I{ctype}.

           @raise TypeError: Invalid I{name}, I{value} or I{ctype} type.
        '''
        return set_ivar(self._objc_ptr, name, value, ctype=ctype)

    @property_RO
    def Type(self):
        '''Get the Python Type for this instance' ObjC class (C{class}).
        '''
        ty = self._objc_class.Type
        if ty and callable(ty):
            return ty
        raise AttributeError(_fmt('Type(%r): %r', self, ty or missing))


class ObjCConstant(ObjCInstance):
    '''Python wrapper for an ObjC constant.
    '''
    def __new__(cls, dylib, name, const_t=ObjC_t):
        '''New L{ObjCConstant} pointer constant in a C{dylib}.

           @param dylib: The library (C{ctypes.CDLL}).
           @param name: The constant's name (C{str} or C{bytes}).
           @keyword const_t: C type (C{ObjC_t} or other C{ctypes}_t).
        '''
        n =  bytes2str(name, name=_name_)
        c = _dllattr(dylib, n, const_t)  # **{n: const_t}
        return super(ObjCConstant, cls).__new__(cls, c)


class ObjCMethod(_ObjCBase):
    '''Python class representing an unbound ObjC instance
       method, actually an L{IMP_t}.
    '''
    _argtypes = []  # list of ctypes
    _callable =  None
    _encoding = _bNN_
    _IMP      =  None
    _pyresult =  None  # None, ObjCClass or ObjCInstance
    _SEL      =  None
    _restype  =  None  # None (i.e. c_void), Class_t or Id_t

    def __init__(self, method):
        '''New C{ObjC[Class]Method} for an ObjC method pointer.

           @param method: The method pointer (L{IMP_t}).
        '''
        self._IMP  = _libObjC.method_getImplementation(method)
        self._SEL  = _libObjC.method_getName(method)
        self._name = _libObjC.sel_getName(self._SEL)  # bytes

        # determine the return and argument types of the method
        self._encoding = _libObjC.method_getTypeEncoding(method)
        try:  # to get the ctype for all args
            c, t = c_buffer(512), []
            for i in range(_libObjC.method_getNumberOfArguments(method)):
                _libObjC.method_getArgumentType(method, i, c, len(c))
                t.append(emcoding2ctype(c.value))
        except TypeError:
            t = []  # XXX ignore all?
        self._argtypes = t

        # Some hacky stuff to get around ctypes issues on 64-bit:
        # can't let ctypes convert the return value itself, because
        # it truncates the pointer along the way.  Instead, set the
        # return type to c_void_p to ensure we get 64-bit addresses
        # and then convert the return value manually
        c = _libObjC.method_copyReturnType(method)
        self._pyresult, t = _PyRes_t2.get(c, (None, None))
        if t is None:
            try:  # to get the ctype from the result encoding
                t = emcoding2ctype(c, name=self._name)
            except TypeCodeError:
                pass  # assume c_void for b'v', b'Vv' code
        self._restype = t

        # finally, build a Python callable for the method
        t = CFUNCTYPE(self._restype, *self._argtypes)
        self._callable = cast(self._IMP, t)
        # XXX also _csignature_list, _str, _variadic?
        _csignature(self._callable, self._restype, *self._argtypes)

    def __call__(self, inst, objc_id, *args):
        '''Call an ObjC instance or class method with the given arguments.

           @param inst: The ObjC instance (L{ObjCInstance}), only
                        used for reporting errors.
           @param objc_id: The ObjC instance (L{ObjCInstance}) or
                           ObjC class (C{Class_t}).
           @param args: Method arguments (C{all positional}).

           @note: Do not pass in the C{Sel/cmd} as an argument, since
                  that is provided automatically.

           @see: L{ObjCBoundMethod}C{.__call__}.
        '''
        try:
            r = self._callable(objc_id, self._SEL, *args)
            if self._pyresult:
                r = self._pyresult(r)
        except (ArgumentError, TypeError) as x:
            n = _DOT_(inst.name, self.name)
            raise _Xargs(x, n, self.argtypes, self.restype)
        return r

#   def __repr__(self):
#       return _fmt('<%s %s(%s) %s>', ObjCMethod.__name__,
#                                     self.name, _c_tstr(*self.argtypes),
#                                     bytes2str(self.encoding))

    def __str__(self):
        t = _instr(self.name, _c_tstr(*self.argtypes))
        return _SPACE_(t, _c_tstr(self.restype), bytes2str(self.encoding))

    @property_RO
    def argtypes(self):
        '''Get this method's argument types (C{ctypes}[]).
        '''
        return self._argtypes  # or []

    @property_RO
    def encoding(self):
        '''Get this method's encoding (C{bytes}).
        '''
        return self._encoding

    @property_RO
    def name(self):
        '''Get this method's C{Sel/cmd} name (C{str}).
        '''
        return name2py(self._name)

    @property_RO
    def restype(self):
        '''Get this method's result type (C{ctype}).
        '''
        return self._restype  # or c_void


class ObjCClassMethod(ObjCMethod):
    '''Python class representing an unbound ObjC class method,
       only to distinguish class methods from instance methods.
    '''
    pass


class ObjCSubclass(_ObjCBase):
    '''Python class creating an ObjC sub-class of an existing ObjC (super)class.

       This class is used only to I{define} the interface and implementation
       of an ObjC sub-class from Python.  It should not be used in any other
       way.  If you want a Python representation of the resulting class,
       create it with L{ObjCClass}.

       I{It consists primarily of function decorators which you use to add
       methods to the sub-class.}

       L{ObjCSubclass} is used to define an ObjC sub-class of an existing
       class registered with the runtime.  When you create an instance of
       L{ObjCSubclass}, it registers the new sub-class with the ObjC
       runtime and creates a set of function decorators that you can use
       to add instance methods or class methods to the sub-class.

       Typical usage would be to first create and register the sub-class:

       >>> MySubclass = ObjCSubclass('NSObject', 'MySubclassName')

       and then add methods with:

       >>> @MySubclass.method('v')
       >>> def methodThatReturnsVoid(self):
       >>>     pass

       >>> @MySubclass.method('Bi')
       >>> def boolReturningMethodWithInt_(self, x):
       >>>     return True

       >>> @MySubclass.classmethod('@')
       >>> def classMethodThatReturnsId(self):
       >>>     return self

       It is probably a good idea to organize the code related to a single
       sub-class by either (a) putting it in its own module (note that you
       don't actually need to expose any of the method names or the
       L{ObjCSubclass}) or (b) bundling it all up inside a Python class
       definition, perhaps called MySubclassImplementation.

       It is also possible to add ObjC I{ivars} to the sub-class, however
       if you do so, you I{must call} the C{.__init__} method with keyword
       argument I{register=False}, and then call the C{.register} method
       after the I{ivars} have been added.

       However, instead of creating the I{ivars} in ObjC land, it is easier to
       just define Python-based I{ivars} in your sub-class' C{.__init__} method.

       Instances are created as a pointer to the ObjC object by using:

       >>> myinstance = send_message('MySubclassName', 'alloc')
       >>> myinstance = send_message(myinstance, 'init')

       or wrapped inside an L{ObjCInstance} by using:

       >>> myclass = ObjCClass('MySubclassName')
       >>> myinstance = myclass.alloc().init()
    '''
    _imp_cache      = {}  # local, decorated class/method cache
    _objc_class     =  None
    _objc_metaclass =  None  # None means, not (yet) registered

    def __init__(self, parent, name, register=True, **ivars):
        '''New sub-class of the given (super-)class.

           @param parent: The super-class (C{str} or C{ObjCClass}).
           @param name: The sub-class name (C{str}).
           @keyword register: Register the new sub-class (C{bool}).
           @keyword ivars: Optionally, specify any number of instance
                           variables to be added I{before} registering
                           the new class, each by a keyword argument
                           C{name=ctype} to specify the name and C{ctype}
                           of the instance variable.
        '''
        self._imp_cache = {}
        self._name = str2bytes(name)
        self._as_parameter_ = \
        self._objc_class    = add_subclass(parent, name)

        # must add instance variables before registering!
        for ivar, ctype in ivars.items():
            self.add_ivar(ivar, ctype)

        if register:
            self.register()

        _ObjC_log(self, 'new', 'S')

    def __str__(self):
        return _instr('sub-class', repr(self.name))

    def _add_classmethod(self, method, name, encoding):
        if not self._objc_metaclass:
            raise self._add_Error('method', name, 'un')
        imp = add_method(self._objc_metaclass, name, method, encoding)
        self._imp_cache[name] = imp

    def _add_Error(self, kind, name, un=_NN_):  # helper for _classmethod, _ivar
        t = _fmt('add %s %s to %sregistered %s %r', kind,
                  bytes2str(name), un, 'sub-class', self.name)
        return ValueError(t)

    def _add_method(self, method, name, encoding):
        imp = add_method(self._objc_class, name, method, encoding)
        self._imp_cache[name] = imp

    def add_ivar(self, name, ctype):
        '''Add an instance variable to the sub-class.

           @param name: Name of the ivar (C{str}).
           @param ctype: The ivar type (C{ctypes}).

           @raise ValueError: This class is already registered.

           @note: Instance variables can only be added
                  BEFORE the class is registered.
        '''
        if self._objc_metaclass:
            raise self._add_Error('ivar', name)
        return add_ivar(self._objc_class, name, ctype)

    def classmethod(self, encoding):
        '''Decorator for class methods.

           @param encoding: Signature of the method (C{encoding})
                            without C{Id/self} and C{SEL/cmd} encoding.

           @return: Decorated class method.
        '''
        codes3, encoding = split_emcoding2(encoding, 3)

        def decorator(m):
            def objc_classmethod(objc_class, objc_cmd, *args):  # PYCHOK expected
                _pycls = ObjCClass(objc_class)
                _pycls.objc_cmd = objc_cmd
                return _pyresult(m(_pycls, *_pyargs(codes3, args)))

            n = m.__name__
#           if n.startswith(_UNDER_):
#               raise NameError(_fmt_invalid(classmethod=n))
            self._add_classmethod(objc_classmethod, n, encoding)
            objc_classmethod.name = n  # preserve name
            return objc_classmethod

        return decorator

    @property_RO
    def isregistered(self):
        '''Check whether the (sub)class is registered (C{bool}).
        '''
        return bool(self._objc_metaclass)

    def method(self, encoding):
        '''Decorator for instance methods.

           @param encoding: Signature of the method (C{encoding}),
                            I{without} C{Id/self} and C{SEL/cmd} encoding.

           @return: Decorated instance method.
        '''
        codes3, encoding = split_emcoding2(encoding, 3)

        def decorator(m):
            def objc_method(objc_self, objc_cmd, *args):  # PYCHOK expected
                _pyself = ObjCInstance(objc_self, cached=True)
                _pyself.retained(True)
                _pyself.objc_cmd = objc_cmd
                return _pyresult(m(_pyself, *_pyargs(codes3, args)))

            n = m.__name__
#           if n.startswith(_UNDER_):
#               raise NameError(_fmt_invalid(method=n))
            self._add_method(objc_method, n, encoding)
            objc_method.name = n  # preserve name
            return objc_method

        return decorator

    @property_RO
    def name(self):
        '''Get the name of this ObjC sub-class (C{str}).
        '''
        return bytes2str(self._name)

    @property_RO
    def objc_class(self):
        '''Get the ObjC class.
        '''
        return self._objc_class

    @property_RO
    def objc_metaclass(self):
        '''Get the ObjC metaclass, or C{None} if un-registered.
        '''
        return self._objc_metaclass

    def rawmethod(self, encoding):
        '''Decorator for instance methods without any fancy shenanigans.

           @param encoding: Signature of the method (C{encoding})
                            I{without} C{Id/self} and C{SEL/cmd} encoding.

           @return: The instance method.

           @note: The method must have signature M{m(self, cmd, *args)}
                  where both C{Id/self} and C{SEL/cmd} are just pointers
                  to ObjC objects of type C{Id_t} respectively C{SEL_t}.
        '''
        _, encoding = split_emcoding2(encoding)

        def decorator(m):
            self._add_method(m, m.__name__, encoding)
            return m

        return decorator

    def register(self):
        '''Register this new class with the ObjC runtime.
        '''
        if self._objc_metaclass:
            t = _fmt('already registered %s: %r', 'sub-class', self)
            raise ValueError(t)

        register_subclass(self._objc_class)
        # We can't get the metaclass before the class is registered.
        self._objc_metaclass = get_metaclass(self.name)


def add_ivar(clas, name, ctype):
    '''Add an instance variable to an ObjC class,

       @param clas: Class to add the ivar to (C{ObjCClass/Subclass}).
       @param name: Name of the ivar (C{str}).
       @param ctype: The ivar type code (C{ctypes} or C{encoding}).

       @return: True if the ivar was added, False otherwise.

       @raise TypeCodeError: Invalid I{ctype}.

       @note: The I{ctype} must be a C{ctypes} type or a valid
              ObjC type encoding.

       @see: The C{_ObjCDeallocObserver} below.
    '''
    try:
        code = ctype2encoding(ctype, dflt=None)
        if code is None:
            code, ctype = ctype, encoding2ctype(str2bytes(ctype))
    except TypeError:
        raise TypeCodeError('ivar', ctype, name=name)

    try:
        z = sizeof(ctype)
    except NameError:
        if ctype is not Id_t:
            raise
        z = 8  # XXX 4?
    return bool(_libObjC.class_addIvar(clas, str2bytes(name), z,
                                             alignment(ctype), code))


def add_method(clas, name_, method, encoding):
    '''Add a method to an ObjC class.

       @param clas: Class to add the method to (C{ObjCClass/Subclass}).
       @param name_: Selector name (C{str}).
       @param method: Decorated class or instance method (C{callable}).
       @param encoding: Method signature (C{encoding}).

       @return: The method (L{IMP_t}) if added, C{None} otherwise.

       @raise TypeError: If I{method} is not a Python callable.
    '''
    if isinstance(method, _ObjCBase) or not callable(method):
        t = callable.__name__
        raise TypeError(_fmt_invalid(t, method=method))

    codes, signature = split_emcoding2(encoding)

    imp = get_c_func_t(signature, codes)
    imp = imp(method)
    imp = cast(imp, IMP_t)

#   _libObjC.class_addMethod.argtypes = [Class_t, SEL_t, IMP_t, c_char_p]
    return imp if _libObjC.class_addMethod(clas, get_selector(name_),
                                                 imp, signature) else None


def add_protocol(clas, protocol):
    '''Add a protocol to an ObjC class.

       @param clas: Class to add the protocol to (C{ObjCClass/Subclass}).
       @param protocol: The C{protocol} to add (C{str} or L{Protocol_t} instance).

       @return: The protocol (L{Protocol_t}) if added, C{None} otherwise.
    '''
    protocol, _ = _objc_name2(protocol, get_protocol)
    return protocol if _libObjC.class_addProtocol(clas, protocol) else None


def add_subclass(Super, name, register=False):
    '''Create a new sub-class of a given super-class.

       @param Super: The parent class (C{str} or C{Object}).
       @param name: The name of the sub-class (C{str}).
       @keyword register: Optionally, register the new sub-class (bool).

       @return: The sub-class (C{Class_t}) if added, C{None} otherwise.

       @note: After calling C{add_subclass}, you I{MUST} register the
              new sub-class with L{register_subclass}, I{before} using
              the new sub-class.  New methods can be added I{after} the
              sub-class has been registered, but any C{ivar}s I{must
              be added BEFORE}.
    '''
    S, _ = _objc_name2(Super, get_class)
    clas = _libObjC.objc_allocateClassPair(S, str2bytes(name), 0)
    if clas and register:
        register_subclass(clas)
    return clas or None


def drain(objc):
    '''Release all objects in an C{NSAutoreleasePool} instance.

       @return: The number of C{ObjC} objects cleared.

       @note: C{NSAutoreleasePool.drain} invokes the C{dealloc}
              method only for the pool itself, I{not} for any
              of the objects held/allocated in the pool.
    '''
    if isObjCInstanceOf(objc, _nstypes.NSAutoreleasePool):
        objc.drain()
        n = objc._cache_clear()
    else:
        n = 0
    return n


def isClass(objc):
    '''Check whether an object is an ObjC clas.

       @param objc: Object to check (C{Object} or C{Class}).

       @return: True if the I{objc} is a clas, False otherwise.
    '''
    # an objc is a class if its super-class is a metaclass
    return isMetaClass(get_classof(objc))


def isImmutable(objc, *immutableClasses, **raiser_name):
    '''Check that an ObjC object is an immutable class' instance.

       @param objc: The instance to check (L{ObjCInstance}).
       @param immutableClasses: Optional I{immutable} classes to
                                use (C{NS...} or C{Object}s), in
                                lieu of all predefined ones.
       @keyword raiser_name: Optional instance name (C{str}) to
                             raise TypeError.

       @return: C{True} if I{objc} is immutable, C{False} otherwise.

       @raise TypeError: If I{objc} isn't I{immutable}, but only if
                         keyword I{raiser='...'} is specified.
    '''
    # remove initial NSMutable arg for backward compatibility
    if immutableClasses and immutableClasses[0] in _nstypes._NSMtbs:
        immutableClasses = immutableClasses[1:]
    return _isI_M(objc, raiser_name, isImmutable, immutableClasses or _nstypes._NSImms)


def _isI_M(objc, raiser_name, isIm_Mutable, Classes):  # helper for isIm/Mutable
    if isinstanceOf(objc, ObjCInstance, **raiser_name):  # like isObjCInstanceOf
        if objc.objc_class in Classes or get_classof(objc) in Classes:
            return True
        name = _raiser_name(**raiser_name)
        if name:
            raise _TypeError(name, objc, isIm_Mutable, *Classes)
    return False


def isMetaClass(objc):
    '''Check whether an object is an ObjC metaclass.

       @param objc: Object to check (C{Object} or C{Class}).

       @return: True if the I{objc} is a metaclass, False otherwise.
    '''
    return bool(_libObjC.class_isMetaClass(objc))


def isMutable(objc, *mutableClasses, **raiser_name):
    '''Check that an ObjC object is a mutable class' instance.

       @param objc: The instance to check (L{ObjCInstance}).
       @param mutableClasses: Optional I{mutable} classes to use
                              (C{NSMutable...}s or C{Object}s),
                              in lieu of all predefined ones.
       @keyword raiser_name: Optional instance name (C{str}) to
                             raise TypeError.

       @return: C{True} if I{objc} is mutable, C{False} otherwise.

       @raise TypeError: If I{objc} isn't I{mutable}, but only if
                         keyword I{raiser='...'} is specified.
    '''
    return _isI_M(objc, raiser_name, isMutable, mutableClasses or _nstypes._NSMtbs)


def isObjCInstanceOf(objc, *Classes, **raiser_name):  # MCCABE 14
    '''Check whether an ObjC object is an instance of some ObjC class.

       @param objc: The instance to check (L{ObjCInstance} or C{c_void_p}).
       @param Classes: One or several ObjC classes (C{Object}).
       @keyword raiser_name: Optional instance name (C{str}) to raise
                             TypeError.

       @return: The matching I{Class} from I{Classes}, C{None} otherwise.

       @raise TypeError: If I{objc} is not an L{ObjCInstance} or C{c_void_p}
                         or if I{objc} isn't any I{Classes}' instance and
                         only if keyword I{raiser='...'} is specified.

       @see: Function L{isinstanceOf} for checking Python instances.
    '''
    name = _raiser_name(**raiser_name) if raiser_name else None
    if isinstance(objc, ObjCInstance):
        try:
            if objc.objc_class in Classes or get_classof(objc) in Classes:
                return objc.objc_class
            # <https://Developer.Apple.com/documentation/objectivec/
            #        1418956-nsobject/1418511-iskindofclass/>
            isC_ = objc.isKindOfClass_
            for C in Classes:
                if isC_(C):
                    return C
        except AttributeError:
            pass
    elif isinstance(objc, ObjC_t):
        if ObjC_t in Classes:  # XXX or type(objc) in Classes?
            return ObjC_t
    elif isinstance(objc, c_void_p):
        if c_void_p in Classes:  # XXX or type(objc) in Classes?
            return c_void_p
    else:  # objc is not any ObjC..., NS..., ObjC_t or c_void_p
        raise _TypeError(name or 'objc', objc, isObjCInstanceOf,
                         ObjCInstance, ObjC_t, c_void_p)  # NSObject
    if name:
        raise _TypeError(name, objc, isObjCInstanceOf, *Classes)
    return None


def _libobjcall(objc_, restype, argtypes, *args):  # in printer.py
    '''(INTERNAL) Call a C{libobjc} library function I{objc_} with
       the specified I{restype} and I{argtypes} and handle errors.
    '''
    if 'X' in _OBJC_LOG:
        t = _instr(objc_, *args)
        try:
            r = _fmt('%s, [%s]', restype.__name__,
                     _COMMASPACE_.join(_.__name__ for _ in argtypes))
        except AttributeError:
            r = _NN_
        _OBJC_LOG['X'] += 1
        logf('%s libobjc.%s %d  %s', 'call', t, _OBJC_LOG['X'], r)
    try:
        # objc_        = _copy(objc_) throws ValueError
        objc_.restype  =  restype   # or c_void
        objc_.argtypes =  argtypes  # or []

        r = objc_(*args)
        if _OBJC_NON and not (objc_.restype  is restype
                         and  objc_.argtypes is argtypes):
            raise RuntimeError('nonatomic')
    except (ArgumentError, Exception) as x:
        raise _Xargs(x, objc_, argtypes, restype)

    if restype is c_void_p or (restype and issubclass(restype, ObjC_t)
                                   and not isinstance(r, ObjC_t)):
        r = restype(r)
    return r


if __i386__:  # or __x86_64__  # Intel-emulation?
    from pycocoa.octypes import __LP64__

    # <https://www.SealieSoftware.com/blog/archive/2008/11/16/objc_explain_objc_msgSend_fpret.html>
    # def _x86_use_fpret(restype):
    #     '''Determine if objc_msgSend_fpret is required to return a floating point type.
    #     '''
    #     if not __i386__:   # Unneeded on non-intel processors
    #         return False
    #     if __LP64__ and restype == c_longdouble:
    #         return True  # Use only for long double on x86_64
    #     if not __LP64__ and restype in (c_float, c_double, c_longdouble):
    #         return True
    #     return False

    # <https://www.SealieSoftware.com/blog/archive/2008/10/30/objc_explain_objc_msgSend_stret.html>
    # <XXXX://www.x86-64.org/documentation/abi-0.99.pdf> (pp.17-23) executive summary, lost?
    # <https://StackOverflow.com/questions/18133812/where-is-the-x86-64-system-v-abi-documented>
    # def _x86_use_stret(restype):
    #     '''Try to figure out when a return type will be passed on stack.
    #     '''
    #     if type(restype) != type(c_struct_t):
    #         return False
    #     if not __LP64__ and sizeof(restype) <= 8:
    #         return False
    #     if __LP64__ and sizeof(restype) <= 16:  # maybe? I don't know?
    #         return False
    #     return True

    if __LP64__:
        _C_FLOATS = {c_longdouble,}

        def _istruct(restype):
            return issubclass(restype, c_struct_t) and sizeof(restype) > 16
    else:
        _C_FLOATS = {c_longdouble, c_float, c_double}
        _1_2_4_8  = {1, 2, 4, 8}  # XXX > 8

        def _istruct(restype):  # PYCHOK expected
            return issubclass(restype, c_struct_t) and sizeof(restype) not in _1_2_4_8

    def _libobjc_msgSend(restype, argtypes, *args):
        # invoke _libObjC.objc_msgSend, _fpret or _stret
        if restype in _C_FLOATS:  # _x86_use_fpret(restype)
            objc_ = _libObjC.objc_msgSend_fpret
        elif _istruct(restype):  # _x86_use_stret(restype)
            objc_ = _libObjC.objc_msgSend_stret
            # args.insert(0, byref(restype()))
            args = (byref(restype()),) + args
            argtypes = [POINTER(restype)] + argtypes
            restype  =  c_void
        else:
            objc_ = _libObjC.objc_msgSend
        return _libobjcall(objc_, restype, argtypes, *args)

    def _libobjc_msgSendSuper(restype, *argtypes_args):
        # invoke _libObjC.objc_msgSendSuper or _stret
        objc_ = _libObjC.objc_msgSendSuper_stret if _istruct(restype) else \
                _libObjC.objc_msgSendSuper  # _x86_use_stret(restype)
        return _libobjcall(objc_, restype, *argtypes_args)

else:  # non-Intel
    # ctypes.CDLL provides .attr and [key] access for dlsym names,
    # dlsyms accessed by .attr are cached, by [key] are not

    def _libobjc_msgSend(*restype_argtypes_args):  # PYCHOK expected
        # invoke _libObjC.objc_msgSend, _fpret or _stret
        return _libobjcall(_libObjC.objc_msgSend, *restype_argtypes_args)

    def _libobjc_msgSendSuper(*restype_argtypes_args):  # PYCHOK expected
        # invoke _libObjC.objc_msgSendSuper or _stret
        return _libobjcall(_libObjC.objc_msgSendSuper, *restype_argtypes_args)


def _libobject_setInstanceVariable(*restype_argtypes_args):
    # <https://Developer.Apple.com/documentation/objectivec/
    #        1441499-object_getinstancevariable>
    # and ../1441498-object_setinstancevariable>
    return _libobjcall(_libObjC.object_setInstanceVariable, *restype_argtypes_args)


def _objc_cast(objc):
    '''(INTERNAL) Re-cast an ObjC C{send_message/_super} instance.
    '''
    # from PyBee/Rubicon-Objc <https://GitHub.com/pybee/rubicon-objc>
    objc = getattr(objc, '_as_parameter_', objc)
    if isinstance(objc, Id_t):
        return objc
    elif isinstanceOf(objc, c_void_p, ObjCInstance):
        return cast(objc, Id_t)
#   elif isinstance(objc, _Strs):
#       return cast(get_class(objc), Id_t)
    raise TypeError(_fmt_invalid(objc=repr(objc)))


def _objc_dealloc(nso, sel_name_):
    '''(INTERNAL) Remove an L{ObjCInstance} from the instances cache
       called by the instance' associated C{dealloc/finalize} observer.

       @param nso: The instance' observer (C{_ObjCDeallocObserver}).
       @param sel_name_: Parent's message selector (C{SEL_t}) or name
                         (C{str} or C{bytes}).
    '''
    objc_ptr_value = get_ivar(nso, _Ivar1.name, ctype=_Ivar1.c_t)
#   print(sel_name_, hex(objc_ptr_value))
    if objc_ptr_value:
        # dis-associate the observer from ObjC C{objc_ptr_value}
        # by remove all associations (but just one in this case)
        # libobjc.objc_removeAssociatedObjects(objc_ptr_value)

        # U{preferably<https://Developer.Apple.com/documentation/
        # objectivec/1418683-objc_removeassociatedobjects> set the
        # association C{target} to C{nil} (courtesy caffeinepills
        # U{issue #6<https://GitHub.com/mrJean1/ PyCocoa/issues/6>},
        # also see <https://StackOverflow.com/questions/41827988>)
        nil = _nstypes.NSMain.nil
        _libObjC.objc_setAssociatedObject(objc_ptr_value, nso, nil,
                                          OBJC_ASSOCIATION.RETAIN)
        objc = ObjCInstance._objc_cache.pop(objc_ptr_value, None)
        if objc:
            objc._cache_clear()
            objc._dealloc_d = True
    send_super(nso, sel_name_)


def _ObjC_log(inst, what, T, *args, **kwds):  # B, C, D, I, M, S
    '''(INTERNAL) Log a new/del Instance, Sub-/Class, Bound-/Method
       call or pool/cache Drain.
    '''
    if inst and T in _OBJC_LOG:
        _OBJC_LOG[T] += 1
        r = _instr(inst, *args)
        t = _kwdstr(kwds) if kwds else _NN_
        t = _SPACE_(what, r, _OBJC_LOG[T], t)
        logf(t)


def _ObjC_log_totals():
    '''(INTERNAL) Log a summary.
    '''
    if _OBJC_LOG:
        logf('%s: ...', _OBJC_ENV, nl=1)
        for t in sorted(_OBJC_LOG.items()):
            logf('_OBJC_LOG[%s]: %d', *t)


def _objc_name2(name_or_obj, getter):
    '''(INTERNAL) Return or get an object by name.
    '''
    name = str2bytes(name_or_obj, dflt=None)
    if name is not None:
        name_or_obj = getter(name)
    return name_or_obj, name


def _objc_super(objc):
    '''(INTERNAL) Re-cast an ObjC C{send_super} instance.
    '''
    objc = _objc_cast(objc)
    supr =  objc_super_t(objc, get_superclassof(objc))
    return byref(supr)


def _pyargs(codes3, args):
    '''(INTERNAL) Used by L{ObjCSubclass} to convert ObjC method
       arguments to the corresponding Python type/value before
       passing those to the decorated Python method.
    '''
    if len(codes3) != len(args):
        raise ValueError(_fmt_invalid(len(codes3), args=len(args)))

    for code, arg in zip(codes3, args):
        ObjC, _ = _PyRes_t2.get(code, (lambda1, None))
        yield ObjC(arg)


def _pyresult(result):
    '''(INTERNAL) Used by L{ObjCSubclass} to convert the result
       of an ObjC method to the corresponding Python type/value.
    '''
    if isinstance(result, (ObjCInstance, ObjCClass)):
        result = result.ptr.value
    return result


def register_subclass(subclas):
    '''Register an ObjC sub-class.

       @param subclas: Class to be registered (C{Class}).

       @see: L{ObjCSubclass}C{.register}.
    '''
    if not isinstance(subclas, Class_t):
        subclas = Class_t(subclas)
    _libObjC.objc_registerClassPair(subclas)


def release(objc):
    '''Release an ObjC instance to be deleted, eventually.

       @param objc: The instance to release (L{ObjCInstance}).

       @return: The instance I{objc}.

       @raise TypeError: If I{objc} is not releasable.

       @note: May result in Python memory errors, aborts and/or
              segfaults.  Use 'python3 -X faulthandler ...' to
              get a Python traceback in such circumstances.
    '''
    try:
        objc.autorelease()  # XXX or objc.release()?
    except (AttributeError, TypeError):
        raise TypeError(_fmt_invalid('releasable', objc=objc))
    return objc


def retain(objc):
    '''Preserve an ObjC instance from destruction.

       @param objc: The instance to retain (L{ObjCInstance}).

       @return: The retained instance I{objc}.

       @raise TypeError: If I{objc} is not retainable.

       @note: May result in Python memory errors, aborts and/or
              segfaults.  Use 'python3 -X faulthandler ...' to
              get a Python traceback in such circumstances.
    '''
    try:
        objc.retain()  # L{ObjCMethod}
    except (AttributeError, TypeError):
        raise TypeError(_fmt_invalid('retainable', objc=objc))
    return objc


def send_message(objc, sel_name_, *args, **restype_argtypes):
    '''Send message to an ObjC object.

       @param objc: The recipient (C{Object}, C{Id_t}, etc.) instance.
       @param sel_name_: Message selector (C{SEL_t}) or name (C{str} or C{bytes}).
       @param args: Message arguments (I{all positional}).
       @keyword resargtypes: Optional, result and argument types (C{ctypes}).

       @return: Message result (I{restype}).

       @raise ArgumentError: Invalid I{objc}, I{sel_name_}, I{args} or
                             I{resargtypes}.

       @raise TypeError: Invalid I{objc}, I{sel_name_}, I{args} or
                         I{resargtypes} type.

       @note: By default, the result and any arguments are C{c_void_p}
              wrapped.  Use keyword arguments I{restype=c_void_p} and
              I{argtypes=[]} to change the defaults.  The I{restype}
              defines the C{ctypes} type for the returned result and
              I{argtypes} is the list of C{ctypes} types for the
              I{message arguments only without} the C{Id/self} and
              C{SEL/cmd} arguments.
    '''
    objc, _ = _objc_name2(objc, get_class)
    objc = _objc_cast(objc)
    restype, argtypes, sel = _signature3(type(objc), sel_name_,
                                         args, **restype_argtypes)
    return _libobjc_msgSend(restype, argtypes, objc, sel, *args)


# https://StackOverflow.com/questions/3095360/what-exactly-is-super-in-objective-c
def send_super(objc, sel_name_, *args, **restype_argtypes):
    '''Send message to the super-class of an ObjC object.

       @param objc: The recipient (C{Object}, C{Id_t}, etc.) instance.
       @param sel_name_: Message selector (C{SEL_t}) or name (C{str} or C{bytes}).
       @param args: Message arguments (I{all positional}).
       @keyword resargtypes: Optional, result and argument types (C{ctypes}).

       @return: Message result (I{restype}).

       @raise ArgumentError: Invalid I{objc}, I{sel_name_}, I{args} or
                             I{resargtypes}.

       @raise TypeError: Invalid I{objc}, I{sel_name_}, I{args} or
                         I{resargtypes} type.

       @note: By default, the result and any arguments are C{c_void_p}
              wrapped.  Use keyword arguments I{restype=c_void_p} and
              I{argtypes=[]} to change the defaults.  The I{restype}
              defines the C{ctypes} type for the returned result and
              I{argtypes} is the list of C{ctypes} types for the
              I{message arguments only without} the C{Id/self} and
              C{SEL/cmd} arguments.
    '''
    restype, argtypes, sel = _signature3(objc_super_t_ptr, sel_name_,
                                         args, **restype_argtypes)
    return _libobjc_msgSendSuper(restype, argtypes,
                                _objc_super(objc), sel, *args)


def send_super_init(objc):
    '''Send 'init' message to the super-class of an ObjC object.

       @param objc: The recipient (C{Object}, C{Id_t}, etc.) instance.

       @return: Message result (C{Id_t}).
    '''
    return _libobjc_msgSendSuper(Id_t, [],  # [objc_super_t_ptr, SEL_t]
                                _objc_super(objc), get_selector('init'))


def set_ivar(objc, name, value, ctype=None):
    '''Set an instance variable of an ObjC object.

       @param objc: The instance (C{Object}).
       @param name: Name of the ivar (C{str}).
       @param value: New value for the ivar (C{any}).
       @keyword ctype: Optional, the ivar type (C{ctypes}).

       @return: The ivar (L{Ivar_t}).

       @raise ArgumentError: Invalid I{name}, I{value} or I{ctype}.

       @raise TypeError: Invalid I{name}, I{value} or I{ctype} type.
    '''
    if ctype is None or ctype is missing:
        ctype = _ivar_ctype(objc, name)
    argtypes = [Id_t, c_char_p, ctype]  # ObjC_t
    # returns the same ptr value for all ivar's
    return _libobject_setInstanceVariable(c_void_p, argtypes,
                                          objc, str2bytes(name), value)


def _signature3(objc_t, sel_name_, args, restype=c_void_p,  # == Id_t
                                         argtypes=[], **extra):
    '''(INTERNAL) Return the I{restype}, the I{argtypes} and the
       C{SEL/cmd} for C{send_message/_super} as 3-tuple C{(restype,
       argtypes, sel)}, where a non-empty C{argtypes} has been
       prefixed with the C{type(Id/self)} and C{type(sel)} pair as
       [I{objc_t}, C{SEL_t}].
    '''
    if extra:  # must be empty
        raise ValueError(_fmt('extra %s kwds %s',
                               sel_name_, Adict(extra)))

    if argtypes:  # XXX allow varargs
        if len(argtypes) != len(args):
            t = _fmt('len %s%r[%d] vs argtypes[%s][%d]',
                      sel_name_, tuple(args), len(args),
                     _c_tstr(*argtypes), len(argtypes))
            raise ValueError(t)
        argtypes = [objc_t, SEL_t] + argtypes

    if isinstance(sel_name_, _ByteStrs):
        sel = get_selector(sel_name_)
    elif isinstanceOf(sel_name_, SEL_t, raiser='sel_name_'):
        sel = sel_name_
    return restype, argtypes, sel


def _Xargs(x, name, argtypes=[], restype=c_void):  # in .nstypes, .printers
    '''(INTERNAL) Expand the args of an C{ctypes.ArgumentError} I{x}.
    '''
    # x.args = tuple(x.args) + (_fmt('%s(%s) %s', name, _c_tstr(*argtypes),
    #                                                   _c_tstr(restype)),)
    c = _SPACE_(_instr(name, _c_tstr(*argtypes)), _c_tstr(restype))
    try:
        t = _COMMASPACE_(*x.args)
    except AttributeError:
        t =  str(x)
    x.args = _COMMASPACE_(t, c),
    return x


class _ObjCDeallocObserver(object):  # XXX (_ObjCBase):  # must be last
    '''(INTERNAL) A separate C{_ObjCDeallocObserver} instance is associated
       with each ObjC object that is cached by L{ObjCInstance}, I{except}
       when the ObjC object is created within an L{NSAutoreleasePool}.

       The sole purpose is to watch when the ObjC object is de-allocated,
       and then remove the object from the L{ObjCInstance}C{._objc_cache_}
       dictionary kept by the L{ObjCInstance} class.

       The methods of the class below are decorated with C{.rawmethod}
       instead of C{.method} because C{_ObjCDeallocObserver} instances are
       created inside the L{ObjCInstance}C{.__new__} method and we must
       be careful to not create another L{ObjCInstance} here (which happens
       when the usual method decorator turns the C{self} argument into an
       L{ObjCInstance}) and gets trapped in an infinite recursion.

       The I{sel} argument in all decorated methods below represents
       the C{SEL/cmd} C{SEL_t}, see L{ObjCSubclass}C{.rawmethod}.
    '''
    #            _nstypes.NSObject.name
    _ObjC = ObjCSubclass(_NSObject_, '_ObjCDeallocObserver',  # .__name__
                                       register=False,  # defer
                                    **_Ivar1.akwd())  # ivar
#   ... instead of, previously:
#   _ObjC = ObjCSubclass(_NSObject_, '_ObjCDeallocObserver', register=False)
#   _ObjC.add_ivar(_Ivar1.name, ctype=_Ivar1.c_t)
#   _ObjC.register()

    @_ObjC.rawmethod('@@')
    def initWithObject_(self, unused, objc_ptr_value):
        ptr = send_super_init(self).value
        set_ivar(ptr, _Ivar1.name, objc_ptr_value, ctype=_Ivar1.c_t)
        return ptr

    @_ObjC.rawmethod('@')
    def dealloc(self, sel):
        # called before the observer is destroyed
        _objc_dealloc(self, sel)  # sel.name = 'dealloc'

    @_ObjC.rawmethod('@')
    def finalize(self, sel):
        # called instead of dealloc if using garbage collection
        # (which would have to be explicitly started with
        # objc_startCollectorThread(), so probably not much
        # reason to have this here, but it can't hurt)
        _objc_dealloc(self, sel)  # sel.name = 'finalize'

    @staticmethod
    def _new(objc_ptr_value):
        '''Create a de-allocation observer for an ObjC instance.

           @param objc_ptr_value: The ObjC instance to be observed
                                  (L{ObjCInstance}C{.ptr.value}).

           @return: The observer (C{_ObjCDeallocObserver}).

           @note: When the observed ObjC instance is de-allocated, the
                  C{_ObjCDeallocObserver} removes the corresponding
                  L{ObjCInstance} from the cached objects dictionary
                  L{ObjCInstance}C{._objc_cache_}, effectively destroying
                  the L{ObjCInstance}.
        '''
        # only .register(), don't use ObjCDelegate
        if not _ObjCDeallocObserver._ObjC.isregistered:
            _ObjCDeallocObserver._ObjC.register()

        nso = send_message(_ObjCDeallocObserver.__name__, _alloc_,
                            restype=Id_t)  # argtypes=[]
        nso = send_message(nso, 'initWithObject_', objc_ptr_value,
                           restype=Id_t, argtypes=[_Ivar1.c_t])
        # the observer is retained by ObjC objc_ptr_value
        # and associated to it as key=nso with value=nso
        _libObjC.objc_setAssociatedObject(objc_ptr_value, nso, nso,
                                          OBJC_ASSOCIATION.RETAIN)
        # double-check the association
#       obs = _libObjC.objc_getAssociatedObject(objc_ptr_value, nso)
#       assert(obs and obs.value == nso.value)
        # release to observer now, such that dealloc/finalize
        # messages are received which delete the ObjCInstance
        send_message(nso, release.__name__)
        return nso

    @staticmethod
    def _testIvar1():  # in .__main__
        '''(INTERNAL) Check that C{_ObjCDeallocObserver} has exactly one C{ivar}.
        '''
        from pycocoa.getters import get_ivars
        t = _fmt_invalid('found', ivar=_Ivar1.astr())
        for n, _, c, i in get_ivars(_ObjCDeallocObserver._ObjC):
            if n != _Ivar1.name or c != _Ivar1.c_t:
                t = _fmt_invalid(_Ivar1.astr(), ivar=_Ivar1.astr(n, c))
            else:
                t =  None
            break
        if t:
            raise AssertionError(t)


_PyRes_t2 = {_bAT:   (ObjCInstance, Id_t),
             _bHASH: (ObjCClass, Class_t)}

from ctypes import sizeof  # see from ctypes ... comments at the top

if __name__ == _Dmain_:

    from pycocoa.utils import _all_listing, _varstr

    print(_varstr(OBJC_ASSOCIATION, strepr=hex))

    _all_listing(__all__, locals())

# % python3 -m pycocoa.runtime
#
# pycocoa.runtime.__all__ = tuple(
#  pycocoa.runtime.add_ivar is <function .add_ivar at 0x1013ab740>,
#  pycocoa.runtime.add_method is <function .add_method at 0x1013d19e0>,
#  pycocoa.runtime.add_protocol is <function .add_protocol at 0x1013d1a80>,
#  pycocoa.runtime.add_subclass is <function .add_subclass at 0x1013d1b20>,
#  pycocoa.runtime.drain is <function .drain at 0x1013d1bc0>,
#  pycocoa.runtime.isClass is <function .isClass at 0x1013d1c60>,
#  pycocoa.runtime.isImmutable is <function .isImmutable at 0x1013d1d00>,
#  pycocoa.runtime.isMetaClass is <function .isMetaClass at 0x1013d1e40>,
#  pycocoa.runtime.isMutable is <function .isMutable at 0x1013d1ee0>,
#  pycocoa.runtime.isObjCInstanceOf is <function .isObjCInstanceOf at 0x1013d1f80>,
#  pycocoa.runtime.OBJC_ASSOCIATION.ASSIGN=0,
#                                  .COPY=771,
#                                  .COPY_NONATOMIC=3,
#                                  .RETAIN=769,
#                                  .RETAIN_NONATOMIC=1,
#  pycocoa.runtime.ObjCBoundClassMethod is <class .ObjCBoundClassMethod>,
#  pycocoa.runtime.ObjCBoundMethod is <class .ObjCBoundMethod>,
#  pycocoa.runtime.ObjCClass is <class .ObjCClass>,
#  pycocoa.runtime.ObjCClassMethod is <class .ObjCClassMethod>,
#  pycocoa.runtime.ObjCConstant is <class .ObjCConstant>,
#  pycocoa.runtime.ObjCDelegate is <class .ObjCDelegate>,
#  pycocoa.runtime.ObjCInstance is <class .ObjCInstance>,
#  pycocoa.runtime.ObjCMethod is <class .ObjCMethod>,
#  pycocoa.runtime.ObjCSubclass is <class .ObjCSubclass>,
#  pycocoa.runtime.register_subclass is <function .register_subclass at 0x1013d2840>,
#  pycocoa.runtime.release is <function .release at 0x1013d28e0>,
#  pycocoa.runtime.retain is <function .retain at 0x1013d2980>,
#  pycocoa.runtime.send_message is <function .send_message at 0x1013d2a20>,
#  pycocoa.runtime.send_super is <function .send_super at 0x1013d2ac0>,
#  pycocoa.runtime.send_super_init is <function .send_super_init at 0x1013d2b60>,
#  pycocoa.runtime.set_ivar is <function .set_ivar at 0x1013d2c00>,
# )[27]
# pycocoa.runtime.version 25.3.24, .isLazy 1, Python 3.13.2 64bit arm64, macOS 15.3.2

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
