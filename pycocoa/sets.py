
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Types L{FrozenSet} and L{Set}, wrapping ObjC C{NS[Mutable]Set}.
'''
# all imports listed explicitly to help PyChecker
from bases   import _Type0
from nstypes import isNone, ns2py, NSMutableSet, nsSet2set, NSSet
from pytypes import frozenset2NS, py2NS, set2NS
from runtime import isImmutable, isInstanceOf, ObjCInstance
from utils   import _Types

__all__ = ('FrozenSet',
           'Set')
__version__ = '18.06.28'


if True:  # MCCABE 69

    class FrozenSet(frozenset, _Type0):  # frozenset, first to maintain frozenset behavior
        '''Python C{frozenset} Type, wrapping an immutable ObjC L{NSSet}.
        '''
        def __new__(cls, ns_frozenset=()):
            '''New L{FrozenSet} from a C{frozenset}, C{tuple}, L{FrozenSet} or L{NSSet}.
            '''
            if isinstance(ns_frozenset, FrozenSet):
                return ns_frozenset
            elif isinstance(ns_frozenset, frozenset):
                py = ns_frozenset
                ns = frozenset2NS(py)
            elif isinstance(ns_frozenset, tuple):
                py = frozenset(ns_frozenset)
                ns = frozenset2NS(py)
            elif isImmutable(ns_frozenset, NSMutableSet,
                                           NSSet, name=FrozenSet.__name__):
                ns = ns_frozenset
                py = nsSet2set(ns)

            self = super(FrozenSet, cls).__new__(cls, py)
            self.NS = ns
            return self

        def copy(self):
            '''Make a copy of this frozen set.

               @return: The copy (L{FrozenSet}).
            '''
            return self.__class__(self)

    class Set(set, _Type0):  # set, first to maintain set behavior
        '''Python c{Set} Type, wrapping an ObjC L{NSMutableSet}.
        '''
        def __new__(cls, ns_set=[]):
            '''New L{Set} from a C{set}, C{list}, L{Set} or L{NSMutableSet}.
            '''
            if isinstance(ns_set, Set):
                ns, py = ns_set.NS, ns_set
            elif isinstance(ns_set, set):
                py = ns_set
                ns = set2NS(py)
            elif isinstance(ns_set, list):
                py = set(ns_set)
                ns = set2NS(py)
            elif isInstanceOf(ns_set, NSMutableSet, name=Set.__name__):
                ns = ns_set
                py = nsSet2set(ns)

            self = super(Set, cls).__new__(cls, py)
            self.NS = ns
            return self

        def copy(self):
            '''Make a copy of this set.

               @return: The copy (L{Set}).
            '''
            return self.__class__(self)

        @property
        def NS(self):
            self.NS = set2NS(self)  # mutable
            return self._NS

else:  # XXX far too much duplication

    class FrozenSet(_Type0):  # PYCHOK expected
        '''Python C{frozenset} Type, wrapping an immutable ObjC L{NSSet}.
        '''
        _set  = frozenset()  # or set(), empty to start
        _type = frozenset

        def __init__(self, ns_set=()):
            '''New L{FrozenSet} from a C{frozenset}, C{tuple}, L{FrozenSet} or L{NSSet}.
            '''
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
                self._set = nsSet2set(ns_set)

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
            '''Make a copy of this frozen/set.

               @return: The copy (L{FrozenSet} or L{Set}).
            '''
            return self.__class__(self._type(self._set))

        def difference(self, *others):
            '''Like C{frozen/set.difference}.

               @return: New instance (L{FrozenSet} or L{Set}).
            '''
            return self.__class__(self._set.difference(*others))

        def intersection(self, *others):  # &
            '''Like C{frozen/set.intersection}.

               @return: New instance (L{FrozenSet} or L{Set}).
            '''
            return self.__class__(self._set.intersection(*others))

        def isdisjoint(self, other):
            '''Like C{frozen/set.isdisjoint}.
            '''
            return self._set.isdisjoint(other)

        def issubset(self, other):  # <= / <
            '''Like C{frozen/set.issubset}.
            '''
            return self._set.issubset(other)

        def issuperset(self, other):  # >= / >
            '''Like C{frozen/set.issuperset}.
            '''
            return self._set.issuperset(other)

        @property
        def NS(self):
            if isNone(self._NS):
                self._NS = py2NS(self._type(self._set))
            return self._NS

        def symmetric_difference(self, other):  # ^
            '''Like C{frozen/set.symmetric_difference}.

               @return: New instance (L{FrozenSet} or L{Set}).
            '''
            return self.__class__(self._set.symmetric_difference(other))

        def union(self, *others):  # |
            '''Like C{frozen/set.union}.

               @return: New instance (L{FrozenSet} or L{Set}).
            '''
            return self.__class__(self._set.union(*others))

    class Set(FrozenSet):  # PYCHOK expected
        '''Python C{Set} Type, wrapping an ObjC L{NSMutableSet}.
        '''
        _type = set

        def __init__(self, ns_set=[]):
            '''New L{Set} from a C{set}, C{list}, L{FrozenSet}, L{Set} or L{NSMutableSet}.
            '''
            if isinstance(ns_set, set):
                self._set = ns_set
            elif isinstance(ns_set, list):
                self._set = set(ns_set)
            elif isinstance(ns_set, (Set, FrozenSet)):
                self._set = set(ns_set._set)
            elif isInstanceOf(ns_set, NSMutableSet, name=Set.__name__):
                self._set = nsSet2set(ns_set)

        def __iand__(self, elem):
            return self._set.__iand__(elem)

        def __ior__(self, elem):
            return self._set.__ior__(elem)

        def __isub__(self, elem):
            return self._set.__isub__(elem)

        def __ixor__(self, elem):
            return self._set.__ixor__(elem)

        def add(self, elem):
            '''Like C{set.add}.
            '''
            self.NS = None
            self._set.add(elem)

        def clear(self):
            '''Like C{set.clear}.
            '''
            self.NS = None
            self._set.clear()

        def difference_update(self, *others):  # -=
            '''Like C{set.difference_update}.
            '''
            self.NS = None
            self._set.difference_update(*others)

        def discard(self, elems):
            '''Like C{set.discard}.
            '''
            self.NS = None
            self._set.discard(elems)

        def intersection_update(self, *others):  # &=
            '''Like C{set.intersection_update}.
            '''
            self.NS = None
            self._set.intersection_update(*others)

        def pop(self):
            '''Like C{set.pop}.
            '''
            self.NS = None
            return self._set.pop(self)

        def remove(self, elems):
            '''Like C{set.remove}.
            '''
            self.NS = None
            self._set.remove(elems)

        def symmetric_difference_update(self, other):  # ^=
            '''Like C{set.symmetric_difference_update}.
            '''
            self.NS = None
            self._set.symmetric_difference_update(other)

        def update(self, *others):  # |=
            '''Like C{set.update}.
            '''
            self.NS = None
            self._set.update(*others)


NSSet._Type        = _Types.FrozenSet = FrozenSet
NSMutableSet._Type = _Types.Set       = Set

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
