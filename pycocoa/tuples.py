
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Type L{Tuple}, wrapping (immutable) ObjC C{NSArray}.
'''
from pycocoa.bases import _Type0
from pycocoa.internals import _Dmain_, _DOT_, _fmt, _fmt_frozen, \
                             _fmt_invalid, _Ints, _instr
from pycocoa.lazily import _ALL_LAZY, _Types
from pycocoa.octypes import NSNotFound, NSRange_t
from pycocoa.oslibs import _libCF
from pycocoa.nstypes import NSArray, _NSImms, nsIter2, \
                            NSMutableArray, ns2Type
from pycocoa.pytypes import py2NS, tuple2NS
from pycocoa.runtime import isImmutable, isinstanceOf

__all__ = _ALL_LAZY.tuples
__version__ = '25.02.25'


def _at(inst, index):
    if not isinstance(index, _Ints):
        i = ' or '.join(_.__name__ for _ in _Ints)
        raise TypeError(_fmt_invalid(i, index=repr(index)))
    n, i = len(inst), index
    if i < 0:
        i += n
    if 0 <= i < n:
        return i
    r = _fmt('in range(%s)', n)
    raise IndexError(_fmt_invalid(r, index=index))


class Tuple(_Type0):  # note, List subclasses Tuple
    '''Python C{tuple} Type, wrapping an immutable ObjC C{NSArray}.
    '''
    _type = tuple

#   def __add__(self, *unused):
#       raise NotImplementedError(_DOT_(self, _Dadd_))

#   def __iadd__(self, *unused):
#       raise NotImplementedError(_DOT_(self, _Diadd_))

#   def __imul__(self, *unused):
#       raise NotImplementedError(_DOT_(self, _Dimul_))

#   def __mul__(self, *unused):
#       raise NotImplementedError(_DOT_(self, _Dmul_))

#   def __rmul__(self, *unused):
#       raise NotImplementedError(_DOT_(self, _Drmul_))

    def __init__(self, ns_tuple=()):
        '''New L{Tuple} from a C{tupe}, L{Tuple}, L{List} or C{NS[Mutable]Array}.
        '''
        if isinstance(ns_tuple, tuple):
            self.NS = tuple2NS(ns_tuple)
        elif isinstance(ns_tuple, Tuple):
            self.NS = ns_tuple.NS
        elif isinstance(ns_tuple, _Types.List):
            self.NS = ns_tuple.NS.copy()  # immutableCopy?
        elif isImmutable(ns_tuple, *_NSImms.Arrays, raiser='ns_tuple'):
            self.NS = ns_tuple

    def __contains__(self, value):
        return self.NS.containsObject_(py2NS(value))

    def __delitem__(self, key):
        raise TypeError(_fmt('%s %s[%r]', 'del', self, key))

    def __eq__(self, other):
        isinstanceOf(other, _Types.List, Tuple, list, tuple, raiser='other')
        if len(self) == len(other):
            for s, o in zip(self, other):
                if o != s:
                    break
            else:
                return True
        return False

    def __getitem__(self, index):
        if isinstance(index, slice):
            indices = range(*index.indices(len(self)))
            return self._type(ns2Type(self.NS.objectAtIndex_(i) for i in indices))
        else:
            return ns2Type(self.NS.objectAtIndex_(_at(self, index)))

    def __iter__(self):
        '''Yield the items in forward order.
        '''
        for value, _ in nsIter2(self.NS):
            yield value
#       for i in range(len(self)):
#           yield ns2Type(self.NS.objectAtIndex_(i))

    def __len__(self):
        '''Return the number of items.
        '''
        # can't use self.NS.count() <https://Developer.Apple.com//
        # documentation/foundation/nsarray/1409982-count>
        return _libCF.CFArrayGetCount(self.NS)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __reversed__(self):  # PYCHOK Python 3+
        '''Yield the items in reverse order.
        '''
        for value, _ in nsIter2(self.NS, reverse=True):
            yield value
#       i = len(self)
#       while i > 0:
#           i -= 1
#           yield ns2Type(self.NS.objectAtIndex_(i))

    def __setitem__(self, index, value):
        raise TypeError(_fmt_frozen(self, index, value))

    def append(self, value):
        raise self._TypeError(self.append, value)

    def clear(self):
        raise self._TypeError(self.clear)

    def copy(self, *ranged):
        '''Make a shallow copy of this tuple.

          @param ranged: Optional index range.

          @return: The copy (L{Tuple}).
        '''
        return type(self)(self._NS_copy(False, *ranged))

    def count(self, value, identical=False):
        '''Count the number of occurances of an item, like C{tuple./list.count}.

           @keyword idential: Use ObjC C{idential} as comparison (bool).
        '''
        v = py2NS(value)
        n = len(self)
        c = i = 0
        indx_ = self.NS.indexOfObject_inRange_ if not identical else \
                self.NS.indexOfObjectIdenticalTo_inRange_
        while i < n:
            i = indx_(v, NSRange_t(i, n - i))
            if i == NSNotFound:
                break
            i += 1
            c += 1
        return c

    def extend(self, values):
        raise self._TypeError(self.extend, values)

    def index(self, value, identical=False):
        '''Find an item, like C{tuple./list.index}.

           @keyword idential: Use ObjC C{idential} as comparison (bool).
        '''
        v = py2NS(value)
        i = self.NS.indexOfObject_(v) if not identical else \
            self.NS.indexOfObjectIdenticalTo_(v)
        if i == NSNotFound:
            t = self._TypeError(self.index, value)
            raise ValueError(str(t))
        return i

    def insert(self, index, value):
        raise self._TypeError(self.insert, index, value)

    def pop(self, index=-1):
        raise self._TypeError(self.pop, index)

    def _NS_copy(self, mutable, *ranged):
        '''(INTERNAL) Copy into an ObjC C{NS[Mutable]Array}.
        '''
        if ranged:
            ns = NSMutableArray.array()
            for i in range(*slice(*ranged).indices(len(self))):
                ns.addObject_(self.NS.objectAtIndex_(i))
            if not mutable:
                ns = NSArray.alloc().initWithArray_(ns)
        elif mutable:
            ns = self.NS.mutableCopy()
        else:
            ns = self.NS.copy()
        return ns

    def _TypeError(self, where, *args):
        m = _DOT_(self, where.__name__)
        return TypeError(_instr(m, *map(repr, args)))


NSArray._Type = _Types.Tuple = Tuple

if __name__ == _Dmain_:

    from pycocoa.utils import _all_listing

    _all_listing(__all__, locals())

# % python3 -m pycocoa.tuples
#
# pycocoa.tuples.__all__ = tuple(
#  pycocoa.tuples.Tuple is <class .Tuple>,
# )[1]
# pycocoa.tuples.version 25.2.25, .isLazy 1, Python 3.13.2 64bit arm64, macOS 14.7.3

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
