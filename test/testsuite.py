
# -*- coding: utf-8 -*-

# Module to run PyCocoa tests as  python setup.py test

import os
import sys
import unittest

__all__ = ('TestSuite',)
__version__ = '23.01.18'

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
#       self._run('simple_VLCplayer <video_file_name>')

    def test_simple_window(self):
        self._run('simple_window 1')

    def test_Colors(self):
        self._run('test_Colors')

    def test_Dicts(self):
        self._run('test_Dicts')

    def test_drain(self):
        self._run('test_drain')

    def test_Fonts(self):
        self._run('test_Fonts')

    def test_Fonts4(self):
        self._run('test_Fonts4')

    def test_Keys(self):
        self._run('test_Keys 0.5')

    def test_Lazily(self):
        self._run('test_Lazily')

    def test_NStypes(self):
        self._run('test_NStypes')

    def test_Panels(self):
        self._run('test_Panels 2')

    def test_Types(self):
        self._run('test_Types')


if __name__ == '__main__':

    unittest.main(argv=sys.argv, verbosity=2)  # catchbreak=None, failfast=None

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
