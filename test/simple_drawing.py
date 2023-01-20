
# encoding: utf-8

# Reworked from <https://GitHub.com/ActiveState/code/tree/master/recipes/Python/303058_Simple_PyObjC_Example>
# showing an NSWindow with a basic, drawable NSView.

import run as _  # PYCHOK sys.path
# all imports listed explicitly to help PyChecker
from pycocoa import NSApplication, NSBackingStoreBuffered, \
                    NSBezierPath, NSColor, NSMakeRect, NSPoint_t, \
                    NSStr, NSWindow, NSWindowStyleMaskUsual, \
                    PyObjectEncoding, ObjCClass, ObjCInstance, \
                    ObjCSubclass, send_super, terminating, \
                    NSAutoreleasePool, NSDate

from pycocoa.oslibs import libAppKit

from math import sin, cos, pi as PI

__version__ = '23.01.19'

NSRectFill = libAppKit.NSRectFill


class _View_Implementation(object):
    _View = ObjCSubclass('NSView', '_View')

    @_View.method(b'@' + PyObjectEncoding * 2)
    def initWithFrame_(self, frame, n):
        objc = ObjCInstance(send_super(self, 'initWithFrame:', frame))
        self._n = n
        return objc  # objc is self

    @_View.method(b'v@')
    def drawRect_(self, rect):

        # w, h = self.boundsSize().width, -.height
        b = rect or self.bounds()
        w = b.size.width * 0.5
        h = b.size.height * 0.5

        NSColor.whiteColor().set()
        NSRectFill(b)  # not a class

        # set up the points
        n = max(self._n, 4)
        s = 2 * PI / n
        ps = []
        for r in range(n):
            x, y = w, h
            r *= s
            x *= sin(r) + 1.0
            y *= cos(r) + 1.0
            p = NSPoint_t(x, y)
            ps.append(p)

        NSColor.blackColor().set()
        for i, p1 in enumerate(ps):
            for i in range(i + 1, n):
                p2 = ps[i]
                NSBezierPath.strokeLineFromPoint_toPoint_(p1, p2)

        # double check _objc_cache clearance/retention
        pool = NSAutoreleasePool.alloc().init()
        date = NSDate.dateWithTimeIntervalSinceNow_(0.0)
        pool.drain()
        del date


_View = ObjCClass('_View')  # the actual class


class _Delegate_Implementation(object):
    _Delegate = ObjCSubclass('NSObject', '_Delegate')

    @_Delegate.method(b'@' + PyObjectEncoding)
    def init(self, app):
        objc = ObjCInstance(send_super(self, 'init'))
        self._app = app
        return objc  # objc is self

    @_Delegate.method(b'v@')
    def windowWillClose_(self, notification):
        self._app.terminate_(self)


_Delegate = ObjCClass('_Delegate')  # the actual class


def main(timeout=None):

    app = NSApplication.sharedApplication()

    frame = NSMakeRect(10, 10, 500, 400)
    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                              frame,
                              NSWindowStyleMaskUsual,
                              NSBackingStoreBuffered,
                              False)
    window.setTitle_(NSStr('Drawing - Close window to Quit'))

    view = _View.alloc().initWithFrame_(frame, 11)
    window.setContentView_(view)

    delegate = _Delegate.alloc().init(app)
    window.setDelegate_(delegate)

    window.display()
    window.orderFrontRegardless()

    # set up the timeout
    terminating(app, timeout)
    app.run()
#   print('Done')


if __name__ == '__main__':

    import sys

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
