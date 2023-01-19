
# -*- coding: utf-8 -*-

# List all the instance variables of an Objective-C class.

__version__ = '23.01.18'

if __name__ == '__main__':

    from run import pycocoa
    import sys

    if len(sys.argv) < 2:
        print('USAGE: python list_ivalues.py <Obj-C Class> [prefix] ...]')
        exit(1)

    clstr, prefs = sys.argv[1], sys.argv[2:]

    cls, n = pycocoa.get_class(clstr), 0
    for name, encoding, ctype, _ in pycocoa.sortuples(pycocoa.get_ivars(cls, *prefs)):
        n += 1
        value = pycocoa.get_ivar(cls, name, ctype)
        t = getattr(ctype, '__name__', ctype)
        print('%s %s %s: %r' % (name, encoding, t, value))

    print('%s %s instance variables total %s' % (n, clstr, pycocoa.leaked2()))

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
