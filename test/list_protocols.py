
# -*- coding: utf-8 -*-

# List the protocols of an Objective-C class.

__version__ = '23.01.18'

if __name__ == '__main__':

    from run import pycocoa
    import sys

    if len(sys.argv) < 2:
        print('USAGE: python list_protocols.py <Obj-C Class> [prefix] ...')

    clstr, prefs = sys.argv[1], sys.argv[2:]

    n, cls = 0, pycocoa.get_class(clstr)
    for name, _ in pycocoa.sortuples(pycocoa.get_protocols(cls, *prefs)):
        n += 1
        print(name)

    print('%s %s protocols total %s' % (n, clstr, pycocoa.leaked2()))

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
