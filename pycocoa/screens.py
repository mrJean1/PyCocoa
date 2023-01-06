
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Types L{Frame} and L{Screen}, wrapping ObjC C{NSScreen}.
'''
# all imports listed explicitly to help PyChecker
from pycocoa.bases import _Type0
from pycocoa.geometry import Point, Rect, Size
from pycocoa.lazily import _ALL_LAZY, _COMMASPACE_  # PYCHOK used!
from pycocoa.nstypes import ns2py, NSScreen, nsString2str
from pycocoa.octypes import NSRect_t
from pycocoa.oslibs import libCG
from pycocoa.runtime import isObjCInstanceOf
from pycocoa.utils import _Ints, isinstanceOf, property_RO, \
                          _Singletons, _Types

__all__ = _ALL_LAZY.screens
__version__ = '21.11.04'


class Frame(Rect):
    '''A screen frame, wrapping ObjC L{NSRect_t}.
    '''
    def __init__(self, screen_frame=None, fraction=None, cascade=10):
        '''New, partial screen L{Frame}.

           @keyword screen: The screen to place the window on (C{int}) or
                            C{None} for the current one.  Use C{screen=0}
                            for the BuiltIn screen or C{screen=1} for the
                            first External monitor, etc.
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
        elif isinstanceOf(screen_frame, NSRect_t, Rect, name='screen_frame'):
            f = screen_frame

        if isinstance(fraction, (float, int)):
            if 0.1 < fraction < 1.0:
                z = f.size
                # use the lower left side of the screen
                w = int(z.width * fraction + 0.5)
                h = int(z.height * w / z.width)
                # avoid cascading window off-screen
                c = min(max(0, cascade), min(z.width, z.height))
                f = f.origin.x + c, f.origin.y + c, w, h
            elif fraction < 0 or fraction > 1:
                raise ValueError('invalid %s: %.2f' % ('fraction', fraction))
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
        elif isObjCInstanceOf(screen, NSScreen, name='screen'):
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

           @param fraction: Of the size (C{float}).

           @return: The screen point (L{Point}).
        '''
        p = self.topleft
        if 0 < fraction <= 1:
            f = self.frame
            p = Point((p.x + fraction * f.size.width,
                       p.y - fraction * f.size.height))
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
        return self.displayID == libCG.CGMainDisplayID()

    @property_RO
    def isExternal(self):
        '''Is this screen an External one (C{bool})?
        '''
        return self.displayID != libCG.CGMainDisplayID()

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


class BuiltInScreen(Screen):
    '''The BuiltIn screen.
    '''
    _name = 'BuiltIn'


class DeepestScreen(Screen):
    '''The Deepest screen, the one with most colors.
    '''
    _name = 'Deepest'


class ExternalScreen(Screen):
    '''An External screen or monitor.
    '''
    _name = 'External'


class MainScreen(Screen):
    '''A Main screen, the one with the menu bar, key focus, etc.
    '''
    _name = 'Main'


class Screens(_Singletons):

    _len     = 0
    _NS      = None  # NS-master
    _screens = {}  # dict!

    def __call__(self, n=None):
        '''Get screen by index, C{0} for BuiltIn, C{1..4} for
           External, iff present or by C{displayID} or C{None}
           for current Main screen.

           @see: Property C{screens} and method C{items}.
        '''
        if n is None:
            return self.Main
        try:
            return self.screens[n]
        except (KeyError, TypeError, ValueError):
            pass
        raise ValueError('invalid %s: %s' % ('screen', n))

    def __getitem__(self, n):
        '''Objects __getitem__, __len__ and 0-based indices are iterable.
        '''
        if n is None:
            return self.Main
        elif 0 <= n < len(self):
            return self.screens[n]
        raise IndexError('invalid %s: %s' % ('screen', n))

    def __len__(self):
        '''Return the total number of screens present,
           including the BuiltIn one.
        '''
        return self._len or len(self.screens) // 2

    def __repr__(self):
        return '(%s)' % (self,)  # like tuple

    def __str__(self):
        return _COMMASPACE_(*(s for _, s in self.items()))

    @property_RO
    def AirPlay(self):
        '''Return the I{AirPlay} screen, iff present.
        '''
        return None

    @property_RO
    def BuiltIn(self):
        '''Return the I{BuiltIn} screen.
        '''
        return self.screens[0]

    @property_RO
    def Deepest(self):
        '''Return screen with the best color.
        '''
        return DeepestScreen(screen=self.NS.deepestScreen())

    def items(self):
        '''Yield each screen I{once}, starting with the
           BuiltIn screen, then External ones iff present.
        '''
        for i in range(len(self)):
            yield i, self.screens[i]

    @property_RO
    def Main(self):
        '''Get the I{Main} screen, the screen currently with the menu
           bar, key focus, etc.  It may be (a coly of) the BuiltIn or
           an External screen.
        '''
        return MainScreen(screen=self.NS.mainScreen())

    @property_RO
    def NS(self):
        '''Get a bare ObjC C{NSScreen} instance.
        '''
        if self._NS is None:
            self._NS = NSScreen.alloc().init()
        return self._NS

    @property_RO
    def screens(self):
        '''Get the BuiltIn and other, External screens iff present (C{dict}
           of C{Screen}s).

           @note: Each screen is represented twice and accessable by 2 C{int}
                  keys, a 0-based index and its C{displayID}.  The BuiltIn
                  screen has index key 0, always.

           @see: Methods C{__call__} and C{items}.
        '''
        if not self._screens:
            x, d = 1, {0: None}
            for ns in ns2py(self.NS.screens()):
                s = Screen(ns)
                if s.isBuiltIn:
                    d[0] = d[s.displayID] = BuiltInScreen(s)
                else:
                    d[x] = d[s.displayID] = ExternalScreen(s)
                    x += 1
            self._screens = d
            self._len = x
        return self._screens

Screens = Screens()  # PYCHOK tuple-like, singleton

_Types.Screen = NSScreen._Type = Screen

if __name__ == '__main__':

    from pycocoa.utils import _all_listing, printf

    for s in tuple(Screens) + (Screens.Deepest, Screens.Main):
        printf(str(s), nl=1)
        for a in ('colorSpace', 'displayID', 'frame', 'named',
                  'pixels', 'ratio', 'resolutions', 'visibleFrame'):
            printf('  %s: %r', a, getattr(s, a, None))

    _all_listing(__all__, locals())

# % python3 -m pycocoa.screens
#
# pycocoa BuiltInScreen(NSScreen, name='BuiltIn')
# pycocoa   colorSpace: 'NSCalibratedRGBColorSpace'
# pycocoa   displayID: 1
# pycocoa   frame: Rect(origin=Point(x=0.0, y=0.0), size=Size(width=1440.0, height=900.0)) at 0x101332a90
# pycocoa   named: 'Built-in Retina Display'
# pycocoa   pixels: Size(width=2560.0, height=1600.0) at 0x101332dc0
# pycocoa   ratio: (8, 5)
# pycocoa   resolutions: Size(width=144.0, height=144.0) at 0x101332df0
# pycocoa   visibleFrame: Rect(origin=Point(x=0.0, y=0.0), size=Size(width=1440.0, height=875.0)) at 0x101332fd0
#
# pycocoa ExternalScreen(NSScreen, name='External')
# pycocoa   colorSpace: 'NSCalibratedRGBColorSpace'
# pycocoa   displayID: 2
# pycocoa   frame: Rect(origin=Point(x=-2560.0, y=-540.0), size=Size(width=2560.0, height=1440.0)) at 0x101332fa0
# pycocoa   named: '...'
# pycocoa   pixels: Size(width=2560.0, height=1440.0) at 0x10134a190
# pycocoa   ratio: (16, 9)
# pycocoa   resolutions: Size(width=72.0, height=72.0) at 0x10134a1c0
# pycocoa   visibleFrame: Rect(origin=Point(x=-2511.0, y=-540.0), size=Size(width=2511.0, height=1440.0)) at 0x10134a1c0
#
# pycocoa DeepestScreen(NSScreen, name='Deepest')
# pycocoa   colorSpace: 'NSCalibratedRGBColorSpace'
# pycocoa   displayID: 1
# pycocoa   frame: Rect(origin=Point(x=0.0, y=0.0), size=Size(width=1440.0, height=900.0)) at 0x10134a370
# pycocoa   named: 'Built-in Retina Display'
# pycocoa   pixels: Size(width=2560.0, height=1600.0) at 0x10134a3d0
# pycocoa   ratio: (8, 5)
# pycocoa   resolutions: Size(width=144.0, height=144.0) at 0x10134a3a0
# pycocoa   visibleFrame: Rect(origin=Point(x=0.0, y=0.0), size=Size(width=1440.0, height=875.0)) at 0x10134a3a0
#
# pycocoa MainScreen(NSScreen, name='Main')
# pycocoa   colorSpace: 'NSCalibratedRGBColorSpace'
# pycocoa   displayID: 1
# pycocoa   frame: Rect(origin=Point(x=0.0, y=0.0), size=Size(width=1440.0, height=900.0)) at 0x101332c40
# pycocoa   named: 'Built-in Retina Display'
# pycocoa   pixels: Size(width=2560.0, height=1600.0) at 0x101332c10
# pycocoa   ratio: (8, 5)
# pycocoa   resolutions: Size(width=144.0, height=144.0) at 0x101332430
# pycocoa   visibleFrame: Rect(origin=Point(x=0.0, y=0.0), size=Size(width=1440.0, height=875.0)) at 0x101332430

# pycocoa.screens.__all__ = tuple(
#  pycocoa.screens.BuiltInScreen is <class .BuiltInScreen>,
#  pycocoa.screens.DeepestScreen is <class .DeepestScreen>,
#  pycocoa.screens.ExternalScreen is <class .ExternalScreen>,
#  pycocoa.screens.Frame is <class .Frame>,
#  pycocoa.screens.MainScreen is <class .MainScreen>,
#  pycocoa.screens.Screen is <class .Screen>,
#  pycocoa.screens.Screens is (BuiltInScreen(NSScreen, name='BuiltIn'), ExternalScreen(NSScreen, name='External')),
# )[7]
# pycocoa.screens.version 21.11.04, .isLazy 1, Python 3.11.0 64bit arm64, macOS 13.0.1

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
