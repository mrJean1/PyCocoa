
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Types L{AutoResize}, L{Window}, L{MediaWindow}, L{Screen},
L{WindowStyle}, wrapping ObjC C{NSWindow}, etc.

@var AutoResize: AutoResize options (C{mask}, wrapping C{NSAutoresizingMaskOptions}).
@var AutoResize.HeightSizable: 0x10
@var AutoResize.MaxXMargin: 0x4
@var AutoResize.MaxYMargin: 0x20
@var AutoResize.MinXMargin: 0x1
@var AutoResize.MinYMargin: 0x8
@var AutoResize.NotSizable: 0x0
@var AutoResize.Sizable: 0x12
@var AutoResize.WidthSizable: 0x2

@var BezelStyle: Bezel style constants (C{int}).
@var BezelStyle.Circular: 7
@var BezelStyle.Disclosure: 5
@var BezelStyle.HelpButton: 9
@var BezelStyle.Inline: 15
@var BezelStyle.Recessed: 13
@var BezelStyle.RegularSquare: 2
@var BezelStyle.Rounded: 1
@var BezelStyle.RoundedDisclosure: 14
@var BezelStyle.RoundRect: 12
@var BezelStyle.ShadowlessSquare: 6
@var BezelStyle.SmallSquare: 10
@var BezelStyle.TexturedRounded: 11
@var BezelStyle.TexturedSquare: 8

@var Border: Border type constants (C{int}).
@var Border.Bezel: 2
@var Border.Groove: 3
@var Border.Line: 1
@var Border.No: 0

@var WindowStyle: Window style constants (C{mask}).
@var WindowStyle.Closable: 0x2
@var WindowStyle.Miniaturizable: 0x4
@var WindowStyle.Resizable: 0x8
@var WindowStyle.Titled: 0x1
@var WindowStyle.Typical: 0xf
@var WindowStyle.Utility: 0x10
'''
from pycocoa.bases import _Type2
from pycocoa.geometry import Rect
from pycocoa.internals import _Dmain_, bytes2str, _Constants, _fmt_invalid, \
                              _fmt, _Globals, _Ints, property_RO, proxy_RO
from pycocoa.lazily import _ALL_LAZY, _isPython3, _Types
from pycocoa.nstypes import isNone, NSConcreteNotification, NSFont, \
                            NSImageView, NSMain, NSNotification, \
                            NSScreen, NSScrollView, _NSStr, NSTableView, \
                            nsTextSize3, NSTextView, NSView, NSWindow
from pycocoa.octypes import NSIntegerMax, NSPoint_t, NSSize_t
from pycocoa.oslibs import NO, NSBackingStoreBuffered, \
                           NSWindowStyleMaskClosable, \
                           NSWindowStyleMaskMiniaturizable, \
                           NSWindowStyleMaskResizable, \
                           NSWindowStyleMaskTitled, \
                           NSWindowStyleMaskUsual, \
                           NSWindowStyleMaskUtilityWindow, YES
from pycocoa.runtime import isObjCInstanceOf, ObjCDelegate, _ObjCDelegate, \
                            ObjCInstance, retain, send_super_init
from pycocoa.screens import Frame, Screen, Screens
from pycocoa.utils import aspect_ratio, isinstanceOf, _text_title2

# from enum import Enum

__all__ = _ALL_LAZY.windows
__version__ = '25.03.18'


class AutoResizeError(ValueError):
    '''C{AutoResize} option error.
    '''
    pass


# <https://Developer.Apple.com/documentation/appkit/nsautoresizingmaskoptions>
class AutoResize(_Constants):  # Enum?
    '''AutoResize options (C{mask}, wrapping C{NSAutoresizingMaskOptions}).
    '''
    HeightSizable = 16  # NSViewHeightSizable
    MaxXMargin    =  4  # NSViewMaxXMargin
    MaxYMargin    = 32  # NSViewMaxYMargin
    MinXMargin    =  1  # NSViewMinXMargin
    MinYMargin    =  8  # NSViewMinYMargin
    NotSizable    =  0  # NSViewNotSizable
    Sizable       = 18  # NSViewHeightSizable | NSViewWidthSizable
    WidthSizable  =  2  # NSViewWidthSizable

AutoResize = AutoResize()  # PYCHOK AutoResize options


def autoResizes(*options):
    '''Return a combination of auto resize options, specified by name.

       @param options: Option names (I{all positional}), case-insensitive.

       @return: Combined options (L{AutoResize}s C{mask}).

       @raise AutoResizeError: One or more I{options} are invalid.
    '''
    M, x = AutoResize._masks(*options)
    if x is None:
        return M
    raise AutoResizeError(_fmt_invalid(options=x))


# <https://Developer.Apple.com/documentation/appkit/nsbezelstyle>
class BezelStyle(_Constants):  # Enum?
    '''Bezel style constants (C{int}).
    '''
    Circular          =  7  # NSCircularBezelStyle
    Disclosure        =  5  # NSDisclosureBezelStyle
    HelpButton        =  9  # NSHelpButtonBezelStyle
    Inline            = 15  # NSInlineBezelStyle
    Recessed          = 13  # NSRecessedBezelStyle
    RegularSquare     =  2  # NSRegularSquareBezelStyle
    Rounded           =  1  # NSRoundedBezelStyle
    RoundedDisclosure = 14  # NSBezelStyleRoundedDisclosure
    RoundRect         = 12  # NSRoundRect
    ShadowlessSquare  =  6  # NSShadowlessSquareBezelStyle
    SmallSquare       = 10  # NSSmallSquareBezelStyle
    TexturedRounded   = 11  # NSBezelStyleTexturedRounded
    TexturedSquare    =  8  # NSTexturedSquareBezelStyle

BezelStyle = BezelStyle()  # PYCHOK bezel style constants


# <https://Developer.Apple.com/documentation/appkit/nsbordertype>
class Border(_Constants):  # Enum?
    '''Border type constants (C{int}).
    '''
    Bezel  = 2  # NSBezelBorder
    Groove = 3  # NSGrooveBorder
    Line   = 1  # NSLineBorder
    No     = 0  # NSNoBorder

Border = Border()  # PYCHOK border type constants


class Window(_Type2):
    '''Basic window Python Type, wrapping ObjC C{NSWindow}.
    '''
    _auto     = False
    _frame    = None
    _isKey    = None  # True or False
    _isMain   = None  # True or False
    _NSuniqID = 0
    _NSview   = None
    _PMview   = None
    _untrans  = None

    def __init__(self, title='Main', screen=None, fraction=0.5,
                                     frame=None, excl=0, auto=False, **kwds):
        '''Create a new L{Window}.

           @keyword title: Window title (C{str}).
           @keyword screen: The screen to place the window on (C{int}) or
                            C{None} for the current one.  Use C{screen=0}
                            for the built-in screen or C{screen=1} for the
                            first external monitor, etc.
           @keyword fraction: Window size as fraction of the screen (C{float}),
                              defining the window C{B{frame}}.
           @keyword frame: The window's origin and I{content} size (L{Rect},
                           L{NSRect_t}, L{NSRect4_t}), overriding B{C{fraction}}.
           @keyword excl: Window I{styles} to exclude (L{WindowStyle}C{.attribute}).
           @keyword auto: Release window resource when closed (C{bool}).
           @keyword kwds: Optional, additional keyword arguments.

           @raise WindowError: Unique C{Id} exists.
        '''
        ns = NSWindow.alloc()
        t = (WindowStyle.Typical ^ excl,  # PYCHOK expected
             NSBackingStoreBuffered, NO)
        if frame is None:
            f  = Frame(screen, fraction=fraction)
            ns = ns.initWithContentRect_styleMask_backing_defer_
        else:  # for .tables.TableWindow
            f  = Frame(frame)
            ns = ns.initWithContentRect_styleMask_backing_defer_screen_
            t += Screens.Main.NS,  # like .tables.TableWindow
        self._frame  = f
        self.NS = ns = ns(f.NS, *t)

        self.title = bytes2str(title)
        self.front(True)
        if kwds:
            super(Window, self).__init__(**kwds)

        # XXX self.NS.setIdentifier_(int2NS(id(self)))
        self._NSuniqID = u = ns.uniqueID()
        if u in _Globals.Windows:
            t = _fmt('%s %r exists: %r', '.uniqueID', u, _Globals.Windows[u])
            raise WindowError(t)
        elif u:
            _Globals.Windows[u] = self

        if _Globals.App and not self.app:
            self.app = _Globals.App

        if auto:
            ns.setReleasedWhenClosed_(YES)
            self._auto = True

        self.NSdelegate = retain(NSWindowDelegate.alloc().init(self))

    @property
    def alpha(self):
        '''Get this window's alpha value (C{float}).
        '''
        return float(self.NS.alphaValue())

    @alpha.setter  # PYCHOK property.setter
    def alpha(self, alpha):
        '''Set this window's alpha value (C{float}, 0.0..1.0).

           @see: Properties L{opaque} and L{transparent}.
        '''
        self.NS.setAlphaValue_(max(0.0, min(1.0, float(alpha))))

    def close(self):
        '''Close this window (by a click of the close button).

           @note: The C{.windowWillClose_} action is invoked iff
                 C{.windowShouldClose_} returns True.
        '''
        self.NS.performClose_(self.NS)  # XXX self.delegate

    def cascade(self):
        '''Cascade window placement (from the top left screen corner).
        '''
        p = self.screen._NScascade
        if p is None:
            self.screen._NScascade = p = NSPoint_t(25, 25)
        self.NS.cascadeTopLeftFromPoint_(p)
        p.x += 25
        if p.x > self.frame.center.x:
            p.x = 25

    @property
    def frame(self):
        '''Get this window's frame (L{Rect}).
        '''
        return self._frame  # or Frame(self.NS.frame())

    @frame.setter  # PYCHOK property.setter!
    def frame(self, frame):
        '''Set the frame of this window (L{Rect}, C{NSRect_t}, C{NSRect4_t}, or None).
        '''
        if frame:
            self._frame.rect = Frame(frame)
        # self.NS.setFrame_(self._frame.NS)
        self.NS.setFrame_display_(self._frame.NS, YES)

    def front(self, focus=False):
        '''Order this window to the front.

           @keyword focus: Make this window C{Key} (C{bool}).
        '''
        ns = self.NS
        if focus:
            ns.makeKeyAndOrderFront_(None)
        else:
            ns.orderFrontRegardless()
        ns.display()
        ns.orderFront_(None)  # vs .orderOut_(None)

    def full(self, full):
        '''Enter or exit full screen mode for this window.

           @param full: Enter or exit (C{bool}).
        '''
        ns = self.NS  # self.NSview
        f_ = ns.enterFullScreenMode_ if full else \
             ns.exitFullScreenMode_
        return bool(f_(ns.screen()))

    def hide(self, hide):
        '''Hide or unhide this window.

           @param hide: Hide or show (C{bool}).
        '''
        ns = self.NS
        if hide:  # click the hide/miniaturize button
            ns.performMiniaturize_(ns)  # XXX self.delegate
        elif self.isHidden:
            ns.deminiaturize_(ns)

    @property_RO
    def isBuiltIn(self):
        '''Is this window's screen built-in (C{bool} or C{None} if unknown)?
        '''
        return self.screen.isBuiltIn if self.screen else None

    @property_RO
    def isExternal(self):
        '''Is this window's screen external (C{bool} or C{None} if unknown)?
        '''
        return self.screen.isBuiltIn if self.screen else None

    @property_RO
    def isFull(self):
        '''Get this window's full screen mode or zoomed state (C{bool} or C{None} if unknown).
        '''
        f = self.isFullScreen
        z = self.isZoomed
        return z if f is None else (
               f if z is None else (f or z))

    @property_RO
    def isFullScreen(self):
        '''Get this window's full screen mode (C{bool} or C{None} if unknown).
        '''
        # XXX unreliable if this window.isExternal
        ns = self.NSview
        return bool(ns.isInFullScreenMode()) if ns else None

    @property_RO
    def isHidden(self):
        '''Get this window's hidden state (C{bool}).
        '''
        return bool(self.NS.isMiniaturized())

    @property_RO
    def isKey(self):
        '''Get this window's C{Key} state (C{bool}).
        '''
        return self._isKey  # self.NS.isKeyWindow()

    @property_RO
    def isMain(self):
        '''Get this window's C{Main} state (C{bool}).
        '''
        return self._isMain  # self.NS.isMainWindow()

    @property_RO
    def isPrintable(self):
        '''Get this window's printable state (C{bool}).
        '''
        return bool(self.PMview)

    @property_RO
    def isVisible(self):
        '''Get this window's visible state (C{bool}).
        '''
        return bool(self.NS.isVisible())

    @property_RO
    def isZoomed(self):
        '''Get this window's zoomed state (C{bool}).
        '''
        return bool(self.NS.isZoomed())

    def limit(self, width=3840, height=4160):
        '''Limit this window's content size.

           @keyword width: Width limit (C{float} or C{int}).
           @keyword height: Height limit (C{float} or C{int}).
        '''
        self.NS.setContentMaxSize_(NSSize_t(width, height))

    @property
    def NSview(self):
        '''Get this window's view (C{NSView...}).
        '''
        return self._NSview or NSMain.Null  # self.NS.contentView()

    @NSview.setter  # PYCHOK property.setter
    def NSview(self, ns_view):
        '''Set this window's view (C{NSView...}).
        '''
        if ns_view and not isNone(ns_view):
            isObjCInstanceOf(ns_view, NSScrollView, NSView, raiser='ns_view')
            self.NS.setContentView_(ns_view)
        self._NSview = ns_view  # or NSMain.Null

    @property
    def opaque(self):
        '''Get this window's opaque setting (C{bool}).
        '''
        return bool(self.NS.isOpaque())

    @opaque.setter  # PYCHOK property.setter
    def opaque(self, opaque):
        '''Make this window opaque or not (C{bool}).
        '''
        self.NS.setOpaque_(YES if opaque else NO)

    @property
    def PMview(self):
        '''Get this window's print view (C{NSView...}).
        '''
        return self._PMview  # or NSMain.Null

    @PMview.setter  # PYCHOK property.setter
    def PMview(self, ns_view):
        '''Set this window's print view (C{NSView...}).
        '''
        if not (ns_view and isObjCInstanceOf(
                ns_view, NSImageView, NSTableView, NSTextView, NSView)):
            ns_view = None
        self._PMview = ns_view

    @property
    def ratio(self):
        '''Get this window's contents' aspect ratio (2-tuple C{(w, h)}).
        '''
        r = self.NS.contentAspectRatio()
        return int(r.width), int(r.height)

    @ratio.setter  # PYCHOK property.setter
    def ratio(self, ratio):
        '''Set this window's contents' aspect ratio.

           @param ratio: New ratio (L{Size}, 2-tuple C{(w, h)}, C{str("w:h")} or C{NSSize_t}).

           @raise WindowError: Invalid I{ratio}.
        '''
        r = aspect_ratio(ratio, Error=WindowError)
        if r:
            self.NS.setContentAspectRatio_(NSSize_t(*r))
            # self.NS.setViewsNeedDisplay_(YES)
            # self.NSview.setNeedsDisplay_(YES)

    @property
    def screen(self):
        '''Get the screen of this window (L{Screen}) or C{None}
           if this window is off-screen.
        '''
        s = self.NS.screen()
        return Screen(s) if s else None

    @screen.setter  # PYCHOK property.setter
    def screen(self, screen):
        '''Move this window to an other screen.

           @param screen: The screen to move to (L{Screen}) or C{None}
                          for the current C{Screens.Main} screen or an
                          C{int} for any of the available C{Screens}.
        '''
        if screen is None or isinstance(screen, _Ints):
            screen = Screens(screen)
        if isinstanceOf(screen, Screen):
            f = screen.frame
        elif isObjCInstanceOf(screen, NSScreen, raiser='screen'):
            f = screen.frame()
        self.frame.origin = f.origin
        self.NS.setFrame_display_(self.frame.NS, YES)
        self.windowScreen_(True)

    @property
    def transparent(self):
        '''Has this window been made transparent (C{bool})?
        '''
        return self._untrans is not None

    @transparent.setter  # PYCHOK property.setter
    def transparent(self, transparent):
        '''Make this window transparent or undo (C{bool}).

           @see: U{Custom<https://www.CocoaWithLove.com/2008/12/drawing-custom-window-on-mac-os-x.html>},
                 U{transparent<https://StackoOverflow.com/questions/34531118/
                 how-can-i-create-a-window-with-transparent-background-with-swift-on-osx>} window on
                 OS X, U{RoundTransparentWindow<https://PyObjC.ReadTheDocs.io/en/latest/examples/
                 Cocoa/AppKit/RoundTransparentWindow/index.html>} and U{NSThemeFrame
                 <https://Parmanoir.com/Custom_NSThemeFrame>}.
        '''
        def _nset(ns, opaque, shadow, bgColor):
            ns.setOpaque_(opaque)
            ns.setHasShadow_(shadow)
            ns.setBackgroundColor_(bgColor)

        ns, p = self.NS, self.transparent
        if transparent and not p:  # make
            from pycocoa.colors import GrayScaleColors
            self._untrans = ns.isOpaque(), ns.hasShadow(), ns.backgroundColor()
            _nset(ns, NO, NO, GrayScaleColors.Clear)
        elif p and not transparent:  # undo
            _nset(ns, *self._untrans)
            self._untrans = None

    @property
    def transparentTitlebar(self):
        '''Is this window's title bar transparent (C{bool})?
        '''
        return bool(self.NS.titlebarAppearsTransparent())

    @transparentTitlebar.setter  # PYCHOK property.setter
    def transparentTitlebar(self, transparent):
        '''Make this window title bar transparent or undo (C{bool}).
        '''
        self.NS.setTitlebarAppearsTransparent_(YES if transparent else NO)

    def zoom(self, zoom):
        '''Toggle, zoom or un-zoom this window.

           @param zoom: Use C{True} to zoom, C{False} to un-zoom or C{None} to toggle.
        '''
        if zoom is None or self.isZoomed is bool(not bool(zoom)):
            # click the "zoom box", toggles the zoom state
            # <https://Developer.Apple.com/documentation/appkit/nswindow/1419513-zoom>
            self.NS.performZoom_(self.NS)  # XXX self.delegate

    # Callback methods from NSWindowDelegate, to be overloaded as needed.
    def windowClose_(self):
        '''Closing I{window} callback.
        '''
        if self.app:
            self.app.windowClose_(self)
        if self._auto:
            self.NSdelegate.release()

    def windowCloseOK_(self):
        '''Callback Is it OK to close I{window}?

           @return: C{True} if OK to close, C{False} otherwise.
        '''
        return self.app.windowCloseOK_(self) if self.app else True

    def windowKey_(self, key):
        '''Callback I{window} becomes/resigns C{Key}.

           @param key: Make or un-make C{Key} (C{bool}).
        '''
        self._isKey = bool(key)
        if self.app:
            self.app.windowKey_(self if key else None)

    def windowMain_(self, main):
        '''Callback I{window} becomes/resigns C{Main}.

           @param main: Make or un-make C{Main} (C{bool}).
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
        self.frame.NS = self.NS.frame()
        if self.app:
            self.app.windowResize_(self)

    def windowScreen_(self, change):
        '''Called I{window} when screen or screen profile changed C{Main}.

           @param change: C{True} if the screen changed or C{False} if
                          the profile changed (C{bool}).

           @note: Typically, changing screen involves 2 callback invokations,
                  once for the profile and once for the screen.
        '''
        self.frame.NS = self.NS.frame()
        if self.app:
            self.app.windowScreen_(self, change)

    def windowZoomOK_(self, frame=None):
        '''Callback Is it OK to zoom I{window}?

           @keyword frame: The frame to zoom to (L{Rect}).

           @return: C{True} if OK to zoom, C{False} otherwise.
        '''
        a = self.app
        return a.windowZoomOK_(self, frame) if a else True


class WindowError(ValueError):
    '''Window error.
    '''
    pass


class WindowStyleError(WindowError):
    '''Window style error.
    '''
    pass


class WindowStyle(_Constants):  # Enum?
    '''Window style constants (C{mask}).
    '''
    Closable       = NSWindowStyleMaskClosable
    Miniaturizable = NSWindowStyleMaskMiniaturizable  # aka Hidable
#   Movable        = ?
    Resizable      = NSWindowStyleMaskResizable
    Titled         = NSWindowStyleMaskTitled
    Typical        = NSWindowStyleMaskUsual  # all of the above
    Utility        = NSWindowStyleMaskUtilityWindow

WindowStyle = WindowStyle()  # PYCHOK window style constants


def windowStyles(*styles):
    '''Return a combination of window styles, specified by name.

       @param styles: Style names (I{all positional}), case-insensitive.

       @return: Combined styles (L{WindowStyle}s C{mask}).

       @raise WindowStyleError: One or more I{styles} are invalid.
    '''
    M, x = WindowStyle._masks(*styles)
    if x is None:
        return M
    raise WindowStyleError(_fmt_invalid(styles=x))


class MediaWindow(Window):
    '''Media window Python Type, wrapping ObjC C{NSWindow/NSView}.
    '''
    def __init__(self, title='Media', fraction=0.5, **kwds):
        '''Create a L{MediaWindow}.

           @keyword title: Window name or title (string).
           @keyword fraction: Window size as fraction of the screen (C{float}).
           @keyword kwds: Optional, additional keyword arguments, see L{Window}.
        '''
        super(MediaWindow, self).__init__(title=title, fraction=fraction, **kwds)
        # create the drawable_nsobject NSView for vlc.py, see vlc.MediaPlayer.set_nsobject()
        # for an alternate NSView object with protocol VLCOpenGLVideoViewEmbedding
        # <https://StackOverflow.com/questions/11562587/create-nsview-directly-from-code>
        # <https://GitHub.com/ariabuckles/pyobjc-framework-Cocoa/blob/master/Examples/AppKit/DotView/DotView.py>
        self.NSview = v = NSView.alloc().initWithFrame_(self.frame.NS)
        # XXX printView(VLC, toPDF=...) crashes on Python 2, an empty box on Python 3
        self.PMview = v if _isPython3 else None


class TextWindow(Window):
    '''Scrollable text window Python Type, wrapping ObjC C{NSWindow/NSView}.
    '''
    def __init__(self, text_or_file, font=None, title='Text', fraction=0.5, **kwds):
        '''Create a L{TextWindow}.

           @param text_or_file: The contents (C{str} or C{file}).
           @keyword font: Optional font (L{Font}), default C{Fonts.MonoSpace}.
           @keyword title: Window name or title (C{str}).
           @keyword fraction: Window size as fraction of the screen (C{float}).
           @keyword kwds: Optional, additional keyword arguments, see L{Window}.
        '''
        text, t = _text_title2(text_or_file, title)
        super(TextWindow, self).__init__(title=t, fraction=fraction, **kwds)

        f = NSFont.userFixedPitchFontOfSize_(12) if font is None else font.NS
        w, _, _ = nsTextSize3(text, f)
        # <https://Developer.Apple.com/library/content/documentation/
        #        Cocoa/Conceptual/TextUILayer/Tasks/CreateTextViewProg.html>
        # <https://Developer.Apple.com/library/content/documentation/
        #        Cocoa/Conceptual/TextUILayer/Tasks/TextInScrollView.html>
        ns = self.NS
        cf = ns.contentView().frame()
        hs = w > cf.size.width

        sv = NSScrollView.alloc().initWithFrame_(cf)
        sv.setBorderType_(Border.No)
        if hs:
            sv.setHasHorizontalScroller_(YES)
            sv.setAutoresizingMask_(AutoResize.Sizable)
        else:
            sv.setHasHorizontalScroller_(NO)
            sv.setAutoresizingMask_(AutoResize.WidthSizable)
        sv.setHasVerticalScroller_(YES)

        tv = NSTextView.alloc().initWithFrame_(cf)
        tv.setMaxSize_(NSSize_t(NSIntegerMax, NSIntegerMax))
        tv.setMinSize_(NSSize_t(16, cf.size.height))
        tc = tv.textContainer()
        if hs:
            tv.setHorizontallyResizable_(YES)
            tv.setAutoresizingMask_(AutoResize.Sizable)
            tc.setContainerSize_(NSSize_t(NSIntegerMax, NSIntegerMax))  # FLT_MAX
            tc.setWidthTracksTextView_(NO)  # YES?
        else:
            tv.setHorizontallyResizable_(NO)
            tv.setAutoresizingMask_(AutoResize.WidthSizable)
            tc.setContainerSize_(NSSize_t(cf.size.width, NSIntegerMax))  # FLT_MAX
            tc.setWidthTracksTextView_(YES)  # NO?
        tv.setVerticallyResizable_(YES)

        tv.setFont_(f)  # XXX set font BEFORE text
        tv.insertText_(_NSStr(text))
        tv.setEditable_(NO)
        tv.setDrawsBackground_(NO)

        self.NSView = sv  # == ns.setContentView_(sv)
        self.PMview = tv  # XXX or sv?
        ns.makeKeyAndOrderFront_(None)
        ns.makeFirstResponder_(tv)


class _NSWindowDelegate(object):
    '''An ObjC-callable C{NSDelegate} class to handle C{NSWindow} events
       as L{Window}.window..._ and L{App}.window..._ callback calls.

       The event typically involves an C{NSNotification} instance the name
       of which determines the callback method to invoke.  For example,
       for notification named C{NSXxxYyyZzzNotification} will call the
       method named C{xxxYyyZzz_}, i.e. the notification name less the
       leading "NS" and trailing C"Notification", with "_" suffix added
       and the first character in lower case.

       @see: The C{_NSApplicationDelegate} for more C{NSDelegate} details.
    '''
    _ObjC = _ObjCDelegate('_NSWindowDelegate')

    @_ObjC.method('@P')
    def init(self, window):
        '''Initialize the allocated C{NSWindowDelegate}.

           @note: I{MUST} be called as C{.alloc().init(...)}.
        '''
        isinstanceOf(window, Window, raiser='window')
#       self = ObjCInstance(send_message(_NSObject_, _alloc_))
        self = ObjCInstance(send_super_init(self))
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
            raise RuntimeError(_fmt('%r vs %r', self.window, w))

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
#       if self.isFull and _Globals.MenuBar:
#           _Globals.MenuBar.isVisible = False  # hide

    @_ObjC.method('v@')
    def windowDidChangeScreen_(self, ns_notification):
        '''ObjC callback to handle C{NSWindow} events.
        '''
        self._ns2w(ns_notification)
        self.window.windowScreen_(True)

    @_ObjC.method('v@')
    def windowDidChangeScreenProfile_(self, ns_notification):
        '''ObjC callback to handle C{NSWindow} events.
        '''
        self._ns2w(ns_notification)
        self.window.windowScreen_(False)

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
#       if self.isFull and _Globals.MenuBar:
#           _Globals.MenuBar.isVisible = True  # show

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
        # <https://Developer.Apple.com/documentation/appkit/
        #        nswindowdelegate/1419533-windowshouldzoom>
        ok = self.window.windowZoomOK_(Rect(ns_frame))
        return YES if ok else NO

    @_ObjC.method('v@')
    def windowWillClose_(self, ns_notification):
        '''ObjC callback to handle C{NSWindow} events.
        '''
        # set the window's delegate to the app's to
        # make method .windowWillClose_ work, see
        # <https://Gist.GitHub.com/kaloprominat/6105220>
        self._ns2w(ns_notification)
        self.window.windowClose_()

#   @_ObjC.method('@@@')
#   def windowWillResize_toSize_(self, ns_window, ns_size):
        # <https://Developer.Apple.com/documentation/appkit/
        #        nswindowdelegate/1419292-windowwillresize>
#       self._ns2w(ns_window)
#       return ns_size

#   @_ObjC.method('@@@')
#   def windowWillReturnFieldEditor_toObject_(self, ns_window, ns_obj):
#       self._ns2w(ns_window)
#       return NSMain.Null


@proxy_RO
def NSWindowDelegate():
    '''The L{ObjCClass}C{(_NSWindowDelegate.__name__)}.
    '''
    return ObjCDelegate(_NSWindowDelegate)


def ns2Window(ns):
    '''Get the L{Window} instance for an ObjC C{NSWindow} or
       C{NSNotification} instance.

       @param ns: The ObjC instance (C{NS...}).

       @return: The window instance (L{Window}).

       @raise AttributeError: Unexpected I{ns} type.

       @raise RuntimeError: L{Window} mismatch.

       @raise TypeError: Invalid I{ns} type.
    '''
    if isObjCInstanceOf(ns, NSWindow):
        u = ns.uniqueID()
    elif isObjCInstanceOf(ns, NSConcreteNotification, NSNotification, raiser='ns'):
        u = ns.object().uniqueID()
    try:
        w = _Globals.Windows[u]
        if w._NSuniqID == u:
            return w
        t = _fmt('%r of %r', w._NSuniqID, w)
    except KeyError:
        t = None
    raise RuntimeError(_fmt('%s %s %r vs %s', ns, '.uniqueID', u, t))


_Types.Window = NSWindow._Type = Window
_Types.MediaWindow             = MediaWindow
_Types.TextWindow              = TextWindow

if __name__ == _Dmain_:

    from pycocoa.utils import _all_listing, _varstr

    print(_varstr(AutoResize, strepr=hex))  # mask XXX oct
    print(_varstr(BezelStyle, strepr=str))
    print(_varstr(Border, strepr=str))
    print(_varstr(WindowStyle, strepr=hex))  # mask

    _all_listing(__all__, locals())

# % python3 -m pycocoa.windows
#
# pycocoa.windows.__all__ = tuple(
#  pycocoa.windows.AutoResize.HeightSizable=16 or 1<<4,
#                            .MaxXMargin=4 or 1<<2,
#                            .MaxYMargin=32 or 1<<5,
#                            .MinXMargin=1,
#                            .MinYMargin=8 or 1<<3,
#                            .NotSizable=0,
#                            .Sizable=18,
#                            .WidthSizable=2,
#  pycocoa.windows.AutoResizeError is <class .AutoResizeError>,
#  pycocoa.windows.autoResizes is <function .autoResizes at 0x100b7c360>,
#  pycocoa.windows.BezelStyle.Circular=7,
#                            .Disclosure=5,
#                            .HelpButton=9,
#                            .Inline=15,
#                            .Recessed=13,
#                            .RegularSquare=2,
#                            .Rounded=1,
#                            .RoundedDisclosure=14,
#                            .RoundRect=12 or 3<<2,
#                            .ShadowlessSquare=6,
#                            .SmallSquare=10,
#                            .TexturedRounded=11,
#                            .TexturedSquare=8 or 1<<3,
#  pycocoa.windows.Border.Bezel=2,
#                        .Groove=3,
#                        .Line=1,
#                        .No=0,
#  pycocoa.windows.MediaWindow is <class .MediaWindow>,
#  pycocoa.windows.ns2Window is <function .ns2Window at 0x100f3e7a0>,
#  pycocoa.windows.NSWindowDelegate is <pycocoa.internals.proxy_RO object at 0x100f282d0>,
#  pycocoa.windows.TextWindow is <class .TextWindow>,
#  pycocoa.windows.Window is <class .Window>,
#  pycocoa.windows.WindowError is <class .WindowError>,
#  pycocoa.windows.WindowStyle.Closable=2,
#                             .Miniaturizable=4 or 1<<2,
#                             .Resizable=8 or 1<<3,
#                             .Titled=1,
#                             .Typical=15,
#                             .Utility=16 or 1<<4,
#  pycocoa.windows.WindowStyleError is <class .WindowStyleError>,
#  pycocoa.windows.windowStyles is <function .windowStyles at 0x100f128e0>,
# )[14]
# pycocoa.windows.version 25.3.18, .isLazy 1, Python 3.13.2 64bit arm64, macOS 15.3.2

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2025 -- mrJean1 at Gmail -- All Rights Reserved.
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
