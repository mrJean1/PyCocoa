
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Types L{AutoResize}, L{Window}, L{MediaWindow}, L{Screen},
L{WindowStyle}, wrapping ObjC C{NSWindow}, etc.

@var AutoResize:  Window resize options (C{mask}).
@var BezelStyle:  Bezel kinds (C{enum}).
@var Border:      Border kinds (C{enum}).
@var WindowStyle: Window styles (C{mask}).
'''
# all imports listed explicitly to help PyChecker
from pycocoa.bases    import _Type2
from pycocoa.geometry import Rect
from pycocoa.lazily   import _ALL_LAZY
from pycocoa.nstypes  import isNone, NSConcreteNotification, NSFont, \
                             NSImageView, NSMain, NSNotification, \
                             NSScrollView, NSStr, NSTableView, \
                             nsTextSize3, NSTextView, NSView, NSWindow
from pycocoa.octypes  import NSIntegerMax, NSPoint_t, NSSize_t
from pycocoa.oslibs   import NO, NSBackingStoreBuffered, \
                             NSWindowStyleMaskClosable, \
                             NSWindowStyleMaskMiniaturizable, \
                             NSWindowStyleMaskResizable, \
                             NSWindowStyleMaskTitled, \
                             NSWindowStyleMaskUsual, \
                             NSWindowStyleMaskUtilityWindow, YES
from pycocoa.runtime  import isObjCInstanceOf, ObjCDelegate, ObjCInstance, \
                             ObjCSubclass, release, retain, send_super_init
from pycocoa.utils    import aspect_ratio, bytes2str, _Constants, \
                             _Globals, isinstanceOf, module_property_RO, \
                             property_RO, _Python3, _text_title2, _Types

# from enum   import Enum

__all__ = _ALL_LAZY.windows
__version__ = '20.01.08'

_Cascade = NSPoint_t(25, 25)  # PYCHOK false


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
    c, e = AutoResize._masks(*options)
    if e is None:
        return c
    raise AutoResizeError('invalid %s: %s' % ('option', e))


# <https://Developer.Apple.com/documentation/appkit/nsbezelstyle>
class BezelStyle(_Constants):  # Enum?
    '''Bezel style constants (C{int}).
    '''
    NCircular         =  7  # NSCircularBezelStyle
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


class Screen(Rect):
    '''Screen Python Type, wrapping ObjC L{NSRect_t}.
    '''
    def __init__(self, fraction=0.5, cascade=10):
        '''New, partial screen L{Rect}.

           @keyword fraction: Size of the screen (C{float}).
           @keyword cascade: Shift from lower left corner (C{float} or C{int}).

           @raise ValueError: Invalid I{fraction} value.
        '''
        f = NSMain.ScreenFrame
        if 0.1 < fraction < 1.0:
            # use the lower left side of the screen
            w = int(f.size.width * fraction + 0.5)
            h = int(f.size.height * w / f.size.width)
            # avoid cascading window off-screen
            c = min(max(0, cascade), min(f.size.width, f.size.height))
            f = f.origin.x + c, f.origin.y + c, w, h
        elif fraction < 0 or fraction > 1:
            raise ValueError('invalid %s: %.2f' % ('fraction', fraction))
        self.rect = f


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
    _ratio    = ()

    def __init__(self, title='Main', frame=None, excl=0, auto=False, **kwds):
        '''Create a new L{Window}.

           @keyword title: Window title (C{str}).
           @keyword frame: Window frame (L{Rect}, L{NSRect_t}, L{NSRect4_t}, or None).
           @keyword excl: Window styles to exclude (L{WindowStyle}C{.attribute}).
           @keyword auto: Release window resource when closed (C{bool}).
           @keyword kwds: Optional, additional keyword arguments.

           @raise WindowError: Unique C{Id} exists.
        '''
        self._frame = Screen(0.5) if frame is None else Rect(frame)
        self._ratio = self._frame.width, self._frame.height

        self.NS = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                                   self.frame.NS,
                                   WindowStyle.Typical ^ excl,  # PYCHOK expected
                                   NSBackingStoreBuffered,
                                   NO)
        self.title = bytes2str(title)
        self.front(True)

        if kwds:
            super(Window, self).__init__(**kwds)

        # XXX self.NS.setIdentifier_(int2NS(id(self)))
        self._NSuniqID = u = self.NS.uniqueID()
        if u in _Globals.Windows:
            raise WindowError('%s %r exists: %r' % ('.uniqueID', u,  _Globals.Windows[u]))
        _Globals.Windows[u] = self

        if _Globals.App and not self.app:
            self.app = _Globals.App

        if auto:
            self.NS.setReleasedWhenClosed_(YES)
            self._auto = True

        self.NSdelegate = retain(NSWindowDelegate.alloc().init(self))

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

    @property_RO
    def frame(self):
        '''Get this window's frame (L{Rect}).
        '''
        return self._frame

    def front(self, focus=False):
        '''Order this window to the front.

           @keyword focus: Make this window C{Key} (C{bool}).
        '''
        if focus:
            self.NS.makeKeyAndOrderFront_(None)
        else:
            self.NS.orderFrontRegardless()
        self.NS.display()
        self.NS.orderFront_(None)  # vs .orderOut_(None)

    def full(self, full):
        '''Enter or exit full screen mode for this window.

           @param full: Enter or exit (C{bool}).
        '''
        if full:
            self.NS.enterFullScreenMode_(self.NS.screen())
        else:
            self.NS.exitFullScreenMode_(self.NS.screen())

    def hide(self, hide):
        '''Hide or unhide this window.

           @param hide: Hide or show (C{bool}).
        '''
        if hide:  # click the hide/miniaturize button
            self.NS.performMiniaturize_(self.NS)  # XXX self.delegate
        elif self.isHidden:
            self.NS.deminiaturize_(self.NS)

    @property_RO
    def isFull(self):
        '''Get this window's full screen state (C{bool}).
        '''
        return True if self.NS.isInFullScreenMode() else False

    @property_RO
    def isHidden(self):
        '''Get this window's hidden state (C{bool}).
        '''
        return True if self.NS.isMiniaturized() else False

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
    def isVisible(self):
        '''Get this window's visible state (C{bool}).
        '''
        return True if self.NS.isVisible() else False

    @property_RO
    def isPrintable(self):
        '''Get this window's printable state (C{bool}).
        '''
        return True if self.PMview else False

    @property_RO
    def isZoomed(self):
        '''Get this window's zoomed state (C{bool}).
        '''
        return True if self.NS.isZoomed() else False

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
        return self._NSview or NSMain.Null

    @NSview.setter  # PYCHOK property.setter
    def NSview(self, ns_view):
        '''Set this window's view (C{NSView...}).
        '''
        if not isNone(ns_view):
            isObjCInstanceOf(ns_view, NSScrollView, NSView, name='ns_view')
            self.NS.setContentView_(ns_view)
        self._NSview = ns_view

    @property
    def PMview(self):
        '''Get this window's print view (C{NSView...}).
        '''
        return self._PMview  # or NSMain.Null

    @PMview.setter  # PYCHOK property.setter
    def PMview(self, ns_view):
        '''Set this window's print view (C{NSView...}).
        '''
        if ns_view and isObjCInstanceOf(ns_view, NSImageView, NSTableView, NSTextView, NSView):
            self._PMview = ns_view
        else:
            self._PMview = None

    @property
    def ratio(self):
        '''Get this window's aspect ratio as 2-tuple (width, height).
        '''
        return self._ratio

    @ratio.setter  # PYCHOK property.setter
    def ratio(self, ratio):
        '''Set this window's aspect ratio.

           @param ratio: New ratio (L{Size}, 2-tuple (width, height), str("w:h") or C{NSSize_t}).

           @raise WindowError: Invalid I{ratio}.
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
            raise WindowError('invalid %s: %r' % ('ratio', ratio))

        r = aspect_ratio(*r)
        if r:
            self._ratio = r
            self.NS.setContentAspectRatio_(NSSize_t(*r))

    def zoom(self, zoom):
        '''Toggle, zoom or un-zoom this window.

           @param zoom: Zoom or un-zoom (C{bool}) or C{None} to toggle.
        '''
        if zoom is None or (zoom and not self.isZoomed) \
                        or (self.isZoomed and not zoom):
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
        '''Is it OK? to close I{window} callback.

           @return: True if OK to close, False otherwise.
        '''
        if self.app:
            return self.app.windowCloseOK_(self)
        else:
            return True

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


WindowStyle = WindowStyle()  # window style constants


def windowStyles(*styles):
    '''Return a combination of window styles, specified by name.

       @param styles: Style names (I{all positional}), case-insensitive.

       @return: Combined styles (L{WindowStyle}s C{mask}).

       @raise WindowStyleError: One or more I{styles} are invalid.
    '''
    c, e = WindowStyle._masks(*styles)
    if e is None:
        return c
    raise WindowStyleError('invalid %s: %s' % ('styles', e))


class MediaWindow(Window):
    '''Media window Python Type, wrapping ObjC C{NSWindow/NSView}.
    '''
    def __init__(self, title='Media', fraction=0.5, **kwds):
        '''Create a L{MediaWindow}.

           @keyword title: Window name or title (string).
           @keyword fraction: Window size as fraction of the screen (C{float}).
           @keyword kwds: Optional, additional keyword arguments, see L{Window}.
        '''
        super(MediaWindow, self).__init__(title=title, frame=Screen(fraction), **kwds)
        # create the drawable_nsobject NSView for vlc.py, see vlc.MediaPlayer.set_nsobject()
        # for an alternate NSView object with protocol VLCOpenGLVideoViewEmbedding
        # <https://StackOverflow.com/questions/11562587/create-nsview-directly-from-code>
        # <https://GitHub.com/ariabuckles/pyobjc-framework-Cocoa/blob/master/Examples/AppKit/DotView/DotView.py>
        self.NSview = v = NSView.alloc().initWithFrame_(self.frame.NS)
        # XXX printView(VLC, toPDF=...) crashes on Python 2, an empty box on Python 3
        self.PMview = v if _Python3 else None


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
        super(TextWindow, self).__init__(title=t, frame=Screen(fraction), **kwds)

        if font is None:
            f = NSFont.userFixedPitchFontOfSize_(12)
        else:
            f = font.NS
        w, _, _ = nsTextSize3(text, f)
        # <https://Developer.Apple.com/library/content/documentation/
        #        Cocoa/Conceptual/TextUILayer/Tasks/CreateTextViewProg.html>
        # <https://Developer.Apple.com/library/content/documentation/
        #        Cocoa/Conceptual/TextUILayer/Tasks/TextInScrollView.html>
        ns = self.NS
        cr = ns.contentView().frame()
        hs = w > cr.size.width

        sv = NSScrollView.alloc().initWithFrame_(cr)
        sv.setBorderType_(Border.No)
        if hs:
            sv.setHasHorizontalScroller_(YES)
            sv.setAutoresizingMask_(AutoResize.Sizable)
        else:
            sv.setHasHorizontalScroller_(NO)
            sv.setAutoresizingMask_(AutoResize.WidthSizable)
        sv.setHasVerticalScroller_(YES)

        tv = NSTextView.alloc().initWithFrame_(cr)
        tv.setMaxSize_(NSSize_t(NSIntegerMax, NSIntegerMax))
        tv.setMinSize_(NSSize_t(16, cr.size.height))
        tc = tv.textContainer()
        if hs:
            tv.setHorizontallyResizable_(YES)
            tv.setAutoresizingMask_(AutoResize.Sizable)
            tc.setContainerSize_(NSSize_t(NSIntegerMax, NSIntegerMax))  # FLT_MAX
            tc.setWidthTracksTextView_(NO)  # YES?
        else:
            tv.setHorizontallyResizable_(NO)
            tv.setAutoresizingMask_(AutoResize.WidthSizable)
            tc.setContainerSize_(NSSize_t(cr.size.width, NSIntegerMax))  # FLT_MAX
            tc.setWidthTracksTextView_(YES)  # NO?
        tv.setVerticallyResizable_(YES)

        tv.setFont_(f)  # XXX set font BEFORE text
        tv.insertText_(release(NSStr(text)))
        tv.setEditable_(NO)
        tv.setDrawsBackground_(NO)

        self.NSView = sv  # == ns.setContentView_(sv)
        self.PMview = tv  # XXX or sv?
        ns.makeKeyAndOrderFront_(None)
        ns.makeFirstResponder_(tv)


class _NSWindowDelegate(object):
    '''An ObjC-callable C{NSDelegate} class to handle C{NSWindow} events
       as L{Window}.window..._ and L{App}.window..._ callback calls.

       @see: The C{_NSApplicationDelegate} for more C{NSDelegate} details.
    '''
    _ObjC = ObjCSubclass('NSObject', '_NSWindowDelegate', register=False)  # defer

    @_ObjC.method('@P')
    def init(self, window):
        '''Initialize the allocated C{NSWindowDelegate}.

           @note: I{MUST} be called as C{.alloc().init(...)}.
        '''
        isinstanceOf(window, Window, name='window')
#       self = ObjCInstance(send_message('NSObject', 'alloc'))
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
            raise RuntimeError('%r vs %r' % (self.window, w))

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


@module_property_RO
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
    elif isObjCInstanceOf(ns, NSConcreteNotification, NSNotification, ns='ns'):
        u = ns.object().uniqueID()
    try:
        w = _Globals.Windows[u]
        if w._NSuniqID == u:
            return w
        t = '%r of %r' % (w._NSuniqID, w)
    except KeyError:
        t = None
    raise RuntimeError('%s %s %r vs %s' % (ns, '.uniqueID', u, t))


_Types.Window = NSWindow._Type = Window
_Types.MediaWindow             = MediaWindow
_Types.TextWindow              = TextWindow

if __name__ == '__main__':

    from pycocoa.utils import _all_exports, _all_listing

    _all_exports(locals(), 'BezelStyle', 'Border', 'MediaWindow',
                           'NSWindowDelegate', 'Screen', 'TextWindow',
                 starts=('AutoResize', 'autoResizes', 'ns', 'Window', 'window'))
    _all_listing(__all__, locals())

    _ = '''% python3 -m pycocoa.windows

 windows.__all__ = tuple(
   windows.AutoResize.HeightSizable=1<<4,
                     .MaxXMargin=1<<2,
                     .MaxYMargin=1<<5,
                     .MinXMargin=1,
                     .MinYMargin=1<<3,
                     .NotSizable=0,
                     .Sizable=9<<1,
                     .WidthSizable=1<<1,
   windows.AutoResizeError is <class .AutoResizeError>,
   windows.autoResizes is <function .autoResizes at 0x10bf34ef0>,
   windows.BezelStyle.Disclosure=5,
                     .HelpButton=9,
                     .Inline=15,
                     .NCircular=7,
                     .Recessed=13,
                     .RegularSquare=1<<1,
                     .Rounded=1,
                     .RoundedDisclosure=7<<1,
                     .RoundRect=3<<2,
                     .ShadowlessSquare=3<<1,
                     .SmallSquare=5<<1,
                     .TexturedRounded=11,
                     .TexturedSquare=1<<3,
   windows.Border.Bezel=1<<1,
                 .Groove=3,
                 .Line=1,
                 .No=0,
   windows.MediaWindow is <class .MediaWindow>,
   windows.ns2Window is <function .ns2Window at 0x10bf40e60>,
   windows.nsTextSize3 is <function pycocoa.nstypes.nsTextSize3 at 0x10bf34170>,
   windows.NSWindowDelegate is <pycocoa.utils.module_property_RO object at 0x10bf3ed50>,
   windows.Screen is <class .Screen>,
   windows.TextWindow is <class .TextWindow>,
   windows.Window is <class .Window>,
   windows.WindowError is <class .WindowError>,
   windows.WindowStyle.Closable=1<<1,
                      .Miniaturizable=1<<2,
                      .Resizable=1<<3,
                      .Titled=1,
                      .Typical=15,
                      .Utility=1<<4,
   windows.WindowStyleError is <class .WindowStyleError>,
   windows.windowStyles is <function .windowStyles at 0x10bba3b90>,
 )[16]
 windows.version = '20.01.08'
'''
    del _

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2020 -- mrJean1 at Gmail -- All Rights Reserved.
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
