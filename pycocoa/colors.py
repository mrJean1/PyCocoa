
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Types L{Color}, L{ColorError}, L{CMYColor}, L{GrayScaleColor}, L{HSBColor},
L{RGBColor}, L{TintColor} and L{UIColor} wrapping Cocoa's C{NSColor} and
C{enum}-like constants L{CMYColors}, L{GrayScaleColors}, L{HSBColors},
L{RGBColors}, L{TintColor}, L{TintColors}, L{UIColors} and all L{Colors}
accessible by color space acronym like C{CMY}, C{GS}, C{RGB}, etc.

@var Colors:          Colors by color space acronym, like C{Colors.RGB.Red}, C{Colors.Tint.Red} (C{enum}).
@var CMYColors:       Some standard C{Cyan-Magenta-Yellow} colors, all L{CMYColor} instances (C{enum}).
@var GrayScaleColors: Some standard C{Gray-Scale} colors, all L{GrayScaleColor} instances (C{enum}).
@var HSBColors:       I{No} standard C{Hue-Saturation-Brightness} colors, L{HSBColor} instances (C{enum}).
@var RGBColors:       Some standard C{Red-Green-Blue} colors, all L{RGBColor} instances (C{enum}).
@var TintColors:      Some I{dynamic} tints, adaptable to vibrancy and accessibility settings, all L{TintColor} instances (C{enum}).
@var UIColors:        Some I{dynamic} UI element colors, adaptable to vibrancy and accessibility settings, all L{UIColor} instances (C{enum}).
'''
# all imports listed explicitly to help PyChecker
from pycocoa.bases   import _Type0
from pycocoa.lazily  import _ALL_LAZY
from pycocoa.nstypes import  NSColor
from pycocoa.utils   import _Constants, property_RO, _Types

from copy import copy as _copy
# from enum   import Enum

__all__ = _ALL_LAZY.colors
__version__ = '20.11.14'


def _Xhandler(unused):
    raise ColorError


class ColorError(ValueError):
    '''C{Color} issue.
    '''
    pass


# <https://Developer.Apple.com/documentation/appkit/nscolor>
class Color(_Type0):
    '''Base C{Color} class wrapping C{NSColor} objects,
       intended I{specifically} to avoid fatal exceptions
       when accessing I{non-applicable} C{NSColor} attributes.

       For example, getting the C{cyanComponent} of an RGB
       C{NSColor} instance throws an C{NSException}, but
       using L{Color.cyan} for any non-L{CMYColor} safely
       returns C{None}.  Likewise for other attributes.

       @note: Only pre-existing C{NSColor} can be wrapped,
              creating new C{NSColor} is reserved for a
              future C{PyCocoa} release.  Also, color
              conversion and any other U{"color math"
              <https://PyPI.org/project/colormath/>} are
              not supported (yet).
    '''

    _name    = None
    _nsColor = None

    def __init__(self, name, nsColor=''):
        ''' New L{Color} from an existing C{NSColor}.

           @arg name: Given color nsme (C{str}).
           @kwarg nsColor: Optionally, the name of an
                           existing C{NSColor} (C{str}).

           @note: If no B{C{nsColor}} is specified, it is
                  assumed to be the value of B{C{name}}
                  suffixed with C{"Color"}, provided
                  B{C{name}} does not end with C{"Color"}.

           @raise ColorError: Invalid B{C{name}} or
                              B{C{nsColor}}.
        '''
        if nsColor:
            c = nsColor
        elif name.endswith('Color'):
            raise ColorError('name %r invalid' % (name,))
        else:
            c = name + 'Color'
        ns = getattr(NSColor, c, None)
        if ns is None or not callable(ns):
            raise ColorError("color %r doesn't exist" % (c,))
        self.NS = ns()
        self.name = name  # capitalized
        self._nsColor = c

    @property_RO
    def alpha(self):
        '''Get the I{alpha} component (C{float}) or C{None} if not applicable or I{ignored}.
        '''
        return float(self.NS.alphaComponent())  # if not self.NS.ignoresAlpha() else None

    @property_RO
    def black(self):
        '''Get the I{black} component (C{float}) or C{None} if not applicable.
        '''
        return None

    @property_RO
    def blue(self):
        '''Get the I{blue} component (C{float}) or C{None} if not applicable.
        '''
        return None

    @property_RO
    def brightness(self):
        '''Get the I{brightness} component (C{float}) or C{None} if not applicable.
        '''
        return None

    @property_RO
    def colorSpace(self):
        '''Get the space of this color (C{str}).
        '''
        return self._colorSpace

    def copy(self, name):
        '''Copy this color with a new I{given} name.
        '''
        c = _copy(self)
        c.name = name
        return c

    @property_RO
    def cyan(self):
        '''Get the I{cyan} component (C{float}) or C{None} if not applicable.
        '''
        return None

    @property_RO
    def green(self):
        '''Get the I{green} component (C{float}) or C{None} if not applicable.
        '''
        return None

    @property_RO
    def hex(self):
        '''Get the I{RGB} components as I{hex} (C{int}) or C{None} if not applicable.
        '''
        h, t = None, self.toRGB3(upscale=255)
        if t:
            h = 0
            for c in t:
                h = (h << 8) + c
        return h

    @property_RO
    def hue(self):
        '''Get the I{hue} component (C{float}) or C{None} if not applicable.
        '''
        return None

    @property_RO
    def magenta(self):
        '''Get the I{magenta} component (C{float}) or C{None} if not applicable.
        '''
        return None

    @property_RO
    def n(self):
        '''Get the number of components of this color (C{int}) or C{None} if not applicable.
        '''
        return int(self.NS.numberOfComponents())

    @property
    def name(self):
        '''Get the given name of this color (C{str}).
        '''
        return self._name

    @name.setter  # PYCHOK property setter!
    def name(self, name):
        '''Set the given name of this color (C{str}).
        '''
        if name[:1].islower():
            name = name[:1].upper() + name[1:]
        self._name = name

    @property_RO
    def nsColor(self):
        '''Get the I{name} of the C{NSColor} of this color (C{str}).
        '''
        return self._nsColor

    @property_RO
    def red(self):
        '''Get the I{red} component (C{float}) or C{None} if not applicable.
        '''
        return None

    @property_RO
    def saturation(self):
        '''Get the I{saturation} component (C{float}) or C{None} if not applicable.
        '''
        return None

    def _to3(self, upscale, *components):
        '''(INTERNAL) Helper for C{.toCMY3}, C{.toHSB3} and C{.toRGB3}.
        '''
        t = tuple(c for c in components if c is not None) or None
        if t and upscale and isinstance(upscale, (int, float)):
            t = tuple(type(upscale)(max(0, min(upscale, upscale * c))) for c in t)
        return t

    def toCMY3(self, upscale=0):
        '''Get the I{RGB} components as 3-tuple C{(cyan, magenta, yellow}) or C{None} if not applicable.
        '''
        return self._to3(upscale, self.cyan, self.magenta, self.yellow)

    def toHSB3(self, upscale=0):
        '''Get the I{HSB} components as 3-tuple C{(hue, saturation, brightness}) or C{None} if not applicable.
        '''
        return self._to3(upscale, self.hue, self.saturation, self.brightness)

    def toRGB3(self, upscale=0):
        '''Get the I{RGB} components as 3-tuple C{(red, green, blue}) or C{None} if not applicable.
        '''
        return self._to3(upscale, self.red, self.green, self.blue)

    @property_RO
    def white(self):
        '''Get the I{white} component (C{float}) or C{None} if not applicable.
        '''
        return None

    @property_RO
    def yellow(self):
        '''Get the I{yellow} component (C{float}) or C{None} if not applicable.
        '''
        return None


class CMYColor(Color):
    '''Color in the Cyan-Magenta-Yellow space.
    '''
    @property_RO
    def cyan(self):
        '''Get the I{cyan} component (C{float}) or C{None} if not applicable.
        '''
        return 1.0 if self.name == 'Cyan' else 0.0  # float(self.NS.cyanComponent()) CRASHES

    @property_RO
    def magenta(self):
        '''Get the I{magenta} component (C{float}) or C{None} if not applicable.
        '''
        return 1.0 if self.name == 'Magenta' else 0.0  # float(self.NS.magentaComponent()) CRASHES

    @property_RO
    def yellow(self):
        '''Get the I{yellow} component (C{float}) or C{None} if not applicable.
        '''
        return 1.0 if self.name == 'Yellow' else 0.0  # float(self.NS.yellowComponent()) CRASHES


# <https://Developer.Apple.com/documentation/appkit/nscolor/standard_colors>
class CMYColors(_Constants):
    '''Some standard C{Cyan-Magenta-Yellow} colors.
    '''
    Cyan    = CMYColor('cyan')
    Magenta = CMYColor('magenta')
    Yellow  = CMYColor('yellow')

CMYColors = CMYColors()  # PYCHOK singleton


class GrayScaleColor(Color):
    '''Color in the Gray-Scale space.
    '''
    @property_RO
    def black(self):
        '''Get the I{black} component (C{float}) or C{None} if not applicable.
        '''
        return 1.0 - self.white  # float(self.NS.blackComponent()) CRASHES

    @property_RO
    def white(self):
        '''Get the I{white} component (C{float}) or C{None} if not applicable.
        '''
        return float(self.NS.whiteComponent())


# <https://Developer.Apple.com/documentation/appkit/nscolor/standard_colors>
class GrayScaleColors(_Constants):
    '''Some standard C{Gray-Scale} colors.
    '''
    Black      = GrayScaleColor('black')
    Clear      = GrayScaleColor('clear')
    DarkGray   = GrayScaleColor('darkGray')
    Gray       = GrayScaleColor('gray')
    LightGray  = GrayScaleColor('lightGray')
    Tansparent = Clear.copy('transparent')
    White      = GrayScaleColor('white')

GrayScaleColors = GrayScaleColors()  # PYCHOK singleton


class HSBColor(Color):
    '''Color in thecHue-Saturation-Brightness space.
    '''
    @property_RO
    def brightness(self):
        '''Get the I{brightness} component (C{float}) or C{None} if not applicable.
        '''
        return float(self.NS.brightnessComponent())

    @property_RO
    def hue(self):
        '''Get the I{hue} component (C{float}) or C{None} if not applicable.
        '''
        return float(self.NS.hueComponent())

    @property_RO
    def saturation(self):
        '''Get the I{saturation} component (C{float}) or C{None} if not applicable.
        '''
        return float(self.NS.saturationComponent())


# <https://Developer.Apple.com/documentation/appkit/nscolor/standard_colors>
class HSBColors(_Constants):
    '''I{No} standard C{Hue-Saturation-Brightness} colors, I{yet}.
    '''
    NoneYet=None

HSBColors = HSBColors()  # PYCHOK singleton


class RGBColor(Color):
    '''Color in the Red-Green-Blue space.
    '''
    @property_RO
    def blue(self):
        '''Get the I{blue} component (C{float}) or C{None} if not applicable.
        '''
        return float(self.NS.blueComponent())

    @property_RO
    def green(self):
        '''Get the I{green} component (C{float}) or C{None} if not applicable.
        '''
        return float(self.NS.greenComponent())

    @property_RO
    def red(self):
        '''Get the I{red} component (C{float}) or C{None} if not applicable.
        '''
        return float(self.NS.redComponent())


# <https://Developer.Apple.com/documentation/appkit/nscolor/standard_colors>
class RGBColors(_Constants):
    '''Some standard C{Red-Green-Blue} colors.
    '''
    Red     = RGBColor('red')
    Green   = RGBColor('green')
    Blue    = RGBColor('blue')

    Brown   = RGBColor('brown')
    Orange  = RGBColor('orange')
    Purple  = RGBColor('purple')

RGBColors = RGBColors()  # PYCHOK singleton


class _SystemColor(Color):
    '''I{Dynamic} color, adaptable to vibrancy and accessibility settings.
    '''
    @property_RO
    def n(self):
        '''Get the number of components of this color (C{int}) or C{None} if not applicable.
        '''
        return None  # int(self.NS.numberOfComponents())


class TintColor(_SystemColor):
    '''I{Dynamic} color, adaptable to vibrancy and accessibility settings.
    '''
    def __init__(self, name):
        Color.__init__(self, 'system' + name)
        self.name = name


# <https://Developer.Apple.com/documentation/appkit/nscolor/standard_colors>
class TintColors(_Constants):
    '''Some I{dynamic} tints, adaptable to vibrancy and accessibility settings.
    '''
    Blue    = TintColor('Blue')
    Brown   = TintColor('Brown')
    Gray    = TintColor('Gray')
    Green   = TintColor('Green')
    Indigo  = TintColor('Indigo')
    Orange  = TintColor('Orange')
    Pink    = TintColor('Pink')
    Purple  = TintColor('Purple')
    Red     = TintColor('Red')
    Teal    = TintColor('Teal')
    Yellow  = TintColor('Yellow')

TintColors = TintColors()  # PYCHOK singleton


class UIColor(_SystemColor):
    '''I{Dynamic} color for User-Interface elements, adaptable to vibrancy and accessibility settings.
    '''
    pass


# <https://Developer.Apple.com/documentation/appkit/nscolor/ui_element_colors>
class UIColors(_Constants):
    '''Some I{dynamic} UI element colors, adaptable to vibrancy and accessibility settings.
    '''
    Control           = UIColor('control')
    ControlBackground = UIColor('controlBackground')
    Grid              = UIColor('grid')
    HeaderText        = UIColor('headerText')
    Highlight         = UIColor('highlight')
    Label             = UIColor('label')
    Link              = UIColor('link')
    Separator         = UIColor('separator')
    SelectedText      = UIColor('selectedText')
    Shadow            = UIColor('shadow')
    Text              = UIColor('text')
    WindowBackground  = UIColor('windowBackground')

UIColors = UIColors()  # PYCHOK singleton


class Colors(_Constants):
    '''Colors by color space acronym, like C{Colors.RGB.Red}, C{Colors.Tint.Red}.
    '''
    CMY  = CMYColors
    GS   = GrayScaleColors
    HSB  = HSBColors
    RGB  = RGBColors
    Tint = TintColors
    UI   = UIColors

#   CMYK = None
#   dP3  = None  # displayP3
#   Lab  = None
#   sRGB = None

    def __repr__(self):
        def _fmt(n, v):  # just XYZColor class names
            return '%s=%s' % (n, v.__class__.__name__)
        return self._strepr(_fmt)

Colors = Colors()  # PYCHOK singleton

NSColor._Type = _Types.Color = Color

if __name__ == '__main__':

    from pycocoa.utils import _all_listing

    _all_listing(__all__, locals())

# % python3 -m pycocoa.colors
#
# pycocoa.colors.__all__ = tuple(
#  pycocoa.colors.CMYColor is <class .CMYColor>,
#  pycocoa.colors.CMYColors.Cyan=CMYColor(_NSTaggedPointerColor),
#                          .Magenta=CMYColor(_NSTaggedPointerColor),
#                          .Yellow=CMYColor(_NSTaggedPointerColor),
#  pycocoa.colors.Color is <class .Color>,
#  pycocoa.colors.ColorError is <class .ColorError>,
#  pycocoa.colors.Colors.CMY=CMYColors,
#                       .GS=GrayScaleColors,
#                       .HSB=HSBColors,
#                       .RGB=RGBColors,
#                       .Tint=TintColors,
#                       .UI=UIColors,
#  pycocoa.colors.GrayScaleColor is <class .GrayScaleColor>,
#  pycocoa.colors.GrayScaleColors.Black=GrayScaleColor(_NSTaggedPointerColor),
#                                .Clear=GrayScaleColor(_NSTaggedPointerColor),
#                                .DarkGray=GrayScaleColor(_NSTaggedPointerColor),
#                                .Gray=GrayScaleColor(_NSTaggedPointerColor),
#                                .LightGray=GrayScaleColor(_NSTaggedPointerColor),
#                                .Tansparent=GrayScaleColor(_NSTaggedPointerColor),
#                                .White=GrayScaleColor(_NSTaggedPointerColor),
#  pycocoa.colors.HSBColor is <class .HSBColor>,
#  pycocoa.colors.HSBColors.NoneYet=None,
#  pycocoa.colors.RGBColor is <class .RGBColor>,
#  pycocoa.colors.RGBColors.Blue=RGBColor(_NSTaggedPointerColor),
#                          .Brown=RGBColor(_NSTaggedPointerColor),
#                          .Green=RGBColor(_NSTaggedPointerColor),
#                          .Orange=RGBColor(NSCachedRGBColor),
#                          .Purple=RGBColor(NSCachedRGBColor),
#                          .Red=RGBColor(_NSTaggedPointerColor),
#  pycocoa.colors.TintColor is <class .TintColor>,
#  pycocoa.colors.TintColors.Blue=TintColor(NSDynamicSystemColor),
#                           .Brown=TintColor(NSDynamicSystemColor),
#                           .Gray=TintColor(NSDynamicSystemColor),
#                           .Green=TintColor(NSDynamicSystemColor),
#                           .Indigo=TintColor(NSDynamicSystemColor),
#                           .Orange=TintColor(NSDynamicSystemColor),
#                           .Pink=TintColor(NSDynamicSystemColor),
#                           .Purple=TintColor(NSDynamicSystemColor),
#                           .Red=TintColor(NSDynamicSystemColor),
#                           .Teal=TintColor(NSDynamicSystemColor),
#                           .Yellow=TintColor(NSDynamicSystemColor),
#  pycocoa.colors.UIColor is <class .UIColor>,
#  pycocoa.colors.UIColors.Control=UIColor(NSDynamicSystemColor),
#                         .ControlBackground=UIColor(NSDynamicSystemColor),
#                         .Grid=UIColor(NSDynamicSystemColor),
#                         .HeaderText=UIColor(NSDynamicSystemColor),
#                         .Highlight=UIColor(NSDynamicSystemColor),
#                         .Label=UIColor(NSDynamicSystemColor),
#                         .Link=UIColor(NSDynamicSystemColor),
#                         .SelectedText=UIColor(NSDynamicSystemColor),
#                         .Separator=UIColor(NSDynamicSystemColor),
#                         .Shadow=UIColor(NSDynamicSystemColor),
#                         .Text=UIColor(NSDynamicSystemColor),
#                         .WindowBackground=UIColor(NSDynamicSystemColor),
# )[15]
# pycocoa.colors.version 20.11.14, .isLazy 1, Python 3.9.0 64bit, macOS 10.15.7

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2020 -- mrJean1 at Gmail -- All Rights Reserved.
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
