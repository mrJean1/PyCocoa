
# -*- coding: utf-8 -*-

# Originally <http://GitHub.com/phillip-nguyen/cocoa-python/blob/master/examples/list_methods.py>

# List all methods of an Objective-C class.

from pycocoa import get_class, get_methods, leaked2

__version__ = '18.06.28'


def _up(t4):
    return t4[0].upper()


if __name__ == '__main__':

    import sys

    if len(sys.argv) < 2:
        print('USAGE: python list_methods.py <Obj-C Class> [prefix] ...')
        exit(1)

    clstr, prefs = sys.argv[1], sys.argv[2:]

    cls, n = get_class(clstr), 0
    for name, encoding, rargtypes, _ in sorted(get_methods(cls, *prefs), key=_up):
        n += 1
        rargtypes = [getattr(rarg, '__name__', rarg) for rarg in rargtypes]
        print('%s %s (%s)' % (name, encoding, ', '.join(map(str, rargtypes))))

    print('%s %s methods total %s' % (n, clstr, leaked2()))
