
# -*- coding: utf-8 -*-

# <http://StackOverflow.com/questions/1517342/basic-cocoa-application-
#         using-dock-in-python-but-not-xcode-and-all-that-extras>

# generic Python imports
# import datetime
# import os
import sched
# import sys
# import tempfile
import threading
import time
# all imports listed explicitly to help PyChecker
from pycocoa import get_selector, NSApplication, NSAutoreleasePool, \
                    NSMenu, NSMenuItem, NSStatusBar, NSStr, \
                    PyObjectEncoding, ObjCClass, ObjCInstance, \
                    ObjCSubclass, send_super

__version__ = '18.05.25'

# <http://StackOverflow.com/questions/24024723/swift-using-
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
    t.setDaemon(1)
    t.start()

    # set up the timeout
    if timeout is not None:
        try:  # PyCocoa/test
            from test import terminating
            terminating(app, timeout)
        except ImportError:
            pass

    # let her rip!-)
    app.run()  # AppHelper.runEventLoop()


if __name__ == '__main__':

    import sys

    if len(sys.argv) > 1:
        main(sys.argv.pop(1))
    else:
        main()
