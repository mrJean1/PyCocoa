
# -*- coding: utf-8 -*-

# Module to run PyCocoa tests as  python setup.py test

import os
import sys
import unittest


__all__ = ('TestSuite',)
__version__ = '18.03.10'

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

    def test_Class(self):
        self._run('class_wrapper4 NSColor')

    def test_Classes(self):
        self._run('list_classes NS')

    def test_Inheritance(self):
        self._run('list_inheritance NSAutoreleasePool')

    def test_Ivalues(self):
        self._run('list_ivalues NSApplication')

    def test_Ivars(self):
        self._run('list_ivars NSView')  # NSObject crashes

    def test_Methods(self):
        self._run('list_methods NSWindow set')

    def test_NStypes(self):
        self._run('list_nstypes')

    def test_Properties(self):
        self._run('list_properties NSWindow')

    def test_Protocols(self):
        self._run('list_protocols NSColor')

    def test_Application(self):
        self._run('simple_application 3')  # waits 3 secs

    def test_Delegate(self):
        self._run('simple_delegate 1')  # waits 1 secs

    def test_Drawing(self):
        self._run('simple_drawing 2')  # waits 2 secs

    def test_Menu(self):
        self._run('simple_menu 3')

    def test_SubClasses(self):
        self._run('simple_subclass')

#   def test_VLCplayer(self):
#       self._run('simple_VLCplayer <secs> <video_file_name>')


if __name__ == '__main__':

    unittest.main(argv=sys.argv, verbosity=2)  # catchbreak=None, failfast=None
