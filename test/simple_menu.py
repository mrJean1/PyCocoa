
# -*- coding: utf-8 -*-

# Originally <http://GitHub.com/phillip-nguyen/cocoa-python/blob/master/examples/window_menu.py>

# Example of using PyCocoa to create an NSWindow with
# an application menu item for quitting.

# all imports listed explicitly to help PyChecker
from pycocoa import NSApplication, NSAutoreleasePool, \
                    NSBackingStoreBuffered, NSMakeRect, NSMenu, \
                    NSMenuItem, NSString, NSUsualWindowMask, \
                    NSWindow, get_selector

__version__ = '18.03.10'


def create_window(title=''):
    frame = NSMakeRect(10, 100, 300, 100)
    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                frame,
                NSUsualWindowMask,
                NSBackingStoreBuffered,
                0)
    window.setTitle_(NSString('Menu ' + title))
    window.makeKeyAndOrderFront_(None)
    return window


def create_menu(name='', app=None):
    menubar = NSMenu.alloc().init()
    appMenuItem = NSMenuItem.alloc().init()
    menubar.addItem_(appMenuItem)
    appMenu = NSMenu.alloc().init()

    quitItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                NSString('Quit ' + name), get_selector('terminate:'), NSString('q'))
    appMenu.addItem_(quitItem)

    appMenu.addItem_(NSMenuItem.separatorItem())

    hideItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                NSString('Hide ' + name), get_selector('hide:'), NSString('h'))
    appMenu.addItem_(hideItem)

    appMenuItem.setSubmenu_(appMenu)

    if app:
        app.setMainMenu_(menubar)
    return menubar


def create_autorelease_pool():
    pool = NSAutoreleasePool.alloc().init()
    return pool


def application(name='app'):
    app = NSApplication.sharedApplication()
    create_autorelease_pool()
    create_window(title=name)
    create_menu(name=name, app=app)
    return app


if __name__ == '__main__':

    import os
    import sys

    app = application(os.path.basename(__file__))

    if len(sys.argv) > 1:
        from test import terminating
        terminating(app, sys.argv.pop(1))

    app.run()  # never returns
