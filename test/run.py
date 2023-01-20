# -*- coding: utf-8 -*-

# Script to run some or all PyGeodesy tests with Python 2 or 3.

# Tested with 64-bit Python 3.11, 3.9.6, 3.8.10, 3.7.6, 2.7.18 and
# and macOS's Python 2.7.16 and on macOS Ventura 13.1, Big Sur 11.5.2
# (aka 10.16) and Apple Silicon (arm64) and Intel emulation (x86_64),
# all in 64-bit only.

__version__ = '23.01.20'

import os
from os.path import abspath, dirname
import sys

test_dir    = dirname(abspath(__file__))
PyCocoa_dir = dirname(test_dir)
# extend sys.path to include the ../.. directory
if PyCocoa_dir not in sys.path:  # Python 3+ ModuleNotFoundError
    sys.path.insert(0, PyCocoa_dir)
import pycocoa  # PYCHOK for all tests

pythonx  = sys.executable if sys.version_info[0] > 2 else 'python2'
_OO      = '' if __debug__ else ' -OO'
pythonX_ = pythonx + _OO  # python or Pythonista path
if sys.version_info[:2] > (3, 3):
    pythonX_ += ' -X faulthandler'

if __name__ == '__main__':

    def _cmd(cmd, *args):
        if args:
            cmd = cmd % args
        if len(cmd) > 128:
            cmd = cmd[:60] + '...' + cmd[-60:]
        print('\nrunning%s: %s ...' % (_OO, cmd))
        return os.system(cmd)

    for t in ('list_classes',
              'list_inheritance NSWindow',  # NSAutoreleasePool',
              'list_ivalues NSApplication',
              'list_ivars NSView',  # NSObject' crashes
              'list_methods NSException',
              'list_methods NSWindow',
              'list_nstypes',
              'list_properties NSWindow',
              'list_protocols NSColor',
              'simple_application 3',
              'simple_delegate 1',
              'simple_drawing 2',
              'simple_menu 2',
              'simple_subclass',
              'simple_table 2',
#             'simple_VLCplayer <secs> <video_file>',
              'simple_window 1',
              'test_Colors',
              'test_Dicts',
              'test_drain',
              'test_Fonts',
              'test_Fonts4',
              'test_Keys 0.5',
              'test_Lazily',
              'test_NStypes',
              'test_Panels 2',
              'test_Types'):
        if _cmd('%s -m test.%s  1>/dev/null', pythonX_, t):
            sys.exit('%s test %s FAILED' % (pythonX_, t))
