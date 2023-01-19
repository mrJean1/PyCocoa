
# -*- coding: utf-8 -*-

import run as __  # PYCHOK sys.path
from pycocoa import Dict, isNone, NSMain, NSStr, \
                    ns2Type, ObjCClass, Str, type2NS

__version__ = '23.01.18'

# get PyCocoa-internal _ObjCBase class
_ObjCBase = tuple(_ for _ in ObjCClass.mro() if _.__name__ == '_ObjCBase')


def _strepr(o):
    n = o.__class__.__name__
    t = str(o) if isinstance(o, _ObjCBase) else repr(o)  # .lstrip('<').rstrip('>')
    if not t.startswith(n):
        t = '%s(%s)' % (n, t)
    return t


if __name__ == '__main__':

    import sys

    try:
        # see pycocoa.nstypes.nsBundleRename
        b = NSMain.Bundle
        assert(not isNone(b))

        print('%s: %s' % ('b', _strepr(b)))

        # <https://Developer.Apple.com/library/content/documentation/MacOSX/
        #        Conceptual/BPFrameworks/Concepts/FrameworkAnatomy.html>
        # Table 2 Framework configuration keys
        nsD = b.localizedInfoDictionary() or b.infoDictionary()
        print('%s: %s' % ('nsD', _strepr(nsD)))
        assert(isinstance(nsD, _ObjCBase))

        D = ns2Type(nsD)
        print('%s: %s' % ('D', _strepr(D)))
        assert(isinstance(D, Dict))

        for k, v in D.items():
            print(' %s: %s' % (_strepr(k), _strepr(v)))
            assert(isinstance(k, (str, Str, NSStr)))

        # test missinh key
        k = type2NS('missing')
        v = D.NS.objectForKey_(k)  # returns nil -> None
        print('%s: %s, %r' % ('[missing] key', _strepr(k), _strepr(v)))
        assert(v is NSMain.nil)
        assert(v is None)

        print('D: %s[%s]' % (_strepr(D), len(D)))
        t = dict(D.items())
        print('%s: %s[%s]' % ('t', 'dict(D.items())', len(t)))
        assert(len(t) == len(D))
        assert(D == t)

        t = dict(D)
        print('%s: %s[%s]' % ('t', 'dict(D)', len(t)))
        assert(len(t) == len(D))
        assert(D == t)

        t = Dict(nsD)
        print('%s: %s[%s]' % ('Dict', _strepr(t), len(t)))
        assert(len(t) == len(D))
        assert(D == t)

        t = ns2Type(nsD)
        print('%s: %s[%s]' % ('nsD', _strepr(t), len(t)))
        assert(len(t) == len(D))
        assert(D == t)

        t = nsD.allKeys()
        print('%s: %s' % ('allKeys()', _strepr(t)))
        t = nsD.allKeys().objectEnumerator
        print('%s: %s' % ('allKeys()...Enumerator', _strepr(t)))
        assert(isinstance(t, _ObjCBase))

    except Exception:
        # XXX kludge
        sys.excepthook(*sys.exc_info())
        sys.exit(1)

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
