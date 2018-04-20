
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

from bases   import _Type2
from menus   import _menuItemHandler_name, Menu, MenuBar, ns2Item
from nstypes import NSApplication, nsBundleRename, \
                    NSConcreteNotification, NSNotification, nsOf, NSStr
from runtime import isInstanceOf, ObjCClass, ObjCInstance, \
                    _ObjC_log_totals, ObjCSubclass, send_super
from utils   import _Globals, bytes2str, instanceof

from threading import Thread
from time import sleep

__all__ = ('App',  'AppDelegate',
           'Tile',
           'ns2App')
__version__ = '18.04.18'


class App(_Type2):
    '''The basic App class.
    '''
    _bar        = None
    _badge      = None
    _isUp       = None
    _keyWindow  = None  # Window
    _mainWindow = None  # Window
    _timeout    = None

    def __init__(self, title='PyCocao', **attrs):
        '''Create an App.
        '''
        if _Globals.App:
            raise RuntimeError('%s already exists' % (_Globals.App,))
        _Globals.App = self

        self.NS = NSApplication.sharedApplication()
        # add a method to set the app's title
        self.NS.setTitle_ = nsBundleRename
#       pool = NSAutoreleasePool.alloc().init()  # created by NSApplication
        self.title = title
        if attrs:  # optional, additional attributes
            super(App, self).__init__(**attrs)

        self.delegate = AppDelegate.alloc().init(self)

    def append(self, menu):
        '''Append a menu to the app's menu bar
        '''
        instanceof(menu, Menu, name='menu')

        if self._bar is None:
            # create the menu bar, once
            self._bar = MenuBar(self)

            main = Menu(self.title)
            main.append(
                main.item('Full ' + 'Screen', key='f', ctrl=True),  # Ctrl-Cmd-F, Esc to exit
                main.separator(),
                main.item('Hide ' + self.title, 'menuHide_', key='h'),  # Cmd-H, implied
                main.item('Hide Others', key='h', alt=True),  # Alt-Cmd-H
                main.item('Show All'),  # no key
                main.separator(),
                main.item('Quit ' + self.title, 'menuTerminate_', key='q'),  # Cmd-Q
            )
            self._bar.append(main)
            self._bar.main(self)

        self._bar.append(menu)

    @property
    def badge(self):
        '''Get the dock tile/badge (L{Tile}).
        '''
        # <http://Developer.Apple.com/documentation/appkit/nsdocktile>
        # <http://Developer.Apple.com/documentation/appkit/nsapplication>
        if self._badge is None:
            self._badge = Tile(self)
        return self._badge

    def hide(self, hide):
        '''Hide or show this app.
        '''
        if hide:
            self.NS.hide_(self.NS)
        elif self.isHidden:
            self.NS.unhide_(self.NS)

    def hideOther(self, hide):
        '''Hide other or show all apps.
        '''
        if hide:
            self.NS.hideOtherApplications_(self.NS)
        else:
            self.NS.unhideAllApplications_(self.NS)

    def full(self, full):
        '''Enter or exit full screen.
        '''
        if full:
            self.NS.enterFullScreenMode_(self.NS)
        else:
            self.NS.exitFullScreenMode_(self.NS)

    @property
    def isHidden(self):
        '''Get the hidden state (bool).
        '''
        return True if self.NS.isHidden() else False

    @property
    def isRunning(self):
        '''Get the running state (bool).
        '''
        return True if self.NS.isRunning() else False

    @property
    def isUp(self):
        '''Get the launched state (bool).
        '''
        return self._isUp

    @property
    def keyWindow(self):
        '''Get the key window (L{Window}).
        '''
        return self._keyWindow

    @property
    def mainWindow(self):
        '''Get the main window (L{Window}).
        '''
        return self._mainWindow

    def run(self, timeout=None):
        '''Run the app, never returns.

           However, any Python threads started
           earlier remain running, concurrently.
        '''
        if timeout is not None:
            try:
                secs = float(timeout or 0)
            except ValueError:
                secs = 0

            if secs > 0:
                self._timeout = secs

                def _terminate():
                    sleep(secs + 0.5)
                    self.terminate()

                t = Thread(target=_terminate)
                t.start()

        self.NS.run()

    def terminate(self):
        '''Terminate the app.
        '''
        _ObjC_log_totals()
        # <http://Developer.Apple.com/documentation/
        #  appkit/nsapplication/1428417-terminate>
        self.NS.terminate_(self.NS)

    # Callback methods for Window instances,
    # menus, etc. to be overloaded as needed

    def appLaunched_(self, app):  # PYCHOK expected
        self._isUp = True

#   def appStop_(self, sender=None):
        # Stop this app's event loop.
        # <http://Developer.Apple.com/documentation/
        #  appkit/nsapplication/1428473-stop>
#       self.NS.stop_(nsOf(sender or self))

    def menuFullScreen_(self, item):  # PYCHOK expected
        self.full(True)

    def menuHide_(self, item):  # PYCHOK expected
        self.hide(True)

    def menuHideOthers_(self, item):  # PYCHOK expected
        self.hideOther(True)

    def menuShowAll_(self, item):  # PYCHOK expected
        self.hideOther(False)

    def menuTerminate_(self, item):  # PYCHOK expected
        self.terminate()

    def windowClose_(self, window):
        if self.keyWindow is window:
            self._keyWindow = None
        if self.mainWindow is window:
            self._mainWindow = None

    def windowCloseOK_(self, window):  # PYCHOK expected
        # return False if the window should not close
        return True

    def windowKey_(self, window):
        self._keyWindow = window
#       if self._bar:
#           self._bar.NS.update()

    def windowMain_(self, window):
        self._mainWindow = window

    def windowResize_(self, window, size=None):  # PYCHOK expected
        # size is None, (w, h) or NSSize_t
        return size

    def windowZoomOK_(self, window, frame=None):  # PYCHOK expected
        # return True if toggling zoom is OK
        return True


# <http://developer.apple.com/library/content/samplecode/
#       CocoaTipsAndTricks/Listings/ExceptionReporting_ExceptionReportingAppDelegate_m.html>
# <http://developer.apple.com/library/content/samplecode/
#       CocoaTipsAndTricks/Listings/ExceptionReporting_main_m.html>
# <http://developer.apple.com/library/content/samplecode/
#       CocoaTipsAndTricks/Listings/ExceptionReporting_MyApplication_m.html>


class _AppDelegate(object):
    '''An ObjC Delegate class to handle C{NSApplication} and C{NSMenu}
       events as L{App}.app..._ respectively L{App}.menu..._  method
       calls.
    '''
    # Cobbled together from the pycocoa.ObjCSubClass.__doc__,
    # pycocoa.runtime._DeallocObserver and PyObjC examples:
    # <http://TaoOfMac.com/space/blog/2007/04/22/1745> and
    # <http://StackOverflow.com/questions/24024723/swift-using-
    #       nsstatusbar-statusitemwithlength-and-nsvariablestatusitemlength>
    _ObjC = ObjCSubclass('NSObject', '_AppDelegate')

    # The _ObjC.method(signature) decorator specifies the signature
    # of a Python method in Objective-C type encoding to make the
    # Python method callable from Objective-C.

    # See pycocoa.runtime.split_encoding for ObjC type encoding of
    # method signatures: first is the return value, then the method
    # args, no need to include @: for self and the ObjC selector/cmd.

    @_ObjC.method('@P')
    def init(self, app):
        instanceof(app, App, name='app')
#       self = ObjCInstance(send_message('NSObject', 'alloc'))
        self = ObjCInstance(send_super(self, 'init'))
        self.app = app
        return self

    @_ObjC.method('v@')
    def applicationDidFinishLaunching_(self, ns_notification):
        self.app._isUp = True
        self.app.appLaunched_(ns2App(ns_notification))

    @_ObjC.method('v@')
    def menuItemHandler_(self, ns_item):
        item = ns2Item(ns_item)
        act = item._action
        for t, i in ((self.app, item),
                     (self,  ns_item)):
            m = getattr(t, act, None)
            if m and callable(m):
                try:
                    m(i)
                    break
                except Exception:
                    if _Globals.raiser:
                        print('%s(%r): %r method %s ...' % (
                              _menuItemHandler_name, i, t, act))
                        raise


assert(_AppDelegate.menuItemHandler_.name == _menuItemHandler_name)
AppDelegate = ObjCClass('_AppDelegate')


class Tile(_Type2):
    '''The dock tile for an L{App}.
    '''
    _label = ''

    def __init__(self, app):
        self.app = app
        self.NS = nsOf(app).dockTile()

    @property
    def label(self):
        '''Get the badge text of the App's dock tile.
        '''
        return self._label

    @label.setter  # PYCHOK property.setter
    def label(self, label):
        '''Set the badge text of the App's dock tile.
        '''
        self._label = bytes2str(label)
        self.NS.setBadgeLabel_(NSStr(self._label))
        self.NS.display()


def ns2App(ns):
    '''Get the L{App} instance for an C{NSApplication} or an
    C{NSNotification} instance.
    '''
    if isInstanceOf(ns, NSApplication):
        pass
    elif isInstanceOf(ns, NSConcreteNotification, NSNotification, ns='ns'):
        ns = ns.object()
    if ns == _Globals.App.NS:
        return _Globals.App
    raise AssertionError('%r vs %r' % (ns, _Globals.App.NS))


if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)
