
# -*- coding: utf-8 -*-

# List all ObjC NS... types.

__version__ = '23.01.18'

if __name__ == '__main__':

    from run import pycocoa
    import sys

    i = 0
    for k in sorted(pycocoa.__all__, key=str.lower):
        if k.startswith(('ObjC', 'NS')) and k not in ('NSLog', 'ObjCBase',):
            c = getattr(pycocoa, k)
            try:
                s = r = c.alloc()  # .init()
            except Exception:
                try:
                    s = r = c()
                except Exception:
                    r = c
                    s = c.__class__.__name__
            i += 1
            print('%4d: %-40s: %s : %r' % (i, k, s, r))

    sys.exit(int(i < 200))

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
