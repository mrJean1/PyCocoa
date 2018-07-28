
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Types L{App} and L{Tile}, wrapping ObjC C{NSApplication} and C{NSDocktile}.
'''
# all imports listed explicitly to help PyChecker
from bases   import _Type2
from menus   import _menuItemHandler_name, Menu, MenuBar, ns2Item
from nstypes import NSApplication, nsBundleRename, \
                    NSConcreteNotification, NSMain, NSNotification, \
                    nsOf, NSStr
# from oslibs  import YES
from runtime import isInstanceOf, ObjCClass, ObjCInstance, \
                    _ObjC_log_totals, ObjCSubclass, release, retain, \
                    send_super_init
from utils   import _Globals, bytes2str, isinstanceOf, printf, _Types

from threading import Thread
from time import sleep

__all__ = ('App',
           'NSApplicationDelegate',
           'Tile',
           'app_title',
           'ns2App')
__version__ = '18.07.27'


class App(_Type2):
    '''Python C{App} Type, wrapping an ObjC L{NSApplication}.
    '''
    _badge      = None
    _isUp       = None
    _keyWindow  = None  # Window
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

    def append(self, menu):
        '''Add a menu to this app's menu bar.

           @param menu: The menu to add (L{Menu}).

           @note: The first menu item of the bar menu is provided by default.
        '''
        isinstanceOf(menu, Menu, name='menu')

        if self._menubar is None:
            # create the menu bar, once
            self._menubar = MenuBar(self)

            m = Menu(self.title)
            m.append(
                m.item('Full ' + 'Screen', key='f', ctrl=True),  # Ctrl-Cmd-F, Esc to exit
                m.separator(),
                m.item('Hide ' + self.title, 'menuHide_', key='h'),  # Cmd-H, implied
                m.item('Hide Others', key='h', alt=True),  # Alt-Cmd-H
                m.item('Show All'),  # no key
                m.separator(),
                m.item('Quit ' + self.title, 'menuTerminate_', key='q'),  # Cmd-Q
            )
            self._menubar.append(m)
            self._menubar.main(self)

        self._menubar.append(menu)

    @property
    def badge(self):
        '''Get this app's dock tile/badge (L{Tile}).
        '''
        # <http://Developer.Apple.com/documentation/appkit/nsdocktile>
        # <http://Developer.Apple.com/documentation/appkit/nsapplication>
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
        '''Hide or show this app's main window.

           @param hide: Hide or show (C{bool}).
        '''
        if hide:
            self.NS.hide_(self.NS)
        elif self.isHidden:
            self.NS.unhide_(self.NS)

    def hideOther(self, hide):
        '''Hide other or show all apps's windows.

           @param hide: Hide or show (C{bool}).
        '''
        if hide:
            self.NS.hideOtherApplications_(self.NS)
        else:
            self.NS.unhideAllApplications_(self.NS)

    @property
    def isHidden(self):
        '''Get this app's hidden state (C{bool}).
        '''
        return True if self.NS.isHidden() else False

    @property
    def isRunning(self):
        '''Get this app's running state (C{bool}).
        '''
        return True if self.NS.isRunning() else False

    @property
    def isUp(self):
        '''Get this app's launched state (C{bool}).
        '''
        return self._isUp

    @property
    def keyWindow(self):
        '''Get this app's key window (L{Window}).
        '''
        return self._keyWindow

    @property
    def mainWindow(self):
        '''Get this app's main window (L{Window}).
        '''
        return self._mainWindow

    @property
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

           @keyword timeout: Run time limit in seconds (float).

           @note: Although I{run} never returns, any Python threads
           started earlier continue to run concurrently.
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
        '''Terminate this app (never returns).
        '''
        _ObjC_log_totals()
        # <http://Developer.Apple.com/documentation/
        #       appkit/nsapplication/1428417-terminate>
        self.NS.terminate_(self.NS)

    # Callback methods for Window instances,
    # menus, etc. to be overloaded as needed
    def appLaunched_(self, app):  # PYCHOK expected
        '''Callback, the app launched and is up.
        '''
        self._isUp = True

#   def appStop_(self, sender=None):
        # Stop this app's event loop.
        # <http://Developer.Apple.com/documentation/
        #       appkit/nsapplication/1428473-stop>
#       self.NS.stop_(nsOf(sender or self))

    def menuFullScreen_(self, item):  # PYCHOK expected
        '''Callback for C{Full Screen} menu I{item}.
        '''
        self.full(True)

    def menuHide_(self, item):  # PYCHOK expected
        '''Callback for C{Hide} menu I{item}.
        '''
        self.hide(True)

    def menuHideOthers_(self, item):  # PYCHOK expected
        '''Callback for C{Hide Other} menu I{item}.
        '''
        self.hideOther(True)

    def menuShowAll_(self, item):  # PYCHOK expected
        '''Callback for C{Show All} menu I{item}.
        '''
        self.hideOther(False)

    def menuTerminate_(self, item):  # PYCHOK expected
        '''Callback for C{Quit} menu I{item}.
        '''
        self.terminate()

    def windowClose_(self, window):
        '''Closing I{window} callback.
        '''
        if self.keyWindow is window:
            self._keyWindow = None
        if self.mainWindow is window:
            self._mainWindow = None

    def windowCloseOK_(self, window):  # PYCHOK expected
        '''Is it OK? to close I{window} callback.

           @return: True if OK to close, False otherwise.
        '''
        return True

    def windowKey_(self, window):
        '''Callback I{window} becomes/resigns C{Key}.
        '''
        self._keyWindow = window or None
#       if self._menubar:
#           self._menubar.NS.update()

    def windowMain_(self, window):
        '''Callback I{window} becomes/resigns C{Main}.
        '''
        self._mainWindow = window or None

    def windowPrint_(self, window):  # PYCHOK expected
        '''Print I{window} callback.
        '''
        pass

    def windowResize_(self, window):  # PYCHOK expected
        '''Resizing I{window} callback.
        '''
        pass

    def windowZoomOK_(self, window, frame=None):  # PYCHOK expected
        '''Is it OK? to toggle zoom I{window} callback.

           @keyword frame: The frame to zoom to (L{Rect}).

           @return: True if OK to toggle, False otherwise.
        '''
        return True


# <http://Developer.Apple.com//library/content/samplecode/
#       CocoaTipsAndTricks/Listings/ExceptionReporting_ExceptionReportingAppDelegate_m.html>
# <http://Developer.Apple.com//library/content/samplecode/
#       CocoaTipsAndTricks/Listings/ExceptionReporting_main_m.html>
# <http://Developer.Apple.com//library/content/samplecode/
#       CocoaTipsAndTricks/Listings/ExceptionReporting_MyApplication_m.html>


class _NSApplicationDelegate(object):
    '''An ObjC-callable I{NSDelegate} class to handle L{NSApplication},
       L{NSMenu} and L{NSWindow} events as calls to Python
       L{App}C{.app..._}, L{App}C{.menu..._} respectively
       L{App}C{.window..._} callback methods.
    '''
    # Cobbled together from the pycocoa.ObjCSubclass.__doc__,
    # pycocoa.runtime._NSDeallocObserver and PyObjC examples:
    # <http://TaoOfMac.com/space/blog/2007/04/22/1745> and
    # <http://StackOverflow.com/questions/24024723/swift-using-
    #       nsstatusbar-statusitemwithlength-and-nsvariablestatusitemlength>
    _ObjC = ObjCSubclass('NSObject', '_NSApplicationDelegate')

    # The _ObjC.method(signature) decorator specifies the signature
    # of a Python method in Objective-C type encoding to make the
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

    # <http://GitHub.com/thesecretlab/LearningCocoa4thEd/tree/master/
    #       AwesomeGrid/AwesomeGrid>,
    # <http://GitHub.com/thesecretlab/LearningCocoa4thEd/tree/master/
    #       HelloCocoa/HelloCocoa>, etc.

#   @_ObjC.method('v@')
#   def applicationDidBecomeActive_(self, ui_application):
#       '''Restart any tasks that were paused (or not yet started) while the
#          application was inactive. If the application was previously in the
#          background, optionally refresh the user interface.
#       '''
#       pass

    # <http://GitHub.com/thesecretlab/LearningCocoa4thEd/tree/master/
    #       AppNapping/AppNapping>
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
        '''ObjC callback to handle L{NSApplication} event.
        '''
        self.app._isUp = True
        self.app.appLaunched_(ns2App(ns_notification))

#   @_ObjC.method('Bv@')
#   def applicationDidFinishLaunchingWithOptions_(self, ns_dictionary):
#       '''ObjC callback to handle C{UIApplication} event.
#       '''
#       return YES

#   @_ObjC.method('Bv@')
#   def applicationShouldTerminateAfterLastWindowClosed_(self, ns_application):
#       return YES

#   @_ObjC.method('v@')
#   def applicationWillEnterForeground_(self, ui_application):
#       '''Called as part of the transition from the background to the
#          inactive state; here you can undo many of the changes made
#          on entering the background.
#       '''
#       pass

#   @_ObjC.method('v@')
#   def applicationWillResignActive_(self, ui_application):
#       '''Sent when the application is about to move from active to
#          inactive state.  This can occur for certain types of temporary
#          interruptions (such as an incoming phone call or SMS message)
#          or when the user quits the application and it begins the
#          transition to the background state.
#
# 	       Use this method to pause ongoing tasks, disable timers, and
# 	       throttle down OpenGL ES frame rates. Games should use this
# 	       method to pause the game.
#       '''
#       pass

#   @_ObjC.method('v@')
#   def applicationWillTerminate_(self, ui_application):
#       '''App is about to terminate.  Save data if appropriate.
#          @see: C{applicationDidEnterBackground_}.
#       '''
#       pass

    @_ObjC.method('v@')
    def menuItemHandler_(self, ns_item):
        '''ObjC callback to handle and dispatch L{NSMenuItem}
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
                               _menuItemHandler_name, i, t, act)
                        raise
        else:
            if _Globals.raiser:
                raise RuntimeError('%s(%r): %s' % ('unhandled', item, act))


assert (_NSApplicationDelegate.menuItemHandler_.name == _menuItemHandler_name), _menuItemHandler_name
NSApplicationDelegate = ObjCClass('_NSApplicationDelegate')


class Tile(_Type2):
    '''Dock tile for an L{App}, wrapping an ObjC L{NSDockTile}.
    '''
    _label = ''

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
    '''Get the L{App} instance from an L{NSApplication} or an
       L{NSNotification} instance.

       @param ns: The ObjC instance (C{NS...}).

       @return: The app instance (L{App}).

       @raise RuntimeError: L{App} mismatch.

       @raise TypeError: Invalid I{ns} type.
    '''
    if isInstanceOf(ns, NSApplication):
        pass
    elif isInstanceOf(ns, NSConcreteNotification, NSNotification, ns='ns'):
        ns = ns.object()
    if ns == _Globals.App.NS:
        return _Globals.App
    raise RuntimeError('%r vs %r' % (ns, _Globals.App.NS))


NSApplication._Type = _Types.App = App

if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)

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
