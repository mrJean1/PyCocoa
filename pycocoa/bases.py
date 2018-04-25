
# -*- coding: utf-8 -*-

# MIT License <http://opensource.org/licenses/MIT>
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

'''(INTERNAL) Base classes for Python C{Types}.
'''
# all imports listed explicitly to help PyChecker
from nstypes import isNone, NSNone, NSStr
from octypes import c_struct_t, ObjC_t
from runtime import ObjCInstance
from utils   import bytes2str, instanceof, type2strepr

__all__ = ()
__version__ = '18.04.23'


class _Type0(object):
    '''The base Type.
    '''

    def __repr__(self):
        return '%s at %#x' % (self, id(self))

    def __str__(self):
        return type2strepr(self)

    type2strepr = __str__

    @property
    def NS(self):
        '''Get the C{NS...} instance.
        '''
        return self._NS

    @NS.setter  # PYCHOK property.setter
    def NS(self, ns):
        '''Set the C{NS...} instance.
        '''
        if not isNone(ns):  # see also .nstypes.nsOf
            instanceof(ns, ObjCInstance, c_struct_t, ObjC_t, name='ns')
        elif not isNone(self.NS):
            # self.NS.release()
            pass
        self._NS = ns


class _Type1(_Type0):
    '''Basic Type with app and delegate.
    '''
    _app = None
    _NS  = NSNone

    def __init__(self, *args, **kwds):
        # ignore __init__ from __new__, like Item
        if kwds and not args:
            for a, v in kwds.items():
                if hasattr(self, a):
                    raise AttributeError('%s=%r exists' % (a, v))
                setattr(self, a, v)

    @property
    def app(self):
        '''Get the app.
        '''
        return self._app

    @app.setter  # PYCHOK property.setter
    def app(self, app):
        '''Set the app.
        '''
        if app not in (None,):
            from apps import App
            instanceof(app, App, name='app')
        self._app = app

    @property
    def NSdelegate(self):
        '''Get the class' delegate.
        '''
        return self.NS.delegate()

    @NSdelegate.setter  # PYCHOK property.setter
    def NSdelegate(self, delegate):
        '''Set the class' delegate.
        '''
        if not isNone(delegate):
            instanceof(delegate, ObjCInstance, name='delegate')  # XXXX ????
            self.NS.setDelegate_(delegate)


class _Type2(_Type1):
    '''Basic Type with app, delegate, tag and title.
    '''
    _tag   = None
    _title = None

    def __str__(self):
        return '%s(%r)' % (self.__class__.__name__, self._title)

    @property
    def tag(self):
        '''Get the (L{Item}, ...) tag.
        '''
        try:
            return self.NS.tag()
        except AttributeError:
            return self._tag

    @tag.setter  # PYCHOK property.setter
    def tag(self, tag):
        '''Set the (L{Item}, ...) tag (int).
        '''
        if tag not in (None, NSNone):
            try:
                self.NS.setTag_(int(tag))
                self._tag = tag
            except AttributeError:
                pass

    @property
    def title(self):
        '''Get the title.
        '''
        return self._title

    @title.setter  # PYCHOK property.setter
    def title(self, title):
        '''Set the title.
        '''
        self._title = bytes2str(title)
        try:
            self.NS.setTitle_(NSStr(self._title))
        except AttributeError:
            pass  # no NSApplication.setTitle_


if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)
