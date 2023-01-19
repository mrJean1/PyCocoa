
# -*- coding: utf-8 -*-

# Originally <https://GitHub.com/phillip-nguyen/cocoa-python/blob/master/examples/subclass.py>

# Simple example of subclassing NSObject and creating
# basic Objective-C callable methods using decorators.

import run as _  # PYCHOK sys.path
# all imports listed explicitly to help PyChecker
from pycocoa import PyObjectEncoding, ObjCClass, ObjCInstance, \
                    ObjCSubclass, send_super

__version__ = '23.01.18'


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
