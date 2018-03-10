
# -*- coding: utf-8 -*-

# Originally <http://GitHub.com/phillip-nguyen/cocoa-python/blob/master/examples/subclass.py>

# Simple example of subclassing NSObject and creating
# basic Objective-C callable methods using decorators.

# all imports listed explicitly to help PyChecker
from pycocoa import PyObjectEncoding, ObjCClass, ObjCInstance, \
                    ObjCSubclass, send_super

__version__ = '17.11.18'


class MySubclass_Implementation(object):

    # Create a Objective-C sub-class of NSObject
    MySubclass = ObjCSubclass('NSObject', 'MySubclass')

    # Through some magic, the self variable received by these
    # methods is an instance of the python ObjCInstance object.
    # It has an attribute objc_cmd set to the hidden _cmd
    # aka the selector argument.
    @MySubclass.method('@')  # return type object, no args
    def init(self):
        self = ObjCInstance(send_super(self, 'init'))
#       self = ObjCInstance(send_message('NSObject', 'alloc'))
        print('inside init: self = %r' % (self,))
        self.x = 1
        return self

    # A normal Objective-C instance method.  This gets added
    # to the Objective-C class.  The type-encoding string says
    # that this method returns void and has no other arguments.
    @MySubclass.method('v')
    def doSomething(self):
        print('doSomething %s' % (self,))
        print('x = %d' % (self.x,))
        self.x += 1

    @MySubclass.method('v@')  # return void, 1 object
    def doSomethingElse(self, other):
        print('doSomethingElse %r %r' % (self, other))
        other.doSomething()

    @MySubclass.method(b'v' + PyObjectEncoding)  # return void, 1 Python object
    def takePyObject(self, pyobject):
        print('takePyObject %r %r' % (self, pyobject))
        print('x = %d' % (self.x,))

    @MySubclass.method('v')  # return void, no args
    def dealloc(self):
        print('dealloc %r' % (self,))
        send_super(self, 'dealloc')

    @MySubclass.method('vi')  # return void, int arg
    def method(self, number):
        print('method %r %r' % (self, number))


if __name__ == '__main__':

    MySubclass = ObjCClass('MySubclass')  # the actual class

    myobject1 = MySubclass.alloc().init()
    print('after init: myobject1 = % r\n' % (myobject1,))

    myobject1.doSomething()
    myobject1.method(100)
    myobject1.takePyObject(1)

    print()

    myobject2 = MySubclass.alloc().init()
    print('after init: myobject2 = %r' % (myobject2,))

    myobject2.doSomething()
#   myobject2.doSomething()
#   myobject2.doSomethingElse()

    print()

    myobject1.doSomethingElse(myobject2)

    print()

    class Foo:
        pass

    f = Foo()
    myobject1.takePyObject(f)

    myobject1.release()  # dealloc and finalize
    myobject2.release()
