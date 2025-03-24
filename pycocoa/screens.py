
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Types L{Frame} and L{Screen}, wrapping ObjC C{NSScreen}.

@var Screens: An L{Adict} of all available screens or monitors.
@var Screens.BuiltIn: Get the I{BuiltIn} screen (C{Screen}).
@var Screens.External: Get an External screen (C{Screen}) or C{None}.
'''
from pycocoa.bases import _Type0
from pycocoa.geometry import Point, Rect, Size
from pycocoa.internals import _COMMASPACE_, _Dmain_, _fmt, \
                              _fmt_invalid, _Ints, property_RO
from pycocoa.lazily import _ALL_LAZY, _Types
from pycocoa.nstypes import ns2py, NSScreen, nsString2str
from pycocoa.octypes import NSRect_t
from pycocoa.oslibs import _libCG  # PYCHOK used!
from pycocoa.runtime import isObjCInstanceOf,  isinstanceOf
# from pycocoa.utils import isinstanceOf  # from .runtime

__all__ = _ALL_LAZY.screens
__version__ = '25.03.16'


class Frame(Rect):
    '''A screen frame, wrapping ObjC L{NSRect_t}.
    '''
    def __init__(self, screen_frame=None, fraction=None, cascade=10):
        '''New, partial screen L{Frame}.

           @keyword screen_frame: The screen to place the window on (C{int})
                           or C{None} for the current one.  Use C{screen=0}
                           for the BuiltIn screen or C{screen=1} for the
                           first External monitor, etc. otherwise a screen,
                           or frame (L{Screen}, L(Frame) or L{Rect}).
           @keyword fraction: Size of the screen (C{float}).
           @keyword cascade: Shift from lower left corner (C{float} or C{int}).

           @raise TypeError: Invalid I{screen_frame}.

           @raise ValueError: Invalid I{fraction} value.
        '''
        if screen_frame is None:
            f = Screens.Main.frame
        elif isinstance(screen_frame, _Ints):
            f = Screens(screen_frame).frame
        elif isinstance(screen_frame, Screen):
            f = screen_frame.frame
        elif isinstanceOf(screen_frame, NSRect_t, Rect, raiser='screen_frame'):
            f = screen_frame

        if isinstanceOf(fraction, float, int):
            if 0.1 < fraction < 1.0:
                z = f.size
                # use the lower left side of the screen
                w = int(z.width  * fraction + 0.5)
                h = int(z.height * w / z.width)
                # avoid cascading window off-screen
                c = min(max(0, cascade), min(z.width, z.height))
                z = f.origin
                f = (z.x + c), (z.y + c), w, h
            elif fraction < 0.1 or fraction > 1:
                f = None
        elif fraction is not None:
            f = None

        if f is None:
            t = _fmt_invalid(fraction=repr(fraction))
            raise ValueError(t)
        self.rect = f


class Screen(_Type0):
    '''Screen Python Type, wrapping ObjC L{NSRect_t}.
    '''
    _deviceDescription = None
    _name              = ''
    _NScascade         = None  # .windows.Window.cascade

    def __new__(cls, screen=None, name=''):
        if screen is None:
            self = Screens.Main
        elif isinstance(screen, _Ints):
            self = Screens(screen)
        elif isinstanceOf(screen, Screen):
            self = _Type0.__new__(cls)
            self.NS = screen.NS
            if screen._deviceDescription:
                self._deviceDescription = screen._deviceDescription  # XXX copy
        elif isObjCInstanceOf(screen, NSScreen, raiser='screen'):
            self = _Type0.__new__(cls)
            self.NS = screen
        if name:
            self._name = name
        return self

    def __eq__(self, other):
        return other is self or (isinstance(other, Screen) and
                                 other.displayID == self.displayID)

    @property_RO
    def bottom(self):
        '''Get the lower y coordinate (C{float} or C{int}).
        '''
        return self.frame.bottom

    @property_RO
    def bottomleft(self):
        '''Get the lower left corner (L{Point}).
        '''
        return self.frame.bottomleft

    @property_RO
    def bottomright(self):
        '''Get the lower right corner (L{Point}).
        '''
        return self.frame.bottomright

    def cascade(self, fraction=0.1):
        '''Return a screen point off the upper left corner.

           @param fraction: Of the screen size (C{float}).

           @return: The screen or topleft point (L{Point}).
        '''
        p = self.topleft
        if 0 < fraction <= 1:
            z = self.frame.size
            p = Point((p.x + fraction * z.width,
                       p.y - fraction * z.height))
        return p

    @property_RO
    def center(self):
        '''Get the center (L{Point}).
        '''
        return self.frame.center

    @property_RO
    def colorSpace(self):
        '''Get the device color space (C{str}).
        '''

        return self.deviceDescription.NSDeviceColorSpaceName  # self.NS.colorSpace()?

#   @property_RO
#   def depth(self):
#       '''Get the depth (L{??}).
#       '''
#       return self.NS.depth()

    @property_RO
    def deviceDescription(self):
        '''Get the device descriptions (L{Adict}).
        '''
        if self._deviceDescription is None:
            self._deviceDescription = ns2py(self.NS.deviceDescription())
        return self._deviceDescription

    deviceDict = deviceDescription

    @property_RO
    def displayID(self):
        '''Get the C{displayID} aka C{NSScreenNumber} of this screen (C{int}).
        '''
        return self.deviceDescription.NSScreenNumber

    @property
    def frame(self):
        '''Get the frame (L{Rect}).
        '''
        return Rect(self.NS.frame())

    @frame.setter  # PYCHOK setter!
    def frame(self, rect):
        '''Set the rect (L{Rect}, C{2-list}, C{4-list},
           C{2-tuple}, C{4-tuple} or C{NSRect[4]_t}).
        '''
        self.NS.setFrame_(Rect(rect).NS)

    @property_RO
    def isBuiltIn(self):
        '''Is this the single, BuiltIn screen (C{bool})?
        '''
        return self.displayID == _libCG.CGMainDisplayID()

    @property_RO
    def isExternal(self):
        '''Is this screen an External one (C{bool})?
        '''
        return self.displayID != _libCG.CGMainDisplayID()

    @property_RO
    def isMain(self):
        '''Is this screen he current Main one (C{bool})?
        '''
        return self == Screens.Main

    @property_RO
    def isPrinter(self):
        '''Is this screen a printer (C{bool} or C{None})?
        '''
        try:
            return bool(self.deviceDescription.NSDeviceIsPrinter)
        except (AttributeError, KeyError):
            return None

    @property_RO
    def isScreen(self):
        '''Is this screen a monitor (C{bool} or C{None})?
        '''
        try:
            return bool(self.deviceDescription.NSDeviceIsScreen)
        except (AttributeError, KeyError):
            return None

    @property_RO
    def left(self):
        '''Get the leftmost x coordinate (C{float} or C{int}).
        '''
        return self.frame.left

    @property_RO
    def name(self):
        '''Get the screen name (C{str}).
        '''
        return self._name

    @property_RO
    def named(self):
        '''Get the localized name (C{str}).
        '''
        return nsString2str(self.NS.localizedName())

    @property_RO
    def origin(self):
        '''Get the origin (L{Point}).
        '''
        return self.frame.origin

    @property_RO
    def pixels(self):
        '''Get the device width and height pixel count (C{Size}).
        '''
        return Size(self.NS.devicePixelCounts())  # deviceDescription.NSDeviceSize

    @property_RO
    def ratio(self):
        '''Get the aspect ratio (C{2-tuple(wide, high)}).
        '''
        return self.size.ratio

    @property_RO
    def resolutions(self):
        '''Get the device width and height resolution in DPI (C{Size}).
        '''
        return Size(self.deviceDescription.NSDeviceResolution)

    @property_RO
    def right(self):
        '''Get the rightmost x coordinate (C{float} or C{int}).
        '''
        return self.frame.right

    @property_RO
    def size(self):
        '''Get the width and height (L{Size}).
        '''
        return self.frame.size

    @property_RO
    def top(self):
        '''Get the upper y coordinate (C{float} or C{int}).
        '''
        return self.frame.top

    @property_RO
    def topleft(self):
        '''Get the upper left corner (L{Point}).
        '''
        return self.frame.topleft

    @property_RO
    def topright(self):
        '''Get the upper right corner (L{Point}).
        '''
        return self.frame.topright

    @property_RO
    def visibleFrame(self):
        '''Get the fram of the visible area (L{Frame}).
        '''
        return Rect(self.NS.visibleFrame())


class Screens(dict):
    '''A L{dict} of all available screens or monitors.

       @note: Each screen is represented I{twice} and accessable by
              2 C{int} keys, a 0-origin index and its C{displayID}.
              The BuiltIn screen has key C{0}, always.
    '''
    def __init__(self, **unused):
        pass

    def __call__(self, n=None):
        '''Get screen by index, C{0} for BuiltIn, C{1..4} for
           External, iff present or by C{displayID} or C{None}
           for current Main screen.

           @see: Method C{items} and C{screens}.
        '''
        return self.Main if n is None else self[n]

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:  # try name match
            for i, s in self.items():
                if s.name == key or str(i) == key:
                    return s
            raise

    def __len__(self):
        '''Return the number of screens present, including the BuiltIn one.
        '''
        return self._len  # == len(self) // 2

    def __repr__(self):
        return _fmt('(%s)', self)  # like tuple

    def __str__(self):
        t = (str(s) for _, s in self.items())
        return _COMMASPACE_.join(t)

    @property_RO
    def AirPlay(self):
        '''Return the I{AirPlay} screen, iff present (C{Screen}) or C{None}.
        '''
        return None

    @property_RO
    def BuiltIn(self):
        '''Get the I{BuiltIn} screen (C{Screen}).
        '''
        return self._set(BuiltIn=self._named(BuiltIn=self[0]))

    @property_RO
    def Deepest(self):
        '''Get the screen with the most color.
        '''
        return self._named(Deepest=Screen(self.NS.deepestScreen()))

    def displayIDs(self):
        '''Yield each screen's C{displayID} I{once}.

           @see: Methods C{items}, C{keys} and C{screens}.
        '''
        for s in self.values():
            yield s.displayID

    @property_RO
    def External(self):
        '''Get an External screen (C{Screen}) or C{None}.
        '''
        bID = self.BuiltIn.displayID
        for s in self.screens():
            if s.displayID != bID:
                s = self._named(External=s)
                break
        else:
            s = None
        return s

    def items(self):
        '''Yield each screen I{once}, starting with the BuiltIn screen, then
           External ones iff present, each as 2-tuple C{(key, Screen)}.

           @see: Method C{screens}.
        '''
        for i in range(len(self)):
            yield i, self[i]

    def keys(self):
        '''Yield each screen's C{keys} I{once} C({str}).

           @see: Methods C{items} and C{screens}.
        '''
        for i, s in self.items():
            yield s.name or str(i)

    @property_RO
    def _len(self):
        '''(INTERNAL) Lazily __init__(self), I{once}.
        '''
        n, d = 1, {0: None}
        for ns in ns2py(self.NS.screens()):
            s = Screen(ns)
            if s.isBuiltIn:
                d[0] = S = self._named(BuiltIn=s)
            else:
                d[n] = S = self._named(External=s)
                n += 1
            d[s.displayID] = S
        self.update(d)  # dict.update(self, d)
        return self._set(_len=n)  # cache

    @property_RO
    def Main(self):
        '''Get the current I{Main} screen, the one currently with the menu bar, key
           focus, etc.  It may be (a copy of) the BuiltIn or an External screen.
        '''
        return self._named(Main=Screen(self.NS.mainScreen()))

    def _named(self, **name_screen):
        '''(INTERNAL) Name or rename a screen.
        '''
        n, s = name_screen.popitem()
        if not s.name:
            s._name = n
        return s

    @property_RO
    def NS(self):
        '''Get the bare ObjC C{NSScreen} instance.
        '''
        return self._set(NS=NSScreen.alloc().init())

    def screens(self, twice=False):
        '''Yield each screen I{once} or I{twice} (C{Screen}), starting
           with BuiltIn, then External, etc.
        '''
        for _, s in (dict.items(self) if twice else enumerate(
                     self.values())):
            yield s

    def _set(self, **name_value):
        '''(INTERNAL) Cache an I{instance} attribute.
        '''
        n, v = name_value.popitem()
        self.__dict__[n] = v  # cached
        return v

    def values(self):
        '''Yield each screen I{once} (C{Screen}).

           @see: Methods C{items} and C{screens}.
        '''
        for i in range(len(self)):
            yield self[i]

Screens = Screens()  # PYCHOK singleton

_Types.Screen = NSScreen._Type = Screen

if __name__ == _Dmain_:

    from pycocoa.utils import _all_listing, printf, _varstr

    for s in tuple(Screens.screens()) + (Screens.Deepest, Screens.Main):
        printf(str(s), nl=1, argv0='#')
        for a in ('colorSpace', 'displayID', 'frame', 'named',
                  'pixels', 'ratio', 'resolutions', 'visibleFrame'):
            printf('.%s: %r', a, getattr(s, a, None), argv0='# ')

    _all_listing(__all__, locals())

    print(_varstr(Screens))

# % python3 -m pycocoa.screens
#
# Screen(NSScreen, name='BuiltIn')
#  .colorSpace: 'NSCalibratedRGBColorSpace'
#  .displayID: 1
#  .frame: Rect(origin=Point(x=0.0, y=0.0), size=Size(height=900.0, width=1440.0)) at 0x101153770
#  .named: 'Built-in Retina Display'
#  .pixels: Size(height=1600.0, width=2560.0) at 0x1013f0e10
#  .ratio: (8, 5)
#  .resolutions: Size(height=144.0, width=144.0) at 0x101209ba0
#  .visibleFrame: Rect(origin=Point(x=0.0, y=0.0), size=Size(height=875.0, width=1440.0)) at 0x1013f0f50

# Screen(NSScreen, name='External')
#  .colorSpace: 'NSCalibratedRGBColorSpace'
#  .displayID: 2
#  .frame: Rect(origin=Point(x=-2560.0, y=-540.0), size=Size(height=1440.0, width=2560.0)) at 0x101209ba0
#  .named: 'LEN Q27h-10'
#  .pixels: Size(height=1440.0, width=2560.0) at 0x101404490
#  .ratio: (16, 9)
#  .resolutions: Size(height=72.0, width=72.0) at 0x101202b50
#  .visibleFrame: Rect(origin=Point(x=-2511.0, y=-540.0), size=Size(height=1440.0, width=2511.0)) at 0x1011ef410

# Screen(NSScreen, name='Deepest')
#  .colorSpace: 'NSCalibratedRGBColorSpace'
#  .displayID: 1
#  .frame: Rect(origin=Point(x=0.0, y=0.0), size=Size(height=900.0, width=1440.0)) at 0x101404490
#  .named: 'Built-in Retina Display'
#  .pixels: Size(height=1600.0, width=2560.0) at 0x1011fe210
#  .ratio: (8, 5)
#  .resolutions: Size(height=144.0, width=144.0) at 0x10140c910
#  .visibleFrame: Rect(origin=Point(x=0.0, y=0.0), size=Size(height=875.0, width=1440.0)) at 0x101202950

# Screen(NSScreen, name='Main')
#  .colorSpace: 'NSCalibratedRGBColorSpace'
#  .displayID: 1
#  .frame: Rect(origin=Point(x=0.0, y=0.0), size=Size(height=900.0, width=1440.0)) at 0x101202c50
#  .named: 'Built-in Retina Display'
#  .pixels: Size(height=1600.0, width=2560.0) at 0x1011f3410
#  .ratio: (8, 5)
#  .resolutions: Size(height=144.0, width=144.0) at 0x1010f38b0
#  .visibleFrame: Rect(origin=Point(x=0.0, y=0.0), size=Size(height=875.0, width=1440.0)) at 0x1011fe210

# pycocoa.screens.__all__ = tuple(
#  pycocoa.screens.Frame is <class .Frame>,
#  pycocoa.screens.Screen is <class .Screen>,
#  pycocoa.screens.Screens is (Screen(NSScreen, name='BuiltIn'), Screen(NSScreen, name='External')),
# )[3]
# pycocoa.screens.version 25.3.16, .isLazy 1, Python 3.13.2 64bit arm64, macOS 14.7.3

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
