
# -*- coding: utf-8 -*-

# <http://GitHub.com/phillip-nguyen/cocoa-python/blob/master/examples/list_ivars.py>

# List the instance variables of an Objective-C class.

from pycocoa import get_class, get_ivars, leaked2

__version__ = '18.06.28'


def _up(t4):
    return t4[0].upper()


if __name__ == '__main__':

    import sys

    if len(sys.argv) < 2:
        print('USAGE: python list_ivars.py <Obj-C Class> [prefix] ...')
        exit(1)

    clstr, prefs = sys.argv[1], sys.argv[2:]

    cls, n = get_class(clstr), 0
    for name, encoding, ctype, _ in sorted(get_ivars(cls, *prefs), key=_up):
        n += 1
        t = getattr(ctype, '__name__', ctype)
        print('%s %s %s' % (name, encoding, t))

    print('%s %s instance variables total %s' % (n, clstr, leaked2()))
