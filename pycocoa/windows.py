
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

'''Types L{Window}, L{MediaWindow}, L{Screen}, L{Style}, wrapping ObjC C{NSWindow}, etc.
'''
# all imports listed explicitly to help PyChecker
from bases    import _Type2
from geometry import Rect
from nstypes  import isNone, NSConcreteNotification, NSFalse, NSNone, \
                     NSNotification, NSScreen, NSScrollView, NSTrue, \
                     NSView, NSWindow
from octypes  import NSPoint_t, NSSize_t
from oslibs   import NO, NSBackingStoreBuffered, \
                     NSWindowStyleMaskClosable, \
                     NSWindowStyleMaskMiniaturizable, \
                     NSWindowStyleMaskResizable, \
                     NSWindowStyleMaskTitled, \
                     NSWindowStyleMaskUsual, \
                     NSWindowStyleMaskUtilityWindow, YES
from runtime  import isInstanceOf, ObjCClass, ObjCInstance, \
                     ObjCSubclass, send_super
from utils    import aspect_ratio, _Constants, _Globals, \
                     bytes2str, instanceof, _Types
# from enum   import Enum

__all__ = ('MediaWindow',
           'NSWindowDelegate',
           'Screen', 'Style',
           'Window',
           'ns2Window')
__version__ = '18.04.26'

_Cascade = NSPoint_t(25, 25)  # PYCHOK false
_Screen  = NSScreen.alloc().init().mainScreen()


class Screen(Rect):
    '''Screen Python Type, wrapping ObjC C{NSRect_t}.
    '''
    def __init__(self, fraction=0.5, cascade=10):
        '''New, partial screen L{Rect}.

           @keyword fraction: Size of the screen (float).
           @keyword cascade: Shift from lower left corner (float or int).

           @raise ValueError: Invalid I{fraction} value.
        '''
        f = _Screen.frame()
        if 0.1 < fraction < 1.0:
            # use the lower left side of the screen
            w = int(f.size.width * fraction + 0.5)
            h = int(f.size.height * w / f.size.width)
            # avoid cascading window off-screen
            c = min(max(0, cascade), min(f.size.width, f.size.height))
            f = f.origin.x + c, f.origin.y + c, w, h
        elif fraction < 0 or fraction > 1:
            raise ValueError('%s invalid: %.2f' % ('fraction', fraction))
        self.rect = f


class Style(_Constants):  # Enum?
    '''Window style mask constants.
    '''
    Closable       = NSWindowStyleMaskClosable
    Miniaturizable = NSWindowStyleMaskMiniaturizable  # aka Hidable
#   Movable        = ?
    Resizable      = NSWindowStyleMaskResizable
    Titled         = NSWindowStyleMaskTitled
    Typical        = NSWindowStyleMaskUsual  # all of the above
    Utility        = NSWindowStyleMaskUtilityWindow


class Window(_Type2):
    '''Basic, base window Python Type, wrapping ObjC C{NSWindow}.
    '''
    _frame     = None
    _isKey     = None
    _isMain    = None
    _ns_uniqID = 0
    _ns_view   = NSNone
    _ratio     = ()

    def __init__(self, title='Main', frame=None, excl=0, auto=False, **kwds):
        '''Create a new L{Window}.

        @keyword title: Window title (str).
        @keyword frame: Window frame (L{Rect}, L{NSRect_t}, L{NSRect4_t}, or None).
        @keyword excl: Window styles to exclude (L{Style}C{.attribute}).
        @keyword auto: Release window resource when closed (bool).
        @keyword kwds: Optional, additional keyword arguments.
        '''
        self._frame = Screen(0.5) if frame is None else Rect(frame)
        self._ratio = self._frame.width, self._frame.height

        self.NS = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                                   self.frame.NS,
                                   Style.Typical ^ excl,  # PYCHOK expected
                                   NSBackingStoreBuffered,
                                   NSFalse)  # or False or 0
        self.title = bytes2str(title)
        self.front(True)

        if kwds:
            super(Window, self).__init__(**kwds)

        # XXX self.NS.setIdentifier_(int2NS(id(self)))
        self._ns_uniqID = u = self.NS.uniqueID()
        if u in _Globals.Windows:
            raise KeyError('%s %r exists: %r' % ('.uniqueID', u,  _Globals.Windows[u]))
        _Globals.Windows[u] = self

        if _Globals.App and not self.app:
            self.app = _Globals.App

        if auto:
            self.NS.setReleasedWhenClosed_(NSTrue)
        self.NSdelegate = NSWindowDelegate.alloc().init(self)

    def close(self):
        '''Close this window (by a click of the close button).

           @note: The C{.windowWillClose_} action is invoked iff
                 C{.windowShouldClose_} returns True.
        '''
        self.NS.performClose_(self.NS)  # XXX self.delegate

    def cascade(self):
        '''Cascade window placement (from the top left screen corner).
        '''
        self.NS.cascadeTopLeftFromPoint_(_Cascade)
        _Cascade.x += 25

    @property
    def frame(self):
        '''Get this window's frame (L{Rect}).
        '''
        return self._frame

    def front(self, focus=False):
        '''Order this window to the front.

           @keyword focus: Make this window C{Key} (bool).
        '''
        if focus:
            self.NS.makeKeyAndOrderFront_(None)
        else:
            self.NS.orderFrontRegardless()
        self.NS.display()
        self.NS.orderFront_(None)  # vs .orderOut_(None)

    def full(self, full):
        '''Enter or exit full screen mode for this window.

           @param full: Enter or exit (bool).
        '''
        if full:
            self.NS.enterFullScreenMode_(self.NS.screen())
        else:
            self.NS.exitFullScreenMode_(self.NS.screen())

    def hide(self, hide):
        '''Hide or unhide this window.

           @param hide: Hide or show (bool).
        '''
        if hide:  # click the hide/miniaturize button
            self.NS.performMiniaturize_(self.NS)  # XXX self.delegate
        elif self.isHidden:
            self.NS.deminiaturize_(self.NS)

    @property
    def isFull(self):
        '''Get this window's full screen state (bool).
        '''
        return True if self.NS.isInFullScreenMode() else False

    @property
    def isHidden(self):
        '''Get this window's hidden state (bool).
        '''
        return True if self.NS.isMiniaturized() else False

    @property
    def isKey(self):
        '''Get this window's C{Key} state (bool).
        '''
        return self._isKey  # self.NS.isKeyWindow()

    @property
    def isMain(self):
        '''Get this window's C{Main} state (bool).
        '''
        return self._isMain  # self.NS.isMainWindow()

    @property
    def isVisible(self):
        '''Get this window's visible state (bool).
        '''
        return True if self.NS.isVisible() else False

    @property
    def isZoomed(self):
        '''Get this window's zoomed state (bool).
        '''
        return True if self.NS.isZoomed() else False

    def limit(self, width=3840, height=4160):
        '''Limit this window's content size.

           @keyword width: Width limit (float or int).
           @keyword height: Height limit (float or int).
        '''
        self.NS.setContentMaxSize_(NSSize_t(width, height))

    @property
    def NSview(self):
        '''Get this window's C{NS} view (C{NSView...}).
        '''
        return self._ns_view

    @NSview.setter  # PYCHOK property.setter
    def NSview(self, ns_view):
        '''Set this window's C{NS} view (C{NSView...}).
        '''
        if not isNone(ns_view):
            isInstanceOf(ns_view, NSScrollView, NSView, name='ns_view')
            self.NS.setContentView_(ns_view)
        self._ns_view = ns_view

    @property
    def ratio(self):
        '''Get this window's aspect ratio as 2-tuple (width, height).
        '''
        return self._ratio

    @ratio.setter  # PYCHOK property.setter
    def ratio(self, ratio):
        '''Set this window's aspect ratio.

           @param ratio: New ratio (L{Size}, 2-tuple (width, height), str("w:h") or C{NSSize_t}).
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
        '''Toggle, zoom or un-zoom this window.

           @param zoom: Zoom or un-zoom (bool) or C{None} to toggle.
        '''
        if zoom is None or (zoom and not self.isZoomed) \
                        or (self.isZoomed and not zoom):
            # click the "zoom box", toggles the zoom state
            # <http://Developer.Apple.com//documentation/appkit/nswindow/1419513-zoom>
            self.NS.performZoom_(self.NS)  # XXX self.delegate

    # Callback methods from NSWindowDelegate, to be overloaded as needed.
    def windowClose_(self):
        '''Closing I{window} callback.
        '''
        if self.app:
            self.app.windowClose_(self)

    def windowCloseOK_(self):
        '''Is it OK? to close I{window} callback.

           @return: True if OK to close, False otherwise.
        '''
        if self.app:
            return self.app.windowCloseOK_(self)
        else:
            return True

    def windowKey_(self, key):
        '''Callback I{window} becomes/resigns C{Key}.

           @param key: Make or un-make C{Key} (bool).
        '''
        self._isKey = bool(key)
        if self.app:
            self.app.windowKey_(self if key else None)

    def windowMain_(self, main):
        '''Callback I{window} becomes/resigns C{Main}.

           @param main: Make or un-make C{Main} (bool).
        '''
        self._isMain = bool(main)
        if self.app:
            self.app.windowMain_(self if main else None)

    def windowPrint_(self):
        '''Print I{window} callback.
        '''
        if self.app:
            self.app.windowPrint_(self)

    def windowResize_(self):
        '''Resizing I{window} callback.
        '''
        if self.app:
            self.app.windowResize_(self)

    def windowZoomOK_(self, frame=None):
        '''Is it OK? to toggle zoom I{window} callback.

           @keyword frame: The frame to zoom to (L{Rect}).

           @return: True if OK to toggle, False otherwise.
        '''
        if self.app:
            return self.app.windowZoomOK_(self, frame)
        else:
            return True


class MediaWindow(Window):
    '''Media window Python Type, wrapping ObjC C{NSWindow/NSView}.
    '''
    def __init__(self, title='Media', fraction=0.5, **kwds):
        '''Create a L{MediaWindow}.

           @keyword title: Window name or title (string).
           @keyword fraction: Window size as fraction of the screen (float).
           @keyword kwds: Optional, additional keyword arguments, see L{Window}.
        '''
        super(MediaWindow, self).__init__(title=title, frame=Screen(fraction), **kwds)
        # create the drawable_nsobject NSView for vlc.py, see vlc.MediaPlayer.set_nsobject()
        # for an alternate NSView object with protocol VLCOpenGLVideoViewEmbedding
        # <http://StackOverflow.com/questions/11562587/create-nsview-directly-from-code>
        # <http://GitHub.com/ariabuckles/pyobjc-framework-Cocoa/blob/master/Examples/AppKit/DotView/DotView.py>
        self.NSview = NSView.alloc().initWithFrame_(self.frame.NS)


class _NSWindowDelegate(object):
    '''An ObjC-callable C{NSDelegate} class to handle C{NSWindow} events
       as L{Window}.window..._ and L{App}.window..._ callback calls.

       @see: The C{_NSApplicationDelegate} for more C{NSDelegate} details.
    '''
    _ObjC = ObjCSubclass('NSObject', '_NSWindowDelegate')

    @_ObjC.method('@P')
    def init(self, window):
        '''Initialize the allocated C{NSWindowDelegate}.

           @note: I{MUST} be called as C{.alloc().init(...)}.
        '''
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
        '''ObjC callback to handle C{NSWindow} events.
        '''
        self._ns2w(ns_notification)
        self.window.windowKey_(True)

    @_ObjC.method('v@')
    def windowDidBecomeMain_(self, ns_notification):
        '''ObjC callback to handle C{NSWindow} events.
        '''
        self._ns2w(ns_notification)
        self.window.windowMain_(True)
#       if self.isFull:
#           NSMenu.setMenuBarVisible_(False)  # hide

    @_ObjC.method('v@')
    def windowDidResignKey_(self, ns_notification):
        '''ObjC callback to handle C{NSWindow} events.
        '''
        self._ns2w(ns_notification)
        self.window.windowKey_(False)

    @_ObjC.method('v@')
    def windowDidResignMain_(self, ns_notification):
        '''ObjC callback to handle C{NSWindow} events.
        '''
        self._ns2w(ns_notification)
        self.window.windowMain_(False)
#       if self.isFull:
#           NSMenu.setMenuBarVisible_(True)  # show

    @_ObjC.method('v@')
    def windowDidResize_(self, ns_notification):
        '''ObjC callback to handle C{NSWindow} events.
        '''
        self._ns2w(ns_notification)
        self.window.windowResize_()

    @_ObjC.method('v@')
    def windowPrint_(self, ns_notification):
        '''ObjC callback to handle C{NSWindow} events.
        '''
        self._ns2w(ns_notification)
        self.window.windowPrint_()
        # self.window.NS.printWindow_(?) ?

    @_ObjC.method('B@')
    def windowShouldClose_(self, ns_notification):
        '''ObjC callback to handle C{NSWindow} events.
        '''
        self._ns2w(ns_notification)
        ok = self.window.windowCloseOK_()
        return YES if ok else NO

    @_ObjC.method('B@')
    def windowShouldZoom_toFrame_(self, ns_frame):
        '''ObjC callback to handle C{NSWindow} events.
        '''
        # <http://Developer.Apple.com//documentation/appkit/
        #       nswindowdelegate/1419533-windowshouldzoom>
        ok = self.window.windowZoomOK_(Rect(ns_frame))
        return YES if ok else NO

    @_ObjC.method('v@')
    def windowWillClose_(self, ns_notification):
        '''ObjC callback to handle C{NSWindow} events.
        '''
        # set the window's delegate to the app's to
        # make method .windowWillClose_ work, see
        # <http://Gist.GitHub.com/kaloprominat/6105220>
        self._ns2w(ns_notification)
        self.window.windowClose_()

#   @_ObjC.method('@@@')
#   def windowWillResize_toSize_(self, ns_window, ns_size):
        # <http://Developer.Apple.com//documentation/appkit/
        #       nswindowdelegate/1419292-windowwillresize>
#       self._ns2w(ns_window)
#       return ns_size

#   @_ObjC.method('@@@')
#   def windowWillReturnFieldEditor_toObject_(self, ns_window, ns_obj):
#       self._ns2w(ns_window)
#       return NSNone


NSWindowDelegate = ObjCClass('_NSWindowDelegate')


def ns2Window(ns):
    '''Get the L{Window} instance for an ObjC C{NSWindow} or
       C{NSNotification} instance.

       @param ns: The ObjC instance (C{NS...}).

       @return: The window instance (L{Window}).

       @raise AssertionError: Mismatched instances.

       @raise AttributeError: Unexpected I{ns} type.

       @raise TypeError: Invalid I{ns} type.
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


_Types.Window = NSWindow._Type = Window
_Types.MediaWindow             = MediaWindow

if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)
