
# -*- coding: utf-8 -*-

# Test the lazy import module lazily.

__version__ = '20.01.07'

import os
import pycocoa
import sys

_all_      = pycocoa.__all__
isPython37 = sys.version_info[:2] >= (3, 7)
lazily     = pycocoa.lazily
PythonX    = sys.executable  # python or Pythonista path

_cmd = PythonX + " -c 'import pycocoa, sys; " \
                      "sys.exit(0 if pycocoa.isLazy == %s else 1)'"
_env_cmd = 'env %s ' + _cmd + ' >>/dev/null'

_HOME = os.environ.get('HOME', '')
if _HOME and _cmd.startswith(_HOME):
    _cmd = '~' + _cmd[len(_HOME):]
del _HOME

if __name__ == '__main__':

    for a in sorted(_all_, key=str.lower):
        v = getattr(pycocoa, a, None)
        v = pycocoa.type2strepr(v).replace('()', '').strip()
        print('pycocoa.%s: %s' % (a, v))

    t = 0
    z = pycocoa.isLazy
    print('%s: %s' % ('isLazy', z))
    if not z:
        for a, m in lazily._all_missing2(_all_):
            print('missing in %s: %s' % (a, m or None))
            if m:
                t += len(m.split(', '))

    # simple lazy_import enable tests
    print('cmd: %s' % (_cmd,))
    for z in range(5):
        e = 'PYCOCOA_LAZY_IMPORT=%s' % (z,)
        c = _env_cmd % (e, z if isPython37 else None)
        x = os.system(c) >> 8  # exit status in high byte
        print('%s: %s' % (e, x))
        if x:
            t += 1

    sys.exit(min(t, 255))
