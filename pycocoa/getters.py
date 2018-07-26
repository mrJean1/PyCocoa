
# -*- coding: utf-8 -*-

# License at the end of this file.

'''C{get_...} functions to obtain ObjC classes, methods, protocols, etc.
'''
# all imports listed explicitly to help PyChecker
from ctypes  import ArgumentError, byref, c_uint, cast, CFUNCTYPE
from octypes import emcoding2ctype, encoding2ctype, \
                    Class_t, Id_t, IMP_t, Ivar_t, Protocol_t, SEL_t, \
                    split_encoding
from oslibs  import libobjc  # get_lib
from utils   import bytes2str, Cache2, _exports, isinstanceOf, missing, \
                    name2objc, str2bytes

__version__ = '18.07.25'

_c_func_t_cache = {}
_SEL_t_cache = Cache2(limit2=128)
_super_cache = Cache2(limit2=32)


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
    raise ValueError('no %r ivar: %r' % (name, objc))


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

       @return: The class (L{Class_t}) if found, None otherwise.
    '''
    return libobjc.objc_getClass(str2bytes(name)) or None


def get_classes(*prefixes):
    '''Yield all loaded ObjC classes with a name
       starting with one of the given prefixes.

       @param prefixes: No, one or more class names to match (C{str}-s).

       @return: For each class yield a 2-tuple (I{name, class})
                where I{name} is the class name and I{class} is
                the ObjC L{Class_t} object.
    '''
    n = libobjc.objc_getClassList(None, 0)
    clases = (Class_t * n)()
    n = libobjc.objc_getClassList(clases, n)
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
    if clas and isinstanceOf(clas, Class_t, name='clas'):
        return bytes2str(libobjc.class_getName(clas))
    if dflt is missing:
        raise ValueError('no such %s: %r' % ('Class', clas))
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

       @return: The object's class (L{Class_t}) if found, None otherwise.
    '''
    return libobjc.object_getClass(cast(objc, Id_t)) or None


def get_ivar(objc, name, ctype=None):
    '''Get the value of an instance variable (ivar).

       @param objc: The object (C{Object} or L{Id_t}).
       @param name: The instance variable name (C{str}).
       @keyword ctype: The instance variable type (C{ctypes}),

       @return: The ivar value (C{any}) if found, None otherwise.
    '''
    if ctype is None:  # lookup ivar by name
        ctype = _ivar_ctype(objc, name)

    ivar = ctype()
    libobjc.object_getInstanceVariable(objc, str2bytes(name), byref(ivar))
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
    for ivar in libobjc.class_copyIvarList(clas, byref(n)):
        name = bytes2str(libobjc.ivar_getName(ivar))
        if name.startswith(prefixes or name):
            # XXX should yield name, ObjCIvar instance
            encoding = libobjc.ivar_getTypeEncoding(ivar)
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
        clas = libobjc.class_getSuperclass(clas)


def get_metaclass(name):
    '''Get a registered ObjC metaclass by name.

       @param name: The metaclass (C{str}).

       @return: The metaclass (L{Class_t}) if found, None otherwise.
    '''
    return libobjc.objc_getMetaClass(str2bytes(name)) or None


def get_method(clas, name):
    '''Get a method of an ObjC class by name.

       @param clas: Class (L{Class_t}).
       @param name: Method name (C{str}).

       @return: The method (L{Method_t}) if found, None otherwise.
    '''
    n = c_uint()
    for method in libobjc.class_copyMethodList(clas, byref(n)):
        sel = libobjc.method_getName(method)
        if bytes2str(libobjc.sel_getName(sel)) == name:
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
    for method in libobjc.class_copyMethodList(clas, byref(n)):
        sel = libobjc.method_getName(method)
        name = bytes2str(libobjc.sel_getName(sel))
        if name.startswith(prefixes or name):
            # XXX should yield name, ObjCMethod instance
            encoding = libobjc.method_getTypeEncoding(method)
            rescode = libobjc.method_copyReturnType(method)
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

       @see: U{Property Attributes<http://Developer.Apple.com/library/content/documentation/
             Cocoa/Conceptual/ObjCRuntimeGuide/Articles/ocrtPropertyIntrospection.html>}.
    '''
    n = c_uint()
    if isinstance(clas_or_proto, Class_t):
        props = libobjc.class_copyPropertyList(clas_or_proto, byref(n))
        setters = set(_[0] for _ in get_methods(clas_or_proto, 'set'))
    elif isinstance(clas_or_proto, Protocol_t):
        props = libobjc.protocol_copyPropertyList(clas_or_proto, byref(n))
        setters = []
    else:
        raise TypeError('%s not a %s nor %s: %r' % ('clas_or_proto',
                        Class_t.__name__, Protocol_t.__name__, clas_or_proto))

    for prop in props:
        name = bytes2str(libobjc.property_getName(prop))
        if name and name.startswith(prefixes or name):
            # XXX should yield name, ObjCProperty instance
            # attrs T@"type",&,C,D,G<name>,N,P,R,S<name>,W,t<encoding>,V<varname>
            attrs = bytes2str(libobjc.property_getAttributes(prop))
            attrs = '%s=(%s)' % (attrs, ', '.join(_PropertyAttributes
                    .get(_[:1], _[:1]) + _[1:] for _ in attrs.split(',')))
            setter = ''
            if setters:
                set_ = 'set' + name.capitalize() + ':'
                if set_ in setters:
                    setter = _PropertyAttributes['S'] + set_
            yield name, attrs, setter, prop


def get_protocol(name):
    '''Get a registered ObjC protocol by name.

       @param name: The protocol name (C{str}).

       @return: The protocol (L{Protocol_t}) if found, None otherwise.
    '''
    return libobjc.objc_getProtocol(str2bytes(name)) or None


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
    for proto in libobjc.class_copyProtocolList(clas, byref(n)):
        name = bytes2str(libobjc.protocol_getName(proto))
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
        sel = libobjc.sel_registerName(name2objc(name_)) or None
        _SEL_t_cache[name_] = sel
    return sel


def get_selectornameof(sel):
    '''Get the name of an ObjC selector.

       @param sel: The selector (L{SEL_t}).

       @return: The selector name (C{str}) if found, C{""} otherwise.
    '''
    isinstanceOf(sel, SEL_t, name='sel')
    return bytes2str(libobjc.sel_getName(sel)) or ''


def get_superclass(clas):
    '''Get the ObjC super-class of an ObjC class.

       @param clas: The class (L{Class_t}).

       @return: The super-class (L{Class_t}), None otherwise.
    '''
    isinstanceOf(clas, Class_t, name='clas')
    try:
        supr = _super_cache[clas.value]
    except KeyError:
        supr = libobjc.class_getSuperclass(clas) or None
        _super_cache[clas.value] = supr
    return supr


def get_superclassof(objc):
    '''Get the ObjC super-class of an object.

       @param objc: The object (C{Object} or L{Id_t}).

       @return: The super-class (L{Class_t}), None otherwise.
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


# filter locals() for .__init__.py
__all__ = _exports(locals(), starts='get_')

if __name__ == '__main__':

    from utils import _allisting

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
