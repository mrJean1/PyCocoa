
# -*- coding: utf-8 -*-

# List the protocols of an Objective-C class.

from pycocoa import leaked2, ns2py, py2NS

try:
    _b = bytes
except NameError:
    _b = bytearray

__version__ = '17.11.19'

if __name__ == '__main__':

    import decimal
    import sys

    def _astr(py):
        t, v = type(py).__name__, repr(py)
        if not v.startswith(t):
            v = '%s(%s)' % (t, v)
        return v

    e = n = 0
    for o in (True,
              int(5),
             _b(b'bytes'),
             {1: 2, 3: '4'},
              decimal.Decimal(123456789),
              float(6),
              frozenset((7, 8.0)),
             ['L', True, 0.0],
              None,
              set((9, '10')),
              'str',
             ('T', False, None),
              u'Unicode'):

        n += 1
        try:
            ns = py2NS(o)
        except Exception as x:
            e += 1
            print('%s FAILED ... %s' % (_astr(o), x))
            continue

        p, f = ns2py(ns, default='FAILED'), ''
        if p != o:
            e += 1
            f = ' ... FAILED'
        print('%s to %r back to %s%s' % (_astr(o), ns, _astr(p), f))
        ns.autorelease()

    print('%s types total, %s failed %s' % (n, e or 'none', leaked2()))

    sys.exit(e)
