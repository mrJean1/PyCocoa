
# -*- coding: utf-8 -*-

# Module to run PyCocoa tests as  python setup.py test

import os
import sys
import unittest

__all__ = ('TestSuite',)
__version__ = '18.05.28'

_python_exe = sys.executable


class TestSuite(unittest.TestCase):
    '''Combine all test modules into a test suite/case
       and run each test module as a separate test.
    '''
    _runs = 0  # pseudo global

    def _run(self, test):
        TestSuite._runs += 1  # pseudo global
        x = os.system('%s -m test.%s >/dev/null' % (_python_exe, test))
        # check the exit status code
        self.assertEqual(x, 0)

    def test_class_wrapper(self):
        self._run('class_wrapper4 NSColor')

    def test_list_classes(self):
        self._run('list_classes NS')

    def test_list_inheritance(self):
        self._run('list_inheritance NSAutoreleasePool')

    def test_list_ivalues(self):
        self._run('list_ivalues NSApplication')

    def test_list_ivars(self):
        self._run('list_ivars NSView')  # NSObject crashes

    def test_list_methods(self):
        self._run('list_methods NSWindow set')

    def test_list_nstypes(self):
        self._run('list_nstypes')

    def test_list_properties(self):
        self._run('list_properties NSWindow')

    def test_list_protocols(self):
        self._run('list_protocols NSColor')

    def test_simple_application(self):
        self._run('simple_application 3')  # waits 3 secs

    def test_simple_delegate(self):
        self._run('simple_delegate 1')  # waits 1 secs

    def test_simple_drawing(self):
        self._run('simple_drawing 2')  # waits 2 secs

    def test_simple_menu(self):
        self._run('simple_menu 3')

    def test_simple_subClass(self):
        self._run('simple_subclass')

    def test_simple_table(self):
        self._run('simple_table 2')

#   def test_simple_VLCplayer(self):
#       self._run('simple_VLCplayer <secs> <video_file_name>')

    def test_simple_window(self):
        self._run('simple_window 1')

    def test_Dicts(self):
        self._run('test_Dicts')

    def test_Fonts(self):
        self._run('test_Fonts')

    def test_Fonts4(self):
        self._run('test_Fonts4')

    def test_NStypes(self):
        self._run('test_NStypes')

    def test_Panels(self):
        self._run('test_Panels 2')

    def test_Types(self):
        self._run('test_Types')


if __name__ == '__main__':

    unittest.main(argv=sys.argv, verbosity=2)  # catchbreak=None, failfast=None
