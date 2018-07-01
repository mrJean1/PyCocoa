
# -*- coding: utf-8 -*-

# List all the instance variables of an Objective-C class.

from pycocoa import get_class, get_ivar, get_ivars, leaked2

__version__ = '18.06.28'


def _up(t4):
    return t4[0].upper()


if __name__ == '__main__':

    import sys

    if len(sys.argv) < 2:
        print('USAGE: python list_ivalues.py <Obj-C Class> [prefix] ...]')
        exit(1)

    clstr, prefs = sys.argv[1], sys.argv[2:]

    cls, n = get_class(clstr), 0
    for name, encoding, ctype, _ in sorted(get_ivars(cls, *prefs), key=_up):
        n += 1
        value = get_ivar(cls, name, ctype)
        t = getattr(ctype, '__name__', ctype)
        print('%s %s %s: %r' % (name, encoding, t, value))

    print('%s %s instance variables total %s' % (n, clstr, leaked2()))
