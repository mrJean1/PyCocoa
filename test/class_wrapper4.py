
# -*- coding: utf-8 -*-

# Originally <http://GitHub.com/phillip-nguyen/cocoa-python/blob/master/examples/class_wrapper3.py>

# Complete attempt at wrapping Objective-C objects in Python.
# ObjCClass and ObjCInstance use cached objects with __new__

# all imports listed explicitly to help PyChecker
from pycocoa import NSApplication, NSBackingStoreBuffered, NSRect4_t, \
                    NSStr, NSWindow, NSWindowStyleMaskUsual, libobjc, \
                    ObjCClass, ObjCInstance, ObjCSubclass

__version__ = '18.04.06'


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
