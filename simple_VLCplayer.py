
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

import os
import sys
if not sys.platform.startswith('darwin'):
    raise ImportError('unsupported platform: %s' % (sys.platform,))

try:  # the imports listed explicitly to help PyChecker
    from pycocoa import NSAlternateKeyMask, NSApplication, \
                        NSBackingStoreBuffered, NSCommandKeyMask, \
                        NSControlKeyMask, NSMakeRect, NSMenu, \
                        NSMenuItem, NSOpenPanel, NSScreen, \
                        NSShiftKeyMask, NSString, NSUsualWindowMask, \
                        NSView, NSWindow, ObjCClass, ObjCInstance, \
                        ObjCSubclass, PyObjectEncoding, \
                        get_selector, nsString2str, send_super
except ImportError:
    raise ImportError('no %s module (%s)' % ('pycocoa',
                      '<http://PyPI.Python.org/pypi/PyCocoa>'))

__all__  = ('appVLC',)
__version__ = '18.03.10'

_Title  = os.path.basename(__file__)
_Movies = '.mov', '.mp4'  # lower-case file types for movies, videos


class _Delegate_Implementation(object):
    # cobbled together from the pycocoa.ObjCSubClass.__doc__
    # and pycocoa.runtime._DeallocObserver_Implementation
    # and the following PyObjC examples:
    # <http://TaoOfMac.com/space/blog/2007/04/22/1745> and
    # <http://StackOverflow.com/questions/24024723/swift-using
    # -nsstatusbar-statusitemwithlength-and-nsvariablestatusitemlength>
    _Delegate = ObjCSubclass('NSObject', '_Delegate')

    # the _Delegate.method(signature) decorator specfies the
    # signature of a Python method in Objective-C type encoding,
    # see pycocoa.runtime.split_encoding for type encoding:
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

    @_Delegate.method(b'@' + PyObjectEncoding)
    def badgelabel(self, label):
        if self.badge:
            self.badge.setBadgeLabel_(NSString(label))

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
    def windowWillClose_(self, notification):
        # this method is only called if this
        # _Delegate is the window's delegate
        self.app.terminate_(self)  # or NSApp()...


_Delegate = ObjCClass('_Delegate')  # the actual class


def _MenuItem(label, action=None, key='', alt=False, cmd=True, ctrl=False, shift=False):
    '''New menu item with action and optional shortcut key.
    '''
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
    '''Create the main window and drawable view.
    '''
    screen = NSScreen.alloc().init()
    frame = screen.mainScreen().frame()
    if 0.1 < fraction < 1.0:
        frame = NSMakeRect(frame.origin.x + 10, frame.origin.y + 10,
                           max(10, int(frame.size.width * fraction) - 10),
                           max(10, int(frame.size.height * fraction) - 10))

    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                frame,
                NSUsualWindowMask,  # PYCHOK expected
                NSBackingStoreBuffered,
                False)  # or 0

    if title:
        window.setTitle_(NSString(title))

    # create the drawable_nsobject NSView for vlc.py see vlc.MediaPlayer.set_nsobject()
    # for an alternate NSView object with protocol VLCOpenGLVideoViewEmbedding
    # <http://StackOverflow.com/questions/11562587/create-nsview-directly-from-code>
    # <http://GitHub.com/ariabuckles/pyobjc-framework-Cocoa/blob/master/Examples/AppKit/DotView/DotView.py>
    view = NSView.alloc().initWithFrame_(frame)
    window.setContentView_(view)

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

    # set up the timeout
    if timeout is not None:
        try:  # PyCocoa/test
            from test import testing
            testing(dlg, timeout)
        except ImportError:
            pass

    return app


if __name__ == '__main__':

    secs = None
    arg0 = os.path.basename(sys.argv[0])  # _Title

    args = sys.argv[1:]
    while args and args[0].startswith('-'):
        o = args.pop(0)
        t = o.lower()
        if t in ('-h', '--help'):
            print('usage: %s  [-h|--help]  [-timeout <secs>]  [video_file_name]' % (arg0,))
            sys.exit(0)
        elif '-timeout'.startswith(t) and len(t) > 1 and args:
            secs = float(args.pop(0))
        else:
            print('%s invalid option: %s' % (arg0, o))
            sys.exit(1)

    if args:
        video = args.pop(0)
    else:
        print('\n%s: select a video from the open file panel ...\n' % (arg0,))
        video = _OpenFilePanel(_Movies)

    if video:
        try:
            import vlc
        except ImportError:
            raise ImportError('no %s module (%s)' % ('vlc.py',
                              '<http://PyPI.Python.org/pypi/python-vlc>'))

        print('\n%s using: vlc.py %s, libVLC %s, Python %s\n' % (arg0,
              vlc.__version__, vlc.libvlc_get_version(), sys.version.split()[0]))

        inst = vlc.Instance()
        player = inst.media_player_new()
        media = inst.media_new(video)
        player.set_media(media)
#       player.play()  # NOT YET!

        app = appVLC(title=arg0, video=video, player=player, timeout=secs)
        app.run()  # never returns
