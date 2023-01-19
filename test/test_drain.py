
# -*- coding: utf-8 -*-

# Test ObjCInstance._cache_drain fixes, courtesy CaffinePills
# Issue #4 <https://github.com/mrJean1/PyCocoa/issues/4>

import run as _  # PYCHOK sys.path
from pycocoa import NSDate, NSAutoreleasePool, ObjCInstance  # drain

import sys

objcache = ObjCInstance._objc_cache

for i in range(1, 17):

    pool = NSAutoreleasePool.alloc().init()
    date = NSDate.alloc().init()  # .timeIntervalSinceNow(0.0)

    n = len(objcache)
    if n < 1:
        sys.exit('%s: len1 %d' % (i, n))

    pool.drain()  # or drain(pool)
    # del pool  # does NOT drain the pool!

    n = len(objcache)
    if n > 0:
        sys.exit('%s: len0 %d' % (i, n))
