
# encoding: utf-8

# Reworked from <https://Gist.GitHub.com/kaloprominat/6105220>
# showing the need to set the delegate for the NSWindow.

import run as _  # PYCHOK sys.path
# all imports listed explicitly to help PyChecker
from pycocoa import NSApplication, NSBackingStoreBuffered, \
                    NSMakeRect, NSStr, NSWindow, \
                    NSWindowStyleMaskUsual, PyObjectEncoding, \
                    ObjCClass, ObjCInstance, ObjCSubclass, \
                    send_super, terminating

__version__ = '23.01.18'


class _Delegate_Implementation(object):
    _Delegate = ObjCSubclass('NSObject', '_Delegate')

    # see pycocoa.runtime.parse_encoding for type encoding:
    # first is return value, then the method args, no need to
    # include @: for self and the Objective-C selector/cmd.
    @_Delegate.method(b'@' + PyObjectEncoding)
    def init(self, app):
        self = ObjCInstance(send_super(self, 'init'))
#       self = ObjCInstance(send_message('NSObject', 'alloc'))
#       print(self)  # <ObjCInstance ...: _Delegate at ...>
        self.app = app
        return self

    @_Delegate.method('v@')
    def applicationDidFinishLaunching_(self, notification):
        '''Called automatically when the application has launched.
        '''
        print('finished launching')

    @_Delegate.method('v@')
    def windowWillClose_(self, notification):
        '''Called automatically when the window is closed'
        '''
        print('window will close')
        # Terminate the application
        self.app.terminate_(self)  # or NSApp()...


_Delegate = ObjCClass('_Delegate')  # the actual class


def main(timeout=None):
    # Create a new application instance ...
    app = NSApplication.sharedApplication()
    # ... and create its delgate.  Note the use of the
    # Objective C constructors below, because Delegate
    # is a subclass of an Objective C class, NSObject
    delegate = _Delegate.alloc().init(app)
    # Tell the application which delegate object to use.
    app.setDelegate_(delegate)

    # Now we can can start to create the window ...
    frame = NSMakeRect(10, 10, 600, 300)
    # (Don't worry about these parameters for the moment. They just
    # specify the type of window, its size and position etc)
    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                      frame,
                      NSWindowStyleMaskUsual,
                      NSBackingStoreBuffered,
                      False)  # or 0
    # tell it which delegate object to use (here it happens
    # to be the same delegate as the application is using),
    # otherwise method .windowWillClose_ will not be called
    window.setDelegate_(delegate)
    # set some properties. Unicode strings are preferred.
    window.setTitle_(NSStr('Delegated - Close window to Quit'))
    # All set.  Now we can show the window
    window.orderFrontRegardless()

    # set up the timeout
    terminating(app, timeout)
    # ... and start the application
    app.run()  # .runEventLoop()


if __name__ == '__main__':

    import sys

    if len(sys.argv) > 1:
        main(sys.argv.pop(1))
    else:
        main()

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
