
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

# all imports listed explicitly to help PyChecker
from ctypes  import alignment, ArgumentError, byref, c_buffer, \
                    c_char_p, c_double, c_float, c_longdouble, c_uint, \
                    c_void_p, cast, CFUNCTYPE, POINTER, Structure, sizeof
from oclibs  import libobjc
from octypes import __i386__, __LP64__, _2bytes, _2str, Class, \
                    ctype2encoding, emcoding2ctype, encoding2ctype, \
                    Id, IMP, Ivar, Protocol, objc_super, SEL, \
                    split_encoding, split_emcoding2

__version__ = '18.03.11'

# <http://Developer.Apple.com/documentation/objectivec/
#         objc_associationpolicy?language=objc>
OBJC_ASSOCIATION_COPY             = 0x303  # 01403
OBJC_ASSOCIATION_COPY_NONATOMIC   = 3
OBJC_ASSOCIATION_RETAIN           = 0x301  # 01401
OBJC_ASSOCIATION_RETAIN_NONATOMIC = 1


def _argtypestr(argtypes):
    '''Simplify names of c_... argument types.
    '''
    return ', '.join(getattr(t, '__name__', str(t)) for t in argtypes)


def _ivar_ctype(obj, name):
    '''Find the ctype of an Objective-C instance variable.
    '''
    for ivar, _, ctype in get_ivars(obj, name):
        if ivar == name:
            return ctype
    raise ValueError('no such ivar %r' % (name,))


def _objcall(objcf, restype, argtypes, *args):
    '''Call an objc function and decorate an ArgumentError if any.
    '''
    objcf.restype = restype
    objcf.argtypes = argtypes
    try:
        return objcf(*args)
    except ArgumentError as x:
        _xargs(x, objcf.__name__, argtypes, restype)
        raise


def _resargtypesel3(args, resargtypes, selName):
    '''Get and check the restype and argtypes keyword arguments.
    '''
    restype  = resargtypes.pop('restype', c_void_p)
    argtypes = resargtypes.pop('argtypes', [])
    if resargtypes:
        t = ', '.join('%s=%r' % _ for _ in sorted(resargtypes.items()))
        raise ValueError('unused %s kwds %s' % (selName, t))

    if argtypes and len(argtypes) != len(args):  # allow varargs
        raise ValueError('mismatch %s%r vs argtypes[%s]' % (selName,
                          tuple(args), _argtypestr(argtypes)))

    return restype, argtypes, get_selector(selName)


def _xargs(x, name, argtypes, restype='void'):
    '''Expand the args of an ArgumentError.
    '''
    restr = getattr(restype, '__name__', str(restype))
    x.args = ('%s: %s(%s) %s' % (', '.join(map(str, x.args)), name,
                                 _argtypestr(argtypes), restr),)


class ObjCBoundMethod(object):
    '''Python wrapper for an Objective-C method (an IMP) which has been
    bound to some Id which is passed as the first method argument.
    '''

    def __init__(self, method, objc_id):
        '''Initialize with a method and ObjCInstance or ObjCClass object.
        '''
        self.method = method
        self.objc_id = objc_id

    def __repr__(self):
        r = (ObjCBoundMethod.__name__, self.method.name, self.objc_id)
        return '<%s %s (%s)>' % r

    def __call__(self, *args):
        '''Call the method with the given arguments.
        '''
        return self.method(self.objc_id, *args)


class ObjCClass(object):
    '''Python wrapper for an Objective-C class.
    '''
    name = ''  # shut PyChecker up
    ptr = None

    _classmethods = {}  # shut PyChecker up
    _methods = {}

    # Only one Python object is created for each Objective-C class.
    # Any future calls with the same class will return the previously
    # created Python object.  Note that these aren't weak references.
    # Each ObjCClass created will exist until the end of the program.
    _objc_classes = {}

    def __new__(cls, name_or_ptr):
        '''Create a new ObjCClass instance or return a previously
        created instance for the given Objective-C class.

        The argument is either the name of the class to retrieve
        or a pointer to the class.
        '''
        # Determine name and ptr values from passed in argument.
        if isinstance(name_or_ptr, (bytes, str)):
            name, ptr = _2str(name_or_ptr), get_class(name_or_ptr)
            if ptr is None or ptr.value is None:
                raise ValueError('no such %s %r' % ('Class', name))
        else:  # Make sure that ptr is wrapped in Class,
            # for safety when passing as ctypes argument.
            ptr = cast(name_or_ptr, Class)
            if ptr is None or ptr.value is None:
                raise ValueError('no such %s %r' % ('Class', 'nil'))
            name = get_classname(ptr)

        # Check if we've already created a Python object for this class
        # and if so, return it rather than making a new one.
        try:
            return cls._objc_classes[name]
        except KeyError:
            pass

        # Otherwise create a new Python object and then initialize it.
        self = super(ObjCClass, cls).__new__(cls)  # objc_class
        self.name = name
        self.ptr = self._as_parameter_ = ptr  # for ctypes

        # Store the new class in dictionary of registered classes.
        cls._objc_classes[name] = self

        # Cache Python representations of all instance methods from
        # by this class (but does not find methods of superclass).
        self._methods = self._cache_methods(ptr)
        # Cache Python representations of all class methods from
        # by this class (but does not find methods of superclass)
        self._classmethods = self._cache_methods(get_classof(ptr))

        return self

    def __getattr__(self, name):
        '''Returns a callable method object with the given name.
        '''
        name = _2bytes(name)

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
        raise AttributeError('ObjCClass %s has no attribute %s' % (
                             _2str(self.name), _2str(name)))

    def __repr__(self):
        r = (ObjCClass.__name__, _2str(self.name), self.ptr.value)
        return "<%s %s at %r>" % r

    def _cache_methods(self, cls_inst):
        # Build cache of all class or instance methods
        n, cache = c_uint(), {}
        if not __debug__:
            for method in libobjc.class_copyMethodList(cls_inst, byref(n)):
                objc_method = ObjCMethod(method)
                cache[objc_method.pyname] = objc_method
        return cache

    def _get_method(self, name, cache, getMethod):
        # If method name isn't in the cached list, it might be a
        # method of the superclass, so call class_getInstanceMethod
        # or class_getClassMethod to check.
        # name = _2str(name).replace(':', '_') or .replace('_', ':')?
        try:
            return cache[name]
        except KeyError:
            method = getMethod(self.ptr, get_selector(name))
            if method and method.value:
                cache[name] = method = ObjCMethod(method)
                return method
        return None

    def get_classmethod(self, name):
        '''Return a Python representation of the named class method,
        either by looking it up in the cached list of methods or by
        searching for and creating a new method object.
        '''
        return self._get_method(name, self._classmethods, libobjc.class_getClassMethod)

    def get_method(self, name):
        '''Return a Python representation of a named instance method,
        either by looking it up in the cached list of methods or by
        searching for and creating a new method object.
        '''
        return self._get_method(name, self._methods, libobjc.class_getInstanceMethod)


def _objects_cache_pop(inst, name, send=''):
    # Remove an instance variable from the objects cache
    obj = get_ivar(inst, name, Id)
    ObjCInstance._objects_cache.pop(obj, None)
    if send:
        send_super(inst, send)


class ObjCInstance(object):
    '''Python wrapper for an Objective-C instance.
    '''
    ptr = None  # shut PyChecker up
    objc_class = None

    _objects_cache = {}  # see DeallocObserver, example class_wrapper4.py

    def __new__(cls, object_ptr):
        '''Create a new ObjCInstance or return a previously created one
        for the given object_ptr which should be an Objective-C id.
        '''
        # Make sure that object_ptr is wrapped in an Id.
        if not isinstance(object_ptr, Id):
            object_ptr = cast(object_ptr, Id)

        if not object_ptr.value:
            return None  # nil pointer

        # Check if we've already created an python ObjCInstance for this
        # object_ptr id and if so, return it.  A single ObjCInstance will
        # be created for any object pointer when it is first encountered.
        # This ObjCInstance will persist until the object is deallocated.
        try:
            return cls._objects_cache[object_ptr.value]
        except KeyError:
            pass

        # Otherwise, create a new ObjCInstance.
        self = super(ObjCInstance, cls).__new__(cls)  # objc_instance
        self.ptr = self._as_parameter_ = object_ptr  # for ctypes

        # Determine class of this object.
        self.objc_class = ObjCClass(get_classof(object_ptr))

        # Store new object in the dictionary of cached objects, keyed
        # by the (integer) memory address pointed to by the object_ptr.
        cls._objects_cache[object_ptr.value] = self

        # Create a DeallocObserver associated with this object,
        # but only if this object is not an Objective-C class.
        if not isClass(self):
            DeallocObserver(self)

        return self

    def __getattr__(self, name):
        '''Returns a callable method object with the given name.
        '''
        name = _2bytes(name)

        # Search for named instance method in the class object and if it
        # exists, return callable object with self as hidden argument.
        method = self.objc_class.get_method(name)
        if method:
            # Note: you should pass self and not self.ptr as a parameter
            # to ObjCBoundMethod, so that it will be able to keep the
            # ObjCInstance alive for chained calls like Class.alloc().init()
            # where the object created by alloc() is not assigned to a variable.
            return ObjCBoundMethod(method, self)

        # Otherwise, search for class method with given name in the class
        # object.  If that exists, return callable object with a pointer
        # to the class as a hidden argument.
        method = self.objc_class.get_classmethod(name)
        if method:
            return ObjCBoundMethod(method, self.objc_class.ptr)

        # Otherwise raise an exception.
        raise AttributeError('ObjCInstance %s has no attribute %s' % (
                             self.objc_classname(), _2str(name)))

    def __repr__(self):
        r = (ObjCInstance.__name__, id(self), self.objc_classname(),
                                    str(self.ptr.value))
        return '<%s %#x: %s at %s>' % r

#   def autorelease(self):
#       '''Release/free this Objective-C object.  Note, this may result
#       in Python memory errors, aborts and/r segfaults, worst case.
#       '''
#       _objcall(libobjc.objc_msgSend, None, (Id, SEL),
#                        self.ptr, get_selector('autorelease'))

#   release = autorelease
#   __del__ = autorelease

    def objc_classname(self):  # overloaded by CFString, NSString
        '''Return the name of this object's Objective-C class.
        '''
        return _2str(self.objc_class.name).replace('__NSCF', 'NS').lstrip('_')

    def set_ivar(self, name, value, ctype=None):
        '''Set an instance variable to the given value.
        '''
        set_ivar(self.ptr, name, value, ctype=ctype)


class ObjCMethod(object):
    '''This represents an unbound Objective-C method (really an IMP).
    '''

    _callable = None

    def _pyresult(self, result):
        return result

    def __init__(self, method):
        '''Initialize with an Objective-C Method pointer.

        We then determine the return type and argument type
        information of the method.
        '''
        self.imp = libobjc.method_getImplementation(method)
        self.selector = libobjc.method_getName(method)
        self.name = libobjc.sel_getName(self.selector)
        self.pyname = self.name.replace(b':', b'_')

        self.encoding = libobjc.method_getTypeEncoding(method)
        try:  # Get the ctype for all args
            self.argtypes = []
            buf = c_buffer(512)
            for i in range(libobjc.method_getNumberOfArguments(method)):
                libobjc.method_getArgumentType(method, i, buf, len(buf))
                self.argtypes.append(emcoding2ctype(buf.value))
        except TypeError:
            self.argtypes = []  # XXX or None?

        # Some hacky stuff to get around ctypes issues on 64-bit.
        # Can't let ctypes convert the return value itself, because
        # it truncates the pointer along the way.  Instead, we must
        # set the return type to c_void_p to ensure we get 64-bit
        # addresses and then convert the return value manually.
        rescode = libobjc.method_copyReturnType(method)
        if rescode == b'@':
            self.restype = Id
            self._pyresult = ObjCInstance
        elif rescode == b'#':
            self.restype = Class
            self._pyresult = ObjCClass
        else:
            try:  # Get the ctype for the result encoding.
                self.restype = emcoding2ctype(rescode, name=self.name)
            except TypeError:
                self.restype = None
#       print('%s (%s) %s %s' % (self.pyname, self.encoding,
#                                self.restype, self.argtypes))

    def __call__(self, objc_id, *args):
        '''Call the method with the given id and arguments.

        You do not need to pass in the selector as an argument
        since it will be automatically provided.
        '''
        try:
            result = self.callable(objc_id, self.selector, *args)
            return self._pyresult(result)
        except ArgumentError as x:
            _xargs(x, _2str(self.name), self.argtypes, self.restype)
            raise

    def __repr__(self):
        r = (ObjCMethod.__name__, _2str(self.name),
                                  _argtypestr(self.argtypes),
                                  _2str(self.encoding))
        return "<%s %s(%s) %s>" % r

    @property
    def callable(self):
        '''Returns a Python-callable for the method's IMP.
        '''
        if not self._callable:
            self._callable = cast(self.imp, self.cfunctype)
            self._callable.restype = self.restype
            self._callable.argtypes = self.argtypes
        return self._callable

    @property
    def cfunctype(self):
        '''Returns a ctypes CFUNCTYPE for the method.
        '''
        return CFUNCTYPE(self.restype, *self.argtypes)


def _pyargs(codes3, args):
    '''Used by ObjCSubclass to convert Objective-C method arguments to
    Python values before passing them on to the Python-defined method.
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
    '''Used by ObjCSubclass to convert Objective-C results to Python values.
    '''
    if isinstance(result, (ObjCInstance, ObjCClass)):
        return result.ptr.value
    else:
        return result


class ObjCSubclass(object):
    '''Use this to create a subclass of an existing Objective-C class.

    It consists primarily of function decorators which you use to add
    methods to the subclass.

    ObjCSubclass is used to define an Objective-C subclass of an existing
    class registered with the runtime.  When you create an instance of
    ObjCSubclass, it registers the new subclass with the Objective-C
    runtime and creates a set of function decorators that you can use to
    add instance methods or class methods to the subclass.

    Typical usage would be to first create and register the subclass:

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
    subclass by either putting it in its own module (note that you don't
    actually need to expose any of the method names or the ObjCSubclass)
    or by bundling it all up inside a Python class definition, perhaps
    called MySubclassImplementation.

    It is also possible to add Objective-C ivars to the subclass, however
    if you do so, you must call the __init__ method with register=False,
    and then call the register method after the ivars have been added.
    But rather than creating the ivars in Objective-C land, it is easier
    to just define Python-based instance variables in your subclass's init
    method.

    This class is used only to *define* the interface and implementation
    of an Objective-C subclass from Python.  It should not be used in
    any other way.  If you want a Python representation of the resulting
    class, create it with ObjCClass.

    Instances are created as a pointer to the objc object by using:

    >>> myinstance = send_message('MySubclassName', 'alloc')
    >>> myinstance = send_message(myinstance, 'init')

    or wrapped inside an ObjCInstance object by using:

    >>> myclass = ObjCClass('MySubclassName')
    >>> myinstance = myclass.alloc().init()
    '''
    objc_cls = None
    objc_metaclass = None

    def __init__(self, supercls, name, register=True, **ivars):
        '''New subclass of the given (super)class.

        Optionally, specify any number of instance variables to be
        added I{before} registering the new class with a keyword
        argument I{ivarname=ctype} the specify the name and ctype
        of each instance variable.
        '''
        self.name = name
        self.objc_cls = add_subclass(supercls, name)
        self._as_parameter_ = self.objc_cls
        # Must add instance variables before registering!
        for ivar, ctype in ivars.items():
            self.add_ivar(ivar, ctype)
        if register:
            self.register()
        self._imp_cache = {}

    def _add_classmethod(self, method, name, encoding):
        if not self.objc_metaclass:
            raise ValueError('unregistered subclass %r' % (_2str(self.name),))
        imp = add_method(self.objc_metaclass, name, method, encoding)
        self._imp_cache[name] = imp

    def _add_method(self, method, name, encoding):
        imp = add_method(self.objc_cls, name, method, encoding)
        self._imp_cache[name] = imp

    def add_ivar(self, name, ctype):
        '''Add an instance variable to the subclass.

        name should be a string.
        ctype is a ctypes type.

        The class must be registered AFTER adding instance variables.
        '''
        if self.objc_metaclass:
            raise ValueError('add ivar %s in registered subclass %r' %
                            (_2str(name), _2str(self.name)))
        return add_ivar(self.objc_cls, name, ctype)

    def classmethod(self, encoding):
        '''Decorator for class methods.
        '''
        codes3, encoding = split_emcoding2(encoding, 3)

        def decorator(m):
            def objc_class_method(objc_cls, objc_cmd, *args):  # PYCHOK expected
                py_cls = ObjCClass(objc_cls)
                py_cls.objc_cmd = objc_cmd
                return _pyresult(m(py_cls, *_pyargs(codes3, args)))
            self._add_classmethod(objc_class_method, m.__name__, encoding)
            return objc_class_method
        return decorator

    def method(self, encoding):
        '''Decorator for instance methods.
        '''
        codes3, encoding = split_emcoding2(encoding, 3)

        def decorator(m):
            def objc_method(objc_self, objc_cmd, *args):  # PYCHOK expected
                py_self = ObjCInstance(objc_self)
                py_self.objc_cmd = objc_cmd
                return _pyresult(m(py_self, *_pyargs(codes3, args)))
            self._add_method(objc_method, m.__name__, encoding)
            return objc_method
        return decorator

    def rawmethod(self, encoding):
        '''Decorator for instance methods without any fancy shenanigans.

        The method must have signature m(self, cmd, *args) where
        both self and cmd are just pointers to Objective-C objects.
        '''
        _, encoding = split_emcoding2(encoding)

        def decorator(m):
            self._add_method(m, m.__name__, encoding)
            return m
        return decorator

    def register(self):
        '''Register the new class with the Objective-C runtime.
        '''
        register_subclass(self.objc_cls)
        # We can get the metaclass only after the class is registered.
        self.objc_metaclass = get_metaclass(self.name)


def add_ivar(cls, name, ctype):
    '''Add an instance variable to an Objective-C class,
    see also DeallocObserver below.

    The I{ctype} must be a C{ctypes} type or a valid Objective-C
    type encoding as C{bytes}.
    '''
    try:
        if isinstance(ctype, bytes):
            code, ctype = ctype, encoding2ctype(ctype)
        elif isinstance(ctype, str):
            raise TypeError
        else:
            code = ctype2encoding(ctype)
    except TypeError:
        raise TypeError('ivar %s type %r' % (name, ctype))

    return libobjc.class_addIvar(cls, _2bytes(name), sizeof(ctype),
                                       alignment(ctype), code)


def add_method(cls, selName, method, signature):
    '''Add a method to an Objective-C class.

    The I{signature} is the type encoding for the result and arguments
    of the I{method} callable.
    '''
    codes, signature = split_emcoding2(signature)

    cfunctype = get_cfunctype(signature, codes)
    imp = cfunctype(method)

#   libobjc.class_addMethod.argtypes = [Class, SEL, IMP, c_char_p]
    libobjc.class_addMethod(cls, get_selector(selName), cast(imp, IMP), signature)
    return imp


def add_subclass(supercls, name, register=False, **ivars):
    '''Create a new sub-class of the given super-class.

    After calling C{add_subclass}, you I{must} register the new class
    with C{register_subclass} and I{before} using the new class.

    New methods can be added I{after} the class has been registered,
    but any ivars must be added I{before} the class is registrated.

    Or, use keyword argument register=True to register the class and
    specify any number of instance variables to be added as keyword
    arguments I{ivarname=ctype}.
    '''
    if isinstance(supercls, (str, bytes)):
        supercls = get_class(supercls)

    cls = libobjc.objc_allocateClassPair(supercls, _2bytes(name), 0)

    if register:
        for ivar, ctype in ivars.items():
            add_ivar(cls, ivar, ctype)
        register_subclass(cls)

    return cls


_cfunctype_cache = {}


def get_cfunctype(signature, codes=None):
    '''Get the C{ctypes} function type for a given signature type encoding.

    Limited to basic type encodings and pointers to basic type encodings
    and does not handle arrays, bitfiels, arbitrary structs and unions.

    The I{signature} is a C{bytes} object and not unicode and I{codes}
    is a list of the individual type encodings.  If I{codes} is not
    supplied, it will be created by L{split_encoding} the signature
    (not L{split_emcoding2}).
    '''
    if not isinstance(signature, bytes):
        raise TypeError('signature not bytes %r' % (signature,))
    try:
        cfunctype = _cfunctype_cache[signature]
    except KeyError:  # create new CFUNCTYPE for the encoding
        cfunctype = CFUNCTYPE(*map(encoding2ctype, codes or split_encoding(signature)))
        # XXX cache new CFUNCTYPE (to prevent it to be gc'd?)
        _cfunctype_cache[signature] = cfunctype
    return cfunctype


def get_class(name):
    '''Get a registered Objective-C class by name.
    '''
    return libobjc.objc_getClass(_2bytes(name)) or None


def get_classes(*prefixes):
    '''Yield all loaded Objective-C classes with a name
    starting with one of the given prefixes.

    For each class yield a 2-tuple (I{name, class}) where
    I{name} is the class name and I{class} is the Objective-C
    class object.
    '''
    n = libobjc.objc_getClassList(None, 0)
    clses = (Class * n)()
    n = libobjc.objc_getClassList(clses, n)
    for cls in clses:
        # XXX should yield name, ObjCClass instance
        name = get_classname(cls)
        if name.startswith(prefixes or name):
            yield name, cls


def get_classname(cls):
    '''Get the name of an Objective-C class.
    '''
    return _2str(libobjc.class_getName(cls))


def get_classof(obj):
    '''Get the Objective-C class of an object.
    '''
    return libobjc.object_getClass(cast(obj, Id))


def get_ivar(obj, name, ctype=None):
    '''Get the value of an instance variable.
    '''
    if ctype is None:  # lookup ivar by name
        ctype = _ivar_ctype(obj, name)

    ivar = ctype()
    libobjc.object_getInstanceVariable(obj, _2bytes(name), byref(ivar))
    try:
        return ivar.value
    except AttributeError:
        if ivar:  # ctype POINTER?
            return ivar.contents
    return None


def get_ivars(cls, *prefixes):
    '''Yield all instance variables of an Objective-C class with
    a name starting with one of the given prefixes.

    For each ivar yield a 4-tuple (I{name, encoding, ctype, ivar})
    where I{name} is the ivar name, I{encoding} is the ivar's type
    encoding, I{ctype} is the ivar's C{ctypes} type and I{ivar} the
    I{Ivar} object.
    '''
    n = c_uint()
    for ivar in libobjc.class_copyIvarList(cls, byref(n)):
        name = _2str(libobjc.ivar_getName(ivar))
        if name.startswith(prefixes or name):
            # XXX should yield name, ObjCIvar instance
            encoding = libobjc.ivar_getTypeEncoding(ivar)
            ctype = emcoding2ctype(encoding, default=c_void_p)
            yield name, _2bytes(encoding), ctype, ivar


def get_inheritance(cls):
    '''Yield the inheritance of an Objective-C class in bottom-up order.
    '''
    while cls:
        yield cls
        # XXX cls = get_superclassof(cls) infinite loop
        cls = libobjc.class_getSuperclass(cls)


def get_metaclass(name):
    '''Get a registered Objective-C metaclass by name.
    '''
    return libobjc.objc_getMetaClass(_2bytes(name)) or None


def get_method(cls, name):
    '''Get a method of an Objective-C class by name.
    '''
    n = c_uint()
    for method in libobjc.class_copyMethodList(cls, byref(n)):
        sel = libobjc.method_getName(method)
        if _2str(libobjc.sel_getName(sel)) == name:
            return method
    return None


def get_methods(cls, *prefixes):
    '''Yield all methods of an Objective-C class with a name
    starting with one of the given prefixes.

    For each method yield a 4-tuple (I{name, encoding, rargtypes,
    method}), where I{name} is the method name, I{encoding} is the
    type encoding of the method signature including the return type,
    I{rargtypes} the C{ctypes} signature, the argtypes list** preceeded
    by the restype and I{method} the I{Method} object.

    **) In Python 3+ I{rargtypes} is a C{map} object, not a list.
    '''
    def _ctype(code):
        return emcoding2ctype(code, default=c_void_p)

    n = c_uint()
    for method in libobjc.class_copyMethodList(cls, byref(n)):
        sel = libobjc.method_getName(method)
        name = _2str(libobjc.sel_getName(sel))
        if name.startswith(prefixes or name):
            # XXX should yield name, ObjCMethod instance
            encoding = libobjc.method_getTypeEncoding(method)
            rescode = libobjc.method_copyReturnType(method)
            if not encoding.startswith(rescode):
                encoding = rescode + encoding
            rargtypes = map(_ctype, split_encoding(encoding))
            yield name, _2bytes(encoding), tuple(rargtypes), method


_PropertyAttributes = {'C': 'copy',      'D': '@dynamic',
                       'G': 'getter=',   'N': 'nonatomic',
                       'P': 'toGC',      'R': 'readonly',
                       'S': 'setter=',   'T': 'Type=',
                       't': 'encoding=', 'V': 'Var=',
                       'W': '__weak',    '&': 'retain'}


def get_properties(cls_or_proto, *prefixes):
    '''Yield all properties of an Objective-C class or protocol
    with a name starting with one of the given prefixes.

    For each property, yield a 3-tuple (I{name}, I{attributes},
    I{setter}, I{property}) where I{attributes} is a comma-separated
    list of the property attibutes, I{setter} is the name of the
    property setter method, provided the property is writable and
    I{property} is the Property object.  The I{setter} is an empty
    name '' for read-only properties.

    Objective-C Property Attributes:

        - T<type>"name" = Type
        - & = Retain last value (retain)
        - C = Copy
        - D = Dynamic (@dynamic)
        - G<name> = Getter selector name
        - N = Non-atomic (nonatomic)
        - P = To be garbage collected
        - R = Read-only (readonly)
        - S<name> = Setter selector name
        - t<encoding> = Old-dtyle type encoding
        - W = Weak reference (__weak)

    See U{Property Attributes<http://Developer.Apple.com/library/content/documentation/
    Cocoa/Conceptual/ObjCRuntimeGuide/Articles/ocrtPropertyIntrospection.html>}.
    '''
    n = c_uint()
    if isinstance(cls_or_proto, Class):
        props = libobjc.class_copyPropertyList(cls_or_proto, byref(n))
        setters = set(_[0] for _ in get_methods(cls_or_proto, 'set'))
    elif isinstance(cls_or_proto, Protocol):
        props = libobjc.protocol_copyPropertyList(cls_or_proto, byref(n))
        setters = []
    else:
        raise TypeError('neither %s nor %s: %r' ('class', 'protocol', cls_or_proto))

    for prop in props:
        name = _2str(libobjc.property_getName(prop))
        if name and name.startswith(prefixes or name):
            # XXX should yield name, ObjCProperty instance
            # attrs T@"type",&,C,D,G<name>,N,P,R,S<name>,W,t<encoding>,V<varname>
            attrs = _2str(libobjc.property_getAttributes(prop))
            attrs = '%s=(%s)' % (attrs, ', '.join(_PropertyAttributes
                    .get(_[:1], _[:1]) + _[1:] for _ in attrs.split(',')))
            setter = ''
            if setters:
                setName = 'set' + name.capitalize() + ':'
                if setName in setters:
                    setter = _PropertyAttributes['S'] + setName
            yield name, attrs, setter, prop


def get_protocol(name):
    '''Get a registered Objective-C protocol by name.
    '''
    return libobjc.objc_getProtocol(_2bytes(name)) or None


def get_protocols(cls, *prefixes):
    '''Yield all protocols of an Objective-C class with a name
    starting with one of the given prefixes.

    For each protocol, yield a 2-tuple (I{name}, I{protocol}) where
    I{name} is the protocol name and I{protocol} the Protocol object.
    '''
    n = c_uint()
    for proto in libobjc.class_copyProtocolList(cls, byref(n)):
        name = _2str(libobjc.protocol_getName(proto))
        if name.startswith(prefixes or name):
            # XXX should yield name, ObjCProtocol instance
            yield name, proto


def get_selector(name):
    '''Get an Objective-C selector (cmd) by name.
    '''
    return libobjc.sel_registerName(_2bytes(name).replace(b'_', b':')) or None


def get_superclassof(obj):
    '''Get the Objective-C superclass of an object.
    '''
    return libobjc.class_getSuperclass(get_classof(obj))


def isClass(obj):
    '''Return True if the Objective-C object is a class.
    '''
    # an obj is a class if its class is a metaclass
    return isMetaClass(get_classof(obj))


def isInstanceOf(obj, *Classes, **c_types):
    '''Return True if the Objective-C object is an instance of
    any of the given Objective-C classes.
    '''
    try:
        for c in Classes:
            if obj.isKindOfClass_(c):
                return True
    except AttributeError:
        pass

    c = getattr(obj, 'objc_class', None) or get_classof(obj)
    if c in Classes:
        return True

    if c_types:
        return isinstance(obj, tuple(c_types.values()))

    return False


def isMetaClass(obj):
    '''Return True if the Objective-C object is a metaclass.
    '''
    return libobjc.class_isMetaClass(obj)


def register_subclass(subcls):
    '''Register an Objective-C subclass, see also DeallocObserver below.
    '''
    if not isinstance(subcls, Class):
        subcls = Class(subcls)
    libobjc.objc_registerClassPair(subcls)


# <http://www.SealieSoftware.com/blog/archive/2008/10/30/objc_explain_objc_msgSend_stret.html>
# <xxxx://www.x86-64.org/documentation/abi-0.99.pdf> (pp.17-23) executive summary, lost?
# <http://StackOverflow.com/questions/18133812/where-is-the-x86-64-system-v-abi-documented>
# def x86_should_use_stret(restype):
#     '''Try to figure out when a return type will be passed on stack.
#     '''
#     if type(restype) != type(Structure):
#         return False
#     if not __LP64__ and sizeof(restype) <= 8:
#         return False
#     if __LP64__ and sizeof(restype) <= 16:  # maybe? I don't know?
#         return False
#     return True
#
#
# <http://www.SealieSoftware.com/blog/archive/2008/11/16/objc_explain_objc_msgSend_fpret.html>
# def should_use_fpret(restype):
#     '''Determine if objc_msgSend_fpret is required to return a floating point type.
#     '''
#     if not __i386__:   # Unneeded on non-intel processors
#         return False
#     if __LP64__ and restype == c_longdouble:
#         return True  # Use only for long double on x86_64
#     if not __LP64__ and restype in (c_float, c_double, c_longdouble):
#         return True
#     return False

if __LP64__:
    _FLOATS_ = c_longdouble,
    _RESIZE_ = 16
else:
    _FLOATS_ = c_longdouble, c_float, c_double
    _RESIZE_ = 8


def send_message(receiver, selName, *args, **resargtypes):
    '''Send message to the given I{receiver}.

    By default, the result and all arguments are C{c_void_p} wrapped.

    Use keyword arguments I{restype=c_void_p} and I{argtypes=[]} to
    change the defaults.  The I{restype} defines the C{ctypes} type
    for the returned result and I{argtypes} is the list of C{ctypes}
    types for the message arguments only (without the C{id/self} and
    C{self/cmd} arguments).
    '''
    if isinstance(receiver, (bytes, str)):
        receiver = get_class(receiver)

    # print('send_message', receiver, selName, args, resargtypes)
    restype, argtypes, selector = _resargtypesel3(args, resargtypes, selName)
    if argtypes:
        argtypes = [type(receiver), SEL] + argtypes

    # Choose the correct version of objc_msgSend based on return type.
    if __i386__ and restype in _FLOATS_:  # should_use_fpret(restype):
        result = _objcall(libobjc.objc_msgSend_fpret, restype, argtypes,
                                  receiver, selector, *args)

    elif type(restype) == type(Structure) and sizeof(restype) > _RESIZE_:  # x86_should_use_stret(restype):
        result, argtypes = restype(), [POINTER(restype)] + argtypes
        _objcall(libobjc.objc_msgSend_stret, None, argtypes,
                         byref(result), receiver, selector, *args)

    else:
        result = _objcall(libobjc.objc_msgSend, restype, argtypes,
                                  receiver, selector, *args)
        if restype == c_void_p:
            result = c_void_p(result)

    return result


objc_super_ptr = POINTER(objc_super)  # XXX backward compatibility


# http://StackOverflow.com/questions/3095360/what-exactly-is-super-in-objective-c
def send_super(receiver, selName, *args, **resargtypes):
    '''Send message to the superclass of the given I{receiver}.

    By default, the result and all arguments are C{c_void_p} wrapped.

    Use keyword arguments I{restype=c_void_p} and I{argtypes=[]} to
    change the defaults.  The I{restype} defines the C{ctypes} type
    for the returned result and I{argtypes} is the list of C{ctypes}
    types for the message arguments only (without the C{id/self} and
    C{self/cmd} arguments).
    '''
    # print('send_super', receiver, selName, args)
    if hasattr(receiver, '_as_parameter_'):
        receiver = receiver._as_parameter_

    superclass = get_superclassof(receiver)
    superobj = objc_super(receiver, superclass)

    restype, argtypes, selector = _resargtypesel3(args, resargtypes, selName)
    if argtypes:
        argtypes = [objc_super_ptr, SEL] + argtypes
#   else:
#       argtypes = None

    result = _objcall(libobjc.objc_msgSendSuper, restype, argtypes,
                              byref(superobj), selector, *args)
    if restype == c_void_p:
        result = c_void_p(result)
    return result


def set_ivar(obj, name, value, ctype=None):
    '''Set an instance variable of an Objective-C object to the given value.
    '''
    if ctype is None:
        ctype = _ivar_ctype(obj, name)

    argtypes = [Ivar, c_char_p, ctype]
    _objcall(libobjc.object_setInstanceVariable, None, argtypes,
                     obj, _2bytes(name), value)


class _DeallocObserver_Implementation(object):
    '''Instances of DeallocObserver are associated with every
    Objective-C object that gets wrapped inside an I{ObjCInstanc}.

    Their sole purpose is to watch when the Objective-C object is
    de-allocated, and then remove the object from the dictionary of
    cached I{ObjCInstanc} objects kept by the I{ObjCInstanc} class.

    The methods of the class defined below are decorated with
    I{.rawmethod()} instead of I{.method()} because DeallocObservers
    are created inside of I{ObjCInstanc}'s __new__ method and we have
    to be careful to not create another I{ObjCInstanc} here (which
    happens when the usual method decorator turns the I{self} argument
    into an I{ObjCInstanc}), or else get trapped in an infinite recursion.
    '''
    DeallocObserver = ObjCSubclass('NSObject', 'DeallocObserver',
                                    observed_obj=Id)  # ivar
#   instead of, previously:
#   DeallocObserver = ObjCSubclass('NSObject', 'DeallocObserver', register=False)
#   DeallocObserver.add_ivar('observed_obj', c_void_p)
#   DeallocObserver.register()

    @DeallocObserver.rawmethod('@@')
    def initWithObject_(self, unused, obj):
        self = send_super(self, 'init').value
        set_ivar(self, 'observed_obj', obj, Id)
        return self

    @DeallocObserver.rawmethod('v')
    def dealloc(self, unused):
        _objects_cache_pop(self, 'observed_obj', send='dealloc')

    @DeallocObserver.rawmethod('v')
    def finalize(self, unused):
        # Called instead of dealloc if using garbage collection.
        # (which would have to be explicitly started with
        # objc_startCollectorThread(), so probably not much
        # reason to have this here, but it can't hurt.)
        _objects_cache_pop(self, 'observed_obj', send='finalize')


def DeallocObserver(obj):
    '''Deallocation observer for an instance object.

    When the Objective-C object is de-allocated, the observer
    removes the corresponding I{ObjCInstanc} object from the cached
    objects dictionary, effectively destroying the I{ObjCInstanc}.
    '''
    alloc = send_message('DeallocObserver', 'alloc',
                         restype=Id, argtypes=[])
    observer = send_message(alloc, 'initWithObject:', obj,
                            restype=Id, argtypes=[Id])
    libobjc.objc_setAssociatedObject(obj, observer, observer,
                                     OBJC_ASSOCIATION_RETAIN)
    # The observer is retained by the object we associate it to.
    # Release the observer now so that it will be deallocated when
    # the associated object is deallocated.
    send_message(observer, 'release')
    return observer


# filter locals() for .__init__.py
__all__ = tuple(_ for _ in locals().keys() if _.startswith(('OBJC_',
          'add_', 'get_', 'ObjC', 'send_', 'set_', 'split_'))) + (
          'isClass', 'libobjc', 'isInstanceOf', 'isMetaClass',
          'register_subclass')

if __name__ == '__main__':

    from octypes import _allist

    _allist(__all__, locals(), __version__, __file__)
