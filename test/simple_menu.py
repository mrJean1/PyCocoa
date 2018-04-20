
# -*- coding: utf-8 -*-

# Originally <http://GitHub.com/phillip-nguyen/cocoa-python/blob/master/examples/window_menu.py>

# Example of using PyCocoa to create an NSWindow with
# an application menu item for quitting.

# all imports listed explicitly to help PyChecker
from pycocoa import NSAlternateKeyMask, NSApplication, NSAutoreleasePool, \
                    NSBackingStoreBuffered, NSControlKeyMask, NSMakeRect, \
                    NSMenu, NSMenuItem, NSStr, NSWindowStyleMaskUsual, \
                    NSWindow, get_selector

__version__ = '18.04.09'


def create_window(title=''):
    frame = NSMakeRect(10, 100, 500, 100)
    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                      frame,
                      NSWindowStyleMaskUsual,
                      NSBackingStoreBuffered,
                      0)
    window.setTitle_(NSStr(title))
    window.makeKeyAndOrderFront_(None)
    return window


def create_menu(name='', app=None):
    menubar = NSMenu.alloc().init()
    appMenuItem = NSMenuItem.alloc().init()
    menubar.addItem_(appMenuItem)
    appMenu = NSMenu.alloc().init()

    fullItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
               NSStr('Full Screen'), get_selector('enterFullScreenMode:'), NSStr('f'))
    fullItem.setKeyEquivalentModifierMask_(NSControlKeyMask)  # Ctrl-Cmd-F
    appMenu.addItem_(fullItem)

    appMenu.addItem_(NSMenuItem.separatorItem())

    hideItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
               NSStr('Hide ' + name), get_selector('hide:'), NSStr('h'))
    appMenu.addItem_(hideItem)

    otherItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
               NSStr('Hide Others'), get_selector('hideOtherApplications:'), NSStr('h'))
    otherItem.setKeyEquivalentModifierMask_(NSAlternateKeyMask)  # Alt-Cmd-H
    appMenu.addItem_(otherItem)

    showItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
               NSStr('Show All'), get_selector('unhideAllApplications:'), NSStr(''))
    appMenu.addItem_(showItem)

    appMenu.addItem_(NSMenuItem.separatorItem())

    quitItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
               NSStr('Quit ' + name), get_selector('terminate:'), NSStr('q'))
    appMenu.addItem_(quitItem)

    appMenuItem.setSubmenu_(appMenu)

    if app:
        app.setMainMenu_(menubar)
    return menubar


def create_autorelease_pool():
    pool = NSAutoreleasePool.alloc().init()
    return pool


def application(name='Menu'):
    app = NSApplication.sharedApplication()
    create_autorelease_pool()
    create_window(title=name + ' - Type ⌘Q or select Quit from the Python menu')
    create_menu(name=name, app=app)
    return app


if __name__ == '__main__':

    import sys

    app = application()

    if len(sys.argv) > 1:
        from test import terminating
        terminating(app, sys.argv.pop(1))

    app.run()  # never returns
