
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Type L{Tuple}, wrapping (immutable) ObjC C{NSArray}.
'''
from pycocoa.bases import _Type0
from pycocoa.internals import _Dmain_, _DOT_, _fmt, \
                             _fmt_invalid, _Ints, _instr
from pycocoa.lazily import _ALL_LAZY, _Types
from pycocoa.octypes import NSNotFound, NSRange_t
from pycocoa.oslibs import _libCF
from pycocoa.nstypes import NSArray, _NSImms, nsIter2, \
                            NSMutableArray, ns2Type
from pycocoa.pytypes import py2NS, tuple2NS
from pycocoa.runtime import isImmutable, isinstanceOf
# from pycocoa.utils import isinstanceOf  # from .runtime

__all__ = _ALL_LAZY.tuples
__version__ = '25.03.13'


def _at(inst, index):
    if isinstance(index, _Ints):
        n, i = len(inst), index
        if i < 0:
            i += n
        if 0 <= i < n:
            return i

        n = _fmt('in range(%s)', n)
        E =  IndexError
    else:
        n = ' or '.join(i.__name__ for i in _Ints)
        E = TypeError
    raise E(_fmt_invalid(n, index=repr(index)))


class Tuple(_Type0):  # note, List subclasses Tuple
    '''Python C{tuple} Type, wrapping an immutable ObjC C{NSArray}.
    '''
    _type = tuple

    def __init__(self, ns_tuple=()):
        '''New L{Tuple} from a C{tuple}, L{Tuple}, C{list}, L{List}
           or C{NS[Mutable]Array}.
        '''
        if _Types.List is None:  # circular import
            import pycocoa.lists as _  # PYCHOK _
            assert _Types.List is not None, '_Types.List None'

        if isinstanceOf(ns_tuple, list, tuple):
            ns = tuple2NS(ns_tuple)
        elif isinstance(ns_tuple, _Types.List):  # class List(Tuple)
            ns = ns_tuple.NS.copy()  # immutable
        elif isinstance(ns_tuple, Tuple):
            ns = ns_tuple.NS
        elif isImmutable(ns_tuple, *_NSImms.Arrays, raiser='ns_tuple'):
            ns = ns_tuple
        self.NS = ns

    def __contains__(self, value):
        return self.NS.containsObject_(py2NS(value))

    def __delitem__(self, index):
        raise self._TypeError(self.__delitem__, index)

    def __eq__(self, other):
        # assert issubclassOf(_Types.List, _Types.Tuple)
        isinstanceOf(other, list, tuple, Tuple, raiser='other')
        if len(self) == len(other):
            for s, o in zip(self, other):
                if o != s:
                    break
            else:
                return True
        return False

    def __getitem__(self, index):
        I_ = self.NS.objectAtIndex_
        if isinstance(index, slice):
            t = map(I_, self._sliced(index))
            t = map(ns2Type, t)
            t = type(self)(self._type(t))
        else:
            t = ns2Type(I_(_at(self, index)))
        return t

    def __iter__(self):
        '''Yield the items in forward order.
        '''
        for value, _ in nsIter2(self.NS):
            yield value
#       I_ = self.NS.objectAtIndex_
#       for i in range(len(self)):
#           yield ns2Type(I_(i))

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
        for v, _ in nsIter2(self.NS, reverse=True):
            yield v
#       i, I_ = len(self), self.NS.objectAtIndex_
#       while i > 0:
#           i -= 1
#           yield ns2Type(I_(i))

    def __setitem__(self, index, value):
        raise self._TypeError(self.__setitem__, index, value)

    def append(self, value):
        raise self._TypeError(self.append, value)

    def clear(self):
        raise self._TypeError(self.clear)

    def copy(self, *ranged):
        '''Make a shallow copy of this tuple.

          @param ranged: Optional index range.

          @return: The copy (L{Tuple}).
        '''
        t = self._NS_copy(False, *ranged)
        return type(self)(self._type(t))

    def count(self, value, identical=False):
        '''Count the number of occurances of an item, like C{tuple./list.count}.

           @keyword idential: Use ObjC C{idential} as comparison (bool).
        '''
        ns = self.NS
        I_ = ns.indexOfObjectIdenticalTo_inRange_ if identical else \
             ns.indexOfObject_inRange_
        c = i = 0
        n = len(self)
        v = py2NS(value)
        while i < n:
            i = I_(v, NSRange_t(i, n))
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
        ns = self.NS
        I_ = ns.indexOfObjectIdenticalTo_ if identical else \
             ns.indexOfObject_
        i  = I_(py2NS(value))
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
        ns = self.NS
        if ranged:
            I_ = ns.objectAtIndex_
            ns = NSMutableArray.array()
            A_ = ns.addObject_
            for i in self._sliced(slice(*ranged)):
                A_(I_(i))
            if not mutable:
                ns = NSArray.alloc().initWithArray_(ns)
        elif mutable:
            ns = ns.mutableCopy()
        else:
            ns = ns.copy()
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
# pycocoa.tuples.version 25.3.13, .isLazy 1, Python 3.13.2 64bit arm64, macOS 14.7.3

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
