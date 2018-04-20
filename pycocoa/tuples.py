
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
from oclibs  import libCF
from octypes import NSNotFound, NSRange_t
from nstypes import ns2Type, NSArray, nsIter2, NSMutableArray, py2NS, \
                    _Types
from runtime import isImmutable
from utils   import instanceof, _Ints

__all__ = ('Tuple',)
__version__ = '18.04.10'


def _at(inst, index):
    if not isinstance(index, _Ints):
        raise TypeError('%s not an %s: %r' (inst, 'index', index))
    i, n = index, len(inst)
    if i < 0:
        i += n
    if 0 <= i < n:
        return i
    raise IndexError('%s out of range: %r' % (inst, index))


class Tuple(_Type0):  # note, List subclasses Tuple
    '''Python Type equivalent of an immutable ObjC NSArray.
    '''
    _type = tuple

#   def __add__(self, *unused):
#       raise NotImplementedError('%s.%s' % (self, '__add__'))

#   def __iadd__(self, *unused):
#       raise NotImplementedError('%s.%s' % (self, '__iadd__'))

#   def __imul__(self, *unused):
#       raise NotImplementedError('%s.%s' % (self, '__iadd__'))

#   def __mul__(self, *unused):
#       raise NotImplementedError('%s.%s' % (self, '__add__'))

#   def __rmul__(self, *unused):
#       raise NotImplementedError('%s.%s' % (self, '__iadd__'))

    def __init__(self, ns_tuple=()):
        if isinstance(ns_tuple, tuple):
            self.NS = py2NS(ns_tuple)
        elif isinstance(ns_tuple, Tuple):
            self.NS = ns_tuple.NS
        elif isinstance(ns_tuple, _Types.List):
            self.NS = ns_tuple.NS.copy()
        elif isImmutable(ns_tuple, NSMutableArray, NSArray, name='ns_tuple'):
            self.NS = ns_tuple

    def __contains__(self, value):
        return self.NS.containsObject_(py2NS(value))

    def __eq__(self, other):
        instanceof(other, _Types.List, Tuple, list, tuple, name='other')
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
        for value, _ in nsIter2(self.NS):
            yield value
#       for i in range(len(self)):
#           yield ns2Type(self.NS.objectAtIndex_(i))

    def __len__(self):
        # can't use self.NS.count()  <http://developer.apple.com/
        # documentation/foundation/nsarray/1409982-count>
        return libCF.CFArrayGetCount(self.NS)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __reversed__(self):  # PYCHOK Python 3+
        for value, _ in nsIter2(self.NS, reverse=True):
            yield value
#       i = len(self)
#       while i > 0:
#           i -= 1
#           yield ns2Type(self.NS.objectAtIndex_(i))

    def copy(self, *ranged):
        '''Make a shallow copy, optionally just a range of items.
        '''
        return self.__class__(self._NS_copy(False, *ranged))

    def count(self, value, identical=False):
        '''Like list./tuple.count(), except I{identical} option.
        '''
        v = py2NS(value)
        n = len(self)
        c = i = 0
        while i < n:
            if identical:
                i = self.NS.indexOfObjectIdenticalTo_inRange_(v, NSRange_t(i, n - i))
            else:
                i = self.NS.indexOfObject_inRange_(v, NSRange_t(i, n - i))
            if i == NSNotFound:
                break
            i += 1
            c += 1
        return c

    def index(self, value, identical=False):
        '''Like list./tuple.index(), except an I{identical} option.
        '''
        if identical:
            i = self.NS.indexOfObjectIdenticalTo_(py2NS(value))
        else:
            i = self.NS.indexOfObject_(py2NS(value))
        if i == NSNotFound:
            raise ValueError('%s no such value: %r' % (self, value))
        return i

    def _NS_copy(self, mutable, *ranged):
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


NSArray._Type = _Types.Tuple = Tuple

if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)
