
# -*- coding: utf-8 -*-

# License at the end of this file.

'''C{get_...} functions to obtain ObjC classes, methods, protocols, etc.
'''
from pycocoa.internals import bytes2str, _COLON_, _COMMA_, _COMMASPACE_, \
                             _Dmain_, missing, _NN_, _no, property_RO, \
                             _UNDER_, str2bytes
from pycocoa.lazily import _ALL_LAZY,  _fmt, _fmt_invalid
from pycocoa.octypes import emcoding2ctype, encoding2ctype, Class_t, Id_t, \
                            IMP_t, Ivar_t, Protocol_t, SEL_t, split_encoding
from pycocoa.oslibs import _libObjC  # get_lib
from pycocoa.utils import isinstanceOf, name2objc

from ctypes import ArgumentError, byref, c_uint, cast, CFUNCTYPE
import itertools
_iter_chain   = itertools.chain.from_iterable
_iter_product = itertools.product
try:
    _iter_zip = itertools.izip_longest  # Python 2
except AttributeError:
    _iter_zip = itertools.zip_longest  # Python 3+
del itertools

__all__ = _ALL_LAZY.getters
__version__ = '25.02.25'


class _Cache2(dict):
    '''Two-level cache implemented by two C{dict}s, a primary
       level-1 C{dict} and a secondary level-2 C{dict}.

       Newly created key-value pairs are entered into the
       secondary C{dict}.  Repeatedly gotten key-value items
       are elevated from the secondary to the primary C{dict}.

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
        return dict.__contains__(self, key) or key in self._dict2

    def __delitem__(self, key):
        return self.pop(key)

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
        except KeyError:  # otherwise add to secondary
            d2 = self.dict2
            if self._limit2:
                n = len(d2)
                if n > max(4, self._limit2):
                    for k in tuple(d2.keys())[:n//4]:
                        d2.pop(k)
            d2[key] = value
            # print(len(self), len(d2))

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

           @param other: Items specified as an iterable of 2-tuples
                         C{(key, value)} or as a C{dict}.
           @keyword kwds: Items given as C{key=value} pairs, with
                          priority over B{C{other}}.
        '''
        if other:
            if len(other) != 1:
                raise ValueError(_fmt_invalid(other=other))
            d = other[0]
            if not isinstance(d, dict):
                raise TypeError(_fmt_invalid(other=d))
            dict.update(self, d)
        if kwds:
            dict.update(self, kwds)

_c_func_t_cache = {}  # PYCHOK singltons
_SEL_t_cache    = _Cache2(limit2=128)
_super_cache    = _Cache2(limit2=32)


def _ivar_ctype(objc, name):
    '''(INTERNAL) Find the ctype of an ObjC instance variable.
    '''
    try:
        for ivar, _, ctype, _ in get_ivars(objc, name):
            if ivar == name:
                return ctype
    except ArgumentError:
        pass
    try:
        for ivar, _, ctype, _ in get_ivars(get_classof(objc), name):
            if ivar == name:
                return ctype
    except ArgumentError:
        pass
    t = _fmt('%r %s: %r', name, 'ivar', objc)
    raise ValueError(_no(t))


def get_c_func_t(encoding, codes=None):
    '''Get the C{ctypes} function type for a given function signature.

       @param encoding: Type encoding of the signature (C{str} or C{bytes}).
       @keyword codes: The individual type codes (C{type encoding}[])

       @note: The signature I{encoding} is a C{str} or C{bytes}, not unicode
              and I{codes} is a list of the individual type encodings, limited
              to basic type encodings and pointers to basic type encodings.
              Does not handle C{array}s, C{bitfield}s, arbitrary C{struct}s
              and C{union}s.  If keyword I{codes} is not supplied, it will be
              created from the I{signature} by L{split_encoding}, not
              L{split_emcoding2}.
    '''
    encoding = str2bytes(encoding)
    try:
        c_func_t = _c_func_t_cache[encoding]
    except KeyError:  # create new CFUNCTYPE for the encoding
        c_func_t = CFUNCTYPE(*map(encoding2ctype, codes or split_encoding(encoding)))
        # XXX cache new CFUNCTYPE (to prevent it to be gc'd?)
        _c_func_t_cache[encoding] = c_func_t
    return c_func_t


def get_class(name):
    '''Get a registered ObjC class by name.

       @param name: The class name (C{str}).

       @return: The class (L{Class_t}) if found, C{None} otherwise.
    '''
    return _libObjC.objc_getClass(str2bytes(name)) or None


def get_classes(*prefixes):
    '''Yield all loaded ObjC classes with a name
       starting with one of the given prefixes.

       @param prefixes: No, one or more class names to match (C{str}-s).

       @return: For each class yield a 2-tuple (I{name, class})
                where I{name} is the class name and I{class} is
                the ObjC L{Class_t} object.
    '''
    n = _libObjC.objc_getClassList(None, 0)
    clases = (Class_t * n)()
    n = _libObjC.objc_getClassList(clases, n)
    for clas in clases:
        # XXX should yield name, ObjCClass instance
        name = get_classname(clas)
        if name.startswith(prefixes or name):
            yield name, clas


def get_classname(clas, dflt=missing):
    '''Get the name of an ObjC class.

       @param clas: The class (L{Class_t}).

       @return: The class name (C{str}).

       @raise ValueError: Invalid I{clas}, iff no I{dflt} provided.
    '''
    if clas and isinstanceOf(clas, Class_t, raiser='clas'):
        return bytes2str(_libObjC.class_getName(clas))
    if dflt is missing:
        raise ValueError(_fmt_invalid(Class=repr(clas)))
    return dflt


def get_classnameof(objc, dflt=missing):
    '''Get the name of the ObjC class of an object.

       @param objc: The object (C{Object} or L{Id_t}).

       @return: The object's class name (C{str}).

       @raise ValueError: Invalid I{objc}, iff no I{dflt} provided.
    '''
    return get_classname(get_classof(objc), dflt=dflt)


def get_classof(objc):
    '''Get the ObjC class of an object.

       @param objc: The object (C{Object} or L{Id_t}).

       @return: The object's class (L{Class_t}) if found, C{None} otherwise.
    '''
    return _libObjC.object_getClass(cast(objc, Id_t)) or None


def get_ivar(objc, name, ctype=None):
    '''Get the value of an instance variable (ivar).

       @param objc: The object (C{Object} or L{Id_t}).
       @param name: The instance variable name (C{str}).
       @keyword ctype: The instance variable type (C{ctypes}),

       @return: The ivar value (C{any}) if found, C{None} otherwise.
    '''
    if ctype is None:  # lookup ivar by name
        ctype = _ivar_ctype(objc, name)

    ivar = ctype()
    _libObjC.object_getInstanceVariable(objc, str2bytes(name), byref(ivar))
    try:
        return ivar.value
    except AttributeError:
        if ivar:  # ctype POINTER?
            return ivar.contents
    return None


def get_ivars(clas, *prefixes):
    '''Yield all instance variables (ivar) of an ObjC class with
       a name starting with one of the given prefixes.

       @param clas: The class (L{Class_t}).
       @param prefixes: No, one or more ivar names to match (C{str}-s).

       @return: For each ivar yield a 4-tuple (I{name, encoding, ctype,
                ivar}) where I{name} is the ivar name, I{encoding} is
                the ivar's type encoding, I{ctype} is the ivar's
                C{ctypes} type and I{ivar} the L{Ivar_t} object.
    '''
    n = c_uint()
    for ivar in _libObjC.class_copyIvarList(clas, byref(n)):
        name = bytes2str(_libObjC.ivar_getName(ivar))
        if name.startswith(prefixes or name):
            # XXX should yield name, ObjCIvar instance
            encoding = _libObjC.ivar_getTypeEncoding(ivar)
            ctype = emcoding2ctype(encoding, dflt=Ivar_t)  # c_void_p
            yield name, str2bytes(encoding), ctype, ivar


def get_inheritance(clas):
    '''Yield the inheritance of an ObjC class.

       @param clas: Class (L{Class_t}).

       @return: The parent classes (L{Class_t}), in bottom-up order.
    '''
    while clas:
        yield clas
        # XXX clas = get_superclassof(clas) infinite loop
        clas = _libObjC.class_getSuperclass(clas)


def get_metaclass(name):
    '''Get a registered ObjC metaclass by name.

       @param name: The metaclass (C{str}).

       @return: The metaclass (L{Class_t}) if found, C{None} otherwise.
    '''
    return _libObjC.objc_getMetaClass(str2bytes(name)) or None


def get_method(clas, name):
    '''Get a method of an ObjC class by name.

       @param clas: Class (L{Class_t}).
       @param name: Method name (C{str}).

       @return: The method (L{Method_t}) if found, C{None} otherwise.
    '''
    n = c_uint()
    for method in _libObjC.class_copyMethodList(clas, byref(n)):
        sel = _libObjC.method_getName(method)
        if bytes2str(_libObjC.sel_getName(sel)) == name:
            return method
    return None


def get_methods(clas, *prefixes):
    '''Yield all methods of an ObjC class with a name
       starting with one of the given prefixes.

       @param clas: The class (L{Class_t}).
       @param prefixes: No, one or more method names to match (C{str}-s).

       @return: For each method yield a 4-tuple (I{name, encoding,
                rargtypes, method}), where I{name} is the method name,
                I{encoding} is the type encoding of the method signature
                including the return type, I{rargtypes} the C{ctypes}
                signature, the argtypes C{list}** preceeded by the
                restype and I{method} the L{Method_t} object.

       @note: In Python 3+ I{rargtypes} is a C{map} object, not a C{list}.
    '''
    def _ctype(code):
        return emcoding2ctype(code, dflt=IMP_t)  # c_void_p

    n = c_uint()
    for method in _libObjC.class_copyMethodList(clas, byref(n)):
        sel = _libObjC.method_getName(method)
        name = bytes2str(_libObjC.sel_getName(sel))
        if name.startswith(prefixes or name):
            # XXX should yield name, ObjCMethod instance
            encoding = _libObjC.method_getTypeEncoding(method)
            rescode = _libObjC.method_copyReturnType(method)
            if not encoding.startswith(rescode):
                encoding = rescode + encoding
            rargtypes = map(_ctype, split_encoding(encoding))
            yield name, str2bytes(encoding), tuple(rargtypes), method


_PropertyAttributes = {'C': 'copy',      'D': '@dynamic',
                       'G': 'getter=',   'N': 'nonatomic',
                       'P': 'toGC',      'R': 'readonly',
                       'S': 'setter=',   'T': 'Type=',
                       't': 'encoding=', 'V': 'Var=',
                       'W': '__weak',    '&': 'retain'}

def _xPA(attr):  # PYCHOK yield an extended PropertyAttribute
    a = attr[:1]
    return _NN_(_PropertyAttributes.get(a, a), attr[1:])


def get_properties(clas_or_proto, *prefixes):
    '''Yield all properties of an ObjC class or protocol
       with a name starting with one of the given prefixes.

       @param clas_or_proto: The class or protocol (L{Class_t} or L{Protocol_t}).
       @param prefixes: No, one or more property names to match (C{str}-s).

       @return: For each property, yield a 3-tuple (I{name}, I{attributes},
                I{setter}, I{property}) where I{attributes} is a comma-separated
                list of the property attibutes, I{setter} is the name of the
                property setter method, provided the property is writable and
                I{property} is the C{Property} object.  For read-only properties,
                the I{setter} is an empty name "".

       @note: ObjC Property Attributes:

           - T<type>"name" = Type
           - & = Retain last value (retain)
           - C = Copy
           - D = Dynamic (@dynamic)
           - G<name> = Getter selector name
           - N = Non-atomic (nonatomic)
           - P = To be garbage collected
           - R = Read-only (readonly)
           - S<name> = Setter selector name
           - t<encoding> = Old-style type encoding
           - W = Weak reference (__weak)

       @see: U{Property Attributes<https://Developer.Apple.com/library/content/documentation/
             Cocoa/Conceptual/ObjCRuntimeGuide/Articles/ocrtPropertyIntrospection.html>}.
    '''
    n = c_uint()
    if isinstance(clas_or_proto, Class_t):
        props = _libObjC.class_copyPropertyList(clas_or_proto, byref(n))
        setters = set(_[0] for _ in get_methods(clas_or_proto, 'set'))
    elif isinstance(clas_or_proto, Protocol_t):
        props = _libObjC.protocol_copyPropertyList(clas_or_proto, byref(n))
        setters = []
    else:
        raise TypeError(_fmt_invalid(clas_or_proto=clas_or_proto))

    for prop in props:
        name = bytes2str(_libObjC.property_getName(prop))
        if name and name.startswith(prefixes or name):
            # XXX should yield name, ObjCProperty instance
            # attrs T@"type",&,C,D,G<name>,N,P,R,S<name>,W,t<encoding>,V<varname>
            attrs = bytes2str(_libObjC.property_getAttributes(prop))
            astrs = _COMMASPACE_.join(map(_xPA, attrs.split(_COMMA_)))
            setter = _NN_
            if setters:
                set_ = _NN_('set', name.capitalize(), _COLON_)
                if set_ in setters:
                    setter = _NN_(_PropertyAttributes['S'], set_)
            yield name, _fmt('%s=(%s)', attrs, astrs), setter, prop


def get_protocol(name):
    '''Get a registered ObjC protocol by name.

       @param name: The protocol name (C{str}).

       @return: The protocol (L{Protocol_t}) if found, C{None} otherwise.
    '''
    return _libObjC.objc_getProtocol(str2bytes(name)) or None


def get_protocols(clas, *prefixes):
    '''Yield all protocols of an ObjC class with a name
       starting with one of the given prefixes.

       @param clas: The class (L{Class_t}).
       @param prefixes: No, one or more protocol names to match (C{str}-s).

       @return: For each protocol, yield a 2-tuple (I{name}, I{protocol})
                where I{name} is the protocol name and I{protocol} the
                L{Protocol_t} object.
    '''
    n = c_uint()
    for proto in _libObjC.class_copyProtocolList(clas, byref(n)):
        name = bytes2str(_libObjC.protocol_getName(proto))
        if name.startswith(prefixes or name):
            # XXX should yield name, ObjCProtocol instance
            yield name, proto


def get_selector(name_):
    '''Get an ObjC selector by name.

       @param name_: The selector name (C{str}).

       @return: The selector (L{SEL_t}) if found, C{None} otherwise.
    '''
    try:
        sel = _SEL_t_cache[name_]
    except KeyError:
        sel = _libObjC.sel_registerName(name2objc(name_)) or None
        _SEL_t_cache[name_] = sel
    return sel


def get_selectornameof(sel):
    '''Get the name of an ObjC selector.

       @param sel: The selector (L{SEL_t}).

       @return: The selector name (C{str}) if found, C{""} otherwise.
    '''
    isinstanceOf(sel, SEL_t, raiser='sel')
    return bytes2str(_libObjC.sel_getName(sel)) or _NN_


def get_selectorname_permutations(name_, leading=False):
    '''Yield all permutations of a Python-style selector name.

       @param name_: The selector name with underscores (C{str}).
       @keyword leading: In-/exclude leading underscores in I{name_}
                         permutations (C{bool}), default C{False}
                         meaning exclude.

       @return: The selector name (C{str}) for each underscore and
                colon permutation.

       @note: Only the underscores in I{name_} are permuted, any
              colons in I{name_} remain unchanged.
    '''
    yield name_  # original, first

    if leading:  # include
        s = name_.split(_UNDER_)
    else:  # exclude
        n = name_.lstrip(_UNDER_)
        s = n.split(_UNDER_)
        p = len(name_) - len(n)
        if p > 0:
            s[0] = name_[:p] + s[0]

    n = len(s) - 1
    if n > 0:
        for p in _iter_product('_:', repeat=n):
            # <https://StackOverflow.com/questions/952914>
            n = _NN_.join(_iter_chain(_iter_zip(s, p, fillvalue=_NN_)))
            if n != name_:
                yield n


def get_superclass(clas):
    '''Get the ObjC super-class of an ObjC class.

       @param clas: The class (L{Class_t}).

       @return: The super-class (L{Class_t}), C{None} otherwise.
    '''
    isinstanceOf(clas, Class_t, raiser='clas')
    try:
        supr = _super_cache[clas.value]
    except KeyError:
        supr = _libObjC.class_getSuperclass(clas) or None
        _super_cache[clas.value] = supr
    return supr


def get_superclassof(objc):
    '''Get the ObjC super-class of an object.

       @param objc: The object (C{Object} or L{Id_t}).

       @return: The super-class (L{Class_t}), C{None} otherwise.
    '''
    clas = get_classof(objc)
    if clas:
        clas = get_superclass(clas)
    return clas


def get_superclassnameof(objc, dflt=missing):
    '''Get the name of the ObjC super-class of an object.

       @param objc: The object (C{Object} or L{Id_t}).

       @return: The object'ssuper-class name (C{str}).

       @raise ValueError: Invalid I{objc}, iff no I{dflt} provided.
    '''
    return get_classname(get_superclassof(objc), dflt=dflt)


if __name__ == _Dmain_:

    from pycocoa.utils import _all_listing

    _all_listing(__all__, locals())

# % python3 -m pycocoa.getters
#
# pycocoa.getters.__all__ = tuple(
#  pycocoa.getters.get_c_func_t is <function .get_c_func_t at 0x102bd8680>,
#  pycocoa.getters.get_class is <function .get_class at 0x102bd8720>,
#  pycocoa.getters.get_classes is <function .get_classes at 0x102bd87c0>,
#  pycocoa.getters.get_classname is <function .get_classname at 0x102bd8860>,
#  pycocoa.getters.get_classnameof is <function .get_classnameof at 0x102bd8900>,
#  pycocoa.getters.get_classof is <function .get_classof at 0x102bd89a0>,
#  pycocoa.getters.get_inheritance is <function .get_inheritance at 0x102bd8b80>,
#  pycocoa.getters.get_ivar is <function .get_ivar at 0x102bd8a40>,
#  pycocoa.getters.get_ivars is <function .get_ivars at 0x102bd8ae0>,
#  pycocoa.getters.get_metaclass is <function .get_metaclass at 0x102bd8c20>,
#  pycocoa.getters.get_method is <function .get_method at 0x102bd8cc0>,
#  pycocoa.getters.get_methods is <function .get_methods at 0x102bd8d60>,
#  pycocoa.getters.get_properties is <function .get_properties at 0x102bd8ea0>,
#  pycocoa.getters.get_protocol is <function .get_protocol at 0x102bd8f40>,
#  pycocoa.getters.get_protocols is <function .get_protocols at 0x102bd8fe0>,
#  pycocoa.getters.get_selector is <function .get_selector at 0x102bd9080>,
#  pycocoa.getters.get_selectorname_permutations is <function .get_selectorname_permutations at 0x102bd91c0>,
#  pycocoa.getters.get_selectornameof is <function .get_selectornameof at 0x102bd9120>,
#  pycocoa.getters.get_superclass is <function .get_superclass at 0x102bd9260>,
#  pycocoa.getters.get_superclassnameof is <function .get_superclassnameof at 0x102bd93a0>,
#  pycocoa.getters.get_superclassof is <function .get_superclassof at 0x102bd9300>,
# )[21]
# pycocoa.getters.version 25.2.25, .isLazy 1, Python 3.13.2 64bit arm64, macOS 14.7.3

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
