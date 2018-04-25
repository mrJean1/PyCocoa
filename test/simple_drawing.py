
# encoding: utf-8

# Reworked from <http://GitHub.com/ActiveState/code/tree/master/recipes/Python/303058_Simple_PyObjC_Example>
# showing an NSWindow with a basic, drawable NSView.

from math import sin, cos, pi as PI
# all imports listed explicitly to help PyChecker
from pycocoa import NSApplication, NSBackingStoreBuffered, \
                    NSBezierPath, NSColor, NSMakeRect, NSPoint_t, \
                    NSStr, NSWindow, NSWindowStyleMaskUsual, \
                    PyObjectEncoding, ObjCClass, ObjCInstance, \
                    ObjCSubclass, send_super
from pycocoa.oslibs import libAppKit

__version__ = '18.04.23'

NSRectFill = libAppKit.NSRectFill


class _View_Implementation(object):
    _View = ObjCSubclass('NSView', '_View')

    @_View.method(b'@' + PyObjectEncoding * 2)
    def initWithFrame_(self, frame, n):
        self = ObjCInstance(send_super(self, 'initWithFrame:', frame))
        self.n = n
        # set up the angles loop
        step = 2 * PI / self.n
        self.loop = [i * step for i in range(self.n)]
        return self

    @_View.method('v@')
    def drawRect_(self, rect):

        # w, h = self.boundsSize().width, -.height
        b = rect or self.bounds()
        w = b.size.width * 0.5
        h = b.size.height * 0.5

        def _x(t, w):
            return (sin(t) + 1.) * w

        def _y(t, h):
            return (cos(t) + 1.) * h

        NSColor.whiteColor().set()
        NSRectFill(b)  # not a class

        NSColor.blackColor().set()
        for f in self.loop:
            for g in self.loop:
                p1 = NSPoint_t(_x(f, w), _y(f, h))
                p2 = NSPoint_t(_x(g, w), _y(g, h))
                NSBezierPath.strokeLineFromPoint_toPoint_(p1, p2)


_View = ObjCClass('_View')  # the actual class


class _Delegate_Implementation(object):
    _Delegate = ObjCSubclass('NSObject', '_Delegate')

    @_Delegate.method(b'@' + PyObjectEncoding)
    def init(self, app):
        self = ObjCInstance(send_super(self, 'init'))
        self.app = app
        return self

    @_Delegate.method(b'v@')
    def windowWillClose_(self, notification):
        self.app.terminate_(self)


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

    view = _View.alloc().initWithFrame_(frame, 10)
    window.setContentView_(view)

    delegate = _Delegate.alloc().init(app)
    window.setDelegate_(delegate)

    window.display()
    window.orderFrontRegardless()

    # set up the timeout
    if timeout is not None:
        try:  # PyCocoa/test
            from test import terminating
            terminating(app, timeout)
        except ImportError:
            pass

    app.run()
#   print('Done')


if __name__ == '__main__':

    import sys

    if len(sys.argv) > 1:
        main(sys.argv.pop(1))
    else:
        main()
