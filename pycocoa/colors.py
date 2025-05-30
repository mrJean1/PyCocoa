
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Types L{Color}, L{ColorError}, L{CMYColor}, L{GrayScaleColor}, L{HSBColor}, L{RGBColor},
L{TintColor} and L{UIColor} wrapping Cocoa's C{NSColor} and C{enum}-like constants
L{CMYColors}, L{GrayScaleColors}, L{HSBColors}, L{RGBColors}, L{TintColor}, L{TintColors},
L{UIColors} and all L{Colors} accessible by color space acronym like C{CMY}, C{GS}, C{RGB}, etc.

@var Colors: Colors by color space acronym, like C{Colors.RGB.Red}, C{Colors.Tint.Red} (C{enum}).
@var Colors.CMY: Some standard C{Cyan-Magenta-Yellow} colors, all L{CMYColor} instances (C{enum}).
@var Colors.GS: Some standard C{Gray-Scale} colors, all L{GrayScaleColor} instances (C{enum}).
@var Colors.HSB: I{No} standard C{Hue-Saturation-Brightness} colors, L{HSBColor} instances (C{enum}).
@var Colors.RGB: Some standard C{Red-Green-Blue} colors, all L{RGBColor} instances (C{enum}).
@var Colors.Tint: Some I{dynamic} tints, adaptable to vibrancy and accessibility settings, all L{TintColor} instances (C{enum}).
@var Colors.UI: Some I{dynamic} UI element colors, adaptable to vibrancy and accessibility settings, all L{UIColor} instances (C{enum}).

@var CMYColors: Some standard C{Cyan-Magenta-Yellow} colors, all L{CMYColor} instances (C{enum}).
@var CMYColors.Cyan: Color in the Cyan-Magenta-Yellow space.
@var CMYColors.Magenta: Color in the Cyan-Magenta-Yellow space.
@var CMYColors.Yellow: Color in the Cyan-Magenta-Yellow space.

@var GrayScaleColors: Some standard C{Gray-Scale} colors, all L{GrayScaleColor} instances (C{enum}).
@var GrayScaleColors.Black: Color in the Gray-Scale space.
@var GrayScaleColors.Clear: Color in the Gray-Scale space.
@var GrayScaleColors.DarkGray: Color in the Gray-Scale space.
@var GrayScaleColors.Gray: Color in the Gray-Scale space.
@var GrayScaleColors.LightGray: Color in the Gray-Scale space.
@var GrayScaleColors.Tansparent: Color in the Gray-Scale space.
@var GrayScaleColors.White: Color in the Gray-Scale space.

@var HSBColors: I{No} standard C{Hue-Saturation-Brightness} colors, L{HSBColor} instances (C{enum}).
@var HSBColors.NoneYet: The type of the None singleton.

@var RGBColors: Some standard C{Red-Green-Blue} colors, all L{RGBColor} instances (C{enum}).
@var RGBColors.Blue: Color in the Red-Green-Blue space.
@var RGBColors.Brown: Color in the Red-Green-Blue space.
@var RGBColors.Green: Color in the Red-Green-Blue space.
@var RGBColors.Orange: Color in the Red-Green-Blue space.
@var RGBColors.Purple: Color in the Red-Green-Blue space.
@var RGBColors.Red: Color in the Red-Green-Blue space.

@var TintColors: Some I{dynamic} tints, adaptable to vibrancy and accessibility settings, all L{TintColor} instances (C{enum}).
@var TintColors.Blue: I{Dynamic} color, adaptable to vibrancy and accessibility settings.
@var TintColors.Brown: I{Dynamic} color, adaptable to vibrancy and accessibility settings.
@var TintColors.Gray: I{Dynamic} color, adaptable to vibrancy and accessibility settings.
@var TintColors.Green: I{Dynamic} color, adaptable to vibrancy and accessibility settings.
@var TintColors.Indigo: I{Dynamic} color, adaptable to vibrancy and accessibility settings.
@var TintColors.Orange: I{Dynamic} color, adaptable to vibrancy and accessibility settings.
@var TintColors.Pink: I{Dynamic} color, adaptable to vibrancy and accessibility settings.
@var TintColors.Purple: I{Dynamic} color, adaptable to vibrancy and accessibility settings.
@var TintColors.Red: I{Dynamic} color, adaptable to vibrancy and accessibility settings.
@var TintColors.Teal: I{Dynamic} color, adaptable to vibrancy and accessibility settings.
@var TintColors.Yellow: I{Dynamic} color, adaptable to vibrancy and accessibility settings.

@var UIColors: Some I{dynamic} UI element colors, adaptable to vibrancy and accessibility settings, all L{UIColor} instances (C{enum}).
@var UIColors.Control: I{Dynamic} color for User-Interface elements, adaptable to vibrancy and accessibility settings.
@var UIColors.ControlBackground: I{Dynamic} color for User-Interface elements, adaptable to vibrancy and accessibility settings.
@var UIColors.Grid: I{Dynamic} color for User-Interface elements, adaptable to vibrancy and accessibility settings.
@var UIColors.HeaderText: I{Dynamic} color for User-Interface elements, adaptable to vibrancy and accessibility settings.
@var UIColors.Highlight: I{Dynamic} color for User-Interface elements, adaptable to vibrancy and accessibility settings.
@var UIColors.Label: I{Dynamic} color for User-Interface elements, adaptable to vibrancy and accessibility settings.
@var UIColors.Link: I{Dynamic} color for User-Interface elements, adaptable to vibrancy and accessibility settings.
@var UIColors.SelectedText: I{Dynamic} color for User-Interface elements, adaptable to vibrancy and accessibility settings.
@var UIColors.Separator: I{Dynamic} color for User-Interface elements, adaptable to vibrancy and accessibility settings.
@var UIColors.Shadow: I{Dynamic} color for User-Interface elements, adaptable to vibrancy and accessibility settings.
@var UIColors.Text: I{Dynamic} color for User-Interface elements, adaptable to vibrancy and accessibility settings.
@var UIColors.WindowBackground: I{Dynamic} color for User-Interface elements, adaptable to vibrancy and accessibility settings.
'''
from pycocoa.baseTypes import _Type0,  _Types
from pycocoa.basics import _Constants
from pycocoa.internals import _Dmain_, _EQUALS_, _nameOf, _NN_, property_RO
from pycocoa.lazily import _ALL_LAZY,  _fmt_invalid
from pycocoa.nstypes import  NSColor

from copy import copy as _copy
# from enum import Enum

__all__ = _ALL_LAZY.colors
__version__ = '25.04.07'


class _ColorConstants(_Constants):
    '''(INTERNAL) Base C{Colors} class.
    '''
    _items_Class = None

    def items_(self, *classes):
        '''See mthods L{items_<_Constants.items_>}.
        '''
        if not classes:
            assert self._items_Class  # is not None
            classes = (self._items_Class,)
        return super(_ColorConstants, self).items_(*classes)


class ColorError(ValueError):
    '''C{Color} issue.
    '''
    pass


# <https://Developer.Apple.com/documentation/appkit/nscolor>
class Color(_Type0):
    '''Base C{Color} class wrapping C{NSColor} objects, intended
       I{specifically} to avoid fatal exceptions when accessing
       I{non-applicable} C{NSColor} attributes.

       For example, getting the C{cyanComponent} of an RGB C{NSColor}
       instance throws an C{NSException}, but using L{Color.cyan} for
       any non-L{CMYColor} safely returns C{None}.  Likewise for other
       attributes.

       @note: Only pre-existing C{NSColor} can be wrapped, creating
              new C{NSColor} is reserved for a future C{PyCocoa}
              release.  Also, color conversion and any other U{"color
              math"<https://PyPI.org/project/colormath/>} are not
              supported (yet).
    '''
    _name    = None
    _nsColor = None

    def __init__(self, name, nsColor=_NN_):
        ''' New L{Color} from an existing C{NSColor}.

           @arg name: Given color name (C{str}).
           @kwarg nsColor: Optionally, the name of an existing
                           C{NSColor} (C{str}).

           @note: If no B{C{nsColor}} is specified, it is assumed
                  to be the value of B{C{name}} suffixed with
                  C{"Color"}, provided B{C{name}} does not end with
                  C{"Color"}.

           @raise ColorError: Invalid B{C{name}} or B{C{nsColor}}.
        '''
        if nsColor:
            c = nsColor
        elif name.endswith(_nameOf(Color)):
            raise ColorError(_fmt_invalid(name=repr(name)))
        else:
            c = name + _nameOf(Color)
        ns = getattr(NSColor, c, None)
        if ns is None or not callable(ns):
            raise ColorError(_fmt_invalid(color=repr(c)))
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
        n = name[:1]
        if n.islower():  # NOT name.capitalize()!
            name = n.upper() + name[1:]
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
class CMYColors(_ColorConstants):
    '''Some standard C{Cyan-Magenta-Yellow} colors, all L{CMYColor} instances (C{enum}).
    '''
    _items_Class = CMYColor

    Cyan         = CMYColor('cyan')
    Magenta      = CMYColor('magenta')
    Yellow       = CMYColor('yellow')

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
class GrayScaleColors(_ColorConstants):
    '''Some standard C{Gray-Scale} colors, all L{GrayScaleColor} instances (C{enum}).
    '''
    _items_Class = GrayScaleColor

    Black        = GrayScaleColor('black')
    Clear        = GrayScaleColor('clear')
    DarkGray     = GrayScaleColor('darkGray')
    Gray         = GrayScaleColor('gray')
    LightGray    = GrayScaleColor('lightGray')
    Tansparent   = Clear.copy('transparent')
    White        = GrayScaleColor('white')

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
class HSBColors(_ColorConstants):
    '''I{No} standard C{Hue-Saturation-Brightness} colors, L{HSBColor} instances (C{enum}).
    '''
    _items_Class = HSBColor
    NoneYet      = None

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
class RGBColors(_ColorConstants):
    '''Some standard C{Red-Green-Blue} colors, all L{RGBColor} instances (C{enum}).
    '''
    _items_Class = RGBColor

    Red          = RGBColor('red')
    Green        = RGBColor('green')
    Blue         = RGBColor('blue')

    Brown        = RGBColor('brown')
    Orange       = RGBColor('orange')
    Purple       = RGBColor('purple')

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
        Color.__init__(self, _NN_('system', name))
        self.name = name


# <https://Developer.Apple.com/documentation/appkit/nscolor/standard_colors>
class TintColors(_ColorConstants):
    '''Some I{dynamic} tints, adaptable to vibrancy and accessibility settings, all L{TintColor} instances (C{enum}).
    '''
    _items_Class = TintColor

    Blue         = TintColor('Blue')
    Brown        = TintColor('Brown')
    Gray         = TintColor('Gray')
    Green        = TintColor('Green')
    try:  # may not exist
        Indigo   = TintColor('Indigo')
    except ColorError:
        pass
    Orange       = TintColor('Orange')
    Pink         = TintColor('Pink')
    Purple       = TintColor('Purple')
    Red          = TintColor('Red')
    Teal         = TintColor('Teal')
    Yellow       = TintColor('Yellow')

TintColors = TintColors()  # PYCHOK singleton


class UIColor(_SystemColor):
    '''I{Dynamic} color for User-Interface elements, adaptable to vibrancy and accessibility settings.
    '''
    pass


# <https://Developer.Apple.com/documentation/appkit/nscolor/ui_element_colors>
class UIColors(_ColorConstants):
    '''Some I{dynamic} UI element colors, adaptable to vibrancy and accessibility settings, all L{UIColor} instances (C{enum}).
    '''
    _items_Class      = UIColor

    Control           = UIColor('control')
    ControlBackground = UIColor('controlBackground')
    Grid              = UIColor('grid')
    HeaderText        = UIColor('headerText')
    Highlight         = UIColor('highlight')
    Label             = UIColor('label')
    Link              = UIColor('link')
    SelectedText      = UIColor('selectedText')
    try:
        Separator     = UIColor('separator')
    except ColorError:
        pass
    Shadow            = UIColor('shadow')
    Text              = UIColor('text')
    WindowBackground  = UIColor('windowBackground')

UIColors = UIColors()  # PYCHOK singleton


class Colors(_ColorConstants):
    '''Colors by color space acronym, like C{Colors.RGB.Red}, C{Colors.Tint.Red} (C{enum}).
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

    _items_Class = _ColorConstants

    def __repr__(self):
        def _fmt2(n, v):  # just XYZColor class names
            return _EQUALS_(n, _nameOf(type(v)))
        return self._strepr(_fmt2)

Colors = Colors()  # PYCHOK singleton

NSColor._Type = _Types.Color = Color

if __name__ == _Dmain_:

    from pycocoa.utils import _all_listing, _varstr

    print(_varstr(Colors))
    print(_varstr(CMYColors))
    print(_varstr(GrayScaleColors))
    print(_varstr(HSBColors))
    print(_varstr(RGBColors))
    print(_varstr(TintColors))
    print(_varstr(UIColors))

    _all_listing(__all__, locals())

# % python3 -m pycocoa.colors
#
# pycocoa.colors.__all__ = tuple(
#  pycocoa.colors.CMYColor is <class .CMYColor>,
#  pycocoa.colors.CMYColors.Cyan=CMYColor(_NSTaggedPointerColor, name='Cyan'),
#                          .Magenta=CMYColor(_NSTaggedPointerColor, name='Magenta'),
#                          .Yellow=CMYColor(_NSTaggedPointerColor, name='Yellow'),
#  pycocoa.colors.Color is <class .Color>,
#  pycocoa.colors.ColorError is <class .ColorError>,
#  pycocoa.colors.Colors.CMY=CMYColors,
#                       .GS=GrayScaleColors,
#                       .HSB=HSBColors,
#                       .RGB=RGBColors,
#                       .Tint=TintColors,
#                       .UI=UIColors,
#  pycocoa.colors.GrayScaleColor is <class .GrayScaleColor>,
#  pycocoa.colors.GrayScaleColors.Black=GrayScaleColor(_NSTaggedPointerColor, name='Black'),
#                                .Clear=GrayScaleColor(_NSTaggedPointerColor, name='Clear'),
#                                .DarkGray=GrayScaleColor(_NSTaggedPointerColor, name='DarkGray'),
#                                .Gray=GrayScaleColor(_NSTaggedPointerColor, name='Gray'),
#                                .LightGray=GrayScaleColor(_NSTaggedPointerColor, name='LightGray'),
#                                .Tansparent=GrayScaleColor(_NSTaggedPointerColor, name='Transparent'),
#                                .White=GrayScaleColor(_NSTaggedPointerColor, name='White'),
#  pycocoa.colors.HSBColor is <class .HSBColor>,
#  pycocoa.colors.HSBColors.NoneYet=None,
#  pycocoa.colors.RGBColor is <class .RGBColor>,
#  pycocoa.colors.RGBColors.Blue=RGBColor(_NSTaggedPointerColor, name='Blue'),
#                          .Brown=RGBColor(_NSTaggedPointerColor, name='Brown'),
#                          .Green=RGBColor(_NSTaggedPointerColor, name='Green'),
#                          .Orange=RGBColor(NSCachedColorSpaceColor, name='Orange'),
#                          .Purple=RGBColor(NSCachedColorSpaceColor, name='Purple'),
#                          .Red=RGBColor(_NSTaggedPointerColor, name='Red'),
#  pycocoa.colors.TintColor is <class .TintColor>,
#  pycocoa.colors.TintColors.Blue=TintColor(NSDynamicSystemColor, name='Blue'),
#                           .Brown=TintColor(NSDynamicSystemColor, name='Brown'),
#                           .Gray=TintColor(NSDynamicSystemColor, name='Gray'),
#                           .Green=TintColor(NSDynamicSystemColor, name='Green'),
#                           .Indigo=TintColor(NSDynamicSystemColor, name='Indigo'),
#                           .Orange=TintColor(NSDynamicSystemColor, name='Orange'),
#                           .Pink=TintColor(NSDynamicSystemColor, name='Pink'),
#                           .Purple=TintColor(NSDynamicSystemColor, name='Purple'),
#                           .Red=TintColor(NSDynamicSystemColor, name='Red'),
#                           .Teal=TintColor(NSDynamicSystemColor, name='Teal'),
#                           .Yellow=TintColor(NSDynamicSystemColor, name='Yellow'),
#  pycocoa.colors.UIColor is <class .UIColor>,
#  pycocoa.colors.UIColors.Control=UIColor(NSDynamicSystemColor, name='Control'),
#                         .ControlBackground=UIColor(NSDynamicSystemColor, name='ControlBackground'),
#                         .Grid=UIColor(NSDynamicSystemColor, name='Grid'),
#                         .HeaderText=UIColor(NSDynamicSystemColor, name='HeaderText'),
#                         .Highlight=UIColor(NSDynamicSystemColor, name='Highlight'),
#                         .Label=UIColor(NSDynamicSystemColor, name='Label'),
#                         .Link=UIColor(NSDynamicSystemColor, name='Link'),
#                         .SelectedText=UIColor(NSDynamicSystemColor, name='SelectedText'),
#                         .Separator=UIColor(NSDynamicSystemColor, name='Separator'),
#                         .Shadow=UIColor(NSDynamicSystemColor, name='Shadow'),
#                         .Text=UIColor(NSDynamicSystemColor, name='Text'),
#                         .WindowBackground=UIColor(NSDynamicSystemColor, name='WindowBackground'),
# )[15]
# pycocoa.colors.version 25.4.7, .isLazy 1, Python 3.13.2 64bit arm64, macOS 15.4

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
