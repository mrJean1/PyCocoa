
# -*- coding: utf-8 -*-

# List the protocols of an Objective-C class.

from pycocoa import leaked2, ns2py, py2NS

try:
    _b = bytes
except NameError:
    _b = bytearray

__version__ = '18.04.04'

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
              'str',
             _b(b'bytes'),
             {1: 2, 3: '4'},
              decimal.Decimal(123456789),
              float(6),
              frozenset((7, 8.0)),
              True,
             ['L', True, 0.0],
              False,
              None,
              set((9, '10')),
             ('T', False, None),
              u'Unicode'):

        n += 1
        try:
            ns = py2NS(o)
        except Exception as x:
            e += 1
            print('%s FAILED ... %r' % (_astr(o), x))
            raise
            continue

        p, f = ns2py(ns, dflt='FAILED'), ''
        if p != o:
            e += 1
            f = ' ... FAILED'
        print('%s to %r ... back to %s%s' % (_astr(o), ns, _astr(p), f))
        try:
            ns.autorelease()
        except AttributeError:
            pass  # bool, NSBool, True

    print('%s types total, %s failed %s' % (n, e or 'none', leaked2()))

    sys.exit(e)
