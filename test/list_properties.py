
# -*- coding: utf-8 -*-

# List the properties of an Objective-C class or protocol.

from pycocoa import get_class, get_properties, get_protocol, leaked2, sortuples

__version__ = '18.11.02'


if __name__ == '__main__':

    import sys

    if len(sys.argv) < 2:
        print('USAGE: python list_properties.py <Obj-C Class> | <Obj-C Protocol> [prefix] ...')

    cls_protostr, prefs = sys.argv[1], sys.argv[2:]

    n, cls_proto = 0, get_class(cls_protostr) or get_protocol(cls_protostr)
    # avoid sorting the prop object in prop[3]
    for name, attrs, setter in sortuples((prop[:3] for prop in
                                          get_properties(cls_proto, *prefs))):
        n += 1
        print(' '.join((name, attrs, setter)))

    print('%s %s properties total %s' % (n, cls_protostr, leaked2()))
