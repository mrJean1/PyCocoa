
# -*- coding: utf-8 -*-

# Basic, __builtin__ Python types wrapping ObjC NS... instances.

# MIT License <http://opensource.org/licenses/MIT>
#
# Copyright (C) 2017-2018 mrJean1 at Gmail dot com
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
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

from bases   import _Type0
from nstypes import ns2py, NSConstantString, NSStr, NSString, \
                    py2NS, _Types
from utils   import instanceof, _Strs

__all__ = ('Str',)
__version__ = '18.04.18'


class Str(str, _Type0):  # str, first to maintain str behavior
    '''Python Type equivalent of an (immutable) ObjC NSStr[ing].
    '''

    def __new__(cls, ns_str=''):
        if isinstance(ns_str, Str):
            ns = ns_str.NS
        elif isinstance(ns_str, _Strs):
            ns = py2NS(ns_str)
        elif instanceof(ns_str, NSStr, name='ns_str'):
            ns = ns_str

        self = super(Str, cls).__new__(cls, ns2py(ns))
        self.NS = ns  # immutable
        return self

    def copy(self, *ranged):
        if ranged:
            s = self[slice(*ranged)]
        else:
            s = self
        return self.__class__(s)


NSConstantString._Type = NSString._Type = NSStr._Type = _Types.Str = Str

if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)
