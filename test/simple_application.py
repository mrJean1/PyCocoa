
# -*- coding: utf-8 -*-

# <https://StackOverflow.com/questions/1517342/basic-cocoa-application-
#         using-dock-in-python-but-not-xcode-and-all-that-extras>

import run as _  # PYCHOK sys.path
# generic Python imports
# import datetime
# import os
import sched
import sys
# import tempfile
import threading
import time
# all imports listed explicitly to help PyChecker
from pycocoa import get_selector, NSApplication, NSAutoreleasePool, \
                    NSMenu, NSMenuItem, NSStatusBar, NSStr, \
                    PyObjectEncoding, ObjCClass, ObjCInstance, \
                    ObjCSubclass, send_super, terminating

__version__ = '23.01.18'

# <https://StackOverflow.com/questions/24024723/swift-using-
#  nsstatusbar-statusitemwithlength-and-nsvariablestatusitemlength>
NSVariableStatusItemLength = -1
NSSquareStatusItemLength   = -2

# all stuff related to the repeating-action
thesched = sched.scheduler(time.time, time.sleep)


def tick(n, writer):
    writer(n)
    thesched.enter(1.0, 2, tick, (n+1, writer))
    print('tick %d' % (n,))
#   fd, name = tempfile.mkstemp('.txt', 'hello', '/tmp');
#   print('%d writing %r' % (n, name))
#   f = os.fdopen(fd, 'w')
#   f.write(datetime.datetime.now().isoformat())
#   f.write('\n')
#   f.close()


def schedule(writer):
    pool = NSAutoreleasePool.alloc().init()  # PYCHOK expected
    thesched.enter(0.0, 2, tick, (1, writer))
    thesched.run()
    # normally you'd want pool.drain() here, but since this
    # function never ends until end of program (thesched.run
    # never returns since each tick schedules a new one), that
    # pool.drain call would never execute here ;-).


# objc-related stuff
class TheDelegate_Implementation(object):  # NSObject):
    TheDelegate = ObjCSubclass('NSObject', 'TheDelegate')

    @TheDelegate.method('@')
    def init(self):
        # self = ObjCInstance(send_message('NSObject', 'alloc'))
        self = ObjCInstance(send_super(self, 'init'))
        # print(self)  # <ObjCInstance 0x...: TheDelegate at ...>
        return self

    app = None
    badge = None
#   statusbar = None
    state = 'idle'

    @TheDelegate.method('v@')
    def applicationDidFinishLaunching_(self, notification):
        statusbar = NSStatusBar.systemStatusBar()
        statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
#       statusitem.setHighlightMode_(1)
#       statusitem.setToolTip_(NSStr('Example'))
#       statusitem.setTitle_(NSStr('Example'))

        menu = NSMenu.alloc().init()
        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                   NSStr('Quit'), get_selector('terminate:'), NSStr(''))
        menu.addItem_(menuitem)
        statusitem.setMenu_(menu)

    @TheDelegate.method(b'v' + PyObjectEncoding)
    def writer(self, s):
        self.badge.setBadgeLabel_(NSStr(str(s)))

    @TheDelegate.method(b'v@')
    def windowWillClose_(self, notification):
        if self.app:
            self.app.terminate_(self)


def main(timeout=None):

    # prepare and set our delegate
    app = NSApplication.sharedApplication()

    TheDelegate = ObjCClass('TheDelegate')  # the actual class

    delegate = TheDelegate.alloc().init()  # PYCHOK expected
    app.setDelegate_(delegate)
    delegate.app = app

    delegate.badge = app.dockTile()
    delegate.writer(0)

    # on a separate thread, run the scheduler
    t = threading.Thread(target=schedule, args=(delegate.writer,))
    if sys.version_info[0] > 2:
        t.deamon = True
    else:  # throws DeprecationWarning
        t.setDaemon(1)
    t.start()

    # set up the timeout
    terminating(app, timeout)
    # let her rip!-)
    app.run()  # AppHelper.runEventLoop()


if __name__ == '__main__':

    if len(sys.argv) > 1:
        main(sys.argv.pop(1))
    else:
        main()

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
#
# __
#
# Copyright (C) 2011 -- Phillip Nguyen -- All Rights Reserved.
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
