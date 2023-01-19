
# -*- coding: utf-8 -*-

# Originally <https://GitHub.com/phillip-nguyen/cocoa-python/blob/master/examples/class_wrapper3.py>

# Complete attempt at wrapping Objective-C objects in Python.
# ObjCClass and ObjCInstance use cached objects with __new__

import run as _  # PYCHOK sys.path
# all imports listed explicitly to help PyChecker
from pycocoa import NSApplication, NSBackingStoreBuffered, NSRect4_t, \
                    NSStr, NSWindow, NSWindowStyleMaskUsual, libobjc, \
                    ObjCClass, ObjCInstance, ObjCSubclass

__version__ = '23.01.18'


class MySubclassImplementation(object):
    MySubclass = ObjCSubclass('NSObject', 'MySubclass')

    @MySubclass.method('v')
    def doSomething(self):
        if not hasattr(self, 'x'):
            self.x = 0
        self.x += 1
        print('doSomething', self.x)
        self.doSomething2()

    @MySubclass.method('v')
    def doSomething2(self):
        print('doSomething2', self.x)


def run_window():

    app = NSApplication.sharedApplication()
#   pool = NSAutoreleasePool.alloc().init()  # PYCHOK expected

    window = NSWindow.alloc()
    window.initWithContentRect_styleMask_backing_defer_(
           NSRect4_t(100,100,300,300),
           NSWindowStyleMaskUsual,
           NSBackingStoreBuffered,
           False)
    window.setTitle_(NSStr("Class Window"))
    window.makeKeyAndOrderFront_(None)

    app.run()


def stupid_stuff(class_name):

    NSObject = ObjCClass(class_name)
    print(NSObject)
    print(libobjc.object_getClassName(NSObject.ptr))

    x = NSObject.alloc()  # PYCHOK expected
    print(libobjc.object_getClassName(x.ptr))
    print('x', x)
    print('x.init', x.init)
    print('x.init()', x.init())
    print('x.objc_class', x.objc_class)
    print(x.retainCount())
    print(x.retain())
    print(x.retainCount())
    print(x.retain())
    print(x.retainCount())
    print(x.retain())
    print(x.retainCount())

    if class_name == 'NSApplication':
        # only one NSApplication allowed
        return

    y = NSObject.alloc()  # PYCHOK expected
    print('y', y)
    print('y.init', y.init)
    print('y.init()', y.init())
    print('y.objc_class', y.objc_class)
    print(y.retainCount())
    print(y.retain())
    print(y.retainCount())


if __name__ == '__main__':

    import sys

    if len(sys.argv) < 2:
        print('USAGE: python class_wrapper4.py <Obj-C Class>')
        exit(1)

    class_name = sys.argv[1]

    MySubclass = ObjCClass('MySubclass')
    print(MySubclass)
    x = MySubclass.alloc().init()
    print(x)

    x.doSomething()
    x.doSomething()
    x.doSomething()

    print(len(ObjCInstance._objc_cache))
    x.release()
    del x
    print(len(ObjCInstance._objc_cache))

    stupid_stuff(class_name)
#   run_window()

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
#
# __
#
# Copyright (C) 2011 -- Phillip Nguyen -- All Rights Reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of objective-ctypes nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
