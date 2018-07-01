
# -*- coding: utf-8 -*-

# License at the end of this file.

import os
import platform
import sys

try:
    import vlc
except ImportError:
    raise ImportError('no %s module (%s)' % ('vlc.py',
                      '<http://PyPI.org/project/python-vlc>'))

# the imports listed explicitly to help PyChecker
from pycocoa import get_selector, NSAlternateKeyMask, NSApplication, \
                    NSBackingStoreBuffered, NSCommandKeyMask, \
                    NSControlKeyMask, NSMenu, NSMenuItem, NSRect4_t, \
                    NSScreen, NSSize_t, NSShiftKeyMask, NSStr, \
                    NSView, NSWindow, NSWindowStyleMaskUsual, \
                    ObjCClass, ObjCInstance, ObjCSubclass, \
                    PyObjectEncoding, send_super, \
                    __version__ as __PyCocoa__  # PYCHOK false

__all__  = ('appVLC',)
__version__ = '18.06.28'

_macOS  = platform.mac_ver()[0:3:2]  # PYCHOK false
_Python = sys.version.split()[0], platform.architecture()[0]  # PYCHOK false
_Title  = _argv0 = os.path.basename(__file__)

_b2str = vlc.bytes_to_str
_str2b = vlc.str_to_bytes

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


def _mspf(fps):
    # convert frames per second to frame length in millisecs
    return 1000.0 / (fps or 25)


def _printf(fmt, *args, **kwds):  # nl=0, nt=0
    # formatted print
    t = (fmt % args) if args else fmt
    nl = '\n' * kwds.get('nl', 0)
    nt = '\n' * kwds.get('nt', 0)
    print('%s%s %s%s' % (nl, _argv0, t, nt))


class _Delegate_Implementation(object):
    # Cobbled together from the pycocoa.ObjCSubClass.__doc__,
    # pycocoa.runtime._DeallocObserver and PyObjC examples:
    # <http://TaoOfMac.com/space/blog/2007/04/22/1745> and
    # <http://StackOverflow.com/questions/24024723/swift-using
    # -nsstatusbar-statusitemwithlength-and-nsvariablestatusitemlength>
    _Delegate = ObjCSubclass('NSObject', '_Delegate')

    # the _Delegate.method(signature) decorator specfies the
    # signature of a Python method in Objective-C type encoding
    # to make the Python method callable from Objective-C.

    # This is rather ugly, especially since the decorator is
    # also required for (private) methods called only from
    # Python, like method .badgelabel, ._rate and ._zoom below.

    # See pycocoa.runtime.split_encoding for type encoding:
    # first is return value, then the method args, no need to
    # include @: for self and the Objective-C selector/cmd.
    @_Delegate.method(b'@' + PyObjectEncoding * 3)
    def init(self, app, title, video):
        self = ObjCInstance(send_super(self, 'init'))
#       self = ObjCInstance(send_message('NSObject', 'alloc'))
        self.app    = app
        self.player = vlc.MediaPlayer(video)
        self.ratio  = 2
        self.scale  = 1
        self.title  = title
        self.video  = video  # file name in window banner
        self.window = None
        return self

    @_Delegate.method('v@')
    def applicationDidFinishLaunching_(self, notification):

        # the player needs an NSView object
        self.window, view = _Window2(title=self.video or self.title)
        # set the window's delegate to the app's to
        # make method .windowWillClose_ work, see
        # <http://Gist.GitHub.com/kaloprominat/6105220>
        self.window.setDelegate_(self)

        # Create the main menu.
        menu = NSMenu.alloc().init()

        menu.addItem_(_MenuItem('Full ' + 'Screen', 'enterFullScreenMode:', 'f', ctrl=True))  # Ctrl-Cmd-F, Esc to exit

        if self.player:  # setup player view and menu
            self.player.set_nsobject(view)

            menu.addItem_(_MenuItemSeparator())
            menu.addItem_(_MenuItem('Play', 'play:', 'p'))
            menu.addItem_(_MenuItem('Pause', 'pause:', 's'))
            menu.addItem_(_MenuItem('Rewind', 'rewind:', 'r'))
            menu.addItem_(_MenuItemSeparator())
            menu.addItem_(_MenuItem('Faster', 'faster:', '>', shift=True))
            menu.addItem_(_MenuItem('Slower', 'slower:', '<', shift=True))
            menu.addItem_(_MenuItem('Zoom In', 'zoomIn:', '+'))
            menu.addItem_(_MenuItem('Zoom Out', 'zoomOut:', '-'))
            menu.addItem_(_MenuItemSeparator())
            menu.addItem_(_MenuItem('Info', 'info:', 'i'))
            menu.addItem_(_MenuItem('Close Windows', 'windowWillClose:', 'w'))

        menu.addItem_(_MenuItemSeparator())
        menu.addItem_(_MenuItem('Hide ' + self.title, 'hide:', 'h'))  # Cmd-H, implied
        menu.addItem_(_MenuItem('Hide Others', 'hideOtherApplications:', 'h', alt=True))  # Alt-Cmd-H
        menu.addItem_(_MenuItem('Show All', 'unhideAllApplications:'))  # no key

        menu.addItem_(_MenuItemSeparator())
        menu.addItem_(_MenuItem('Quit ' + self.title, 'terminate:', 'q'))  # Cmd-Q

        subMenu = NSMenuItem.alloc().init()
        subMenu.setSubmenu_(menu)

        menuBar = NSMenu.alloc().init()
        menuBar.addItem_(subMenu)
        self.app.setMainMenu_(menuBar)

        self.play_(None)
        # adjust the contents' aspect ratio
        self.windowDidResize_(None)

    @_Delegate.method('v@')
    def info_(self, notification):
        try:
            self.pause_(notification)
            p = self.player
            m = p.get_media()

            # print Python, vlc, libVLC, media info
            _printf('PyCocoa %s (%s)', __PyCocoa__, __version__, nl=1)
            _printf('python %s', ' '.join(_Python))
            _printf('macOS %s', ' '.join(_macOS))

            _printf('vlc.py %s (%#x)', vlc.__version__, vlc.hex_version())
            _printf('built: %s', vlc.build_date)

            _printf('libVLC %s (%#x)', _b2str(vlc.libvlc_get_version()), vlc.libvlc_hex_version())
            _printf('libVLC %s', _b2str(vlc.libvlc_get_compiler()), nt=1)

            _printf('media: %s', _b2str(m.get_mrl()))
            _printf('state: %s', p.get_state())
            _printf('track/count: %s/%s', p.video_get_track(), p.video_get_track_count())
            _printf('time/duration: %s/%s', p.get_time(), m.get_duration())
            f = p.get_position()
            _printf('position: %.6f (%.2f%%)', f, f * 100)
            f = p.get_fps()
            _printf('fps: %.6f (%.3f ms)', f, _mspf(f))
            _printf('rate: %s', p.get_rate())

            w, h = p.video_get_size(0)
            r = gcd(w, h) or ''
            if r and w and h:
                r = ' (%s:%s)' % (w // r, h // r)
            _printf('video size: %sx%s%s', w, h, r)  # num=0
            _printf('aspect ratio: %s', p.video_get_aspect_ratio())
            _printf('scale: %.3f (%.3f)', p.video_get_scale(), self.scale)
            _printf('window: %r', p.get_hwnd(), nt=1)
        except Exception as x:
            _printf('%r', x, nl=1, nt=1)

    @_Delegate.method('v@')
    def pause_(self, notification):
        # note, .pause() pauses and un-pauses the video,
        # .stop() stops the video and blanks the window
        if self.player.is_playing():
            self.player.pause()

    @_Delegate.method('v@')
    def play_(self, notification):
        self.player.play()

    @_Delegate.method('v@')
    def rewind_(self, notification):
        self.player.set_position(0.0)
        # can't re-play once at the end
        # self.player.play()

    @_Delegate.method('v@')
    def windowDidResize_(self, notification):
        if self.window and self.ratio:
            # get and maintain the aspect ratio
            # (the first player.video_get_size()
            #  call returns (0, 0), subsequent
            #  calls return (w, h) correctly)
            w, h = self.player.video_get_size(0)
            r = gcd(w, h)
            if r and w and h:
                r = NSSize_t(w // r , h // r)
                self.window.setContentAspectRatio_(r)
                self.ratio -= 1

    @_Delegate.method('v@')
    def windowWillClose_(self, notification):
        self.app.terminate_(self)  # or NSApp()...

    @_Delegate.method('v@')
    def faster_(self, notification):
        self._rate(2.0)

    @_Delegate.method('v@')
    def slower_(self, notification):
        self._rate(0.5)

    @_Delegate.method(b'v' + PyObjectEncoding)
    def _rate(self, factor):  # called from ObjC method
        r = self.player.get_rate() * factor
        if 0.2 < r < 10.0:
            self.player.set_rate(r)

    @_Delegate.method('v@')
    def zoomIn_(self, notification):
        self._zoom(1.25)

    @_Delegate.method('v@')
    def zoomOut_(self, notification):
        self._zoom(0.80)

    @_Delegate.method(b'v' + PyObjectEncoding)
    def _zoom(self, factor):  # called from ObjC method
        self.scale *= factor
        self.player.video_set_scale(self.scale)


_Delegate = ObjCClass('_Delegate')  # the actual class


def _MenuItem(label, action=None, key='', alt=False, cmd=True, ctrl=False, shift=False):
    '''New menu item with action and optional shortcut key.
    '''
    # <http://Developer.Apple.com//documentation/appkit/nsmenuitem/1514858-initwithtitle>
    item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
           NSStr(label), get_selector(action), NSStr(key))
    if key:
        mask = 0
        if alt:
            mask |= NSAlternateKeyMask
        if cmd:
            mask |= NSCommandKeyMask
        if ctrl:
            mask |= NSControlKeyMask
        if shift:
            mask |= NSShiftKeyMask  # NSAlphaShiftKeyMask
        if mask:
            item.setKeyEquivalentModifierMask_(mask)
    return item


def _MenuItemSeparator():
    '''A menu separator item.
    '''
    return NSMenuItem.separatorItem()


def _Window2(title=_Title, fraction=0.5):
    '''Create the main window and the drawable view.
    '''
    frame = NSScreen.alloc().init().mainScreen().frame()
    if 0.1 < fraction < 1.0:
        # use the lower left quarter of the screen size as frame
        w = int(frame.size.width * fraction + 0.5)
        h = int(frame.size.height * w / frame.size.width)
        frame = NSRect4_t(frame.origin.x + 10, frame.origin.y + 10, w, h)

    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                      frame,
                      NSWindowStyleMaskUsual,  # PYCHOK expected
                      NSBackingStoreBuffered,
                      False)  # or 0
    window.setTitle_(NSStr(title))

    # create the drawable_nsobject NSView for vlc.py, see vlc.MediaPlayer.set_nsobject()
    # for an alternate NSView object with protocol VLCOpenGLVideoViewEmbedding
    # <http://StackOverflow.com/questions/11562587/create-nsview-directly-from-code>
    # <http://GitHub.com/ariabuckles/pyobjc-framework-Cocoa/blob/master/Examples/AppKit/DotView/DotView.py>
    view = NSView.alloc().initWithFrame_(frame)
    window.setContentView_(view)
    # force the video/window aspect ratio, adjusted
    # above when the window is/has been resized
    window.setContentAspectRatio_(frame.size)

    window.makeKeyAndOrderFront_(None)
    return window, view


def appVLC(title=_Title, video='', timeout=None):
    '''Create the application and start the VLC player,
       before calling app.run() to start the application.
    '''
    app = NSApplication.sharedApplication()
#   pool = NSAutoreleasePool.alloc().init()  # created by NSApplication

    dlg = _Delegate.alloc().init(app, title, video)
    app.setDelegate_(dlg)

    if timeout is not None:
        try:
            from test import terminating
            terminating(app, timeout)
        except (ImportError, ValueError):
            pass

    return app


if __name__ == '__main__':

    _argv0 = os.path.basename(sys.argv[0])  # _Title

    _timeout = None

    args = sys.argv[1:]
    while args and args[0].startswith('-'):
        o = args.pop(0)
        t = o.lower()
        if t in ('-h', '--help'):
            _printf('usage:  [-h|--help]  [-timeout <secs>]  %s',
                    '<video_file_name>')
            sys.exit(0)
        elif '-timeout'.startswith(t) and len(t) > 1 and args:
            _timeout = args.pop(0)
        else:
            _printf('invalid option: %s', o)
            sys.exit(1)

    if not args:
        _printf('missing %s', '<video_file_name>')
        sys.exit(1)

    app = appVLC(title=_argv0, video=args.pop(0), timeout=_timeout)
    app.run()  # never returns, but Python thread(s) run

# MIT License <http://OpenSource.org/licenses/MIT>
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
