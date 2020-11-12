
# -*- coding: utf-8 -*-

# Test the lazy import module lazily.

__version__ = '20.11.11'

from pycocoa import Color, Colors, utils
import sys

if __name__ == '__main__':

    e = i = 0
    for S, s in Colors.items_(utils._Constants):
        for n, c in s.items_(Color):
            i += 1
            t  = ['']
            for a in ('name', 'nsColor',
                      'cyan', 'magenta', 'yellow',
                      'hue', 'saturation', 'brightness',
                      'red', 'green', 'blue',
                      'black', 'white', 'alpha', 'n'):
                v = getattr(c, a)
                if v is not None:
                    t.append('.%s=%s' % (a, v))
            if len(t) < 4:
                e += 1

            v = c.hex
            if v is not None:
                t.append('.%s=%#6x' % ('hex', v))
            print('%4d %4s.%s: %r%s' % (i, S, n, c, ', '.join(t)))

    sys.exit(min(e, 255))

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2020 -- mrJean1 at Gmail -- All Rights Reserved.
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
