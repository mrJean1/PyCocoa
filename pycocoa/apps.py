
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Types L{App} and L{Tile}, wrapping ObjC C{NSApplication} and C{NSDocktile}.
'''
# all imports listed explicitly to help PyChecker
from pycocoa.bases   import _Type2
from pycocoa.menus   import _callMenuItem_name, _handleMenuItem_name, \
                             Item, ItemSeparator, Menu, MenuBar, ns2Item
from pycocoa.lazily  import _ALL_LAZY, _NN_
from pycocoa.nstypes import NSApplication, nsBundleRename, \
                            NSConcreteNotification, NSMain, \
                            NSNotification, nsOf, NSStr
# from pycocoa.oslibs  import YES
from pycocoa.runtime import isObjCInstanceOf, ObjCDelegate, ObjCInstance, \
                            ObjCSubclass, _ObjC_log_totals, release, retain, \
                            send_super_init
from pycocoa.utils   import _Globals, bytes2str, isinstanceOf, \
                             module_property_RO, printf, property_RO, _Types

from threading import Thread
from time import sleep

__all__ = _ALL_LAZY.apps
__version__ = '21.11.04'


class App(_Type2):
    '''Python C{App} Type, wrapping an ObjC C{NSApplication}.
    '''
    _badge      = None
    _isUp       = None
    _keyWindow  = None  # Window
    _lastWindow = None  # most recent key or main
    _mainWindow = None  # Window
    _menubar    = None
    _timeout    = None

    def __init__(self, title='PyCocao', raiser=False, **kwds):
        '''New L{App}.

           @keyword title: App name or title (C{str}).
           @keyword raiser: Throw exceptions for silent errors (C{bool}).
           @keyword kwds: Optional, additional keyword arguments.

           @raise RuntimeError: Duplicate L{App}s.
        '''
        if _Globals.App:
            raise RuntimeError('%s already exists' % (_Globals.App,))
        _Globals.App = self
        if raiser:
            _Globals.raiser = raiser

        self.NS = NSMain.Application
        # add a method to set the app's title
        self.NS.setTitle_ = nsBundleRename
#       pool = NSAutoreleasePool.alloc().init()  # created by NSApplication
        self.title = title

        if kwds:  # optional, additional attributes
            super(App, self).__init__(**kwds)

        self.NSdelegate = retain(NSApplicationDelegate.alloc().init(self))

    def activate(self, active, force=True):
        '''Active or de-activate this app.

           @param active: Activate or de-activate (C{bool}).
           @keyword force: Activate regardless (C{bool}), otheriwse
                           only activate if no other app is active

           @return: Previous C{isActive} value (C{bool}).

           @see: U{activate(ignoringOtherApps flag: Bool)
                 <https://Developer.Apple.com/documentation/appkit/
                 nsapplication/1428468-activate>}.
        '''
        a = self.isActive
        if a and not active:
            self.NS.deactivate()
        elif active and not a:
            self.NS.activateIgnoringOtherApps_(force)
        return a

    def append(self, menu):
        '''Add a menu to this app's menu bar.

           @param menu: The menu to add (L{Menu}).

           @note: The first menu item of the bar menu is provided by default.
        '''
        isinstanceOf(menu, Menu, name='menu')

        if self._menubar is None:
            # create the menu bar, once
            b = MenuBar(app=self)
            m = Menu(title=self.title)
            m.append(  # note key modifier cmd=True is the default
                Item('Full ' + 'Screen', key='f', ctrl=True),  # Ctrl-Cmd-F, Esc to exit
                ItemSeparator(),
                Item('Hide ' + self.title, self.menuHide_, key='h'),  # Cmd-H
                Item('Hide Others', self.menuOther_, key='h', alt=True),  # Alt-Cmd-H
                ItemSeparator(),
                Item('Quit ' + self.title, self.menuTerminate_, key='q'),  # Cmd-Q
            )
            b.append(m)
            b.main(app=self)
            self._menubar = b

        self._menubar.append(menu)

    @property_RO
    def badge(self):
        '''Get this app's dock tile/badge (L{Tile}).
        '''
        # <https://Developer.Apple.com/documentation/appkit/nsdocktile>
        # <https://Developer.Apple.com/documentation/appkit/nsapplication>
        if self._badge is None:
            self._badge = Tile(self)
        return self._badge

    def full(self, full):
        '''Enter or exit full screen mode for this app.

           @param full: Enter or exit (C{bool}).
        '''
        if full:
            self.NS.enterFullScreenMode_(self.NS)
        else:
            self.NS.exitFullScreenMode_(self.NS)

    def hide(self, hide):
        '''Hide or show this app's windows.

           @param hide: Hide or show (C{bool}).

           @return: Previous C{isHidden} value (C{bool}).

           @see: U{unhideWithoutActivation
                 <https://Developer.Apple.com/documentation/appkit/
                 nsapplication/1428566-unhidewithoutactivation>}.
        '''
        h = self.isHidden
        if h and not hide:
            self.NS.unhide_(self.NS)
        elif hide and not h:
            self.NS.hide_(self.NS)
        return h

    def hideOther(self, hide):
        '''Hide other or show all apps's windows.

           @param hide: Hide or show (C{bool}).
        '''
        if hide:
            self.NS.hideOtherApplications_(self.NS)
        else:
            self.NS.unhideAllApplications_(self.NS)

    @property_RO
    def isActive(self):
        '''Get this app's active state (C{bool}).
        '''
        return True if self.NS.isActive() else False

    @property_RO
    def isHidden(self):
        '''Get this app's hidden state (C{bool}).
        '''
        return True if self.NS.isHidden() else False

    @property_RO
    def isRunning(self):
        '''Get this app's running state (C{bool}).
        '''
        return True if self.NS.isRunning() else False

    @property_RO
    def isUp(self):
        '''Get this app's launched state (C{bool}).
        '''
        return self._isUp

    @property_RO
    def keyWindow(self):
        '''Get this app's key window (L{Window}) or C{None}.
        '''
        return self._keyWindow

    @property_RO
    def lastWindow(self):
        '''Get this app's most recent key or main window (L{Window}).
        '''
        return self._lastWindow

    @property_RO
    def mainWindow(self):
        '''Get this app's main window (L{Window}) or C{None}.
        '''
        return self._mainWindow

    @property_RO
    def menubar(self):
        '''Get this app's menu bar (L{MenuBar}).
        '''
        return self._menubar

    @property
    def raiser(self):
        '''Get raise errors option (C{bool}).
        '''
        return _Globals.raiser

    @raiser.setter  # PYCHOK property.setter
    def raiser(self, raiser):
        '''Set the raise errors option (C{bool}).
        '''
        _Globals.raiser = bool(raiser)

    def run(self, timeout=None):
        '''Run this app (never returns).

           @keyword timeout: Run time limit in seconds (C{float}).

           @note: Although I{run} never returns, any Python threads
                  started earlier continue to run concurrently.
        '''
        if timeout:
            try:
                s = float(timeout or 0)
            except ValueError:
                s = 0

            if s > 0:
                self._timeout = s

                def _t():
                    sleep(s + 0.5)
                    self.terminate()

                Thread(target=_t).start()

        self.NS.run()

    def terminate(self):
        '''Terminate this app (never returns).
        '''
        _ObjC_log_totals()
        # <https://Developer.Apple.com/documentation/
        #        appkit/nsapplication/1428417-terminate>
        self.NS.terminate_(self.NS)

    # Callback methods for Window instances,
    # menus, etc. to be overloaded as needed
    def appLaunched_(self, app):  # PYCHOK expected
        '''Callback, the app launched and is up.
        '''
        self._isUp = True

#   def appStop_(self, sender=None):
        # Stop this app's event loop.
        # <https://Developer.Apple.com/documentation/
        #        appkit/nsapplication/1428473-stop>
#       self.NS.stop_(nsOf(sender or self))

    def menuFullScreen_(self, item):  # PYCHOK expected
        '''Callback for C{Full Screen} menu I{item}.
        '''
        self.full(True)

    def menuHide_(self, item):  # PYCHOK expected
        '''Callback for C{Hide} menu I{item}.
        '''
        self.hide(True)

    def menuOther_(self, item):  # PYCHOK expected
        '''Callback for C{Hide/Show Other} menu I{item}.
        '''
        h = item.title.startswith('Hide')
        self.hideOther(h)
        item.title = 'Show All' if h else 'Hide Others'

    def menuTerminate_(self, item):  # PYCHOK expected
        '''Callback for C{Quit} menu I{item}.
        '''
        self.terminate()

    def windowClose_(self, window):  # PYCHOK expected
        '''Closing I{window} callback.
        '''
        self.windowKey_(None)
        # self.windowLast_(None)
        self.windowMain_(None)

    def windowCloseOK_(self, window):  # PYCHOK expected
        '''Is it OK? to close I{window} callback.

           @return: True if OK to close, False otherwise.
        '''
        return True

    def windowKey_(self, window):
        '''Callback I{window} becomes/resigns C{Key}.
        '''
        self._keyWindow = self._window_None(window)
#       if self._menubar:
#           self._menubar.NS.update()

    def windowLast_(self, window):
        '''Callback I{window} becomes C{Key} or C{Main}.
        '''
        self._lastWindow = window

    def windowMain_(self, window):
        '''Callback I{window} becomes/resigns C{Main}.
        '''
        self._mainWindow = self._window_None(window)

    def windowPrint_(self, window):  # PYCHOK expected
        '''Print I{window} callback.
        '''
        pass

    def windowResize_(self, window):  # PYCHOK expected
        '''Resizing I{window} callback.
        '''
        pass

    def windowScreen_(self, window, change):
        '''Called when I{window} screen or screen profile changed C{Main}.

           @param change: C{True} if the screen or C{False} if
                          the profile changed (C{bool}).
        '''
        pass

    def windowZoomOK_(self, window, frame=None):  # PYCHOK expected
        '''Is it OK? to toggle zoom I{window} callback.

           @keyword frame: The frame to zoom to (L{Rect}).

           @return: True if OK to toggle, False otherwise.
        '''
        return True

    def _window_None(self, window):
        '''(INTERNAL) windowKey and -Main helper.
        '''
        if window:
            if window is not self._lastWindow:
                self.windowLast_(window)
            return window
        else:
            return None

# <https://Developer.Apple.com/library/content/samplecode/
#        CocoaTipsAndTricks/Listings/ExceptionReporting_ExceptionReportingAppDelegate_m.html>
# <https://Developer.Apple.com/library/content/samplecode/
#        CocoaTipsAndTricks/Listings/ExceptionReporting_main_m.html>
# <https://Developer.Apple.com/library/content/samplecode/
#        CocoaTipsAndTricks/Listings/ExceptionReporting_MyApplication_m.html>


class _NSApplicationDelegate(object):
    '''An ObjC-callable I{NSDelegate} class to handle C{NSApplication},
       C{NSMenu} and C{NSWindow} events as calls to Python
       L{App}C{.app..._}, L{App}C{.menu..._} respectively
       L{App}C{.window..._} callback methods.
    '''
    # Cobbled together from the pycocoa.ObjCSubclass.__doc__,
    # pycocoa.runtime._NSDeallocObserver and PyObjC examples:
    # <https://TaoOfMac.com/space/blog/2007/04/22/1745> and
    # <https://StackOverflow.com/questions/24024723/swift-using-
    #        nsstatusbar-statusitemwithlength-and-nsvariablestatusitemlength>
    _ObjC = ObjCSubclass('NSObject', '_NSApplicationDelegate', register=False)  # defer

    # The _ObjC.method(signature) decorator specifies the signature
    # of a Python method as an Objective-C type encoding to make the
    # Python method callable from Objective-C.

    # See pycocoa.runtime.split_encoding for ObjC type encoding of
    # method signatures: first is the return value, then the method
    # args, no need to include @: for self and the ObjC selector/cmd.

    @_ObjC.method('@P')
    def init(self, app):
        '''Initialize the allocated C{NSApplicationDelegate}.

           @note: I{MUST} be called as C{.alloc().init(...)}.
        '''
        isinstanceOf(app, App, name='app')
#       self = ObjCInstance(send_message('NSObject', 'alloc'))
        self = ObjCInstance(send_super_init(self))
        self.app = app
        return self

    # <https://GitHub.com/thesecretlab/LearningCocoa4thEd/tree/master/
    #        AwesomeGrid/AwesomeGrid>,
    # <https://GitHub.com/thesecretlab/LearningCocoa4thEd/tree/master/
    #        HelloCocoa/HelloCocoa>, etc.

#   @_ObjC.method('v@')
#   def applicationDidBecomeActive_(self, ns_notification):
#       '''Sent by the default notification center immediately after
#          the application becomes active.
#
#          Restart any tasks that were paused (or not yet started) while
#          the application was inactive.  If the application was previously
#          in the background, optionally refresh the user interface.
#       '''
#       pass

    # <https://GitHub.com/thesecretlab/LearningCocoa4thEd/tree/master/
    #        AppNapping/AppNapping>
#   @_ObjC.method('v@')
#   def applicationDidChangeOcclusionState_(self, ns_notification):
#       if ([NSApp occlusionState] & NSApplicationOcclusionStateVisible)
#           NSLog(@"You are in the foreground, go nuts");
#       else
#           NSLog(@"You are in the background, slow down");

#   @_ObjC.method('v@')
#   def applicationDidEnterBackground_(self, ui_application):
#      '''Use this method to release shared resources, save user data,
#         invalidate timers, and store enough application state information
#         to restore your application to its current state in case it is
#         terminated later.
#
#         If your application supports background execution, this method
#         is called instead of C{applicationWillTerminate_} when the user
#         quits.
#       '''
#       pass

    @_ObjC.method('v@')
    def applicationDidFinishLaunching_(self, ns_notification):
        '''ObjC callback to handle C{NSApplication} event.
        '''
        self.app._isUp = True
        self.app.appLaunched_(ns2App(ns_notification))

#   @_ObjC.method('B@')
#   def applicationDidFinishLaunchingWithOptions_(self, ns_dictionary):
#       '''ObjC callback to handle C{UIApplication} event.
#       '''
#       return YES

#   @_ObjC.method('v@')
#   def applicationDidResignActive_(self, ns_notification):
#       '''Sent by the default notification center immediately after
#          the application is deactivated.
#       '''
#       pass

#   @_ObjC.method('B@')
#   def applicationShouldTerminateAfterLastWindowClosed_(self, ns_application):
#       return YES

    # <https://developer.apple.com/documentation/uikit/
    #          uiapplicationdelegate/1623076-applicationwillenterforeground>
#   @_ObjC.method('v@')
#   def applicationWillEnterForeground_(self, ui_application):
#       '''Called as part of the transition from the background to the
#          active state.  You can use this method to undo many of the
#          changes you made to your app upon entering the background.
#
#          The call to this method is invariably followed by a call to
#          the applicationDidBecomeActive method, which then moves the
#          app from the inactive to the active state.
#       '''
#       pass

#   @_ObjC.method('v@')
#   def applicationWillResignActive_(self, ns_notification):
#       '''Sent by the default notification center immediately before
#          the application is deactivated.
#       '''
#       pass

#   @_ObjC.method('v@')
#   def applicationWillTerminate_(self, ui_application):
#       '''App is about to terminate.  Save data if appropriate.
#          @see: C{applicationDidEnterBackground_}.
#       '''
#       pass

    @_ObjC.method('v@')
    def callMenuItem_(self, ns_item):
        '''ObjC callback to directly call the action for C{NSMenuItem}
           clicks and shortcuts.

           Unhandled clicks, shortcuts and dispatch errors are
           silently ignored, unless L{App} C{raiser} keyword
           argument was C{True}.
        '''
        item = ns2Item(ns_item)
        act = item._action
        try:
            act(item)
        except Exception:
            if _Globals.raiser:
                printf('%s(%r): callable %r ...',
                       _callMenuItem_name, item, act)
                raise

    @_ObjC.method('v@')
    def handleMenuItem_(self, ns_item):
        '''ObjC callback to handle and dispatch C{NSMenuItem}
           clicks and shortcuts.

           All clicks and shortcuts are dispatched to the I{action}
           method of this I{NSDelegate}'s L{App} instance.

           Unhandled clicks, shortcuts and dispatch errors are
           silently ignored, unless L{App} C{raiser} keyword
           argument was C{True}.
        '''
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
                        printf('%s(%r): %r method %s ...',
                               _handleMenuItem_name, i, t, act)
                        raise
        else:
            if _Globals.raiser:
                raise RuntimeError('%s(%r): %s' % ('unhandled', item, act))

    @_ObjC.method('B@')
    def validateMenuItem_(self, ns_item):
        '''ObjC callback to supply the C{NSMenuItem.isEnabled()} state.
        '''
        # <https://StackOverflow.com/questions/4870141/
        #        menu-item-is-enabled-but-still-grayed-out>
        # <https://Developer.Apple.com/library/archive/documentation/Cocoa/
        #        Conceptual/MenuList/Articles/EnablingMenuItems.html>
        # <https://Developer.Apple.com/library/archive/documentation/Cocoa/
        #        Conceptual/MenuList/Articles/EnablingMenuItems.html>
        return ns_item.isEnabled()  # == ns2Item().isEnabled


assert(_NSApplicationDelegate.callMenuItem_.name   == _callMenuItem_name), _callMenuItem_name
assert(_NSApplicationDelegate.handleMenuItem_.name == _handleMenuItem_name), _handleMenuItem_name


@module_property_RO
def NSApplicationDelegate():
    '''The L{ObjCClass}C{(_NSApplicationDelegate.__name__)}.
    '''
    return ObjCDelegate(_NSApplicationDelegate)


class Tile(_Type2):
    '''Dock tile for an L{App}, wrapping an ObjC C{NSDockTile}.
    '''
    _label = _NN_

    def __init__(self, app):
        '''New dock L{Tile}.

           @param app: The app (L{App}).
        '''
        self.app = app
        self.NS = nsOf(app).dockTile()

    @property
    def label(self):
        '''Get the badge text of the app's dock tile (C{str}).
        '''
        return self._label

    @label.setter  # PYCHOK property.setter
    def label(self, label):
        '''Set the badge text of the app's dock tile (C{str}).
        '''
        self._label = bytes2str(label)
        self.NS.setBadgeLabel_(release(NSStr(label)))
        self.NS.display()


def app_title(title):
    '''Get/set the app title.

       @param title: New title (C{str}).

       @return: Previous title (C{str}).
    '''
    return nsBundleRename(release(NSStr(title)))


def ns2App(ns):
    '''Get the L{App} instance from an C{NSApplication} or an
       C{NSNotification} instance.

       @param ns: The ObjC instance (C{NS...}).

       @return: The app instance (L{App}).

       @raise RuntimeError: L{App} mismatch.

       @raise TypeError: Invalid I{ns} type.
    '''
    if isObjCInstanceOf(ns, NSApplication):
        pass
    elif isObjCInstanceOf(ns, NSConcreteNotification, NSNotification, name='ns'):
        ns = ns.object()
    if ns == _Globals.App.NS:
        return _Globals.App
    raise RuntimeError('%s %r vs %r' % ('ns', ns, _Globals.App.NS))


NSApplication._Type = _Types.App = App

if __name__ == '__main__':

    from pycocoa.utils import _all_listing

    _all_listing(__all__, locals())

# % python3 -m pycocoa.apps
#
# pycocoa.apps.__all__ = tuple(
#  pycocoa.apps.App is <class .App>,
#  pycocoa.apps.app_title is <function .app_title at 0x1012e7b50>,
#  pycocoa.apps.ns2App is <function .ns2App at 0x1012e03a0>,
#  pycocoa.apps.NSApplicationDelegate is <pycocoa.utils.module_property_RO object at 0x1012ce6b0>,
#  pycocoa.apps.Tile is <class .Tile>,
# )[5]
# pycocoa.apps.version 21.11.04, .isLazy 1, Python 3.11.0 64bit arm64, macOS 13.0.1

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2023 -- mrJean1 at Gmail -- All Rights Reserved.
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
