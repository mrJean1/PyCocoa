
# -*- coding: utf-8 -*-

from pycocoa import Dict, isNone, NSMain, NSStr, \
                    ns2Type, ObjCClass, Str, type2NS

__version__ = '18.06.11'

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

        # <http://Developer.Apple.com//library/content/documentation/MacOSX/
        #       Conceptual/BPFrameworks/Concepts/FrameworkAnatomy.html>
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
