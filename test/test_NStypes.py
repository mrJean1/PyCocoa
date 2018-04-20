
# -*- coding: utf-8 -*-

# List the protocols of an Objective-C class.

import pycocoa

__version__ = '18.04.12'

if __name__ == '__main__':

    import sys

    i = 0
    for k in sorted(pycocoa.__all__, key=str.lower):
        if k.startswith(('ObjC', 'NS')) and k not in ('ObjCBase',):
            c = getattr(pycocoa, k)
            try:
                s = r = c.alloc()  # .init()
            except Exception:
                try:
                    s = r = c()
                except Exception:
                    r = c
                    s = c.__class__.__name__
            i += 1
            print('%4d: %-40s: %s : %r' % (i, k, s, r))

    sys.exit(int(i != 151))
