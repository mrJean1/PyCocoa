
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Type L{List}, wrapping ObjC C{NSMutableArray}.
'''
from pycocoa.internals import _Dmain_, _fmt, missing
from pycocoa.lazily import _ALL_LAZY, _Types
from pycocoa.nstypes import NSMutableArray, _NSMtbs
from pycocoa.pytypes import list2NS, py2NS
from pycocoa.runtime import isMutable, isinstanceOf
from pycocoa.tuples import _at, Tuple
# from pycocoa.utils import isinstanceOf  # from .runtime

try:
    from itertools import zip_longest
except ImportError:  # Python 2-
    from itertools import izip_longest as zip_longest

__all__ = _ALL_LAZY.lists
__version__ = '25.03.13'


class List(Tuple):
    '''Python C{list} Type, wrapping an ObjC C{NSMutableArray}.
    '''
    _type = list

    def __init__(self, ns_list=[]):
        '''New L{List} from a C{list}, L{List}, L{Tuple} or C{NSMutableArray}.
        '''
        if isinstanceOf(ns_list, list, tuple):
            self.NS = list2NS(ns_list)
        elif isinstanceOf(ns_list, List, Tuple):
            self.NS = ns_list.NS.mutableCopy()  # PYCHOK safe
        elif isMutable(ns_list, *_NSMtbs.Arrays, raiser='ns_list'):
            self.NS = ns_list

    def __setitem__(self, index, value):
        R_ = self.NS.replaceObjectAtIndex_withObject_
        if isinstance(index, slice):
            r = self._sliced(index)
            for i, v in zip_longest(r, value, fillvalue=missing):
                if missing in (i, v):  # XXX only if val is missing?
                    t = _fmt('%s len() %r vs %r', self, index, value)
                    raise ValueError(t)
                R_(i, py2NS(v))
        else:
            R_(_at(self, index), py2NS(value))

    def __delitem__(self, index):
        R_ = self.NS.removeObjectAtIndex_
        if isinstance(index, slice):
            r = self._sliced(index)
            for i in sorted(r, reverse=True):
                R_(i)
        else:
            R_(_at(self, index))

    def append(self, value):
        '''Add an item to this list, like C{list.append}.
        '''
        self.NS.addObject_(py2NS(value))

    def clear(self):
        '''Remove all items from this list, like C{list.clear}.
        '''
        self.NS.removeAllObjects()

    def copy(self, *ranged):
        '''Make a shallow copy of this list.

          @param ranged: Optional index range.

          @return: The copy (L{List}).
        '''
        return type(self)(self._NS_copy(True, *ranged))

    def extend(self, values):
        '''Add one or more items to this list, like C{list.extend}.
        '''
        A_ = self.NS.addObject_
        for v in values:
            A_(py2NS(v))

    def insert(self, index, value):
        '''Insert an item into this list, like C{list.insert}.
        '''
        self.NS.insertObject_atIndex_(py2NS(value), _at(self, index))

    def pop(self, index=-1):
        '''Remove an item from this list, like C{list.pop}.
        '''
        i = _at(self, index)
        v = self[i]
        del self[i]  # __delitem__
        return v

    def remove(self, value, identical=False):
        '''Remove an item from this list, like C{list.remove}.

           @keyword idential: Use ObjC C{idential} as comparison (bool).
        '''
        i = self.index(value, identical=identical)
        del self[i]  # __delitem__

    def reverse(self):
        '''Reverse this list in-place, like C{list.reverse}.
        '''
        ns = self.NS
        ns.setArray_(ns.reverseObjectEnumerator().allObjects())
#       I_ = ns.objectAtIndex_
#       R_ = ns.replaceObjectAtIndex_withObject_
#       i, n = 0, (len(self) - 1)
#       while i < n:
#           ns  = I_(i)
#           R_(i, I_(n))
#           R_(n, ns)
#           i += 1
#           n -= 1

#   def sort(self, **unused):
#       '''Sort this list in-place, like C{list.sort(cmp=None, key=None, reverse=False).
#       '''
#       raise NotImplementedError('%s.%s' % (self, 'sort'))


NSMutableArray._Type = _Types.List = List

if __name__ == _Dmain_:

    from pycocoa.utils import _all_listing

    _all_listing(__all__, locals())

# % python3 -m pycocoa.lists
#
# pycocoa.lists.__all__ = tuple(
#  pycocoa.lists.List is <class .List>,
# )[1]
# pycocoa.lists.version 25.3.13, .isLazy 1, Python 3.13.2 64bit arm64, macOS 14.7.3

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
