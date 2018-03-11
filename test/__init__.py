
# -*- coding: utf-8 -*-

# Originally <http://GitHub.com/phillip-nguyen/cocoa-python>

# objective-ctypes
#
# Copyright (C) 2011 Phillip Nguyen -- All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of objective-ctypes nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# Copyright (C) 2017-2018 mrJean1 at Gmail dot com
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
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

# run each of the examples as a module, like

# % python -m test.<example_module_name> [arg] ...
from os.path import abspath, dirname
import sys

_test_dir = dirname(abspath(__file__))
# extend sys.path to include the ../.. directory
if _test_dir not in sys.path:  # Python 3+ ModuleNotFoundError
    sys.path.insert(0, _test_dir)

from threading import Thread
from time import sleep

from testsuite import TestSuite  # PYCHOK for setup.py

__all__ = ('terminating', 'testing',)
__version__ = '18.03.10'


def terminating(app, testime):
    '''Set up a separate thread to terminate an NSApplication
    by calling the C{.terminate_} method after the given time
    has elapsed.
    '''
    try:
        secs = float(testime) + 0.5
    except ValueError:
        return

    def _terminate():
        sleep(secs)
        app.terminate_(app)

    t = Thread(target=_terminate)
    t.start()


def testing(delegate, testime):
    '''Set up a separate thread to terminate an NSApplication
    by closing the main window after the given time has elapsed.

    The I{delegate} is the NSWindow or NSApplication C{Delegate}
    instance which must include the C{.windowWillClose_} method
    which in turn terminates the NSApplication by calling its
    C{.terminate_} method.
    '''
    try:
        quit = delegate.windowWillClose_
        secs = float(testime) + 0.5
    except AttributeError:
        raise ValueError('not a Delegate %r' % (delegate,))
    except ValueError:
        return  # no testime

    def _terminate():
        sleep(secs)
        quit(None)

    t = Thread(target=_terminate)
    t.start()
