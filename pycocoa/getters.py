
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

'''C{get_...} functions for obtaining ObjC classes, methods, protocols, etc.
'''
# all imports listed explicitly to help PyChecker
from ctypes  import byref, c_uint, cast, CFUNCTYPE
from oclibs  import libobjc  # get_lib
from octypes import emcoding2ctype, encoding2ctype, \
                    Class_t, Id_t, IMP_t, Ivar_t, Protocol_t, SEL_t, \
                    split_encoding
from utils   import bytes2str, _exports, instanceof, missing, \
                    name2objc, str2bytes

__version__ = '18.04.21'

_cfunctype_cache = {}


def _ivar_ctype(obj, name):
    '''Find the ctype of an ObjC instance variable.
    '''
    for ivar, _, ctype, _ in get_ivars(obj, name):
        if ivar == name:
            return ctype
    raise ValueError('no %r ivar of %r' % (name, obj))


def get_cfunctype(encoding, codes=None):
    '''Get the C{ctypes} function type for a given signature type encoding.

    Limited to basic type encodings and pointers to basic type encodings
    and does not handle arrays, bitfiels, arbitrary structs and unions.

    The I{signature} is a C{bytes} object and not unicode and I{codes}
    is a list of the individual type encodings.  If I{codes} is not
    supplied, it will be created by L{split_encoding} the signature
    (not L{split_emcoding2}).
    '''
    encoding = str2bytes(encoding)
    try:
        cfunctype = _cfunctype_cache[encoding]
    except KeyError:  # create new CFUNCTYPE for the encoding
        cfunctype = CFUNCTYPE(*map(encoding2ctype, codes or split_encoding(encoding)))
        # XXX cache new CFUNCTYPE (to prevent it to be gc'd?)
        _cfunctype_cache[encoding] = cfunctype
    return cfunctype


def get_class(name):
    '''Get a registered ObjC class by name.
    '''
    return libobjc.objc_getClass(str2bytes(name)) or None


def get_classes(*prefixes):
    '''Yield all loaded ObjC classes with a name
    starting with one of the given prefixes.

    For each class yield a 2-tuple (I{name, class}) where
    I{name} is the class name and I{class} is the ObjC
    class object.
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
    '''
    if clas:
        return bytes2str(libobjc.class_getName(clas))
    if dflt is missing:
        raise ValueError('no such %s: %r' % ('Class', clas))
    return dflt


def get_classnameof(obj, dflt=missing):
    '''Get the name of the ObjC class of an object.
    '''
    return get_classname(get_classof(obj), dflt=dflt)


def get_classof(obj):
    '''Get the ObjC class of an object.
    '''
    return libobjc.object_getClass(cast(obj, Id_t))


def get_ivar(obj, name, ctype=None):
    '''Get the value of an instance variable.
    '''
    if ctype is None:  # lookup ivar by name
        ctype = _ivar_ctype(obj, name)

    ivar = ctype()
    libobjc.object_getInstanceVariable(obj, str2bytes(name), byref(ivar))
    try:
        return ivar.value
    except AttributeError:
        if ivar:  # ctype POINTER?
            return ivar.contents
    return None


def get_ivars(clas, *prefixes):
    '''Yield all instance variables of an ObjC class with
    a name starting with one of the given prefixes.

    @param clas: Th class (C{Class}).
    @param prefixes: No, one or more I{ivar} names to match (string).

    @return: The I{ivar}s, each yielded as a 4-tuple (I{name, encoding,
             ctype, ivar}) where I{name} is the ivar name, I{encoding}
             is the ivar's type encoding, I{ctype} is the ivar's
             C{ctypes} type and I{ivar} the I{Ivar} object.
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

    @param clas: Class (C{Class}).

    @return: The parent I{class}es, yielded in bottom-up order.
    '''
    while clas:
        yield clas
        # XXX clas = get_superclassof(clas) infinite loop
        clas = libobjc.class_getSuperclass(clas)


def get_metaclass(name):
    '''Get a registered ObjC metaclass by name.

    @param name: Metaclass (string).

    @return: The C{MetaClass} if found, None otherwise.
    '''
    return libobjc.objc_getMetaClass(str2bytes(name)) or None


def get_method(clas, name):
    '''Get a method of an ObjC class by name.

    @param clas: Class (C{Class}).
    @param name: Method name (string).

    @return: The C{Method} if found, None otherwise.
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

    For each method yield a 4-tuple (I{name, encoding, rargtypes,
    method}), where I{name} is the method name, I{encoding} is the
    type encoding of the method signature including the return type,
    I{rargtypes} the C{ctypes} signature, the argtypes list** preceeded
    by the restype and I{method} the I{Method} object.

    **) In Python 3+ I{rargtypes} is a C{map} object, not a list.
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


def get_properties(cls_or_proto, *prefixes):
    '''Yield all properties of an ObjC class or protocol
    with a name starting with one of the given prefixes.

    For each property, yield a 3-tuple (I{name}, I{attributes},
    I{setter}, I{property}) where I{attributes} is a comma-separated
    list of the property attibutes, I{setter} is the name of the
    property setter method, provided the property is writable and
    I{property} is the Property object.  The I{setter} is an empty
    name '' for read-only properties.

    ObjC Property Attributes:

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
    if isinstance(cls_or_proto, Class_t):
        props = libobjc.class_copyPropertyList(cls_or_proto, byref(n))
        setters = set(_[0] for _ in get_methods(cls_or_proto, 'set'))
    elif isinstance(cls_or_proto, Protocol_t):
        props = libobjc.protocol_copyPropertyList(cls_or_proto, byref(n))
        setters = []
    else:
        raise TypeError('no %s nor %s: %r' ('class', 'protocol', cls_or_proto))

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

    @param name: Protocol (string).

    @return: The C{Protocol} if found, None otherwise.
    '''
    return libobjc.objc_getProtocol(str2bytes(name)) or None


def get_protocols(clas, *prefixes):
    '''Yield all protocols of an ObjC class with a name
    starting with one of the given prefixes.

    For each protocol, yield a 2-tuple (I{name}, I{protocol}) where
    I{name} is the protocol name and I{protocol} the Protocol object.
    '''
    n = c_uint()
    for proto in libobjc.class_copyProtocolList(clas, byref(n)):
        name = bytes2str(libobjc.protocol_getName(proto))
        if name.startswith(prefixes or name):
            # XXX should yield name, ObjCProtocol instance
            yield name, proto


def get_selector(name_):
    '''Get an ObjC selector by name.

    @param name_: Selector (string).

    @return: The C{SEL} if found, None otherwise.
    '''
    sel = name2objc(name_)
#   if not sel.endswith(b':'):
#       raise ValueError('%s invalid: %s' % ('selector', name_))
    return libobjc.sel_registerName(sel) or None


def get_selectornameof(sel):
    '''Get the name of an ObjC selector.

    @param sel: Selector (C{SEL}).

    @return: The name (string) if found, '' otherwise.
    '''
    instanceof(sel, SEL_t, name='sel')
    return bytes2str(libobjc.sel_getName(sel)) or ''


def get_superclass(clas):
    '''Get the ObjC super-class of an ObjC class.

    @param clas: Class (C{Class}).

    @return: C{Superclass}, None otherwise.
    '''
    return libobjc.class_getSuperclass(clas) or None


def get_superclassof(obj):
    '''Get the ObjC super-class of an object.

    @param obj: Object to check (I{Object}).

    @return: C{Superclass}, None otherwise.
    '''
    return libobjc.class_getSuperclass(get_classof(obj)) or None


# filter locals() for .__init__.py
__all__ = _exports(locals(), starts='get_')

if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)
