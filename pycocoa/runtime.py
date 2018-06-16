
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

# Some Objective-C references and introductions:
#
# 1. <http://Developer.Apple.com/library/content/documentation/Cocoa/Conceptual/
# ProgrammingWithObjectiveC/Introduction/Introduction.html#//apple_ref/doc/uid/TP40011210>
#
# 2. <http://Developer.Apple.com/library/content/documentation/Cocoa/Conceptual/
# ObjCRuntimeGuide/Introduction/Introduction.html#//apple_ref/doc/uid/TP40008048-CH1-SW1>
#
# 3. <http://Developer.Apple.com/library/content/documentation/Cocoa/Conceptual/
# MemoryMgmt/Articles/MemoryMgmt.html#//apple_ref/doc/uid/10000011i>

'''Classes C{ObjCClass}, C{ObjCInstance}, C{ObjCMethod}, C{ObjCSubclass}, etc.
'''
# all imports listed explicitly to help PyChecker
from ctypes  import alignment, ArgumentError, byref, cast, c_buffer, \
                    c_char_p, c_double, c_float, CFUNCTYPE, c_longdouble, \
                    c_uint, c_void_p, POINTER, sizeof
from getters import _ivar_ctype, get_c_func_t, get_class, get_classname, \
                    get_classof, get_ivar, get_metaclass, get_protocol, \
                    get_selector, get_superclassof
from octypes import __i386__, __LP64__, c_struct_t, c_void, \
                    ctype2encoding, emcoding2ctype, encoding2ctype, \
                    Class_t, Id_t, IMP_t, Ivar_t, objc_super_t, \
                    objc_super_t_ptr, ObjC_t, SEL_t, split_emcoding2, \
                    TypeCodeError
from oslibs  import cfString2str, libobjc
from utils   import bytes2str, _Constants, _exports, missing, name2py, \
                    printf, property2, str2bytes

__version__ = '18.06.16'

# <http://Developer.Apple.com/documentation/objectivec/
#         objc_associationpolicy?language=objc>
OBJC_ASSOCIATION_COPY             = 0x303  # 01403
OBJC_ASSOCIATION_COPY_NONATOMIC   = 3
OBJC_ASSOCIATION_RETAIN           = 0x301  # 01401
OBJC_ASSOCIATION_RETAIN_NONATOMIC = 1

_objc_msgSend            = 'objc_msgSend'
_objc_msgSend_fpret      = 'objc_msgSend_fpret'
_objc_msgSend_stret      = 'objc_msgSend_stret'
_objc_msgSendSuper       = 'objc_msgSendSuper'
_objc_msgSendSuper_stret = 'objc_msgSendSuper_stret'

# <http://Developer.Apple.com/documentation/objectivec/
#         1441499-object_getinstancevariable>
_object_setInstanceVariable = 'object_setInstanceVariable'

import os
_OBJC_ENV = 'PYCOCOA_OBJC_LOG'
_OBJC_LOG = dict((_, 0) for _ in os.environ.get(_OBJC_ENV, '').upper())
del os


def _c_tstr(*c_ts):
    '''Simplify names of c_..._t result or argument types.
    '''
    return ', '.join(getattr(t, '__name__', str(t)) for t in c_ts)


def _libobjcall(name, restype, argtypes, *args):
    '''Call an ObjC library function and return the result.

       @return: The result (C{any}).

       @raise ArgumentError: Decorated by C{_Xargs}.

       @raise KeyError: Decorated by C{_Xargs}.

       @raise TypeError: Decorated by C{_Xargs}.
    '''
    try:
        objc_func = libobjc[name]  # XXX thread-specific?
        objc_func.restype  = restype  # or c_void
        objc_func.argtypes = argtypes or []

        result = objc_func(*args)
    except (ArgumentError, KeyError, TypeError) as x:
        raise _Xargs(x, objc_func.__name__, argtypes, restype)

    if restype is c_void_p or (restype and issubclass(restype, ObjC_t)
                                   and not isinstance(result, ObjC_t)):
        result = restype(result)
    return result


def _obj_and_name(name_or_obj, getter):
    '''Return or get an object by name.
    '''
    name = str2bytes(name_or_obj, dflt=None)
    if name is not None:
        name_or_obj = getter(name)
    return name_or_obj, name


def _ObjC_log(inst, what, T, *args):  # B, C, I, M, S
    '''Log a new instance, method or call to the console.
    '''
    if inst and T in _OBJC_LOG:
        _OBJC_LOG[T] += 1
        r = repr(inst)
        if args:  # insert method call args
            r = r.replace('))',  '), %s)' % (', '.join(map(repr, args)),))
        printf('%s %s %d', what, r, _OBJC_LOG[T])


def _ObjC_logf(fmt, *args):
    '''Log a message to the console.
    '''
    if 'X' in _OBJC_LOG:
        _OBJC_LOG['X'] += 1
        t = fmt
        if args:
            t = fmt % args
        printf('%s %s %d', 'call', t, _OBJC_LOG['X'])


def _ObjC_log_totals():
    '''Log summary to the console.
    '''
    if _OBJC_LOG:
        printf('%s: ...', _OBJC_ENV, nl=1)
        for k, v in _OBJC_LOG.items():
            printf('_OBJC_LOG[%s]: %d', k, v)


def _resargtypesel3(args, resargtypes, name_):
    '''Get and check the restype and argtypes keyword arguments, get
       the SEL/selector and return 3-tuple (restype, argtypes, SEL).
    '''
    restype  = resargtypes.pop('restype', c_void_p)  # XXX dflt c_void?
    argtypes = resargtypes.pop('argtypes', [])
    if resargtypes:
        t = ', '.join('%s=%r' % _ for _ in sorted(resargtypes.items()))
        raise ValueError('unused %s kwds %s' % (name_, t))

    if argtypes and len(argtypes) != len(args):  # allow varargs
        raise ValueError('mismatch %s%r vs argtypes[%s]' % (name_,
                          tuple(args), _c_tstr(*argtypes)))

    return restype, argtypes, get_selector(name_)


def _Xargs(x, name, argtypes, restype='void'):
    '''Expand the args of an ArgumentError I{x}.
    '''
    # x.args = tuple(x.args) + ('%s(%s) %s' % (name, _c_tstr(*argtypes),
    #                                                _c_tstr(restype)),)
    x.args = ('%s: %s(%s) %s' % (', '.join(map(str, x.args)), name,
                                _c_tstr(*argtypes), _c_tstr(restype)),)
    return x


class _ObjCBase(object):
    '''Base class for Python C{runtime.ObjC...} classes.
    '''
    _as_parameter_ = None  # for ctypes

    def __repr__(self):
        return '<%s(%s) at %#x>' % (self.__class__.__name__, self, id(self))


class ObjCBoundMethod(_ObjCBase):
    '''Python wrapper for an ObjC class or instance method, an L{IMP_t}.

       @note: Each ObjC method invocation requires creation of another,
              new C{ObjC[Bound]Method} instance which is immediately
              discarded thereafter.
    '''
    __slots__ = ('_method', '_objc_id')

    def __init__(self, method, objc_id):
        '''Initialize with an ObjC method L{IMP_t}, L{ObjCInstance}
           or L{ObjCClass} object.
        '''
        self._method = method
        self._objc_id = objc_id

    def __str__(self):
        return '%s.%s' % (self._objc_id, self._method.name)

    def __call__(self, *args):
        '''Call the method with the given arguments.
        '''
        _ObjC_log(self, 'call', 'B', *args)
        return self._method(self._objc_id, *args)

    @property
    def method(self):
        '''Get the method (C{ObjC[Class]Method}).
        '''
        return self._method

    @property
    def objc_id(self):
        '''Get the instance (L{ObjCInstance}).
        '''
        return self._objc_id


class ObjCBoundClassMethod(ObjCBoundMethod):
    '''Only to distinguish bound class from bound (instance) methods.
    '''
    pass


class ObjCClass(_ObjCBase):
    '''Python wrapper for an ObjC class.
    '''
    _classmethods = {}  # shut PyChecker up
    _methods = {}

    _name = b''  # shut PyChecker up
    _ptr  = None

    _Type = None  # Python Type, e.g. Dict, List, Tuple, etc.

    # Only one Python object is created for each ObjC class.  Any
    # future calls with the same class will return the previously
    # created Python object.  Note that these aren't weak references,
    # each ObjCClass created will exist until the end of the program.
    _objc_cache = {}

    def __new__(cls, name_or_ptr, *protocols):
        '''Create a new ObjCClass instance or return a previously
           created instance for the given ObjC class.

           @param name_or_ptr: Either the name of or a pointer to the
                               class to retrieve (C{str} or L{Class_t}).
           @param protocols: None, one or more protocol to add (C{str}s
                             or L{Protocol_t} instances).
        '''
        # Determine name and ptr values from passed in argument.
        ptr, name = _obj_and_name(name_or_ptr, get_class)
        if name is None:
            # Make sure that ptr is wrapped in a Class_t,
            # for safety when passing as ctypes argument.
            ptr = cast(name_or_ptr, Class_t)
            name = str2bytes(get_classname(ptr, dflt='nil'))

        if ptr is None or ptr.value is None:
            raise ValueError('no such %s: %r' % ('Class', bytes2str(name)))

        # Check if we've already created a Python object for this class
        # and if so, return it rather than making a new one.
        try:
            return cls._objc_cache[name]
        except KeyError:
            pass

        # Otherwise create a new Python object and initialize it.
        self = super(ObjCClass, cls).__new__(cls)  # objc_class
        self._name = name
        self._ptr = self._as_parameter_ = ptr  # for ctypes

        _ObjC_log(self, 'new', 'C')

        # Cache Python representations of all instance methods from
        # by this class (but does not find methods of superclass).
        self._methods = self._cache_methods(ptr)
        # Cache Python representations of all class methods from
        # by this class (but does not find methods of superclass)
        self._classmethods = self._cache_methods(get_classof(ptr))

        # add any protocols
        for p in protocols:
            add_protocol(ptr, p)

        # Store the new class in the cache of (registered) classes.
        cls._objc_cache[name] = self

        return self

    def __getattr__(self, name):
        '''Returns a callable method object with the given name.
        '''
        # If name refers to a class method, then return a callable object
        # for the class method with self.ptr as hidden first parameter.
        method = self.get_classmethod(name)
        if method:
            return ObjCBoundMethod(method, self.ptr)

        # If name refers to an instance method, then simply return the method.
        # The caller will need to supply an instance as the first parameter.
        method = self.get_method(name)
        if method:
            return method

        # Otherwise, raise an exception.
        raise AttributeError('no %r [class]method: %s ' % (name, self))

    def __str__(self):
        return '%s of %#x' % (self.name, self.ptr.value)

    def _cache_method(self, name, Class, cache, getter):
        # get and cache a class or instance method
        method = getter(self._ptr, get_selector(name))
        # XXX add a check that .alloc() is called
        # before .init() for any I{NSDelegate} class
        # printf('%s.%s', self.name, name)
        if method and method.value:
            method = Class(method)
            cache[method.name] = method
            _ObjC_log(method, 'new', 'M')
            return method
        return None

    def _cache_methods(self, which):
        # build a cache of all class or instance methods
        cache = {}
        if False:  # not __debug__:
            n = c_uint()
            for method in libobjc.class_copyMethodList(which, byref(n)):
                method = ObjCMethod(method)
                cache[method.name] = method
                _ObjC_log(method, 'new', 'M')
        return cache

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
            return self._classmethods[name2py(name)]
        except KeyError:
            return self._cache_method(name, ObjCClassMethod,
                   self._classmethods, libobjc.class_getClassMethod)

    def get_method(self, name):
        '''Find an instance method.

           @param name: Name of the method (C{str}).

           @return: The instance method wrapper (L{ObjCMethod}) or None.
        '''
        try:
            return self._methods[name2py(name)]
        except KeyError:
            return self._cache_method(name, ObjCMethod,
                   self._methods, libobjc.class_getInstanceMethod)

    @property
    def name(self):
        '''Get the ObjC class name (C{str}).
        '''
        return bytes2str(self._name)

    @property
    def ptr(self):
        '''Get this class' ObjC class (L{Class_t}).
        '''
        return self._ptr

    NS = ptr

    @property
    def Type(self):
        '''Get the Python Type for this ObjC class (C{class} or C{None}).
        '''
        return self._Type


class ObjCInstance(_ObjCBase):
    '''Python wrapper for an ObjC instance.
    '''
    _objc_cache = {}  # see _NSDeallocObserver, example class_wrapper4.py
    _objc_class = None
    _objc_ptr   = None  # shut PyChecker up

    _dealloc_d = False

    def __new__(cls, objc_ptr, cached=True):
        '''New L{ObjCInstance} or return a previously created, cached one.

           @param objc_ptr: The ObjC instance (L{Id_t} or C{c_void_p}).
           @keyword cached: Cache new instance (C{bool}).
        '''
        # Make sure that obj_ptr is wrapped in an Id_t.
        if not isinstance(objc_ptr, Id_t):
            objc_ptr = cast(objc_ptr, Id_t)

        if not objc_ptr.value:
            return None  # nil pointer

        if cached:
            # Check if we've already created an ObjCInstance for this
            # Id_t(objc_ptr) and if so, return it.  Otherwise, create
            # an ObjCInstance any object pointer first encountered.
            # That ObjCInstance will persist until the object is de-
            # allocated by ObjC, see _ns/NSDeallocObserver below.
            try:
                # cls._objc_cache == ObjCInstance._objc_cache
                return cls._objc_cache[objc_ptr.value]
            except KeyError:
                pass

        # Otherwise, create a new ObjCInstance.
        self = super(ObjCInstance, cls).__new__(cls)  # objc_instance
        self._objc_ptr = self._as_parameter_ = objc_ptr  # for ctypes

        # Determine class of this object.
        self._objc_class = ObjCClass(get_classof(objc_ptr))

        _ObjC_log(self, 'new', 'I')

        if cached:
            # store new object in the dictionary of cached objects,
            # keyed by the (integer) memory address pointed to by the
            # obj_ptr (cls._objc_cache == ObjCInstance._objc_cache)
            cls._objc_cache[objc_ptr.value] = self

            # Associate a _NSDeallocObserver with this object, but
            # only if this object is not an ObjC class.
            if not isClass(self):
                # observe the objc_ptr.value, the
                # key used for the _objc_cache dict
                _nsDeallocObserver(objc_ptr.value)

        return self

    # def __eq__(self, other):
    #     return True if (isinstance(other, ObjCInstance) and
    #                     self.isEqualTo_(other)) else False

    # def __ne__(self, other):
    #     return not self.__eq__(other)

    def __getattr__(self, name):
        '''Returns a callable method object with the given name.
        '''
        if self._dealloc_d:
            raise RuntimeError('%r no longer exists' % (self,))

        # Search for named instance method in the class object and if it
        # exists, return callable object with self as hidden argument.
        method = self._objc_class.get_method(name)
        if method:
            # Note: pass self and not self.ptr to ObjCBoundMethod, so
            # that it will be able to keep the ObjCInstance alive for
            # chained calls like Class.alloc().init() where the object
            # created by alloc() isn't assigned to a variable.
            return ObjCBoundMethod(method, self)

        # Otherwise, search for class method with given name in the class
        # object.  If that exists, return callable object with a pointer
        # to the class as a hidden argument.
        method = self._objc_class.get_classmethod(name)
        if method:
            return ObjCBoundClassMethod(method, self._objc_class.ptr)

        # Try this class' property, ...
        get, _ = property2(self, bytes2str(name))
        if get:
            return get(self)

        # ... handle substitutes for method names
        # conflicting with Python reserved words
#       if name in ('throw',):  # and self.isKindOf(NSException):
#           return self.__getattr__('raise')

        # ... otherwise raise error
        raise AttributeError('no %r [class]method: %s' % (name, self))

#   def __repr__(self):
#       return '<%s %#x: %s>' % (ObjCInstance.__name__, id(self), self)

    def __str__(self):
        return '%s(%r) of %#x' % (self.objc_classname, self.ptr, self.ptr.value)

    @property
    def objc_class(self):
        '''Get this instance' ObjC class (L{ObjCClass}).
        '''
        return self._objc_class

    @property
    def objc_classname(self):
        '''Get the name of this instance' ObjC class (C{str}).
        '''
        return self._objc_class.name.replace('__NSCF', 'NS')  # .lstrip('_')

    @property
    def objc_description(self):
        '''Get this instance' ObjC description (C{str}).
        '''
        d = _libobjcall(_objc_msgSend, Id_t, (Id_t, SEL_t),
                         self._objc_ptr, get_selector('description'))
        s = cfString2str(d, dflt='N/A')
        # d.release()
        return s

    @property
    def ptr(self):
        '''Get this instance' equivalent ObjC instance (L{Id_t}).
        '''
        return self._objc_ptr

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

    @property
    def Type(self):
        '''Get the Python Type for this instance' ObjC class (C{class}).
        '''
        ty = self._objc_class.Type
        if ty and callable(ty):
            return ty
        raise AttributeError('Type(%r): %r' % (self, ty or missing))


class ObjCMethod(_ObjCBase):
    '''Python class representing an unbound ObjC class- or
       instance-method (actually an L{IMP_t}).
    '''
    _callable = None
    _IMP      = None
    _name     = b''
    _SEL      = None

    argtypes = []  # ctypes
    encoding = b''
    restype  = None  # c_void

    def _pyresult(self, result):  # overwritten
        return result

    def __init__(self, method):
        '''New C{ObjC[Class]Method} for an ObjC method pointer.

           @param method: The method pointer (L{IMP_t}).
        '''
        self._IMP = libobjc.method_getImplementation(method)
        self._SEL = libobjc.method_getName(method)
        self._name = libobjc.sel_getName(self._SEL)  # bytes

        # determine the return type and argument types of the method
        self.encoding = libobjc.method_getTypeEncoding(method)
        try:  # Get the ctype for all args
            self.argtypes = []
            buf = c_buffer(512)
            for i in range(libobjc.method_getNumberOfArguments(method)):
                libobjc.method_getArgumentType(method, i, buf, len(buf))
                self.argtypes.append(emcoding2ctype(buf.value))
        except TypeError:
            self.argtypes = []  # XXX or None?

        # Some hacky stuff to get around ctypes issues on 64-bit:
        # can't let ctypes convert the return value itself, because
        # it truncates the pointer along the way.  Instead, set the
        # return type to c_void_p to ensure we get 64-bit addresses
        # and then convert the return value manually
        rescode = libobjc.method_copyReturnType(method)
        if rescode == b'@':
            self.restype = Id_t
            self._pyresult = ObjCInstance
        elif rescode == b'#':
            self.restype = Class_t
            self._pyresult = ObjCClass
        else:
            try:  # to get the ctype from the result encoding
                self.restype = emcoding2ctype(rescode, name=self._name)
            except TypeCodeError:
                pass  # assume c_void for b'v', b'Vv' rescode

    def __call__(self, objc_id, *args):
        '''Call the method with the given instance and arguments.

           @note: Do not pass in the selector as an argument,
                  since that is provided automatically.

           @see: L{ObjCBoundMethod}C{.__call__}.
        '''
        try:
            r = self.callable(objc_id, self._SEL, *args)
            return self._pyresult(r)
        except (ArgumentError, TypeError) as x:
            try:
                n = ObjCInstance(objc_id).objc_classname
            except AttributeError:
                n = 'objc_id'
            n = '%s.%s' % (n, self.name)
            raise _Xargs(x, n, self.argtypes, self.restype)

#   def __repr__(self):
#       return '<%s %s(%s) %s>' % (ObjCMethod.__name__, self.name,
#                                 _c_tstr(*self.argtypes),
#                                  bytes2str(self.encoding))

    def __str__(self):
        return '%s(%s) %s %s' % (self.name, _c_tstr(*self.argtypes),
                         _c_tstr(self.restype), bytes2str(self.encoding))

    @property
    def callable(self):
        '''Get a Python-callable for this method's L{IMP_t}.
        '''
        if not self._callable:
            self._callable = cast(self._IMP, self.c_func_t)
            self._callable.restype  = self.restype
            self._callable.argtypes = self.argtypes
        return self._callable

    @property
    def c_func_t(self):
        '''Get a C{ctypes} prototype for this method (C{CFUNCTYPE}).
        '''
        return CFUNCTYPE(self.restype, *self.argtypes)

    @property
    def name(self):
        '''Get the method/SELector/cmd name (C{str}).
        '''
        return name2py(self._name)


class ObjCClassMethod(ObjCMethod):
    '''Only to distinguish class methods from instance methods.
    '''
    pass


def _pyargs(codes3, args):
    '''Used by L{ObjCSubclass} to convert ObjC method arguments to
       Python values before passing those to the Python-defined method.
    '''
    if len(codes3) != len(args):
        raise ValueError('mismatch codes3 %r and args %r' % (codes3, args))

    for code, arg in zip(codes3, args):
        if code == b'@':
            arg = ObjCInstance(arg)
        elif code == b'#':
            arg = ObjCClass(arg)
        yield arg


def _pyresult(result):
    '''Used by L{ObjCSubclass} to convert the result of an ObjC
       method to the corresponding Python type/value.
    '''
    if isinstance(result, (ObjCInstance, ObjCClass)):
        return result.ptr.value
    else:
        return result


class ObjCSubclass(_ObjCBase):
    '''Python class creating an ObjC sub-class of an existing ObjC (super-)class.

       This class is used only to *define* the interface and implementation
       of an ObjC sub-class from Python.  It should not be used in any
       other way.  If you want a Python representation of the resulting
       class, create it with ObjCClass.

       It consists primarily of function decorators which you use to add
       methods to the sub-class.

       ObjCSubclass is used to define an ObjC sub-class of an existing
       class registered with the runtime.  When you create an instance of
       ObjCSubclass, it registers the new sub-class with the ObjC
       runtime and creates a set of function decorators that you can use
       to add instance methods or class methods to the sub-class.

       Typical usage would be to first create and register the sub-class:

       >>> MySubclass = ObjCSubclass('NSObject', 'MySubclassName')

       then add methods with:

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
       sub-class by either putting it in its own module (note that you don't
       actually need to expose any of the method names or the ObjCSubclass)
       or by bundling it all up inside a Python class definition, perhaps
       called MySubclassImplementation.

       It is also possible to add ObjC ivars to the sub-class, however if
       you do so, you must call the __init__ method with register=False,
       and then call the register method after the ivars have been added.

       However, instead of creating the ivars in ObjC land, it is easier
       to just define Python-based instance variables in your sub-class's
       init method.

       Instances are created as a pointer to the objc object by using:

       >>> myinstance = send_message('MySubclassName', 'alloc')
       >>> myinstance = send_message(myinstance, 'init')

       or wrapped inside an ObjCInstance object by using:

       >>> myclass = ObjCClass('MySubclassName')
       >>> myinstance = myclass.alloc().init()
    '''
    _imp_cache = {}  # decorated class/method cache
    _name      = b''

    _objc_class     = None
    _objc_metaclass = None  # None means, not (yet) registered

    def __init__(self, parent, name, register=True, **ivars):
        '''New sub-class of the given (super-)class.

           @param parent: The super-class (C{str} or C{Object}).
           @param name: The sub-class name (C{str}).
           @keyword register: Optionally, register the new sub-class (bool).
           @keyword ivars: Optionally, specify any number of instance
                           variables to be added I{before} registering
                           the new class, each with a keyword argument
                           C{ivarname=ctype} to specify the name and ctype
                           of the instance variable.
        '''
        self._imp_cache = {}
        self._name = str2bytes(name)
        self._as_parameter_ = self._objc_class = add_subclass(parent, name)

        # must add instance variables before registering!
        for ivar, ctype in ivars.items():
            self.add_ivar(ivar, ctype)

        if register:
            self.register()

        _ObjC_log(self, 'new', 'S')

    def __str__(self):
        return '%s(%r)' % ('sub-class', self.name)

    def _add_classmethod(self, method, name, encoding):
        if not self._objc_metaclass:
            raise ValueError('add method %s to unregistered %s %r' %
                            (bytes2str(name), 'sub-class', self.name,))
        imp = add_method(self._objc_metaclass, name, method, encoding)
        self._imp_cache[name] = imp

    def _add_method(self, method, name, encoding):
        imp = add_method(self._objc_class, name, method, encoding)
        self._imp_cache[name] = imp

    def add_ivar(self, name, ctype):
        '''Add an instance variable to the sub-class.

           @param name: Name of the ivar (C{str}).
           @param ctype: The ivar type (C{ctypes}).

           @raise ValueError: Class is already registered.

           @note: Instance variables can only be added
                  BEFORE the class is registered.
        '''
        if self._objc_metaclass:
            raise ValueError('add ivar %r to registered %s %r' %
                            (bytes2str(name), 'sub-class', self.name))
        return add_ivar(self._objc_class, name, ctype)

    def classmethod(self, encoding):
        '''Decorator for class methods.

           @param encoding: Signature of the method (C{encoding}).

           @return: Decorater.
        '''
        codes3, encoding = split_emcoding2(encoding, 3)

        def decorator(m):
            def objc_classmethod(objc_class, objc_cmd, *args):  # PYCHOK expected
                _pycls = ObjCClass(objc_class)
                _pycls.objc_cmd = objc_cmd
                return _pyresult(m(_pycls, *_pyargs(codes3, args)))
            n = m.__name__
#           if n.startswith('_'):
#               raise NameError('%s: %r' % ('classmethod', n))
            self._add_classmethod(objc_classmethod, n, encoding)
            objc_classmethod.name = n  # preserve name
            return objc_classmethod
        return decorator

    def method(self, encoding):
        '''Decorator for instance methods.

           @param encoding: Signature of the method (C{encoding}).

           @return: Decorater.
        '''
        codes3, encoding = split_emcoding2(encoding, 3)

        def decorator(m):
            def objc_method(objc_self, objc_cmd, *args):  # PYCHOK expected
                _pyself = ObjCInstance(objc_self)
                _pyself.objc_cmd = objc_cmd
                return _pyresult(m(_pyself, *_pyargs(codes3, args)))
            n = m.__name__
#           if n.startswith('_'):
#               raise NameError('%s: %r' % ('method', n))
            self._add_method(objc_method, n, encoding)
            objc_method.name = n  # preserve name
            return objc_method
        return decorator

    @property
    def name(self):
        '''Get the name of this ObjC sub-class (C{str}).
        '''
        return bytes2str(self._name)

    @property
    def obj_class(self):
        '''Get the ObjC class.
        '''
        return self._obj_class

    @property
    def obj_metaclass(self):
        '''Get the ObjC metaclass, or None if un-registered.
        '''
        return self._obj_metaclass

    def rawmethod(self, encoding):
        '''Decorator for instance methods without any fancy shenanigans.

           @param encoding: Signature of the method (C{encoding}).

           @return: Decorater.

           @note: The method must have signature M{m(self, cmd, *args)}
                  where both C{self} and C{cmd} are just pointers to
                  ObjC objects.
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
            raise ValueError('%s %r already registered' % ('sub-class', self))

        register_subclass(self._objc_class)
        # We can get the metaclass only after the class is registered.
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

       @see: The C{_NSDeallocObserver} below.
    '''
    try:
        code = ctype2encoding(ctype, dflt=None)
        if code is None:
            code, ctype = ctype, encoding2ctype(str2bytes(ctype))
    except TypeError:
        raise TypeCodeError('%s %s type invalid: %r' % ('type', name, ctype))

    return bool(libobjc.class_addIvar(clas, str2bytes(name), sizeof(ctype),
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
        raise TypeError('%s not a %s: %r' % ('method', 'callable', method))

    codes, signature = split_emcoding2(encoding)

    imp = get_c_func_t(signature, codes)
    imp = imp(method)
    imp = cast(imp, IMP_t)

#   libobjc.class_addMethod.argtypes = [Class_t, SEL_t, IMP_t, c_char_p]
    return imp if libobjc.class_addMethod(clas, get_selector(name_),
                                                imp, signature) else None


def add_protocol(clas, protocol):
    '''Add a protocol to an ObjC class.

       @param clas: Class to add the protocol to (C{ObjCClass/Subclass}).
       @param protocol: The C{protocol} to add (C{str} or L{Protocol_t} instance).

       @return: The protocol (L{Protocol_t}) if added, C{None} otherwise.
    '''
    protocol, _ = _obj_and_name(protocol, get_protocol)
    return protocol if libobjc.class_addProtocol(clas, protocol) else None


def add_subclass(superclas, name, register=False):
    '''Create a new sub-class of the given super-class.

       @param superclas: The parent class (C{str} or C{Object}).
       @param name: The name of the sub-class (C{str}).
       @keyword register: Optionally, register the new sub-class (bool).

       @return: The sub-class (C{Class_t}) if added, C{None} otherwise.

       @note: After calling C{add_subclass}, you I{MUST} register the
              new sub-class with L{register_subclass}, I{before} using
              the new sub-class.  New methods can be added I{after} the
              sub-class has been registered, but any C{ivar}s must be
              added I{BEFORE} the class is registrated.
    '''
    superclas, _ = _obj_and_name(superclas, get_class)
    clas = libobjc.objc_allocateClassPair(superclas, str2bytes(name), 0)
    if clas and register:
        register_subclass(clas)
    return clas or None


def isClass(objc):
    '''Check whether an object is an ObjC clas.

       @param objc: Object to check (C{Object} or C{Class}).

       @return: True if the I{objc} is a clas, False otherwise.
    '''
    # an objc is a class if its super-class is a metaclass
    return isMetaClass(get_classof(objc))


def isImmutable(objc, mutableClass, immutableClass, name='ns'):
    '''Check that an ObjC object is an instance of the immutable class.

       @param objc: The instance to check (L{ObjCInstance}).
       @param mutableClass: The mutable ObjC classes (C{NSMutable...}).
       @param immutableClass: The immutable ObjC classes (C{Object}).
       @keyword name: The name of the instance (C{str}).

       @return: True if I{objc} is an I{immutableClass} instance, False otherwise.

       @raise TypeError: If I{objc} is a I{mutableClass} instance, provided
                         keyword argument I{name='...'} is given.
    '''
    # check for the NSMutable- class first, since the mutable
    # classes seem to be sub-class of the immutable one
    if isInstanceOf(objc, mutableClass):
        raise TypeError('classof(%s) is mutable: %r' % (name, objc))
    return isInstanceOf(objc, immutableClass, name=name) is immutableClass


def isInstanceOf(objc, *Classes, **name_missing):
    '''Check whether an ObjC object is an instance of some ObjC class.

       @param objc: The instance to check (L{ObjCInstance} or C{c_void_p}).
       @param Classes: One or several ObjC classes (C{Object}).
       @keyword name: The name of the instance (C{str}).

       @return: The matching I{Class} from I{Classes}, None otherwise.

       @raise TypeError: If I{objc} is not an L{ObjCInstance} or C{c_void_p}
                         or if I{objc} does not match any of the I{Classes}
                         and only if keyword I{name='...'} is provided.

       @see: Function L{isinstanceOf} for checking Python instances.
    '''
    if isinstance(objc, ObjCInstance):
        try:
            if objc.objc_class in Classes or get_classof(objc) in Classes:
                return objc.objc_class

            iskind_ = objc.isKindOfClass_
            for c in Classes:
                if iskind_(c):
                    return c
        except AttributeError:
            pass

    elif isinstance(objc, ObjC_t):
        if ObjC_t in Classes:
            return ObjC_t
    elif isinstance(objc, c_void_p):
        if c_void_p in Classes:
            return c_void_p

    else:
        name = name_missing.get('name', 'objc')
        t = ObjCInstance.__name__
        raise TypeError('%s not an %s: %r' % (name, t, objc))

    name = name_missing.get('name', missing)
    if name is missing:
        return None

    t = ', '.join(getattr(c, 'name', getattr(c, '__name__', str(c))) for c in Classes)
    raise TypeError('%s not %s: %r' % (name, t, objc))


def isMetaClass(objc):
    '''Check whether an object is an ObjC metaclass.

       @param objc: Object to check (C{Object} or C{Class}).

       @return: True if the I{objc} is a metaclass, False otherwise.
    '''
    return bool(libobjc.class_isMetaClass(objc))


def release(objc):
    '''Release an ObjC instance to eventually be garbage collected.

       @param objc: The instance to release (L{ObjCInstance}).

       @raise TypeError: If I{objc} is not releasable.

       @note: May result in Python memory errors, aborts and/or
              segfaults.  Use 'python3 -X faulthandler ...' to
              get a Python traceback.
    '''
    try:
        objc.autorelease()  # XXX or objc.release()?
    except (AttributeError, TypeError):
        raise TypeError('not releasable: %r' % (objc,))


def register_subclass(subclas):
    '''Register an ObjC sub-class.

       @param subclas: Class to be registered (C{Class}).

       @see: L{ObjCSubclass}C{.register}.
    '''
    if not isinstance(subclas, Class_t):
        subclas = Class_t(subclas)
    libobjc.objc_registerClassPair(subclas)


def _receiver(receiver):
    # from PyBee/Rubicon-Objc <http://GitHub.com/pybee/rubicon-objc>
    receiver = getattr(receiver, '_as_parameter_', receiver)
    if isinstance(receiver, Id_t):
        return receiver
    elif isinstance(receiver, (c_void_p, ObjCInstance)):
        return cast(receiver, Id_t)
#   elif isinstance(receiver, _Strs):
#       return cast(get_class(receiver), Id_t)
    raise TypeError('%s invalid: %r' % ('receiver', receiver))


def retain(objc):
    '''Preserve an ObjC instance from destruction.

       @param objc: The instance to retain (L{ObjCInstance}).

       @return: The retained instance I{objc}.

       @raise TypeError: If I{objc} is not retainable.

       @note: May result in Python memory errors, aborts and/or
              segfaults.  Use 'python3 -X faulthandler ...' to
              get a Python traceback.
    '''
    try:
        objc.retain()  # L{ObjCMethod}
    except (AttributeError, TypeError):
        raise TypeError('not retainable: %r' % (objc,))
    return objc


# <http://www.SealieSoftware.com/blog/archive/2008/11/16/objc_explain_objc_msgSend_fpret.html>
# def x86_should_use_fpret(restype):
#     '''Determine if objc_msgSend_fpret is required to return a floating point type.
#     '''
#     if not __i386__:   # Unneeded on non-intel processors
#         return False
#     if __LP64__ and restype == c_longdouble:
#         return True  # Use only for long double on x86_64
#     if not __LP64__ and restype in (c_float, c_double, c_longdouble):
#         return True
#     return False

# <http://www.SealieSoftware.com/blog/archive/2008/10/30/objc_explain_objc_msgSend_stret.html>
# <XXXX://www.x86-64.org/documentation/abi-0.99.pdf> (pp.17-23) executive summary, lost?
# <http://StackOverflow.com/questions/18133812/where-is-the-x86-64-system-v-abi-documented>
# def x86_should_use_stret(restype):
#     '''Try to figure out when a return type will be passed on stack.
#     '''
#     if type(restype) != type(c_struct_t):
#         return False
#     if not __LP64__ and sizeof(restype) <= 8:
#         return False
#     if __LP64__ and sizeof(restype) <= 16:  # maybe? I don't know?
#         return False
#     return True

if not __i386__:
    _FLOATS_ = ()

    def _stret(unused):
        return False

elif __LP64__:
    _FLOATS_ = c_longdouble,

    def _stret(restype):  # PYCHOK expected
        return issubclass(restype, c_struct_t) and sizeof(restype) > 16

else:
    _FLOATS_ = c_longdouble, c_float, c_double

    def _stret(restype):  # PYCHOK expected
        return issubclass(restype, c_struct_t) and sizeof(restype) not in (1, 2, 4, 8)  # XXX > 8


def send_message(receiver, name_, *args, **resargtypes):
    '''Send message to an ObjC object.

       @param receiver: The recipient (C{Object}).
       @param name_: Message selector (C{str}).
       @param args: Message arguments (I{all positional}).
       @keyword resargtypes: Optional, result and argument types (C{ctypes}).

       @return: Message result (I{restype}).

       @raise ArgumentError: Invalid I{receiver}, I{name}, I{args} or
                             I{resargtypes}.

       @raise TypeError: Invalid I{receiver}, I{name}, I{args} or
                         I{resargtypes} type.

       @note: By default, the result and all arguments are C{c_void_p}
              wrapped.  Use keyword arguments I{restype=c_void_p} and
              I{argtypes=[]} to change the defaults.  The I{restype}
              defines the C{ctypes} type for the returned result and
              I{argtypes} is the list of C{ctypes} types for the message
              arguments only (without the C{Id/self} and C{SEL/cmd}
              arguments).
    '''
    receiver, _ = _obj_and_name(receiver, get_class)
    _ObjC_logf('send_message(%r, %s, %r) %r', receiver, name_, args, resargtypes)
    receiver = _receiver(receiver)

    restype, argtypes, sel = _resargtypesel3(args, resargtypes, name_)
    if argtypes:
        argtypes = [type(receiver), SEL_t] + argtypes

    if restype in _FLOATS_:  # x86_should_use_fpret(restype):
        result = _libobjcall(_objc_msgSend_fpret, restype, argtypes,
                              receiver, sel, *args)
    elif _stret(restype):  # x86_should_use_stret(restype):
        argtypes = [POINTER(restype)] + argtypes
        result = restype()
        _libobjcall(_objc_msgSend_stret, c_void, argtypes,
                     byref(result), receiver, sel, *args)
    else:
        result = _libobjcall(_objc_msgSend, restype, argtypes,
                              receiver, sel, *args)
    return result


# http://StackOverflow.com/questions/3095360/what-exactly-is-super-in-objective-c
def send_super(receiver, name_, *args, **resargtypes):
    '''Send message to the super-class of an ObjC object.

       @param receiver: The recipient (C{Object}).
       @param name_: Message selector (C{str}).
       @param args: Message arguments (I{all positional}).
       @keyword resargtypes: Optional, result and argument types (C{ctypes}).

       @return: Message result (I{restype}).

       @raise ArgumentError: Invalid I{receiver}, I{name}, I{args} or
                             I{resargtypes}.

       @raise TypeError: Invalid I{receiver}, I{name}, I{args} or
                         I{resargtypes} type.

       @note: By default, the result and all arguments are C{c_void_p}
              wrapped.  Use keyword arguments I{restype=c_void_p} and
              I{argtypes=[]} to change the defaults.  The I{restype}
              defines the C{ctypes} type for the returned result and
              I{argtypes} is the list of C{ctypes} types for the message
              arguments only (without the C{Id/self} and C{SEL/cmd}
              arguments).
    '''
    _ObjC_logf('send_super(%r, %s, %r) %r', receiver, name_, args, resargtypes)

    receiver = _receiver(receiver)
    supercls = get_superclassof(receiver)
    superobj = objc_super_t(receiver, supercls)

    restype, argtypes, sel = _resargtypesel3(args, resargtypes, name_)
    if argtypes:
        argtypes = [objc_super_t_ptr, SEL_t] + argtypes
#   else:
#       argtypes = None  # []

    if _stret(restype):  # x86_should_use_stret(restype):
        return _libobjcall(_objc_msgSendSuper_stret, restype, argtypes,
                            byref(superobj), sel, *args)
    else:
        return _libobjcall(_objc_msgSendSuper, restype, argtypes,
                            byref(superobj), sel, *args)


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

    argtypes = [Ivar_t, c_char_p, ctype]
    return _libobjcall(_object_setInstanceVariable, c_void, argtypes,
                        objc, str2bytes(name), value)


class _Ivar1(_Constants):
    # the _NSDeallocObserver ivar
    name = '_ObjCPtrValue'
    c_t  = Id_t


def _objc_cache_pop(nself, sel_cmd):
    '''(INTERNAL) Remove an L{ObjCInstance} from the instances cache
       called by the instance' associated dealloc/finalize observer.

       @param nself: The instance' observer (C{_NSDeallocObserver}).
       @param sel_cmd: The message for the parent (C{str}).
    '''
    objc_ptr_value = get_ivar(nself, _Ivar1.name, ctype=_Ivar1.c_t)
    if objc_ptr_value:
        objc = ObjCInstance._objc_cache.pop(objc_ptr_value, None)
        if objc:
            objc._dealloc_d = True
    send_super(nself, sel_cmd)


class _NSDeallocObserver(object):
    '''Instances of C{_NSDeallocObserver} are associated with every
       ObjC object that gets wrapped and cached by an L{ObjCInstance}.

       Their sole purpose is to watch when the ObjC object is de-allocated,
       and then remove the object from the L{ObjCInstance}C{._objc_cache_}
       dictionary kept by the L{ObjCInstance} class.

       The methods of the class defined below are decorated with
       C{.rawmethod} instead of C{.method} because C{_NSDeallocObserver}s
       are created inside the L{ObjCInstance}C{.__new__} method and we
       must be careful to not create another L{ObjCInstance} here (which
       happens when the usual method decorator turns the C{self} argument
       into an L{ObjCInstance}) and get trapped in an infinite recursion.

       The I{unused} argument in all decorated methods below represents
       the C{SEL/cmd}, see L{ObjCSubclass}C{.rawmethod}.
    '''
    _ObjC = ObjCSubclass('NSObject', '_NSDeallocObserver',  # .__name__
                                   **{_Ivar1.name: _Ivar1.c_t})  # ivar
#   ... instead of, previously:
#   _ObjC = ObjCSubclass('NSObject', '_NSDeallocObserver', register=False)
#   _ObjC.add_ivar(_Ivar1.name, ctype=_Ivar1.c_t)
#   _ObjC.register()

    @_ObjC.rawmethod('@@')
    def initWithObject_(self, unused, objc_ptr_value):
        self = send_super(self, 'init').value
        set_ivar(self, _Ivar1.name, objc_ptr_value, ctype=_Ivar1.c_t)
        return self

    @_ObjC.rawmethod('@')
    def dealloc(self, unused):
        _objc_cache_pop(self, 'dealloc')

    @_ObjC.rawmethod('@')
    def finalize(self, unused):
        # Called instead of dealloc if using garbage collection
        # (which would have to be explicitly started with
        # objc_startCollectorThread(), so probably not much
        # reason to have this here, but it can't hurt.)
        _objc_cache_pop(self, 'finalize')


def _nsDeallocObserver(objc_ptr_value):
    '''Create a de-allocation observer for an ObjC instance.

       @param objc_ptr_value: The ObjC instance to be observed
                              (L{ObjCInstance}C{.ptr.value}).

       @return: The observer (C{_NSDeallocObserver}).

       @note: When the observed ObjC instance is de-allocated, the
              C{_NSDeallocObserver} removes the corresponding
              L{ObjCInstance} from thecached objects dictionary
              L{ObjCInstance}C{._objc_cache_}, effectively destroying
              the L{ObjCInstance}.
    '''
    observer = send_message(_NSDeallocObserver.__name__, 'alloc',
                            restype=Id_t)  # argtypes=[]
    observer = send_message(observer, 'initWithObject_', objc_ptr_value,
                            restype=Id_t, argtypes=[_Ivar1.c_t])
    # the observer is retained by the object associate to it
    libobjc.objc_setAssociatedObject(objc_ptr_value, observer, observer,
                                     OBJC_ASSOCIATION_RETAIN)
    # release the observer now so that it will be de-allocated
    # when the associated object is de-allocated.
    send_message(observer, 'release')
    return observer


def _nsDeallocObserverIvar1():
    # check that exactly one _NSDeallocObserver ivar exists
    from getters import get_ivars

    i = None
    for n, _, c, i in get_ivars(get_class(_NSDeallocObserver.__name__)):
        if n != _Ivar1.name or c != _Ivar1.c_t:
            raise AssertionError('%r %s != %r %s' % (n, c,
                                 _Ivar1.name, _Ivar1.c_t))
    if i is None:
        raise AssertionError('%s %s: %r %s' % ('missing', 'ivar',
                             _Ivar1.name, _Ivar1.c_t))

_nsDeallocObserverIvar1()  # PYCHOK expected
del _nsDeallocObserverIvar1


# filter locals() for .__init__.py
__all__ = _exports(locals(), 'libobjc', 'release', 'register_subclass', 'retain',
                   starts=('add_', 'is', 'OBJC_', 'ObjC', 'send_', 'set_'))

if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)
