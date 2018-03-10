
# -*- coding: utf-8 -*-

# Originally <http://GitHub.com/phillip-nguyen/cocoa-python/blob/master/examples/inheritance.py>

# Print the inheritance chain for a given class.

from pycocoa import get_class, get_classname, get_inheritance

__version__ = '17.11.18'

if __name__ == '__main__':

    import sys

    if len(sys.argv) < 2:
        print('USAGE: python inheritance.py <Obj-C Class>')
        exit(1)

    cls = get_class(sys.argv[1])
    for cls in get_inheritance(cls):
        print(get_classname(cls))
