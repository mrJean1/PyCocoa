
# -*- coding: utf-8 -*-

# List the protocols of an Objective-C class.

import pycocoa

__version__ = '18.04.10'

if __name__ == '__main__':

    import sys

    i = 0
    for k in sorted(pycocoa.__all__, key=str.lower):
        if k in ('Dict', 'FrozenDict', 'FrozenSet', 'List', 'Tuple', 'Set', 'Str'):
            c = getattr(pycocoa, k)
            try:
                r = c()
                s = pycocoa.type2strepr(r)
                ns = r.NS
            except Exception:
                r = c
                s = c.__class__.__name__
                ns = 'N/A'

            i += 1
            print('%4d: %-10s str: %s,  strepr: %s,  repr: %r,  .NS: %s' % (i, k, r, s, r, ns))

    sys.exit(int(i != 7))
