
# -*- coding: utf-8 -*-

# List the protocols of an Objective-C class.

from pycocoa import get_class, get_protocols, leaked2

__version__ = '18.06.28'


def _up(t2):
    return t2[0].upper()


if __name__ == '__main__':

    import sys

    if len(sys.argv) < 2:
        print('USAGE: python list_protocols.py <Obj-C Class> [prefix] ...')

    clstr, prefs = sys.argv[1], sys.argv[2:]

    n, cls = 0, get_class(clstr)
    for name, _ in sorted(get_protocols(cls, *prefs), key=_up):
        n += 1
        print(name)

    print('%s %s protocols total %s' % (n, clstr, leaked2()))
