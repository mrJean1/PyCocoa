
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Types L{FrozenSet} and L{Set}, wrapping ObjC C{NS[Mutable]Set}.
'''
from pycocoa.bases import _Type0
from pycocoa.internals import _Dmain_, property_RO
from pycocoa.lazily import _ALL_LAZY, _Types
from pycocoa.nstypes import _NSImms, NSMutableSet, _NSMtbs, \
                             NSSet, nsSet2set  # ns2py
from pycocoa.pytypes import frozenset2NS, set2NS
from pycocoa.runtime import isImmutable, isinstanceOf, isMutable

__all__ = _ALL_LAZY.sets
__version__ = '25.03.13'

if True:  # MCCABE 71

    class FrozenSet(frozenset, _Type0):  # frozenset, first to maintain frozenset behavior
        '''Python C{frozenset} Type, wrapping an immutable ObjC C{NSSet}.
        '''
        def __new__(cls, ns_frozenset=()):
            '''New L{FrozenSet} from a C{frozenset}, C{list}, C{set},
               C{tuple}, L{FrozenSet} or C{NSSet}.
            '''
            if isinstance(ns_frozenset, FrozenSet):
                return ns_frozenset
            elif isinstance(ns_frozenset, frozenset):
                py = ns_frozenset
                ns = frozenset2NS(py)
            elif isinstanceOf(ns_frozenset, list, tuple, set):
                py = frozenset(ns_frozenset)
                ns = frozenset2NS(py)
            elif isImmutable(ns_frozenset, *_NSImms.Sets, raiser='ns_frozenset'):
                ns = ns_frozenset
                py = nsSet2set(ns)

            self = super(FrozenSet, cls).__new__(cls, py)
            self._NS = ns  # _RO
            return self

        def copy(self):
            '''Make a copy of this frozen set.

               @return: The copy (L{FrozenSet}).
            '''
            return type(self)(self)

        @property_RO
        def NS(self):
            '''Get the ObjC instance (C{NSSet}).
            '''
            return self._NS

    class Set(set, _Type0):  # set, first to maintain set behavior
        '''Python C{set} Type, wrapping an ObjC C{NSMutableSet}.
        '''
        def __new__(cls, ns_set=[]):
            '''New L{Set} from a C{frozenset}, C{list}, C{set}, C{tuple},
               L{Set} or C{NSMutableSet}.
            '''
            if isinstance(ns_set, Set):
                py = ns_set
#               ns = ns_set.NS
            elif isinstance(ns_set, set):
                py = ns_set
#               ns = set2NS(py)
            elif isinstanceOf(ns_set, frozenset, list, tuple):
                py = set(ns_set)
#               ns = set2NS(py)
            elif isMutable(ns_set, *_NSMtbs.Sets, name='ns_set'):
                py = nsSet2set(ns_set)
#               ns = ns_set

            self = super(Set, cls).__new__(cls, py)
#           self._NS = ns  # _RO
            return self

        def copy(self):
            '''Make a copy of this set.

               @return: The copy (L{Set}).
            '''
            return type(self)(self)

        @property_RO
        def NS(self):
            '''Get the ObjC instance (C{NSMutableSet}).
            '''
            return set2NS(self)

# else:  # XXX far too much duplication

#   class FrozenSet(_Type0):  # PYCHOK expected
#       '''Python C{FrozenSet} Type, wrapping an immutable ObjC C{NSSet}.
#       '''
#       _pyset = frozenset()  # or set(), empty to start
#
#       def __init__(self, ns_set=()):
#           '''New L{FrozenSet} from a C{frozenset}, C{list}, C{set},
#              C{tuple}, L{FrozenSet}, L{Set} or C{NSSet}.
#           '''
#           if isinstance(ns_set, frozenset):
#               self._pyset = ns_set
#           elif isinstanceOf(ns_set, list, tuple, set):
#               self._pyset = frozenset(ns_set)
#           elif isinstance(ns_set, FrozenSet):
#               self._pyset = ns_set._pyset
#           elif isinstance(ns_set, Set):
#               self._pyset = frozenset(ns_set._pyset)
#           elif isImmutable(ns_set, *_NSImms.Sets, raiser=self.typename):
#               self._pyset = nsSet2set(ns_set)
#
#       def __contains__(self, elem):
#           if isinstance(elem, ObjCInstance):
#               elem = ns2py(elem)
#           return self._pyset.__contains__(elem)
#
#       def __and__(self, elem):
#           return self._pyset.__and__(elem)
#
#       def __cmp__(self, elem):
#           return self._pyset.__cmp__(elem)
#
#       def __eq__(self, elem):
#           return self._pyset.__eq__(elem)
#
#       def __ge__(self, elem):
#           return self._pyset.__ge__(elem)
#
#       def __gt__(self, elem):
#           return self._pyset.__gt__(elem)
#
#       def __iter__(self):
#           return self._pyset.__iter__()
#
#       def __le_(self, elem):
#           return self._pyset.__le__(elem)
#
#       def __len__(self):
#           return len(self._pyset)
#
#       def __lt__(self, elem):
#           return self._pyset.__lt__(elem)
#
#       def __ne__(self, elem):
#           return self._pyset.__ne__(elem)
#
#       def __or_(self, elem):
#           return self._pyset.__or__(elem)
#
#       def __rand__(self, elem):
#           return self._pyset.__rand__(elem)
#
#       def __ror__(self, elem):
#           return self._pyset.__ror__(elem)
#
#       def __rsub__(self, elem):
#           return self._pyset.__rsub__(elem)
#
#       def __rxor__(self, elem):
#           return self._pyset.__rxor__(elem)
#
#       def __sizeof__(self, elem):  # PYCHOK expected
#           return self._pyset.__sizeof__(elem)
#
#       def __sub__(self, elem):
#           return self._pyset.__sub__(elem)
#
#       def __xor__(self, elem):
#           return self._pyset.__xor__(elem)
#
#       def copy(self):
#           '''Make a copy of this frozen/set.
#
#              @return: The copy (L{FrozenSet} or L{Set}).
#           '''
#           return type(self)(self._pyset)
#
#       def difference(self, *others):
#           '''Like C{frozen/set.difference}.
#
#              @return: New instance (L{FrozenSet} or L{Set}).
#           '''
#           return type(self)(self._pyset.difference(*others))
#
#       def intersection(self, *others):  # &
#           '''Like C{frozen/set.intersection}.
#
#              @return: New instance (L{FrozenSet} or L{Set}).
#           '''
#           return type(self)(self._pyset.intersection(*others))
#
#       def isdisjoint(self, other):
#           '''Like C{frozen/set.isdisjoint}.
#           '''
#           return self._pyset.isdisjoint(other)
#
#       def issubset(self, other):  # <= / <
#           '''Like C{frozen/set.issubset}.
#           '''
#           return self._pyset.issubset(other)
#
#       def issuperset(self, other):  # >= / >
#           '''Like C{frozen/set.issuperset}.
#           '''
#           return self._pyset.issuperset(other)
#
#       @property_RO
#       def NS(self):
#           '''Get the ObjC instance (C{NSSet}).
#           '''
#           if self._NS is None:
#               self._NS = frozenset2NS(self._pyset)
#           return self._NS
#
#       def symmetric_difference(self, other):  # ^
#           '''Like C{frozen/set.symmetric_difference}.
#
#              @return: New instance (L{FrozenSet} or L{Set}).
#           '''
#           return type(self)(self._pyset.symmetric_difference(other))
#
#       def union(self, *others):  # |
#           '''Like C{frozen/set.union}.
#
#              @return: New instance (L{FrozenSet} or L{Set}).
#           '''
#           return type(self)(self._pyset.union(*others))
#
#   class Set(FrozenSet):  # PYCHOK expected
#       '''Python C{Set} Type, wrapping an ObjC C{NSMutableSet}.
#       '''
#
#       def __init__(self, ns_set=[]):
#           '''New L{Set} from a C{frozenset}, C{list}, C{set}, C{tuple},
#              L{FrozenSet}, L{Set} or C{NSMutableSet}.
#           '''
#           if isinstance(ns_set, set):
#               self._pyset = ns_set
#           elif isinstanceOf(ns_set, frozenset, list, tuple):
#               self._pyset = set(ns_set)
#           elif isinstanceOf(ns_set, Set, FrozenSet):
#               self._pyset = set(ns_set._pyset)
#           elif isMutable(ns_set, *_NSMtbs.Sets, raiser=Set.__name__):
#               self._pyset = nsSet2set(ns_set)
#
#       def __iand__(self, elem):
#           return self._pyset.__iand__(elem)
#
#       def __ior__(self, elem):
#           return self._pyset.__ior__(elem)
#
#       def __isub__(self, elem):
#           return self._pyset.__isub__(elem)
#
#       def __ixor__(self, elem):
#           return self._pyset.__ixor__(elem)
#
#       def add(self, elem):
#           '''Like C{set.add}.
#           '''
#           self._pyset.add(elem)
#
#       def clear(self):
#           '''Like C{set.clear}.
#           '''
#           self._pyset.clear()
#
#       def difference_update(self, *others):  # -=
#           '''Like C{set.difference_update}.
#           '''
#           self._pyset.difference_update(*others)
#
#       def discard(self, elems):
#           '''Like C{set.discard}.
#           '''
#           self._pyset.discard(elems)
#
#       def intersection_update(self, *others):  # &=
#           '''Like C{set.intersection_update}.
#           '''
#           self._pyset.intersection_update(*others)
#
#       @property_RO
#       def NS(self):
#           '''Get the ObjC instance (C{NSMutableSet}).
#           '''
#           return set2NS(self._pyset)
#
#       def pop(self):
#           '''Like C{set.pop}.
#           '''
#           return self._pyset.pop(self)
#
#       def remove(self, elems):
#           '''Like C{set.remove}.
#           '''
#           self._pyset.remove(elems)
#
#       def symmetric_difference_update(self, other):  # ^=
#           '''Like C{set.symmetric_difference_update}.
#           '''
#           self._pyset.symmetric_difference_update(other)
#
#       def update(self, *others):  # |=
#           '''Like C{set.update}.
#           '''
#           self._pyset.update(*others)


NSSet._Type        = _Types.FrozenSet = FrozenSet
NSMutableSet._Type = _Types.Set       = Set

if __name__ == _Dmain_:

    from pycocoa.utils import _all_listing

    _all_listing(__all__, locals())

# % python3 -m pycocoa.sets
#
# pycocoa.sets.__all__ = tuple(
#  pycocoa.sets.FrozenSet is <class .FrozenSet>,
#  pycocoa.sets.Set is <class .Set>,
# )[2]
# pycocoa.sets.version 25.3.13, .isLazy 1, Python 3.13.2 64bit arm64, macOS 14.7.3

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
