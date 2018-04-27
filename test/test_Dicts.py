
# -*- coding: utf-8 -*-

from pycocoa import Dict, isNone, NSBundle, NSnil, NSStr, \
                    ns2Type, ObjCBase, Str, type2NS

__version__ = '18.04.26'


def _repr(o):
    n = o.__class__.__name__
    t = str(o) if isinstance(o, ObjCBase) else repr(o)  # .lstrip('<').rstrip('>')
    if not t.startswith(n):
        t = '%s(%s)' % (n, t)
    return t


if __name__ == '__main__':

    import sys

    try:
        # see pycocoa.nstypes.nsBundleRename
        b = NSBundle.mainBundle()
        assert(not isNone(b))

        print('%s: %s' % ('b', _repr(b)))

        # <http://Developer.Apple.com//library/content/documentation/MacOSX/
        #       Conceptual/BPFrameworks/Concepts/FrameworkAnatomy.html>
        # Table 2 Framework configuration keys
        nsD = b.localizedInfoDictionary() or b.infoDictionary()
        print('%s: %s' % ('nsD', _repr(nsD)))
        assert(isinstance(nsD, ObjCBase))

        D = ns2Type(nsD)
        print('%s: %s' % ('D', _repr(D)))
        assert(isinstance(D, Dict))

        for k, v in D.items():
            print(' %s: %s' % (_repr(k), _repr(v)))
            assert(isinstance(k, (str, Str, NSStr)))

        # test missinh key
        k = type2NS('missing')
        v = D.NS.objectForKey_(k)  # returns nil -> None
        print('%s: %s, %r' % ('[missing] key', _repr(k), _repr(v)))
        assert(v is NSnil)
        assert(v is None)

        print('D: %s[%s]' % (_repr(D), len(D)))
        t = dict(D.items())
        print('%s: %s[%s]' % ('t', 'dict(D.items())', len(t)))
        assert(len(t) == len(D))
        assert(D == t)

        t = dict(D)
        print('%s: %s[%s]' % ('t', 'dict(D)', len(t)))
        assert(len(t) == len(D))
        assert(D == t)

        t = Dict(nsD)
        print('%s: %s[%s]' % ('Dict', _repr(t), len(t)))
        assert(len(t) == len(D))
        assert(D == t)

        t = ns2Type(nsD)
        print('%s: %s[%s]' % ('nsD', _repr(t), len(t)))
        assert(len(t) == len(D))
        assert(D == t)

        t = nsD.allKeys()
        print('%s: %s' % ('allKeys()', _repr(t)))
        t = nsD.allKeys().objectEnumerator
        print('%s: %s' % ('allKeys()...Enumerator', _repr(t)))
        assert(isinstance(t, ObjCBase))

    except Exception:
        # XXX kludge
        sys.excepthook(*sys.exc_info())
        sys.exit(1)
