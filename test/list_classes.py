
# -*- coding: utf-8 -*-

# Originally <http://GitHub.com/phillip-nguyen/cocoa-python/blob/master/examples/list_classes.py>

# List all loaded Objective-C classes.

from pycocoa import get_classes, leaked2

__version__ = '17.11.18'

if __name__ == '__main__':

    import sys

    if len(sys.argv) < 2:
        print('USAGE: python list_classes.py [prefix] ...')

    n, prefs = 0, sys.argv[1:]

    for name, _ in sorted(get_classes(*prefs)):
        n += 1
        print(name)

    print('%s %s classes total %s' % (n, ', '.join(prefs), leaked2()))
