
# -*- coding: utf-8 -*-

# Basic, __builtin__ Python types wrapping ObjC NS... instances.

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

from bases   import _Type0
from nstypes import isNone, ns2py, NSMutableSet, py2NS, NSSet, _Types
from runtime import isImmutable, isInstanceOf, ObjCInstance

__all__ = ('FrozenSet',
           'Set')
__version__ = '18.04.18'


if True:  # MCCABE 66

    class FrozenSet(frozenset, _Type0):  # frozenset, first to maintain frozenset behavior
        '''Python Type equivalent of an immutable ObjC NSSet.
        '''
        def __new__(cls, ns_frozenset=()):
            if isinstance(ns_frozenset, FrozenSet):
                ns = ns_frozenset.NS
            elif isinstance(ns_frozenset, frozenset):
                ns = py2NS(ns_frozenset)
            elif isinstance(ns_frozenset, tuple):
                ns = py2NS(frozenset(ns_frozenset))
            elif isImmutable(ns_frozenset, NSMutableSet,
                                           NSSet, name=FrozenSet.__name__):
                ns = ns_frozenset

            self = super(FrozenSet, cls).__new__(cls, ns2py(ns))
            self.NS = ns
            return self

        def copy(self):
            return self.__class__(self)

    class Set(set, _Type0):  # set, first to maintain set behavior
        '''Python Type equivalent of a mutable ObjC NSSet.
        '''
        def __new__(cls, ns_set=[]):
            if isinstance(ns_set, Set):
                ns = ns_set.NS
            elif isinstance(ns_set, set):
                ns = py2NS(ns_set)
            elif isinstance(ns_set, list):
                ns = py2NS(set(ns_set))
            elif isInstanceOf(ns_set, NSMutableSet, name=Set.__name__):
                ns = ns_set

            self = super(Set, cls).__new__(cls, ns2py(ns))
            self.NS = ns
            return self

        def copy(self):
            return self.__class__(self)

        @property
        def NS(self):
            self.NS = py2NS(self)  # mutable
            return self._NS

else:  # XXX far too much duplication

    class FrozenSet(_Type0):  # PYCHOK expected
        '''Python Type equivalent of an immutable ObjC NSSet.
        '''
        _set  = frozenset()  # or set(), empty to start
        _type = frozenset

        def __init__(self, ns_set=()):
            if isinstance(ns_set, frozenset):
                self._set = ns_set
            elif isinstance(ns_set, tuple):
                self._set = frozenset(ns_set)
            elif isinstance(ns_set, FrozenSet):
                self._set = ns_set._set
            elif isinstance(ns_set, Set):
                self._set = frozenset(ns_set._set)
            elif isImmutable(ns_set, NSMutableSet,  # mutable first
                                     NSSet, name=FrozenSet.__name__):
                self._set = ns2py(ns_set)

        def __contains__(self, elem):
            if isinstance(elem, ObjCInstance):
                elem = ns2py(elem)
            return self._set.__contains__(elem)

        def __and__(self, elem):
            return self._set.__and__(elem)

        def __cmp__(self, elem):
            return self._set.__cmp__(elem)

        def __eq__(self, elem):
            return self._set.__eq__(elem)

        def __ge__(self, elem):
            return self._set.__ge__(elem)

        def __gt__(self, elem):
            return self._set.__gt__(elem)

        def __iter__(self):
            return self._set.__iter__()

        def __le_(self, elem):
            return self._set.__le__(elem)

        def __len__(self):
            return len(self._set)

        def __lt__(self, elem):
            return self._set.__lt__(elem)

        def __ne__(self, elem):
            return self._set.__ne__(elem)

        def __or_(self, elem):
            return self._set.__or__(elem)

        def __rand__(self, elem):
            return self._set.__rand__(elem)

        def __ror__(self, elem):
            return self._set.__ror__(elem)

        def __rsub__(self, elem):
            return self._set.__rsub__(elem)

        def __rxor__(self, elem):
            return self._set.__rxor__(elem)

        def __sizeof__(self, elem):  # PYCHOK expected
            return self._set.__sizeof__(elem)

        def __sub__(self, elem):
            return self._set.__sub__(elem)

        def __xor__(self, elem):
            return self._set.__xor__(elem)

        def copy(self):
            '''Make a shallow copy, returning a Frozen/Set instance.
            '''
            return self.__class__(self._type(self._set))

        def difference(self, *others):
            '''Like frozen/set.difference(), but return Frozen/Set instance.
            '''
            return self.__class__(self._set.difference(*others))

        def intersection(self, *others):  # &
            '''Like frozen/set.intersection(), but return Frozen/Set instance.
            '''
            return self.__class__(self._set.intersection(*others))

        def isdisjoint(self, other):
            '''Like frozen/set.isdisjoint().
            '''
            return self.__class__(self._set.isdisjoint(other))

        def issubset(self, other):  # <= / <
            '''Like frozen/set.issubset(), but return Frozen/Set instance.
            '''
            return self.__class__(self._set.issubset(other))

        def issuperset(self, other):  # >= / >
            '''Like frozen/set.issuperset(), but return Frozen/Set instance.
            '''
            return self.__class__(self._set.issuperset(other))

        @property
        def NS(self):
            if isNone(self._NS):
                self._NS = py2NS(self._type(self._set))
            return self._NS

        def symmetric_difference(self, other):  # ^
            '''Like frozen/set.symmetric_difference(), but return Frozen/Set instance.
            '''
            return self.__class__(self._set.symmetric_difference(other))

        def union(self, *others):  # |
            '''Like frozen/set.union(), but return Frozen/Set instance.
            '''
            return self.__class__(self._set.union(*others))

    class Set(FrozenSet):  # PYCHOK expected
        '''Python Type equivalent of a mutable ObjC NSSet.
        '''
        _type = set

        def __init__(self, ns_set=[]):
            if isinstance(ns_set, set):
                self._set = ns_set
            elif isinstance(ns_set, list):
                self._set = set(ns_set)
            elif isinstance(ns_set, (Set, FrozenSet)):
                self._set = ns_set._set
            elif isInstanceOf(ns_set, NSMutableSet, name=Set.__name__):
                self._set = ns2py(ns_set)

        def __iand__(self, elem):
            return self._set.__iand__(elem)

        def __ior__(self, elem):
            return self._set.__ior__(elem)

        def __isub__(self, elem):
            return self._set.__isub__(elem)

        def __ixor__(self, elem):
            return self._set.__ixor__(elem)

        def add(self, elem):
            '''Like set.add().
            '''
            self.NS = None
            self._set.add(elem)

        def clear(self):
            '''Like set.clear().
            '''
            self.NS = None
            self._set.clear()

        def difference_update(self, *others):  # -=
            '''Like set.difference_update().
            '''
            self.NS = None
            self._set.difference_update(*others)

        def discard(self, elems):
            '''Like set.discard().
            '''
            self.NS = None
            self._set.discard(elems)

        def intersection_update(self, *others):  # &=
            '''Like set.intersection_update().
            '''
            self.NS = None
            self._set.intersection_update(*others)

        def pop(self):
            '''Like set.pop().
            '''
            self.NS = None
            return self._set.pop(self)

        def remove(self, elems):
            '''Like set.remove().
            '''
            self.NS = None
            self._set.remove(elems)

        def symmetric_difference_update(self, other):  # ^=
            '''Like set.symmetric_difference_update().
            '''
            self.NS = None
            self._set.symmetric_difference_update(other)

        def update(self, *others):  # |=
            '''Like set.update().
            '''
            self.NS = None
            self._set.update(*others)

NSSet._Type        = _Types.FrozenSet = FrozenSet
NSMutableSet._Type = _Types.Set       = Set

if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)
