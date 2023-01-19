
# -*- coding: utf-8 -*-

# List and test the Objective-C nstypes.

try:
    _b = bytes
except NameError:
    _b = bytearray

__version__ = '23.01.18'

if __name__ == '__main__':

    from run import pycocoa
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
            ns = pycocoa.py2NS(o)
        except Exception as x:
            e += 1
            print('%s FAILED ... %r' % (_astr(o), x))
            raise
            continue

        p, f = pycocoa.ns2py(ns, dflt='FAILED'), ''
        if p != o:
            e += 1
            f = ' ... FAILED'
        print('%s to %r ... back to %s%s' % (_astr(o), ns, _astr(p), f))
        try:
            ns.autorelease()
        except AttributeError:
            pass  # bool, NSBool, True

    print('%s types total, %s failed %s' % (n, e or 'none', pycocoa.leaked2()))

    sys.exit(e)

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2023 -- mrJean1 at Gmail -- All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
