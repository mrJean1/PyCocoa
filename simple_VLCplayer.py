
# -*- coding: utf-8 -*-

# Original <http://code.google.com/archive/p/cocoa-python>

# Example of using ctypes with PyCocoa to create an NSWindow and NSView
# with an application menu to run a video using VLC.  The VLC App must
# be installed on macOS, see <http://www.VideoLan.org/index.html> with
# the Python-VLC binding, see <http://PyPI.Python.org/pypi/python-vlc>.

# This VLC player has only been tested with VLC 2.2.6 and 3.0.1 and the
# corresponding vlc.py Python-VLC binding using 64-bit Python 2.7.14 and
# 3.6.4 on macOS 10.13.3 High Sierra.  The player does not work (yet)
# with PyPy Python <http://pypy.org> nor with Intel(R) Python
# <http://software.intel.com/en-us/distribution-for-python>.

# MIT License <https://opensource.org/licenses/MIT>
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

import platform
import os
import sys
if not sys.platform.startswith('darwin'):
    raise ImportError('unsupported platform: %s' % (sys.platform,))

from threading import Thread
from time import sleep

try:  # the imports listed explicitly to help PyChecker
    from pycocoa import NSAlternateKeyMask, NSApplication, \
                        NSBackingStoreBuffered, NSCommandKeyMask, \
                        NSControlKeyMask, NSMakeRect, NSMenu, \
                        NSMenuItem, NSOpenPanel, NSScreen, NSSize, \
                        NSShiftKeyMask, NSString, NSUsualWindowMask, \
                        NSView, NSWindow, ObjCClass, ObjCInstance, \
                        ObjCSubclass, PyObjectEncoding, \
                        get_selector, nsString2str, send_super
except ImportError:
    raise ImportError('no %s module (%s)' % ('pycocoa',
                      '<http://PyPI.Python.org/pypi/PyCocoa>'))
try:
    import vlc
except ImportError:
    raise ImportError('no %s module (%s)' % ('vlc.py',
                      '<http://PyPI.Python.org/pypi/python-vlc>'))

__all__  = ('appVLC',)
__version__ = '18.03.15'

_macOS  = platform.mac_ver()[0:3:2]  # PYCHOK false
_Movies = '.mov', '.mp4'  # lower-case file types for movies, videos
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
    return 1000 // (fps or 25)


def _printf(fmt, *args, **kwds):  # nl=0, nt=0
    # formatted print
    t = (fmt % args) if args else fmt
    nl = '\n' * kwds.get('nl', 0)
    nt = '\n' * kwds.get('nt', 0)
    print('%s%s %s%s' % (nl, _argv0, t, nt))


class _Delegate_Implementation(object):
    # Cobbled together from the pycocoa.ObjCSubClass.__doc__
    # and pycocoa.runtime._DeallocObserver_Implementation
    # and the following PyObjC examples:
    # <http://TaoOfMac.com/space/blog/2007/04/22/1745> and
    # <http://StackOverflow.com/questions/24024723/swift-using
    # -nsstatusbar-statusitemwithlength-and-nsvariablestatusitemlength>
    _Delegate = ObjCSubclass('NSObject', '_Delegate')

    # the _Delegate.method(signature) decorator specfies the
    # signature of a Python method in Objective-C type encoding
    # to make the Python method callable from Objective-C.

    # This is rather ugly, especially since the decorator is
    # also required for (private) methods called only from
    # Python, like the .badgelabel, ._rate and ._zoom below.

    # See pycocoa.runtime.split_encoding for type encoding:
    # first is return value, then the method args, no need to
    # include @: for self and the Objective-C selector/cmd.
    @_Delegate.method(b'@' + PyObjectEncoding * 4)
    def init(self, app, title, video, player):
        self = ObjCInstance(send_super(self, 'init'))
#       self = ObjCInstance(send_message('NSObject', 'alloc'))
#       print(self)  # <ObjCInstance ...: _Delegate at ...>
        self.app    = app
        self.badge  = None
        self.player = player
        self.ratio  = None
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
            menu.addItem_(_MenuItem('Open...', 'open:', 'o'))
            menu.addItem_(_MenuItemSeparator())
            menu.addItem_(_MenuItem('Play', 'play:', 'p'))
            menu.addItem_(_MenuItem('Pause', 'pause:', 's'))
            menu.addItem_(_MenuItem('Rewind', 'rewind:', 'r'))
            menu.addItem_(_MenuItemSeparator())
            menu.addItem_(_MenuItem('Info', 'info:', 'i'))
            menu.addItem_(_MenuItem('Faster', 'faster:', '>', shift=True))
            menu.addItem_(_MenuItem('Slower', 'slower:', '<', shift=True))
            menu.addItem_(_MenuItem('Zoom In', 'zoomin:', '+'))
            menu.addItem_(_MenuItem('Zoom Out', 'zoomout:', '-'))

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

    @_Delegate.method(b'@' + PyObjectEncoding)
    def badgelabel(self, label):  # called from ObjC method
        if self.badge:
            self.badge.setBadgeLabel_(NSString(label))

    @_Delegate.method('v@')
    def info_(self, notification):
        # print vlc, libVLC, media info
        try:
            _printf('python %s', ' '.join(_Python))
            _printf('macOS %s', ' '.join(_macOS), nt=1)

            _printf('vlc.py %s', vlc.__version__)
            _printf('vlc.py built: %s (%#x)', vlc.build_date, vlc.hex_version(), nt=1)

            _printf('libVLC %s (%#x)', _b2str(vlc.libvlc_get_version()), vlc.libvlc_hex_version())
            _printf('libVLC %s', _b2str(vlc.libvlc_get_compiler()), nt=1)

            p = self.player
            if p:
                self.pause_(notification)
                m = p.get_media()
                _printf('media: %s', _b2str(m.get_mrl()))
                _printf('state: %s', p.get_state())
                _printf('track/count: %s/%s', p.video_get_track(), p.video_get_track_count())
                _printf('time/duration: %s/%s', p.get_time(), m.get_duration())
                f = p.get_position()
                _printf('position: %.9f (%.2f%%)', f, f * 100)
                f = p.get_fps()
                _printf('fps: %s (%d ms)', f, _mspf(f))
                _printf('rate: %s', p.get_rate())
                w, h = p.video_get_size(0)
                r = gcd(w, h) or ''
                if r and w and h:
                    r = ' (%s:%s)' % (w // r, h // r)
                _printf('video size: %sx%s%s', w, h, r)  # num=0
                _printf('aspect ratio: %s', p.video_get_aspect_ratio())
                _printf('scale: %.3f (%.3f)', p.video_get_scale(), self.scale, nt=1)
                # _printf('window:' % p.get_hwnd()
        except Exception:
            _printf('error: %s', sys.exc_info()[1], nl=1, nt=1)

    @_Delegate.method('v@')
    def open_(self, notification):
        # stop the current video and show
        # the panel to select another video
        self.pause_(None)
        self.badgelabel('O')
        video = _OpenFilePanel(_Movies)
        if video and self.player:
            inst = self.player.get_instance()
            media = inst.media_new(video)
            self.player.set_media(media)
            self.window.setTitle_(NSString(video))

    @_Delegate.method('v@')
    def pause_(self, notification):
        if self.player:
            # note, .pause() pauses and un-pauses the video,
            # .stop() stops the video and blanks the window
            if self.player.is_playing():
                self.player.pause()
                self.badgelabel('S')

    @_Delegate.method('v@')
    def play_(self, notification):
        if self.player:
            self.player.play()
            self.badgelabel('P')

    @_Delegate.method('v@')
    def rewind_(self, notification):
        if self.player:
            self.player.set_position(0.0)
            # can't re-play once at the end
            # self.player.play()
            self.badgelabel('R')

    @_Delegate.method('v@')
    def windowDidResize_(self, notification):
        # this method is only called if this
        # _Delegate is the window's delegate
        if self.player and self.window and not self.ratio:
            # get and maintain the aspect ratio
            # (the first player.video_get_size()
            #  call returns (0, 0), subsequent
            #  calls return (w, h) correctly)
            w, h = self.player.video_get_size(0)
            r = gcd(w, h)
            if r and w and h:
                r = NSSize(w // r , h // r)
                self.window.setContentAspectRatio_(r)
                self.ratio = r

    @_Delegate.method('v@')
    def windowWillClose_(self, notification):
        # this method is only called if this
        # _Delegate is the window's delegate
        self.app.terminate_(self)  # or NSApp()...

    @_Delegate.method('v@')
    def faster_(self, notification):
        self._rate(2.0)

    @_Delegate.method('v@')
    def slower_(self, notification):
        self._rate(0.5)

    @_Delegate.method(b'v' + PyObjectEncoding)
    def _rate(self, factor):  # called from ObjC method
        if self.player:
            r = self.player.get_rate() * factor
            if 0.2 < r < 10.0:
                self.player.set_rate(r)

    @_Delegate.method('v@')
    def zoomin_(self, notification):
        self._zoom(1.25)

    @_Delegate.method('v@')
    def zoomout_(self, notification):
        self._zoom(0.80)

    @_Delegate.method(b'v' + PyObjectEncoding)
    def _zoom(self, factor):  # called from ObjC method
        if self.player:
            self.scale *= factor
            self.player.video_set_scale(self.scale)


_Delegate = ObjCClass('_Delegate')  # the actual class


def _MenuItem(label, action=None, key='', alt=False, cmd=True, ctrl=False, shift=False):
    '''New menu item with action and optional shortcut key.
    '''
    # <http://developer.apple.com/documentation/appkit/nsmenuitem/1514858-initwithtitle>
    item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
           NSString(label), get_selector(action), NSString(key))
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


def _OpenFilePanel(filetypes, aliases=False, files=True, dirs=False, multiple=False):
    '''Show a file selection dialog.
    '''
    if multiple:  # setAllowsMultipleSelection
        raise NotImplementedError('multiple %s' % (multiple,))
    panel = NSOpenPanel.openPanel()
    panel.setResolvesAliases_(bool(aliases))
    panel.setCanChooseDirectories_(bool(dirs))
    panel.setCanChooseFiles_(bool(files))
#   panel.allowedFileTypes(NSStrings(*filetypes))
    while True:
        panel.orderFrontRegardless()  # only flashes
        if not panel.runModal():
            return None  # Cancel, nothing selected
#       paths = panel.filenames()  # returns an NSArray
#       urls = panel.URLs()  # returns an NSArray
        path = nsString2str(panel.URL().path())
        # mimick NSOpenPanel.allowedFileTypes_
        if path.lower().endswith(filetypes):
            return path


def _Window2(title=_Title, fraction=0.5):
    '''Create the main window and the drawable view.
    '''
    def _m10(x):  # multiple of 10
        return max(1, int(x * 0.1) - 1) * 10

    screen = NSScreen.alloc().init()
    frame = screen.mainScreen().frame()
    if 0.1 < fraction < 1.0:
        # use the lower left quarter of the screen size as frame
        frame = NSMakeRect(frame.origin.x + 10, frame.origin.y + 10,
                          _m10(frame.size.width * fraction),
                          _m10(frame.size.height * fraction))

    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                frame,
                NSUsualWindowMask,  # PYCHOK expected
                NSBackingStoreBuffered,
                False)  # or 0

    if title:
        window.setTitle_(NSString(title))

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


def appVLC(title=_Title, video='', player=None, timeout=None):
    '''Create the application and start the VLC player,
       before calling app.run() to start the application.
    '''
    app = NSApplication.sharedApplication()
#   pool = NSAutoreleasePool.alloc().init()  # created by NSApplication

    dlg = _Delegate.alloc().init(app, title, video, player)
    app.setDelegate_(dlg)

    # <http://Developer.Apple.com/documentation/appkit/nsdocktile>
    # <http://Developer.Apple.com/documentation/appkit/nsapplication>
    dlg.badge = app.dockTile()  # get the app's NSDockTile instance

    if timeout:
        try:
            s = float(timeout or 0) + 1

            def _terminate():
                sleep(s)
                app.terminate_(app)

            t = Thread(target=_terminate)
            t.start()

        except ValueError:
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
            _printf('usage: %s  [-h|--help]  [-timeout <secs>]  [video_file_name]', _argv0)
            sys.exit(0)
        elif '-timeout'.startswith(t) and len(t) > 1 and args:
            _timeout = args.pop(0)
        else:
            _printf('invalid option: %s', o)
            sys.exit(1)

    if args:
        video = args.pop(0)
    else:
        _printf('- select a video from the open file panel', nl=1, nt=1)
        video = _OpenFilePanel(_Movies)

    if video:
        player = vlc.MediaPlayer(video)
#       player.play()  # NOT YET!

        app = appVLC(title=_argv0, video=video, player=player, timeout=_timeout)
        app.run()  # never returns
