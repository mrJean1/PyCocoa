
# -*- coding: utf-8 -*-

# License at the end of this file.  This file has been superseded
# by an other, more comprehensive VLC player example cocoavlc.py
# <https://GitHub.com/oaubert/python-vlc/tree/master/examples>

import os
import platform  # PYCHOK false
import sys

_Name = os.path.basename(__file__)
if not sys.platform.startswith('darwin'):
    raise ImportError('%s only supported on %s' % (_Name, 'macOS'))

# the imports listed explicitly to help PyChecker
from pycocoa import gcd, get_selector, NSAlternateKeyMask, \
                    NSApplication, NSBackingStoreBuffered, \
                    nsBundleRename, NSCommandKeyMask, \
                    NSControlKeyMask, NSMenu, NSMenuItem, \
                    NSRect4_t, NSScreen, NSShiftKeyMask, \
                    NSSize_t, NSStr, NSView, NSWindow, \
                    NSWindowStyleMaskUsual, ObjCClass, \
                    ObjCInstance, ObjCSubclass, printf, \
                    PyObjectEncoding, send_super, terminating, \
                    __version__ as __PyCocoa__  # PYCHOK false

from pycocoa.utils import _Globals
_Globals.argv0 = _Name  # for printf

__all__  = ('simpleVLCplay',)
__version__ = '19.09.23'


def _mspf(fps):
    # convert frames per second to frame length in millisecs
    return 1000.0 / (fps or 25)


class _Delegate_Implementation(object):
    # Cobbled together from the pycocoa.ObjCSubClass.__doc__,
    # pycocoa.runtime._DeallocObserver and PyObjC examples:
    # <http://TaoOfMac.com/space/blog/2007/04/22/1745> and
    # <http://StackOverflow.com/questions/24024723/swift-using
    # -nsstatusbar-statusitemwithlength-and-nsvariablestatusitemlength>
    _Delegate = ObjCSubclass('NSObject', '_Delegate')

    # The _Delegate.method(signature) decorator specfies the
    # signature of a Python method in Objective-C type encoding
    # and makes the Python method callable from Objective-C.

    # This is rather ugly, especially since the decorator is
    # also required for (private) methods called only from
    # Python.

    # See pycocoa.runtime.split_encoding for type encoding:
    # first is return value, then the method args, no need to
    # include @: for self and the Objective-C selector/cmd.
    @_Delegate.method(b'@' + PyObjectEncoding * 4)
    def init(self, app, player, title, video):
        self = ObjCInstance(send_super(self, 'init'))
#       self = ObjCInstance(send_message('NSObject', 'alloc'))
        self.app    = app
        self.NSitem = None  # Play/Pause toggle
        self.player = player
        self.ratio  = 2
        self.title  = title  # app name, top-level menu title
        self.video  = video  # window banner
        self.window = None
        nsBundleRename(NSStr(title))  # top-level menu title
        return self

    @_Delegate.method('v@')  # void, ObjC
    def applicationDidFinishLaunching_(self, notification):

        # the player needs an NSView object
        self.window, view = _Window2(title=self.video or self.title)
        # set the window's delegate to the app's to
        # make method .windowWillClose_ work, see
        # <https://Gist.GitHub.com/kaloprominat/6105220>
        self.window.setDelegate_(self)
        # pass viewable to VLC player
        self.player.set_nsobject(view)

        menu = NSMenu.alloc().init()  # create main menu
        menu.addItem_(_MenuItem('Full ' + 'Screen', 'enterFullScreenMode:', 'f', ctrl=True))  # Ctrl-Cmd-F, Esc to exit
        menu.addItem_(_MenuItem('Info', 'info:', 'i'))

        menu.addItem_(_MenuItemSeparator())
        self.NSitem = _MenuItem('Pause', 'toggle:', 'p', ctrl=True)  # Ctrl-Cmd-P
        menu.addItem_(self.NSitem)
        menu.addItem_(_MenuItem('Rewind', 'rewind:', 'r', ctrl=True))  # Ctrl-Cmd-R

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

        self.player.play()
        # adjust the contents' aspect ratio
        self.windowDidResize_(None)

    @_Delegate.method('v@')
    def info_(self, notification):
        try:
            p = self.player
            if p.is_playing():
                p.pause()
            m = p.get_media()
            v = sys.modules[p.__class__.__module__]  # import vlc
            b = v.bytes_to_str

            # print Python, vlc, libVLC, media info
            printf('PyCocoa %s (%s)', __PyCocoa__, __version__, nl=1)
            printf('Python %s %s', sys.version.split()[0], platform.architecture()[0])
            printf('macOS %s', ' '.join(platform.mac_ver()[0:3:2]), nt=1)

            printf('vlc.py %s (%#x)', v.__version__, v.hex_version())
            printf('built: %s', v.build_date)

            printf('libVLC %s (%#x)', b(v.libvlc_get_version()), v.libvlc_hex_version())
            printf('libVLC %s', b(v.libvlc_get_compiler()), nt=1)

            printf('media: %s', b(m.get_mrl()))
            printf('state: %s', p.get_state())

            printf('track/count: %s/%s', p.video_get_track(), p.video_get_track_count())
            printf('time/duration: %s/%s ms', p.get_time(), m.get_duration())
            printf('position/length: %.2f%%/%s ms', p.get_position() * 100.0, p.get_length())
            f = p.get_fps()
            printf('fps: %.3f (%.3f ms)', f, _mspf(f))
            printf('rate: %s', p.get_rate())

            w, h = p.video_get_size(0)
            printf('video size: %sx%s', w, h)  # num=0
            r = gcd(w, h) or ''
            if r and w and h:
                r = ' (%s:%s)' % (w // r, h // r)
            printf('aspect ratio: %s%s', p.video_get_aspect_ratio(), r)

            printf('scale: %.3f', p.video_get_scale())
            o = p.get_nsobject()  # for macOS only
            printf('nsobject: %r (%#x)', o, o, nt=1)
        except Exception as x:
            printf('%r', x, nl=1, nt=1)

    @_Delegate.method('v@')
    def rewind_(self, notification):
        self.player.set_position(0.0)
        # can't re-play once at the end
        # self.player.play()

    @_Delegate.method('v@')
    def toggle_(self, notification):
        # toggle between Pause and Play
        if self.player.is_playing():
            # note, .pause() pauses and un-pauses the video,
            # .stop() stops the video and blanks the window
            self.player.pause()
            t = 'Play'
        else:
            self.player.play()
            t = 'Pause'
        self.NSitem.setTitle_(NSStr(t))

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


_Delegate = ObjCClass('_Delegate')  # the actual class


def _MenuItem(label, action=None, key='', alt=False, cmd=True, ctrl=False, shift=False):
    '''New NS menu item with action and optional shortcut key.
    '''
    # <http://Developer.Apple.com/documentation/appkit/nsmenuitem/1514858-initwithtitle>
    ns = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
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
            ns.setKeyEquivalentModifierMask_(mask)
    return ns


def _MenuItemSeparator():
    '''A menu separator item.
    '''
    return NSMenuItem.separatorItem()


def _Window2(title=_Name, fraction=0.5):
    '''Create the main NS window and the drawable NS view.
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


def simpleVLCplay(player, title=_Name, video='', timeout=None):
    '''Create a minimal NS application, drawable window and basic menu
       for the given VLC player (with media) and start the player.

       @note: This function never returns, but the VLC player and
              other Python thread(s) do run.
    '''
    if not player:
        raise ValueError('%s invalid: %r' % ('player', player))

    app = NSApplication.sharedApplication()
#   pool = NSAutoreleasePool.alloc().init()  # created by NSApplication
    dlg = _Delegate.alloc().init(
                    app,
                    player,
                    title or _Name,
                    video or os.path.basename(player.get_media().get_mrl()))
    app.setDelegate_(dlg)
    terminating(app, timeout)
    app.run()  # never returns


if __name__ == '__main__':

    try:
        import vlc  # PYCHOK used
    except ImportError:
        raise ImportError('no %s module (%s)' % ('vlc.py',
                          '<https://PyPI.org/project/python-vlc>'))

    _Globals.argv0 = _name = os.path.basename(sys.argv[0])
    _timeout = None

    args = sys.argv[1:]
    while args and args[0].startswith('-'):
        o = args.pop(0)
        t = o.lower()
        if t in ('-h', '--help'):
            printf('usage:  [-h|--help]  [-name "%s"]  [-timeout <secs>]  %s',
                   _name, '<video_file_name>')
            sys.exit(0)
        elif args and len(t) > 1 and '-name'.startswith(t):
            _name = args.pop(0)
        elif args and len(t) > 1 and '-timeout'.startswith(t):
            _timeout = args.pop(0)
        else:
            printf('invalid option: %s', o)
            sys.exit(1)

    if not args:
        printf('missing %s', '<video_file_name>')
        sys.exit(1)

    # create a VLC player to play a video
    p = vlc.MediaPlayer(args.pop(0))
    simpleVLCplay(p, title=_name, timeout=_timeout)  # never returns

# MIT License <http://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2019 -- mrJean1 at Gmail dot com
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
