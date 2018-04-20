
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

from nstypes import NSMutableArray, py2NS, _Types
from runtime import isInstanceOf
from tuples  import _at, Tuple
from utils   import missing

try:
    from itertools import zip_longest
except ImportError:  # Python 2-
    from itertools import izip_longest as zip_longest

__all__ = ('List',)
__version__ = '18.04.09'


class List(Tuple):
    '''Python Type equivalent of of an ObjC NSMutableArray.
    '''
    _type = list

    def __init__(self, ns_list=[]):
        if isinstance(ns_list, list):
            self.NS = py2NS(ns_list)
        elif isinstance(ns_list, (List, Tuple)):
            self.NS = ns_list.NS.mutableCopy()  # PYCHOK safe
        elif isInstanceOf(ns_list, NSMutableArray, name='ns_list'):
            self.NS = ns_list

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            indices = range(*index.indices(len(self)))
            for i, val in zip_longest(indices, value, fillvalue=missing):
                if missing in (i, val):  # XXX only if val is missing?
                    raise ValueError('%s len() mismatch %r vs %r' %
                                     (self, index, value))
                self.NS.replaceObjectAtIndex_withObject_(i, py2NS(val))
        else:
            self.NS.replaceObjectAtIndex_withObject_(_at(self, index), py2NS(value))

    def __delitem__(self, index):
        if isinstance(index, slice):
            indices = range(*index.indices(len(self)))
            for i in sorted(indices, reverse=True):
                self.NS.removeObjectAtIndex_(i)
        else:
            self.NS.removeObjectAtIndex_(_at(self, index))

    def append(self, value):
        '''Like list.append().
        '''
        self.NS.addObject_(py2NS(value))

    def clear(self):
        '''Like list.clear().
        '''
        self.NS.removeAllObjects()

    def copy(self, *ranged):
        '''Make a shallow copy, optionally just a range of items.
        '''
        return self.__class__(self._NS_copy(True, *ranged))

    def extend(self, values):
        '''Like list.extend().
        '''
        for v in values:
            self.NS.addObject_(py2NS(v))

    def insert(self, index, value):
        '''Like list.insert().
        '''
        self.NS.insertObject_atIndex_(py2NS(value), _at(self, index))

    def pop(self, index=-1):
        '''Like list.pop().
        '''
        i = _at(self, index)
        v = self[i]
        del self[i]  # __delitem__
        return v

    def remove(self, value, identical=False):
        '''Like list.remove(), except an I{identical} option.
        '''
        i = self.index(value, identical=identical)
        del self[i]  # __delitem__

    def reverse(self):
        '''Like list.reverse(), reverse list in-place.
        '''
        self.NS.setArray_(self.NS.reverseObjectEnumerator().allObjects())
#       i, n = 0, len(self)-1
#       while i < n:
#           ns = self.NS.objectAtIndex_(i)
#           self.NS.replaceObjectAtIndex_withObject_(i, self.NS.objectAtIndex_(n))
#           self.NS.replaceObjectAtIndex_withObject_(n, ns)
#           i += 1
#           n -= 1

#   def sort(self, **unused):
#       '''Like list.sort(cmp=None, key=None, reverse=False), in-place.
#       '''
#       raise NotImplementedError('%s.%s' % (self, 'sort'))


NSMutableArray._Type = _Types.List = List

if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)