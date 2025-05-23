
# -*- coding: utf-8 -*-

# License at the end of this file.

'''C{get_...} functions to obtain ObjC classes, methods, protocols,
instance variables, etc. of ObjC objects.

@note: Some functions may SEGFAULT or hand infinitely, see function
L{segfaulty<pycocoa.faults.segfaulty>}.
'''
from pycocoa.basics import _Globals, Proxy1ce
from pycocoa.internals import bytes2str, _COLON_, _COMMA_, _COMMASPACE_, \
                             _Dmain_, _fmt, _fmt_invalid, missing, _NN_, \
                             _no, property_RO, _UNDER_, str2bytes
# from pycocoa.lazily import _ALL_LAZY  # from .oslibs
from pycocoa.octypes import emcoding2ctype, encoding2ctype, Class_t, Id_t, \
                            IMP_t, Ivar_t, Protocol_t, SEL_t, split_encoding
from pycocoa.oslibs import _libObjC,  _ALL_LAZY  # get_lib
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
# import sys  # from .internals

__all__ = _ALL_LAZY.getters
__version__ = '25.04.03'


@Proxy1ce
def _runtime():  # lazily import runtime, I{once}
    from pycocoa import runtime
    return runtime  # .isClass


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
        t = _c_func_t_cache[encoding]
    except KeyError:  # create new CFUNCTYPE for the encoding
        t = map(encoding2ctype, codes or split_encoding(encoding))
        # XXX cache new CFUNCTYPE (to prevent it to be gc'd?)
        _c_func_t_cache[encoding] = t = CFUNCTYPE(*t)
    return t


def get_class(name):
    '''Get a registered ObjC class by name.

       @param name: The class name (C{str}).

       @return: The class (L{Class_t}) if found, C{None} otherwise.
    '''
    return _libObjC.objc_getClass(str2bytes(name)) or None


def get_classes2(*prefixes):
    '''Yield all loaded ObjC classes with a name starting with one of
       the given prefixes.

       @param prefixes: No, one or more class names to match (C{str}-s).

       @return: For each class yield a 2-tuple (I{name, class}) where
                I{name} is the class name and I{class} is the ObjC
                L{Class_t} object.

       @raise SegfaultError: See function L{segfaulty<pycocoa.faults.segfaulty>}.
    '''
    n  =  get_classes_len()
    Cs = (Class_t * n)()
    _  = _libObjC.objc_getClassList(Cs, n)
    for C in Cs:
        # XXX should yield name, ObjCClass instance
        name = get_classname(C)
        if name.startswith(prefixes or name):
            yield name, C
    Cs = None  # del Cs


def get_classes_len():
    '''Get the number of ObjC classes loaded (C{int}).
    '''
    return int(_libObjC.objc_getClassList(None, 0))


def get_classname(clas, dflt=missing):
    '''Get the name of an ObjC class.

       @param clas: The class (L{Class_t}).

       @return: The class name (C{str}).

       @raise SegfaultError: See function L{segfaulty<pycocoa.faults.segfaulty>}.

       @raise ValueError: Invalid I{clas}, iff no I{dflt} provided.
    '''
    if _isClass_t(clas):
        # breakpoint() # <https://PEPs.Python.org/pep-0553/>
        if _Globals.Segfaulty:
            raise _Globals.Segfaulty  # == SegfaultError()
        return bytes2str(_libObjC.class_getName(clas))
    if dflt is missing:
        raise ValueError(_fmt_invalid(clas=repr(clas)))
    return dflt


def get_classnameof(objc, dflt=missing):
    '''Get the name of the ObjC class of an object.

       @param objc: The object (C{Object} or L{Id_t}).

       @return: The object's class name (C{str}).

       @raise SegfaultError: See function L{segfaulty<pycocoa.faults.segfaulty>}.

       @raise ValueError: Invalid I{objc}, iff no I{dflt} provided.
    '''
    return get_classname(get_classof(objc), dflt=dflt)


def get_classof(objc):
    '''Get the ObjC class of an object.

       @param objc: The object (C{Object} or L{Id_t}).

       @return: The object's class (L{Class_t}) if found, C{None} otherwise.
    '''
    return (_libObjC.object_getClass(cast(objc, Id_t)) or None) if objc else None


def get_ivar(objc, name, ctype=None):
    '''Get the value of an instance variable (ivar).

       @param objc: The object (C{Object} or L{Id_t}).
       @param name: The instance variable name (C{str}).
       @keyword ctype: The instance variable type (C{ctypes}),

       @return: The ivar value (C{any}) if found, C{None} otherwise.
    '''
    if objc:
        if ctype is None:  # lookup ivar by name
            ctype = _ivar_ctype(objc, name)

        ivar = ctype()
        _libObjC.object_getInstanceVariable(objc, str2bytes(name), byref(ivar))
        try:
            ivar = ivar.value
        except AttributeError:
            ivar = ivar.contents if ivar else None  # ctype POINTER?
    else:
        ivar = None
    return ivar


def get_ivars4(clas, *prefixes):
    '''Yield all instance variables (ivar) of an ObjC class with
       a name starting with one of the given prefixes.

       @param clas: The class (L{Class_t}).
       @param prefixes: No, one or more ivar names to match (C{str}-s).

       @return: For each ivar yield a 4-tuple (I{name, encoding, ctype,
                ivar}) where I{name} is the ivar name, I{encoding} is
                the ivar's type encoding, I{ctype} is the ivar's
                C{ctypes} type and I{ivar} is the L{Ivar_t} object.
    '''
    if _isClass_t(clas):
        _E = _libObjC.ivar_getTypeEncoding
        _N = _libObjC.ivar_getName
        for ivar in _libObjC.class_copyIvarList(clas, None):
            name = bytes2str(_N(ivar))
            if name.startswith(prefixes or name):
                # XXX should yield name, ObjCIvar instance
                enc = _E(ivar)
                ctype = emcoding2ctype(enc, dflt=Ivar_t)  # c_void_p
                yield name, str2bytes(enc), ctype, ivar


def get_ivars_len(clas):
    '''Get the number of instance variables (ivar) of an ObjC class (C{int}).
    '''
    return sum(1 for _ in get_ivars4(clas))


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
    for method, n in _get_method_names2(clas):
        if n == name:
            return method
    return None


def _get_method_names2(clas):
    # helper for functions get_method and get_methods4
    if _isClass_t(clas):
        _N = _libObjC.method_getName
        _S = _libObjC.sel_getName
        n  =  c_uint()
        for m in _libObjC.class_copyMethodList(clas, byref(n)):
            sel = _N(m)
            yield m, bytes2str(_S(sel))


def get_methods4(clas, *prefixes):
    '''Yield all methods of an ObjC class with a name
       starting with one of the given prefixes.

       @param clas: The class (L{Class_t}).
       @param prefixes: No, one or more method names to match (C{str}-s).

       @return: For each method yield a 4-tuple (I{name, encoding,
                resargtypes, method}), where I{name} is the method name,
                I{encoding} is the type encoding of the method signature
                including the return type, I{resargtypes} the C{ctypes}
                signature, a C{list}list of the argtypes preceeded by
                the restype and I{method} the L{Method_t} object.
    '''
    def _ctype(code):
        return emcoding2ctype(code, dflt=IMP_t)  # c_void_p

    _E = _libObjC.method_getTypeEncoding
    _R = _libObjC.method_copyReturnType
    for method, name in _get_method_names2(clas):
        if name.startswith(prefixes or name):
            r, code = _R(method), _E(method)
            if r and code and not code.startswith(r):
                code = r + code
            elif not code:
                code = r
            resargs = map(_ctype, split_encoding(code))
            # XXX should yield name, ..., ObjCMethod instance?
            yield name, str2bytes(code), list(resargs), method


_PropertyAttributes = {'C': 'copy',      'D': '@dynamic',
                       'G': 'getter=',   'N': 'nonatomic',
                       'P': 'toGC',      'R': 'readonly',
                       'S': 'setter=',   'T': 'Type=',
                       't': 'encoding=', 'V': 'Var=',
                       'W': '__weak',    '&': 'retain'}

def _xtendPA(attr):  # PYCHOK yield an extended PropertyAttribute
    a = attr[:1]
    return _NN_(_PropertyAttributes.get(a, a), attr[1:])


def get_properties4(clas_or_proto, *prefixes):
    '''Yield all properties of an ObjC class or protocol
       with a name starting with one of the given prefixes.

       @param clas_or_proto: The class or protocol (L{Class_t} or L{Protocol_t}).
       @param prefixes: No, one or more property names to match (C{str}-s).

       @return: For each property, yield a 4-tuple (I{name}, I{attributes},
                I{setter}, I{property}) where I{attributes} is a comma-separated
                list of the property attibutes, I{setter} is the name of the
                property setter method, provided the property is writable and
                I{property} is the C{Property} object.  For read-only properties,
                the I{setter} is an empty name C{""}.

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

       @raise TypeError: Invalid B{C{clas_or_proto}}.

       @see: U{Property Attributes<https://Developer.Apple.com/library/content/documentation/
             Cocoa/Conceptual/ObjCRuntimeGuide/Articles/ocrtPropertyIntrospection.html>}.
    '''
    n = c_uint()
    if isinstance(clas_or_proto, Protocol_t):
        props = _libObjC.protocol_copyPropertyList(clas_or_proto, byref(n))
        set_s =  None
    elif _isClass_t(clas_or_proto, Protocol_t, raiser='clas_or_proto'):
        props = _libObjC.class_copyPropertyList(clas_or_proto, byref(n))
        set_s =  set(m[0] for m in get_methods4(clas_or_proto, 'set'))

    _A = _libObjC.property_getAttributes
    _N = _libObjC.property_getName
    for prop in props:
        name = bytes2str(_N(prop))
        if name and name.startswith(prefixes or name):
            # XXX should yield name, ObjCProperty instance
            # attrs T@"type",&,C,D,G<name>,N,P,R,S<name>,W,t<encoding>,V<varname>
            attrs = _NN_(*bytes2str(_A(prop)).split())
            astrs = _COMMASPACE_(*map(_xtendPA, attrs.split(_COMMA_)))
            attrs = _fmt('%s=(%s)', attrs, astrs)
            set_r = _NN_
            if set_s:
                set_ = _NN_('set', name.capitalize(), _COLON_)
                if set_ in set_s:
                    set_r = _NN_(_PropertyAttributes['S'], set_)
            yield name, attrs, set_r, prop


def get_protocol(name):
    '''Get a registered ObjC protocol by name.

       @param name: The protocol name (C{str}).

       @return: The protocol (L{Protocol_t}) if found, C{None} otherwise.
    '''
    return _libObjC.objc_getProtocol(str2bytes(name)) or None


def get_protocols2(clas, *prefixes):
    '''Yield all protocols of an ObjC class with a name
       starting with one of the given prefixes.

       @param clas: The class (L{Class_t}).
       @param prefixes: No, one or more protocol names to match (C{str}-s).

       @return: For each protocol, yield a 2-tuple (I{name}, I{protocol})
                where I{name} is the protocol name and I{protocol} the
                L{Protocol_t} object.
    '''
    if _isClass_t(clas):
        n, _N = c_uint(), _libObjC.protocol_getName
        for proto in _libObjC.class_copyProtocolList(clas, byref(n)):
            name = bytes2str(_N(proto))
            if name.startswith(prefixes or name):
                # XXX should yield name, ObjCProtocol instance?
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
    if _isClass_t(clas):
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
    return get_superclass(clas) if clas else None


def get_superclassnameof(objc, dflt=missing):
    '''Get the name of the ObjC super-class of an object.

       @param objc: The object (C{Object} or L{Id_t}).

       @return: The object'ssuper-class name (C{str}).

       @raise SegfaultError: See function L{segfaulty<pycocoa.faults.segfaulty>}.

       @raise ValueError: Invalid I{objc}, iff no I{dflt} provided.
    '''
    return get_classname(get_superclassof(objc), dflt=dflt)


def _isClass_t(clas, *more, **raiser_name):
    '''(INTERNAL) Is I{clas} a L{Class_t} or an ObjC class?
    '''
    return _runtime.isClass(clas) or \
            isinstanceOf(clas, Class_t, *more,  # ObjCClass, ObjCSubclass
                         **(raiser_name or _raiser_clas))


def _ivar_ctype(objc, ivar_name):
    '''(INTERNAL) Find the ctype of an ObjC instance variable.
    '''
    if objc and ivar_name:
        for o in (objc, get_classof(objc)):
            try:
                for n, _, t, _ in get_ivars4(o, ivar_name):
                    if n == ivar_name:
                        return t
            except ArgumentError:
                pass
    t = _fmt('%s %r: %r', 'ivar', ivar_name, objc)
    raise ValueError(_no(t))


_raiser_clas = dict(raiser='clas')  # see ._isClass_t

if __name__ == _Dmain_:

    from pycocoa.utils import _all_listing

    _all_listing(__all__, locals())

    import sys
    ps = sys.argv[1:]
    if ps:
        i = 0
        for n, _ in sorted(get_classes2(*ps)):
            i += 1
            print('%s %s' % (i, n))
        print(' of %s total' % (get_classes_len(),))

# % python3 -m pycocoa.getters  [NS CF ...]
#
# pycocoa.getters.__all__ = tuple(
#  pycocoa.getters.get_c_func_t is <function .get_c_func_t at 0x1013849a0>,
#  pycocoa.getters.get_class is <function .get_class at 0x101384a40>,
#  pycocoa.getters.get_classes2 is <function .get_classes2 at 0x101384ae0>,
#  pycocoa.getters.get_classes_len is <function .get_classes_len at 0x101384b80>,
#  pycocoa.getters.get_classname is <function .get_classname at 0x101384c20>,
#  pycocoa.getters.get_classnameof is <function .get_classnameof at 0x101384cc0>,
#  pycocoa.getters.get_classof is <function .get_classof at 0x101384d60>,
#  pycocoa.getters.get_inheritance is <function .get_inheritance at 0x101384fe0>,
#  pycocoa.getters.get_ivar is <function .get_ivar at 0x101384e00>,
#  pycocoa.getters.get_ivars4 is <function .get_ivars4 at 0x101384ea0>,
#  pycocoa.getters.get_ivars_len is <function .get_ivars_len at 0x101384f40>,
#  pycocoa.getters.get_metaclass is <function .get_metaclass at 0x101385080>,
#  pycocoa.getters.get_method is <function .get_method at 0x101385120>,
#  pycocoa.getters.get_methods4 is <function .get_methods4 at 0x101385260>,
#  pycocoa.getters.get_properties4 is <function .get_properties4 at 0x1013853a0>,
#  pycocoa.getters.get_protocol is <function .get_protocol at 0x101385440>,
#  pycocoa.getters.get_protocols2 is <function .get_protocols2 at 0x1013854e0>,
#  pycocoa.getters.get_selector is <function .get_selector at 0x101385580>,
#  pycocoa.getters.get_selectorname_permutations is <function .get_selectorname_permutations at 0x1013856c0>,
#  pycocoa.getters.get_selectornameof is <function .get_selectornameof at 0x101385620>,
#  pycocoa.getters.get_superclass is <function .get_superclass at 0x101385760>,
#  pycocoa.getters.get_superclassnameof is <function .get_superclassnameof at 0x1013858a0>,
#  pycocoa.getters.get_superclassof is <function .get_superclassof at 0x101385800>,
# )[23]
# pycocoa.getters.version 25.4.3, .isLazy 1, Python 3.13.2 64bit arm64, macOS 15.4

# 1 NSAEDescriptorTranslator
# 2 NSAKDeserializer
# 3 NSAKDeserializerStream
# 4 NSAKSerializer
# 5 NSAKSerializerStream
# 6 NSATSGlyphStorage
# 7 NSATSLineFragment
# 8 NSATSTypesetter
# 9 NSATSUStyleObject
# 10 NSAVAudioPlayerSoundEngine
# 11 NSAVPlayerTextAttachmentViewProvider
# 12 NSAboutURLProtocol
# 13 NSAcceleratorGestureRecognizer
# 14 NSAccessibilityAXUIElementWrapper
# 15 NSAccessibilityActionEntry
# 16 NSAccessibilityAttributeAccessorInfo
# 17 NSAccessibilityAttributeValueContainer
# 18 NSAccessibilityChildPanel
# 19 NSAccessibilityColorButtonMockUIElement
# 20 NSAccessibilityColorUtilities
# 21 NSAccessibilityCustomAction
# 22 NSAccessibilityCustomChooser
# 23 NSAccessibilityCustomChooserItemResult
# 24 NSAccessibilityCustomChooserSearchPredicate
# 25 NSAccessibilityCustomRotor
# 26 NSAccessibilityCustomRotorItemResult
# 27 NSAccessibilityCustomRotorSearchParameters
# 28 NSAccessibilityElement
# 29 NSAccessibilityImageMockUIElement
# 30 NSAccessibilityIndexedMockUIElement
# 31 NSAccessibilityMenuExtrasMenuBar
# 32 NSAccessibilityMockStatusBarItem
# 33 NSAccessibilityMockUIElement
# 34 NSAccessibilityNotificationTable
# 35 NSAccessibilityNotifier
# 36 NSAccessibilityPathComponent
# 37 NSAccessibilityProxy
# 38 NSAccessibilityRemoteUIElement
# 39 NSAccessibilityReparentingCellProxy
# 40 NSAccessibilityReparentingProxy
# 41 NSAccessibilityRulerMarker
# 42 NSAccessibilityScrollerPart
# 43 NSAccessibilitySectionSearchElement
# 44 NSAccessibilitySegment
# 45 NSAccessibilitySliderValueIndicator
# 46 NSAccessibilityStepperArrowButton
# 47 NSAccessibilityStringIndexPathPair
# 48 NSAccessibilitySystemAppearance
# 49 NSAccessibilityTableHeaderCellProxy
# 50 NSAccessibilityTextLink
#
# ... <deleted> ...
#
# 2550 NSXMLFidelityNode
# 2551 NSXMLNSArrayTransformerName
# 2552 NSXMLNSDataTransformerName
# 2553 NSXMLNSDateTransformerName
# 2554 NSXMLNSNumberTransformerName
# 2555 NSXMLNSURLTransformerName
# 2556 NSXMLNamedFidelityNode
# 2557 NSXMLNamedNode
# 2558 NSXMLNode
# 2559 NSXMLObjectStore
# 2560 NSXMLObjectStore2
# 2561 NSXMLObjectStoreCacheNode2
# 2562 NSXMLParser
# 2563 NSXMLSAXParser
# 2564 NSXMLSchemaType
# 2565 NSXMLTidy
# 2566 NSXMLTreeReader
# 2567 NSXPCCoder
# 2568 NSXPCConnection
# 2569 NSXPCDecoder
# 2570 NSXPCEncoder
# 2571 NSXPCInterface
# 2572 NSXPCListener
# 2573 NSXPCListenerEndpoint
# 2574 NSXPCRow
# 2575 NSXPCSaveRequestContext
# 2576 NSXPCSpellServerClient
# 2577 NSXPCSpellServerClientContext
# 2578 NSXPCStore
# 2579 NSXPCStoreConnection
# 2580 NSXPCStoreConnectionInfo
# 2581 NSXPCStoreConnectionManager
# 2582 NSXPCStoreManagedObjectArchivingToken
# 2583 NSXPCStoreMessageContext
# 2584 NSXPCStoreNotificationObserver
# 2585 NSXPCStoreServer
# 2586 NSXPCStoreServerConnectionContext
# 2587 NSXPCStoreServerPerConnectionCache
# 2588 NSXPCStoreServerRequestHandlingPolicy
# 2589 NSZipFileArchive
# 2590 NSZipTextReader
#  of 10521 total

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
