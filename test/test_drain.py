
# -*- coding: utf-8 -*-

# Test ObjCInstance._cache_drain fixes, courtesy CaffinePills
# Issue #4 <https://github.com/mrJean1/PyCocoa/issues/4>

import run as _  # PYCHOK sys.path
from pycocoa import NSDate, NSAutoreleasePool, ObjCInstance  # drain

import sys

__version__ = '23.02.05'

objc_cache = ObjCInstance._objc_cache
_verbose   = '-verbose'.startswith(sys.argv[1] if len(sys.argv) > 1 else ' ')


def _test1():
    t = []
    for i in range(1, 10):
        p = len(objc_cache)
        pool = NSAutoreleasePool.alloc().init()
        date = NSDate.alloc().init()  # .timeIntervalSinceNow(0.0)
        t.append((p, pool))
        n = len(objc_cache)
        if _verbose:
            print(i, pool.inPool, date.inPool, p, n)
        if date.inPool != pool.inPool:
            sys.exit('%s: inPool %s vs %s' % (i, date.inPool, pool.inPool))
        if not n > p:
            sys.exit('%s: len1 before %s vs after %s' % (i, p, n))
    while t:
        p, pool = t.pop()
        pool.drain()
        n = len(objc_cache)
        if _verbose:
            print(i, pool.inPool, n, p)
        if pool.inPool != i:
            sys.exit('%s: inPool %s vs %s' % (len(t), pool.inPool, i))
        if n != p:
            sys.exit('%s: len2 drained %s vs expected %s' % (len(t), n, p))
        i -= 1


def _test2():
    for i in range(1, 21):
        pool = NSAutoreleasePool.alloc().init()
        date = NSDate.alloc().init()  # .timeIntervalSinceNow(0.0)

        p = len(objc_cache)
        if p < 0:
            sys.exit('%s: len3 %s negative' % (i, p))

        pool.drain()  # or drain(pool)
        # del pool  # does NOT drain the pool!

        n = len(objc_cache)
        if n > p:
            for p, q in objc_cache.items():
                print('cache', hex(p), q)
            sys.exit('%s: len4 %s above %s' % (i, n, p))

        del date  # PYCHOK unused


_test1()
_test2()
