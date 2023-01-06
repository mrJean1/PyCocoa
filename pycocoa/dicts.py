
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Types L{FrozenDict} and L{Dict}, wrapping ObjC C{NS[Mutable]Dictionary}.
'''
# all imports listed explicitly to help PyChecker
from pycocoa.bases   import _Type0
from pycocoa.lazily  import _ALL_LAZY, _DOT_
from pycocoa.nstypes import isNone, NSDictionary, nsIter2, \
                            NSMutableDictionary, ns2Type
from pycocoa.pytypes import py2NS, type2NS
from pycocoa.runtime import isImmutable, isObjCInstanceOf, \
                            ObjCClass, ObjCInstance
from pycocoa.utils   import isinstanceOf, missing, _Types

__all__ = _ALL_LAZY.dicts
__version__ = '21.11.04'


def _dict_cmp(dict1, dict2):
    # compare 2 dicts
    for key in dict1.keys():
        val = dict2.get(key, missing)
        if val is missing or val != dict1[key]:
            return False
    return True


def _dict_kwds(args, kwds, name):
    if not args:
        return kwds, {}
    try:
        if len(args) != 1:
            raise ValueError
        arg0 = args[0]
        if not isinstance(arg0, (Dict, FrozenDict,
                                 ObjCClass, ObjCInstance)):
            arg0 = dict(arg0)  # tuple, list to dict
    except TypeError:
        raise TypeError('%s() invalid: %r' % (name, args))
    except ValueError:
        raise ValueError('%s() invalid: %r' % (name, args))
    return arg0, kwds


class FrozenDict(_Type0):
    '''Python immutable C{dict} Type, wrapping an (immutable) ObjC C{NSDictionary}.
    '''
    def __init__(self, *ns_dict, **kwds):
        '''New immutable L{FrozenDict}, like C{dict.__init__}.
        '''
        ns_dict, kwds = _dict_kwds(ns_dict, kwds, FrozenDict.__name__)
        if isinstance(ns_dict, dict):
            if kwds:
                ns_dict = ns_dict.copy()
                ns_dict.update(kwds)
                kwds = {}
            self.NS = self._NS_Dictionary(py2NS(ns_dict))
        elif isinstance(ns_dict, FrozenDict):
            self.NS = ns_dict.NS
        elif isinstance(ns_dict, Dict):
            self.NS = ns_dict.NS._NS_copy(False)
        elif isImmutable(ns_dict, NSMutableDictionary,
                                  NSDictionary, name=FrozenDict.__name__):
            self.NS = ns_dict

        if kwds:
            ns = self._NS_copy(True)
            ns.update(kwds)
            self.NS = ns._NS_copy(False)

    def __contains__(self, key):
        _, _, value = self._NS_get3(key)
        return value is not missing

    def __eq__(self, other):
        if isinstance(other, (FrozenDict, Dict)):
            return True if self.NS.isEqualToDictionary_(other.NS) else False
        elif isinstanceOf(other, dict, name='other'):
            return len(self) == len(other) and _dict_cmp(self, other) \
                                           and _dict_cmp(other, self)

    def __delitem__(self, key):
        raise TypeError('%s %s[%r]' % ('del', self, key))

    def __getitem__(self, key):
        k, _, value = self._NS_get3(key)
        if value is missing:
            self._NS_KeyError(key, k)
        return value

    def __len__(self):
        '''Return the length, like C{dict.__len__}.
        '''
        # <https://Developer.Apple.com/documentation/foundation/
        #          nsdictionary/1409628-count>
        return self.NS.count()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __setitem__(self, key, value):
        raise TypeError('%s[%r] = %r' % (self, key, value))

    def clear(self):
        raise TypeError('%s()' % (_DOT_(self, 'clear'),))

    def copy(self):
        '''Make a shallow copy.

           @return: The copy (L{FrozenDict}).
        '''
        return self.__class__(self._NS_copy(False))

#   def fromkeys(self):
#       raise NotImplementedError('%s.%s' % (self, 'fromkeys'))

    def get(self, key, default=None):
        '''Return the value for the given key, like C{dict.get}.
        '''
        _, _, value = self._NS_get3(key)
        return default if value is missing else value

    def items(self):
        '''Yield the key, value pairs, like C{dict.items}.
        '''
        for key, k in nsIter2(self.NS.allKeys()):
            v = self.NS.objectForKey_(k)
            if isNone(v):  # missing key?
                self._NS_KeyError(key, k)
            yield key, ns2Type(v)

    def keys(self):
        '''Yield the keys, like C{dict.keys}.
        '''
        for key, _ in nsIter2(self.NS.allKeys()):
            yield key
    __iter__ = keys

    def pop(self, key, **unused):
        raise TypeError('%s(%r)' % (_DOT_(self, self.pop.__name__), key))

    def values(self):
        '''Yield the values, like C{dict.values}.
        '''
        for value, _ in nsIter2(self.NS.allValues()):
            yield value

    def _NS_copy(self, mutable):
        if mutable:
            ns = self.NS.mutableCopy()
        else:
            ns = self._NS_Dictionary(self.NS)
        return ns

    def _NS_Dictionary(self, ns_dict):
        return NSDictionary.alloc().initWithDictionary_(ns_dict)

    def _NS_get3(self, key):
        k = type2NS(key)
        v = self.NS.objectForKey_(k)  # nil for missing key
        return k, v, (missing if isNone(v) else ns2Type(v))

    def _NS_KeyError(self, key, k):
        # XXX KeyError(key) prints repr(key), adding "..."
        raise KeyError('%s no such key: %s (%r)' % (self, key, k))


class Dict(FrozenDict):
    '''Python C{dict} Type, wrapping an ObjC C{NSMutableDictionary}.
    '''
    __iter__ = FrozenDict.keys

    def __init__(self, *ns_dict, **kwds):
        '''New mutable L{Dict}, like C{dict.__init__}.
        '''
        ns_dict, kwds = _dict_kwds(ns_dict, kwds, Dict.__name__)
        if isinstance(ns_dict, dict):
            self.NS = NSMutableDictionary.alloc().init()
            self.update(ns_dict)
        elif isinstance(ns_dict, Dict):
            self.NS = ns_dict.NS
        elif isinstance(ns_dict, FrozenDict):
            self.NS = ns_dict.NS.mutableCopy()  # XXX flat copy only?
        elif isObjCInstanceOf(ns_dict, NSMutableDictionary, name=Dict.__name__):
            self.NS = ns_dict

        if kwds:
            self.update(kwds)

    def __delitem__(self, key):
        '''Remove an item, like C{dict.__delitem__}.

           @raise KeyError: No such I{key}.
        '''
        k, _, value = self._NS_get3(key)
        if value is missing:
            self._NS_KeyError(key, k)
        self.NS.removeObjectForKey_(k)

    def __setitem__(self, key, value):
        self.NS.setObject_forKey_(type2NS(value), type2NS(key))

    def clear(self):
        '''Remove all items, like C{dict.clear}.
        '''
        self.NS.removeAllObjects()

    def copy(self):
        '''Make a shallow copy.

           @return: The copy (L{Dict}).
        '''
        return self.__class__(self._NS_copy(True))

    def pop(self, key, default=missing):  # PYCHOK expected
        '''Remove an item, like C{dict.pop}.

           @raise KeyError: No such I{key} and no I{default} provided.
        '''
        k, _, value = self._NS_get3(key)
        if value is not missing:
            self.NS.removeObjectForKey_(k)
            return value
        elif default is missing:
            self._NS_KeyError(key, k)
        return default

#   def popitem(self):
#       raise NotImplementedError('%s.%s' % (self, 'popitem'))

    def setdefault(self, key, default=missing):  # XXX default=None
        '''Get/set an item, like C{dict.setdefault}, except
           the I{default} keyword argument is required.

           @raise ValueError: No I{default} provided for new I{key}.
        '''
        k, _, value = self._NS_get3(key)
        if value is not missing:
            return value
        elif default is missing:
            raise ValueError('%s missing' % ('default',))
        self.NS.setObject_forKey_(type2NS(default), k)
        return default

    def update(self, *other, **kwds):
        '''Update, like C{dict.update}, except I{other} must be a C{dict},
           L{Dict} or L{FrozenDict}.

           @raise TypeError: Invalid type of I{other}.

           @see: <https://Docs.Python.org/3/library/stdtypes.html#dict.update>
        '''
        other, kwds = _dict_kwds(other, kwds, 'other')
        if other:
            if isinstanceOf(other, Dict, FrozenDict):
                self.NS.addEntriesFromDictionary_(other.NS)
            elif isObjCInstanceOf(other, NSMutableDictionary, NSDictionary):
                self.NS.addEntriesFromDictionary_(other)
            elif isinstanceOf(other, dict, name='other'):
                for k, v in other.items():
                    self[k] = v  # self.__setitem__
        for k, v in kwds.items():
            self[k] = v  # self.__setitem__


NSDictionary._Type        = _Types.FrozenDict = FrozenDict
NSMutableDictionary._Type = _Types.Dict       = Dict

if __name__ == '__main__':

    from pycocoa.utils import _all_listing

    _all_listing(__all__, locals())

# % python3 -m pycocoa.dicts
#
# pycocoa.dicts.__all__ = tuple(
#  pycocoa.dicts.Dict is <class .Dict>,
#  pycocoa.dicts.FrozenDict is <class .FrozenDict>,
# )[2]
# pycocoa.dicts.version 21.11.04, .isLazy 1, Python 3.11.0 64bit arm64, macOS 13.0.1

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2023 -- mrJean1 at Gmail -- All Rights Reserved.
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
