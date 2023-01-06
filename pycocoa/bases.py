
# -*- coding: utf-8 -*-

# License at the end of this file.

'''(INTERNAL) Base classes for Python C{Types}.
'''
# all imports listed explicitly to help PyChecker
from pycocoa.lazily  import _ALL_LAZY
from pycocoa.nstypes import isNone, NSStr, nsString2str
from pycocoa.octypes import c_struct_t, ObjC_t
from pycocoa.runtime import ObjCInstance, release
from pycocoa.utils   import bytes2str, isinstanceOf, type2strepr

__all__ = _ALL_LAZY.bases
__version__ = '21.11.04'


class _Type0(object):
    '''(INTERNAL) The base Type, just property NS.
    '''
    _NS = None  # NSMain.Null

    def __init__(self, *args, **kwds):
        # ignore __init__ from __new__, like Item
        if kwds and not args:
            for a, v in kwds.items():
                if not hasattr(self, a):
                    setattr(self, a, v)
                elif getattr(self, a) != v:
                    raise AttributeError('%s=%r exists' % (a, v))

    def __repr__(self):
        return '%s at %#x' % (self, id(self))

    def __str__(self):
        return type2strepr(self)

    type2strepr = __str__

    @property
    def NS(self):
        '''Get the ObjC instance (C{NS...}).
        '''
        return self._NS  # non _RO

    @NS.setter  # PYCHOK property.setter
    def NS(self, ns):
        '''Set the ObjC instance (C{NS...}).
        '''
        if not isNone(ns):  # see also .nstypes.nsOf
            isinstanceOf(ns, ObjCInstance, c_struct_t, ObjC_t, name='ns')
        elif isinstanceOf(self.NS, ObjCInstance):
            # self.NS.release()
            pass
        self._NS = ns

    @property
    def NSDelegate(self):  # to catch typos
        raise AttributeError('use %r not %r' % ('NSd-', 'NSD-'))

    @NSDelegate.setter  # PYCHOK property.setter
    def NSDelegate(self, unused):
        raise AttributeError('use %r not %r' % ('NSd-', 'NSD-'))


class _Type1(_Type0):
    '''(INTERNAL) Basic Type with properties app, delegate and NS.
    '''
    _app = None

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
            from pycocoa.apps import App
            isinstanceOf(app, App, name='app')
        self._app = app

    @property
    def NSdelegate(self):
        '''Get the class' delegate (C{NS...}) or C{None}.
        '''
        try:
            return self.NS.delegate() or None
        except AttributeError:
            return None

    @NSdelegate.setter  # PYCHOK property.setter
    def NSdelegate(self, delegate):
        '''Set the class' delegate.
        '''
        if not isNone(delegate):
            isinstanceOf(delegate, ObjCInstance, name='delegate')  # XXXX ????
            self.NS.setDelegate_(delegate)


class _Type2(_Type1):
    '''(INTERNAL) Basic Type with properties app, delegate, NS, tag and title.
    '''
    _title = None

    def __str__(self):
        return '%s(%r)' % (self.__class__.__name__, self._title)

    @property
    def title(self):
        '''Get the title.
        '''
        return self._title

    @title.setter  # PYCHOK property.setter
    def title(self, title):
        '''Set the title.
        '''
        if isinstance(title, NSStr):
            try:
                self.NS.setTitle_(title)
            except AttributeError:  # no NSApplication.setTitle_
                pass
            title = nsString2str(title)
        else:
            try:
                t = NSStr(title)
                self.NS.setTitle_(t)
                release(t)
            except AttributeError:  # no NSApplication.setTitle_
                t.release()
        self._title = bytes2str(title)


if __name__ == '__main__':

    from pycocoa.utils import _all_listing

    _all_listing(__all__, locals())

# % python3 -m pycocoa.bases
#
# pycocoa.bases.__all__ = tuple(
# )[0]
# pycocoa.bases.version 21.11.04, .isLazy 1, Python 3.11.0 64bit arm64, macOS 13.0.1

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
