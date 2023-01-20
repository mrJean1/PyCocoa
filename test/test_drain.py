
# -*- coding: utf-8 -*-

# Test ObjCInstance._cache_drain fixes, courtesy CaffinePills
# Issue #4 <https://github.com/mrJean1/PyCocoa/issues/4>

import run as _  # PYCHOK sys.path
from pycocoa import NSDate, NSAutoreleasePool, ObjCInstance  # drain

import sys

__version__ = '23.01.20'

objc_cache = ObjCInstance._objc_cache

for i in range(1, 17):

    pool = NSAutoreleasePool.alloc().init()
    date = NSDate.alloc().init()  # .timeIntervalSinceNow(0.0)

    p = len(objc_cache)
    if p < 0:
        sys.exit('%s: len1 %d' % (i, p))

    pool.drain()  # or drain(pool)
    # del pool  # does NOT drain the pool!

    n = len(objc_cache)
    if n > p:
        for p, q in objc_cache.items():
            print('cache', hex(p), q)
        sys.exit('%s: len2 %d' % (i, n))
