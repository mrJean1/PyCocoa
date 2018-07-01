
# -*- coding: utf-8 -*-

# Originally <http://GitHub.com/phillip-nguyen/cocoa-python/blob/master/examples/list_classes.py>

# List all loaded Objective-C classes.

from pycocoa import get_classes, leaked2

__version__ = '18.06.28'


def _up(t2):
    return t2[0].upper()


if __name__ == '__main__':

    import sys

    if len(sys.argv) < 2:
        print('USAGE: python list_classes.py [prefix] ...')

    n, prefs = 0, sys.argv[1:]

    for name, _ in sorted(get_classes(*prefs), key=_up):
        n += 1
        print(name)

    print('%s %s classes total %s' % (n, ', '.join(prefs), leaked2()))
