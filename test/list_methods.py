
# -*- coding: utf-8 -*-

# Originally <http://GitHub.com/phillip-nguyen/cocoa-python/blob/master/examples/list_methods.py>

# List all methods of an Objective-C class.

from pycocoa import get_class, get_methods, leaked2, sortuples

__version__ = '18.11.06'


if __name__ == '__main__':

    import sys

    if len(sys.argv) < 2:
        print('USAGE: python list_methods.py <Obj-C Class> [prefix] ...')
        exit(1)

    clstr, prefs = sys.argv[1], sys.argv[2:]

    cls, n = get_class(clstr), 0
    if cls is None:  # and clstr.endswith('Delegate')
        import pycocoa  # PYCHOK expected
        cls = pycocoa.__dict__.get(clstr, cls)  # inlieu of __import__ ...
    for name, encoding, rargtypes, _ in sortuples(get_methods(cls, *prefs)):
        n += 1
        rargtypes = [getattr(rarg, '__name__', rarg) for rarg in rargtypes]
        print('%s %s (%s)' % (name, encoding, ', '.join(map(str, rargtypes))))

    print('%s %s methods total %s' % (n, clstr, leaked2()))
