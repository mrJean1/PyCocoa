# -*- coding: utf-8 -*-

# Script to run some or all PyGeodesy tests with Python 2 or 3.

# Tested with 64-bit Python 3.9.6, 3.8.10, 3.7.6, 2.7.18 and
# macOS's Python 2.7.16 and on macOS Big Sur 11.5.2 (aka 10.16)
# and Apple Silicon (arm64) and Intel emulation (x86_64), all
# in 64-bit only.

if __name__ == '__main__':

    import os
    from os.path import abspath, dirname
    import sys

    test_dir = dirname(abspath(__file__))
    PyCocoa_dir = dirname(test_dir)
    # extend sys.path to include the ../.. directory
    if PyCocoa_dir not in sys.path:  # Python 3+ ModuleNotFoundError
        sys.path.insert(0, PyCocoa_dir)

    def _cmd(cmd, *args):
        if args:
            cmd = cmd % args
        if len(cmd) > 128:
            cmd = cmd[:60] + '...' + cmd[-60:]
        print('\nrunning%s: %s ...' % (_OO, cmd))
        return os.system(cmd)

    _OO = '' if __debug__ else ' -OO'
    python_ = sys.executable + _OO + ' -X faulthandler'

    for t in ('list_classes',
              'list_inheritance NSAutoreleasePool',
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
              'test_Fonts',
              'test_Fonts4',
              'test_Keys 0.5',
              'test_Lazily',
              'test_NStypes',
              'test_Panels 2',
              'test_Types'):
        if _cmd('%s -m test.%s  1>/dev/null', python_, t):
            sys.exit('%s test %s FAILED' % (python_, t))
