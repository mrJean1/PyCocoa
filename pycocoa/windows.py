
# -*- coding: utf-8 -*-

# MIT License <http://opensource.org/licenses/MIT>
#
# Copyright (C) 2017-2018 -- mrJean1 at Gmail dot com
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

from bases   import _Type1, _Type2
from nstypes import isNone, NSConcreteNotification, NSFalse, NSNone, \
                    NSNotification, NSScreen, NSScrollView, NSTrue, \
                    NSView, NSWindow, _Constants
from oclibs  import NO, NSBackingStoreBuffered, \
                    NSWindowStyleMaskClosable, \
                    NSWindowStyleMaskMiniaturizable, \
                    NSWindowStyleMaskResizable, \
                    NSWindowStyleMaskTitled, \
                    NSWindowStyleMaskUsual, \
                    NSWindowStyleMaskUtilityWindow, YES
from octypes import NSPoint_t, NSRect_t, NSRect4_t, NSSize_t
from runtime import isInstanceOf, ObjCClass, ObjCInstance, \
                    ObjCSubclass, send_super
from utils   import _Globals, bytes2str, instanceof
# from enum  import Enum

try:
    from math import gcd  # Python 3+
except ImportError:
    try:
        from fractions import gcd  # Python 2-
    except ImportError:
        def gcd(a, b):
            while b:
                a, b = b, (a % b)
            return a

__all__ = ('Frame', 'Frame4',
           'MediaWindow',
           'Screen', 'Style',
           'Window', 'WindowDelegate',
           'aspect_ratio',
           'gcd',
           'ns2Window')
__version__ = '18.04.18'

_Cascade = NSPoint_t(25, 25)  # PYCHOK false
_Screen  = NSScreen.alloc().init().mainScreen()


class Frame(_Type1):
    '''Frame class, signature like C{NSRect_t}.
    '''
    _height = 0
    _width  = 0
    _x      = 0
    _y      = 0

    def __init__(self, frame, **attrs):
        '''New frame from another frame.
        '''
        self.frame = frame
        _Type1.__init__( self, **attrs)

    @property
    def frame(self):
        '''Get the C{NS} instance (C{NSRect}).
        '''
        return self.NS

    @frame.setter  # PYCHOK property.setter
    def frame(self, frame):
        if isinstance(frame, (tuple, list)):
            if len(frame) == 2:  # assume (w, h)
                frame = (self._x, self._y) + tuple(frame)
            elif len(frame) != 4:
                raise ValueError('%s invalid: %r' % ('frame', frame))
        else:
            if isinstance(frame, Frame):
                frame = frame.NS
            instanceof(frame, NSRect_t, name='frame')
            frame = (frame.origin.x, frame.origin.x,
                     frame.size.width, frame.size.height)
        self._x, self._y, self._width, self._height = frame

    @property
    def height(self):
        return self._height

    @property
    def NS(self):
        '''Get the C{NS} instance (C{NSRect}).
        '''
        return NSRect4_t(self.x, self.y, self.width, self.height)

    @property
    def width(self):
        return self._width

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class Frame4(Frame):
    '''Frame class, signature like C{NSRect4_t}.
    '''
    def __init__(self, x=0, y=0, w=0, h=0):
        '''New frame from 4-tuple.
        '''
        self.frame = (x, y, w, h)


class Screen(Frame):
    '''Screen frame class.
    '''
    def __init__(self, fraction=0.5):
        '''New (partial) screen frame.
        '''
        f = _Screen.frame()
        if 0.1 < fraction < 1.0:
            # use the lower left quarter of the screen
            w = int(f.size.width * fraction + 0.5)
            h = int(f.size.height * w / f.size.width)
            f = f.origin.x + 10, f.origin.y + 10, w, h
        else:
            f = f.origin.x, f.origin.y, f.size.width, f.size.height
        self.frame = f


class Style(_Constants):  # Enum?
    '''Window style masks.
    '''
    Closable       = NSWindowStyleMaskClosable
    Miniaturizable = NSWindowStyleMaskMiniaturizable  # aka Hidable
#   Movable        = ?
    Resizable      = NSWindowStyleMaskResizable
    Titled         = NSWindowStyleMaskTitled
    Typical        = NSWindowStyleMaskUsual  # all of the above
    Utility        = NSWindowStyleMaskUtilityWindow


class Window(_Type2):
    '''Basic, base window class.
    '''
    _frame     = None
    _isKey     = None
    _isMain    = None
    _ns_uniqID = 0
    _ns_view   = NSNone
    _ratio     = ()

    def __init__(self, title='Main', frame=None, excl=0, auto=False, **attrs):
        '''Create a new window.

        @param title: Window title (string).
        @param frame: Window frame (None, L{Frame}, L{NSRect_t} or L{NSRect4_t}).
        @param excl: Window styles to exclude (L{Style}C{.attribute}).
        @param auto: Release window resource when closed (bool).
        '''
        self.title = bytes2str(title)

        self._frame = Screen(0.5) if frame is None else Frame(frame)
        self._ratio = self._frame.width, self._frame.height

        self.NS = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                                   self.frame.NS,
                                   Style.Typical ^ excl,  # PYCHOK expected
                                   NSBackingStoreBuffered,
                                   NSFalse)  # or False or 0
        self.front(True)
        if auto:
            self.NS.setReleasedWhenClosed_(NSTrue)
        self.delegate = WindowDelegate.alloc().init(self)

        if attrs:  # optional, additional attributes
            super(Window, self).__init__(**attrs)

        # XXX self.NS.setIdentifier_(int2NS(id(self)))

        self._ns_uniqID = u = self.NS.uniqueID()
        if u in _Globals.Windows:
            raise KeyError('%s %r exists: %r' % ('.uniqueID', u,  _Globals.Windows[u]))
        _Globals.Windows[u] = self

        if _Globals.App and not self.app:
            self.app = _Globals.App

    def close(self):
        '''Close this window by a click of the close button.

           @note: The .windowWillClose_ action is invoked iff
                 .windowShouldClose_ returns True.
        '''
        self.NS.performClose_(self.NS)  # XXX self.delegate

    def cascade(self):
        '''Cascade window placement (from the top left corner of the screen).
        '''
        self.NS.cascadeTopLeftFromPoint_(_Cascade)
        _Cascade.x += 25

    @property
    def frame(self):
        '''Get the window frame rectangle (L{Frame}).
        '''
        return self._frame

    def front(self, focus=False):
        '''Order window to front.
        '''
        if focus:
            self.NS.makeKeyAndOrderFront_(None)
        else:
            self.NS.orderFrontRegardless()
        self.NS.display()
        self.NS.orderFront_(None)  # vs .orderOut_(None)

    def full(self, full):
        '''Show or exit full screen window.
        '''
        if full:
            self.NS.enterFullScreenMode_(self.NS.screen())
        else:
            self.NS.exitFullScreenMode_(self.NS.screen())

    def hide(self, hide):
        '''Hide or unhide this window.
        '''
        if hide:  # click the hide/miniaturize button
            self.NS.performMiniaturize_(self.NS)  # XXX self.delegate
        elif self.isHidden:
            self.NS.deminiaturize_(self.NS)

    @property
    def isFull(self):
        '''Get the full screen state (bool).
        '''
        return True if self.NS.isInFullScreenMode() else False

    @property
    def isHidden(self):
        '''Get the hidden/miniaturized state (bool).
        '''
        return True if self.NS.isMiniaturized() else False

    @property
    def isKey(self):
        '''Get key state (bool).
        '''
        return self._isKey  # self.NS.isKeyWindow()

    @property
    def isMain(self):
        '''Get main state (bool).
        '''
        return self._isMain  # self.NS.isMainWindow()

    @property
    def isVisible(self):
        '''Get the visible state (bool).
        '''
        return True if self.NS.isVisible() else False

    @property
    def isZoomed(self):
        '''Get the zoomed state (bool).
        '''
        return True if self.NS.isZoomed() else False

    def limit(self, width=3840, height=4160):
        '''Limit the window's content size.
        '''
        self.NS.setContentMaxSize_(NSSize_t(width, height))

    @property
    def NSview(self):
        '''Get the C{NS} view (C{NSView...}).
        '''
        return self._ns_view

    @NSview.setter  # PYCHOK property.setter
    def NSview(self, ns_view):
        '''Set the C{NS} view (C{NSView...}).
        '''
        if not isNone(ns_view):
            isInstanceOf(ns_view, NSScrollView, NSView, name='ns_view')
            self.NS.setContentView_(ns_view)
        self._ns_view = ns_view

    @property
    def ratio(self):
        '''Get the aspect ratio as (width, height).
        '''
        return self._ratio

    @ratio.setter  # PYCHOK property.setter
    def ratio(self, ratio):
        '''Set the aspect ratio (string "w:h", 2-tuple (width, height)
        or C{NSSize_t}).
        '''
        try:
            r = bytes2str(ratio, dflt=None)
            if r is not None:
                r = map(int, r.split(':'))
            elif isinstance(ratio, (tuple, list)) and len(ratio) == 2:
                r = tuple(ratio)
            else:  # NSSize_t
                r = ratio.width, ratio.height
        except (AttributeError, ValueError):
            raise ValueError('%s invalid: %r' % ('ratio', ratio))

        r = aspect_ratio(*r)
        if r:
            self._ratio = r
            self.NS.setContentAspectRatio_(NSSize_t(r[0], r[1]))

    def zoom(self, zoom):
        '''Zoom or unzoom this window.
        '''
        if (zoom and not self.isZoomed) or (self.isZoomed and not zoom):
            # click the "zoom box", toggles the zoom state
            # <http://developer.apple.com/documentation/appkit/nswindow/1419513-zoom>
            self.NS.performZoom_(self.NS)  # XXX self.delegate

    # Callback methods for WindowDelegate, to be overloaded as needed.
    def windowClose_(self):
        if self.app:
            self.app.windowClose_(self)

    def windowCloseOK_(self):
        # return False if the window should not close
        if self.app:
            return self.app.windowCloseOK_(self)
        else:
            return True

    def windowKey_(self, key):
        self._isKey = key
        if self.app:
            self.app.windowKey_(self if key else None)

    def windowMain_(self, main):
        self._isMain = main
        if self.app:
            self.app.windowMain_(self if main else None)

    def windowResize_(self, size=None):
        # size is None, (w, h) or NSSize_t
        if self.app:
            return self.app.windowResize_(self, size)
        else:
            return size

    def windowZoomOK_(self, frame=None):
        # return False if the window should not toggle zoom
        if self.app:
            return self.app.windowZoomOK_(self, frame)
        else:
            return True


class MediaWindow(Window):
    '''Media window class.
    '''
    def __init__(self, title='Media', fraction=0.5, **kwds):

        super(MediaWindow, self).__init__(title=title, frame=Screen(fraction), **kwds)
        # create the drawable_nsobject NSView for vlc.py, see vlc.MediaPlayer.set_nsobject()
        # for an alternate NSView object with protocol VLCOpenGLVideoViewEmbedding
        # <http://StackOverflow.com/questions/11562587/create-nsview-directly-from-code>
        # <http://GitHub.com/ariabuckles/pyobjc-framework-Cocoa/blob/master/Examples/AppKit/DotView/DotView.py>
        self.NSview = NSView.alloc().initWithFrame_(self.frame.NS)


class _WindowDelegate(object):
    '''An ObjC Delegate class to handle C{NSWindow} events as
       L{Window}.window..._ and L{App}.window..._ method calls.

       @see: C{_AppDelegate} for more Delegate details.
    '''
    _ObjC = ObjCSubclass('NSObject', '_WindowDelegate')

    @_ObjC.method('@P')
    def init(self, window):
        instanceof(window, Window, name='window')
#       self = ObjCInstance(send_message('NSObject', 'alloc'))
        self = ObjCInstance(send_super(self, 'init'))
        self.window = window
        return self

    # Need the following two methods so that a full-screen
    # window can become the main window.  Otherwise it can't,
    # because it has no title bar.
#   @_ObjC.method('Bv')
#   def canBecomeKeyWindow_(self):
#       return self.window.isVisible

#   @_ObjC.method('Bv')
#   def canBecomeMainWindow_(self):
#       return self.window.isVisible

    @_ObjC.method('v@')
    def _ns2w(self, ns):
        w = ns2Window(ns)
        if self.window != w:
            raise AssertionError('%r vs %r' % (self.window, w))

    @_ObjC.method('v@')
    def windowDidBecomeKey_(self, ns_notification):
        self._ns2w(ns_notification)
        self.window.windowKey_(True)

    @_ObjC.method('v@')
    def windowDidBecomeMain_(self, ns_notification):
        self._ns2w(ns_notification)
        self.window.windowMain_(True)
#       if self.isFull:
#           NSMenu.setMenuBarVisible_(False)  # hide

    @_ObjC.method('v@')
    def windowDidResignKey_(self, ns_notification):
        self._ns2w(ns_notification)
        self.window.windowKey_(False)

    @_ObjC.method('v@')
    def windowDidResignMain_(self, ns_notification):
        self._ns2w(ns_notification)
        self.window.windowMain_(False)
#       if self.isFull:
#           NSMenu.setMenuBarVisible_(True)  # show

    @_ObjC.method('v@')
    def windowDidResize_(self, ns_notification):
        self._ns2w(ns_notification)
        size = self.window.windowResize_()  # PYCHOK expected

    @_ObjC.method('B@')
    def windowShouldClose_(self, ns_notification):
        self._ns2w(ns_notification)
        ok = self.window.windowCloseOK_()
        return YES if ok else NO

    @_ObjC.method('B@')
    def windowShouldZoom_toFrame_(self, ns_frame):
        # <http://developer.apple.com/documentation/appkit/
        #       nswindowdelegate/1419533-windowshouldzoom>
        ok = self.window.windowZoomOK_(Frame(ns_frame))
        return YES if ok else NO

    @_ObjC.method('v@')
    def windowWillClose_(self, ns_notification):
        # set the window's delegate to the app's to
        # make method .windowWillClose_ work, see
        # <http://Gist.GitHub.com/kaloprominat/6105220>
        self._ns2w(ns_notification)
        self.window.windowClose_()

#   @_ObjC.method('@@@')
#   def windowWillResize_toSize_(self, ns_window, ns_size):
        # <http://developer.apple.com/documentation/appkit/
        #       nswindowdelegate/1419292-windowwillresize>
#       self._ns2w(ns_window)
#       return ns_size

#   @_ObjC.method('@@@')
#   def windowWillReturnFieldEditor_toObject_(self, ns_window, ns_obj):
#       self._ns2w(ns_window)
#       return NSNone


WindowDelegate = ObjCClass('_WindowDelegate')


def aspect_ratio(width, height):
    '''Return the smallest ratio as 2-tuple (width, height).
    '''
    # video 4:3, 16:9, 21:9 (14:10, 19:10)
    # photo 1:1, 3:3, 4:3, 5:3, 5:4, 7:5, 16:9
    r = gcd(width, height) or ()  # None
    if r and width and height:
        r = width // r, height // r
    return r


def ns2Window(ns):
    '''Get the L{Window} instance for an C{NSWindow} or an
    C{NSNotification} instance.
    '''
    if isInstanceOf(ns, NSWindow):
        u = ns.uniqueID()
    elif isInstanceOf(ns, NSConcreteNotification, NSNotification, ns='ns'):
        u = ns.object().uniqueID()
    try:
        w = _Globals.Windows[u]
        if w._ns_uniqID == u:
            return w
        t = '%r of %r' % (w._ns_uniqID, w)
    except KeyError:
        t = None
    raise AssertionError('%s %s %r vs %s' % (ns, '.uniqueID', u, t))


if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)
