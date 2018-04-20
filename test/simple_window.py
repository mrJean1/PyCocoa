
# -*- coding: utf-8 -*-

# Originally <http://GitHub.com/phillip-nguyen/cocoa-python/blob/master/examples/simple_window.py>

# Simple example of using PyCocoa to create an NSWindow
# using only fundamental Objective-C send_message calls.

# all imports listed explicitly to help PyChecker
from pycocoa import NSBackingStoreBuffered, NSMakeRect, NSStr, \
                    NSWindowStyleMaskUsual, send_message

__version__ = '18.04.09'


def create_window():
    window = send_message('NSWindow', 'alloc')
    window = send_message(window, 'initWithContentRect:styleMask:backing:defer:',
                          NSMakeRect(10, 500, 600, 300),  # frame
                          NSWindowStyleMaskUsual,
                          NSBackingStoreBuffered,
                          0)  # or False
    send_message(window, 'setTitle:', NSStr("Window - Select Quit from Dock menu"))
    send_message(window, 'makeKeyAndOrderFront:', None)
    return window


def create_autorelease_pool():
    pool = send_message('NSAutoreleasePool', 'alloc')
    pool = send_message(pool, 'init')
    return pool


def application():
    app = send_message('NSApplication', 'sharedApplication')
    create_autorelease_pool()
    create_window()
    return app


if __name__ == '__main__':

    import sys

    app = application()

    if len(sys.argv) > 1:
        from threading import Thread
        from time import sleep

        def _terminating():
            try:
                sleep(float(sys.argv[1]) + 0.5)
            except ValueError:
                return
            send_message(app, 'terminate:')

        t = Thread(target=_terminating)
        t.start()

    send_message(app, 'run')  # never returns
