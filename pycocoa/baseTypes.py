
# -*- coding: utf-8 -*-

# License at the end of this file.

'''(INTERNAL) Base classes for Python C{Types}.
'''
from pycocoa.basics import _MutableConstants, Proxy1ce, _Objectype
from pycocoa.internals import bytes2str, _Dmain_, _fmt_invalid, \
                             _fmt, _instr
# from pycocoa.lazily import _ALL_LAZY  # from .utils
from pycocoa.nstypes import isNone, NSStr, nsString2str
from pycocoa.octypes import c_struct_t, ObjC_t
from pycocoa.runtime import ObjCInstance, release
from pycocoa.utils import isinstanceOf, type2strepr,  _ALL_LAZY

__all__ = _ALL_LAZY.baseTypes
__version__ = '25.04.08'

_NSD_Error = NameError("use 'NSd-', not 'NSD-'")  # PYCHOK used!


class _Type0(_Objectype):
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
                    t = _fmt('%s=%r exists', a, v)
                    raise AttributeError(t)

    def __repr__(self):
        return _fmt('%s at %#x', self, id(self))

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
            isinstanceOf(ns, ObjCInstance, c_struct_t, ObjC_t, raiser='ns')
        elif isinstanceOf(self.NS, ObjCInstance):
            pass  # self.NS.release()
        self._NS = ns

    @property
    def NSDelegate(self):  # to catch 'D' typos
        raise _NSD_Error

    @NSDelegate.setter  # PYCHOK property.setter
    def NSDelegate(self, unused):
        raise _NSD_Error

    def _sliced(self, slindex):
        '''(INTERNAL) Convert a C{slice} index to C{range}.
        '''
        # assert isinstance(slindex, slice)
        return range(*slindex.indices(len(self)))


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
            isinstanceOf(app, App, raiser='app')
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
            isinstanceOf(delegate, ObjCInstance, raiser='delegate')  # XXX ???
            self.NS.setDelegate_(delegate)


class _Type2(_Type1):
    '''(INTERNAL) Basic Type with properties app, delegate, NS, tag and title.
    '''
    _title = None

    def __str__(self):
        return _instr(self.typename, repr(self._title))

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
            ns = NSStr(title)
            try:
                self.NS.setTitle_(ns)
                release(ns)
            except AttributeError:  # no NSApplication.setTitle_
                ns.release()
        self._title = bytes2str(title)


class _Types(_MutableConstants):
    '''Python Types, to avoid circular imports, lazily set.
    '''
    AlertPanel    = None  # set by .panels
    App           = None  # set by .apps
    Color         = None  # set by .colors
    Dict          = None  # set by .dicts
    ErrorPanel    = None  # set by .panels
    Font          = None  # sef by .fonts
    FrozenDict    = None  # set by .dicts
    FrozenSet     = None  # set by .sets
    Item          = None  # set by .menus
    ItemSeparator = None  # set by .menus
    List          = None  # set by .lists
    MediaWindow   = None  # set by .windows
    Menu          = None  # set by .menus
    MenuBar       = None  # set by .menus
    OpenPanel     = None  # set by .panels
    Paper         = None  # set by .printer
    PaperCustom   = None  # set by .printer
    PaperMargins  = None  # set by .printer
    Printer       = None  # set by .printer
    SavePanel     = None  # set by .panels
    Screen        = None  # set by .screens
    Set           = None  # set by .sets
    Str           = None  # set by .strs
    StrAttd       = None  # set by .strs
    Table         = None  # set by .tables
    TableWindow   = None  # set by .tables
    TextPanel     = None  # set by .panels
    TextWindow    = None  # set by .windows
    Tuple         = None  # set by .tuples
    Window        = None  # set by .windows

    def __setattr__(self, name, value):
        t = type(self)
        if not hasattr(t, name):
            t = _fmt_invalid(name=repr(name))
            raise AttributeError(t)
        setattr(t, name, value)

    def __getattr__(self, name):  # called when .__getattribute__ failed
        '''(INTERNAL) Get _Types.name or import lazily if still C{None}.
        '''
        return _MutableConstants.__getattr__(self, name) or _lazily._lazy_import(name)

    def __getattribute__(self, name):  # called when .name accessed
        '''(INTERNAL) Get _Types.name or import lazily if still C{None}.
        '''
        return _MutableConstants.__getattribute__(self, name)  # or _lazily._lazy_import(name)

_Types = _Types()  # PYCHOK singleton


@Proxy1ce  # PYCHOK used!
def _lazily():  # lazily import lazily, I{once}
    from pycocoa import lazily
    return lazily


if __name__ == _Dmain_:

    from pycocoa.utils import _all_listing

    _all_listing(__all__, locals())

# % python3 -m pycocoa.baseTypes
#
# pycocoa.baseTypes.__all__ = tuple(
# )[0]
# pycocoa.baseTypes.version 25.4.8, .isLazy 1, Python 3.13.2 64bit arm64, macOS 15.4

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2025 -- mrJean1 at Gmail -- All Rights Reserved.
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
