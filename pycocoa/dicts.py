
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
from nstypes import NSDictionary, nsIter2, NSMutableDictionary, \
                    NSnil, ns2Type, py2NS, type2NS, _Types
from runtime import isImmutable, isInstanceOf, ObjCClass, ObjCInstance
from utils   import instanceof, missing

__all__ = ('Dict',
           'FrozenDict')
__version__ = '18.04.10'


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
    '''Python Type equivalent of an (immutable) ObjC NSDictionary.
    '''
    def __init__(self, *ns_dict, **kwds):
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
        elif instanceof(other, dict, name='other'):
            return len(self) == len(other) and _dict_cmp(self, other) \
                                           and _dict_cmp(other, self)

    def __getitem__(self, key):
        k, _, value = self._NS_get3(key)
        if value is missing:
            self._NS_KeyError(key, k)
        return value

    def __len__(self):
        # <http://developer.apple.com/documentation/foundation/
        #         nsdictionary/1409628-count>
        return self.NS.count()

    def __ne__(self, other):
        return not self.__eq__(other)

    def copy(self):
        '''Make a shallow copy as an instance of this immutable class.
        '''
        return self.__class__(self._NS_copy(False))

#   def fromkeys(self):
#       raise NotImplementedError('%s.%s' % (self, 'fromkeys'))

    def get(self, key, default=None):
        _, _, value = self._NS_get3(key)
        return default if value is missing else value

    def items(self):
        for key, k in nsIter2(self.NS.allKeys()):
            v = self.NS.objectForKey_(k)
            if v in (NSnil, None):  # missing key?
                self._NS_KeyError(key, k)
            yield key, ns2Type(v)

    def keys(self):
        for key, _ in nsIter2(self.NS.allKeys()):
            yield key
    __iter__ = keys

    def values(self):
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
        return k, v, (missing if v in (NSnil, None) else ns2Type(v))

    def _NS_KeyError(self, key, k):
        # XXX KeyError(key) prints repr(key), adding "..."
        raise KeyError('%s no such key: %s (%r)' % (self, key, k))


class Dict(FrozenDict):
    '''Python Type equivalent of a mutable ObjC NSMutableDictionary.
    '''
    __iter__ = FrozenDict.keys

    def __init__(self, *ns_dict, **kwds):
        ns_dict, kwds = _dict_kwds(ns_dict, kwds, Dict.__name__)
        if isinstance(ns_dict, dict):
            self.NS = NSMutableDictionary.alloc().init()
            self.update(ns_dict)
        elif isinstance(ns_dict, Dict):
            self.NS = ns_dict.NS
        elif isinstance(ns_dict, FrozenDict):
            self.NS = ns_dict.NS.mutableCopy()  # XXX flat copy only?
        elif isInstanceOf(ns_dict, NSMutableDictionary, name=Dict.__name__):
            self.NS = ns_dict

        if kwds:
            self.update(kwds)

    def __delitem__(self, key):
        k, _, value = self._NS_get3(key)
        if value is missing:
            self._NS_KeyError(key, k)
        self.NS.removeObjectForKey_(k)

    def __setitem__(self, key, value):
        self.NS.setObject_forKey_(type2NS(value), type2NS(key))

    def clear(self):
        '''Like dict.clear().
        '''
        self.NS.removeAllObjects()

    def copy(self):
        '''Make a shallow copy as an instance of this mutable class.
        '''
        return self.__class__(self._NS_copy(True))

    def pop(self, key, default=missing):
        '''Like dict.pop().
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
        '''Like dict.setdefault(), except the I{default} is required.
        '''
        k, _, value = self._NS_get3(key)
        if value is not missing:
            return value
        elif default is missing:
            raise ValueError('%s missing' % ('default',))
        self.NS.setObject_forKey_(type2NS(default), k)
        return default

    def update(self, *other, **kwds):
        '''Like dict.update(), except I{other} must be a dict, Dict or DictIM.

        @see: <http://docs.python.org/3/library/stdtypes.html#dict.update>
        '''
        other, kwds = _dict_kwds(other, kwds, 'other')
        if other:
            if instanceof(other, Dict, FrozenDict):
                self.NS.addEntriesFromDictionary_(other.NS)
            elif isInstanceOf(other, NSMutableDictionary, NSDictionary):
                self.NS.addEntriesFromDictionary_(other)
            elif instanceof(other, dict, name='other'):
                for k, v in other.items():
                    self[k] = v  # self.__setitem__
        for k, v in kwds.items():
            self[k] = v  # self.__setitem__


NSDictionary._Type        = _Types.FrozenDict = FrozenDict
NSMutableDictionary._Type = _Types.Dict       = Dict

if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)
