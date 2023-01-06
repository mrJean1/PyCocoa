
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Types L{Point}, L{Rect} and L{Size}, wrapping ObjC C{NSPoint_t}, L{NSRect_t}, C{NSSize_t}.
'''
# all imports listed explicitly to help PyChecker
from pycocoa.bases import _Type0
from pycocoa.lazily import _ALL_LAZY
from pycocoa.nstypes import nsValue2py
from pycocoa.octypes import NSPoint_t, NSRect_t, NSRect4_t, NSSize_t
from pycocoa.utils import aspect_ratio, isinstanceOf, property_RO, \
                          type2strepr

__all__ = _ALL_LAZY.geometry
__version__ = '21.11.04'


class Point(_Type0):
    '''Python Type, wrapping an ObjC C{NSPoint_t}.
    '''
    def __init__(self, point):
        '''New L{Point} from another L{Point}, C{list}, C{tuple} or C{NSPoint_t}.
        '''
        self.point = point

    def __str__(self):
        return type2strepr(self, x=self.x, y=self.y)

    @property
    def point(self):
        '''Get the 2-tuple (x, y) coordinate of (C{float} or C{int}).
        '''
        return self.x, self.y

    @point.setter  # PYCHOK property.setter
    def point(self, point):
        if isinstance(point, (tuple, list)):
            if len(point) != 2:
                raise ValueError('invalid %s: %r' % ('point', point))
            self.NS = NSPoint_t(*point)
        elif isinstance(point, Point):
            self.NS = point.NS
        elif isinstanceOf(point, NSPoint_t, name='point'):
            self.NS = point

    @property
    def x(self):
        '''Get the x coordinate (C{float} or C{int}).
        '''
        return self.NS.x

    @x.setter  # PYCHOK property.setter
    def x(self, x):
        self.NS.x = x

    @property
    def y(self):
        '''Get the y coordinate (C{float} or C{int}).
        '''
        return self.NS.y

    @y.setter  # PYCHOK property.setter
    def y(self, y):
        self.NS.y = y


class Point2(Point):
    '''Python Type, like L{Point}, different signature.
    '''
    def __init__(self, x=0, y=0):
        '''New L{Point2} keyword arguments.
        '''
        self.point = (x, y)


class Rect(_Type0):
    '''Python Type, wrapping an ObjC L{NSRect_t}.
    '''

    def __init__(self, rect):
        '''New L{Rect} from another (L{Rect}, C{list}, C{tuple} or C{NSRect[4]_t}).
        '''
        self.rect = rect

    def __str__(self):
        return type2strepr(self, origin=self.origin, size=self.size)

    @property_RO
    def bottom(self):
        '''Get the lower y coordinate (C{float} or C{int}).
        '''
        return self.y

    @property_RO
    def bottomleft(self):
        '''Get the lower left (L{Point}).
        '''
        return Point(self.x, self.y)

    lowerleft = bottomleft

    @property_RO
    def bottomright(self):
        '''Get the lower right (L{Point}).
        '''
        return Point((self.x, self.y))

    lowerright = bottomright

    @property_RO
    def center(self):
        '''Get the center (L{Point}).
        '''
        return Point(((self.left + self.right) / 2,
                      (self.bottom + self.top) / 2))

    @property
    def height(self):
        '''Get the height (C{float}).
        '''
        return self.NS.size.height

    @height.setter  # PYCHOK property.setter
    def height(self, height):
        '''Set the height (C{float}).
        '''
        if height < 0:
            height = -height
            self.y -= height
        self.NS.size.height = height

    @property_RO
    def left(self):
        '''Get the lower x coordinate (C{float} or C{int}).
        '''
        return self.x

    @property
    def origin(self):
        '''Get the origin (L{Point}, C{list}, C{tuple} or C{NSPoint_t}).
        '''
        return Point(self.NS.origin)

    @origin.setter  # PYCHOK property.setter
    def origin(self, origin):
        '''Set the origin (Point).
        '''
        o = Point(origin)
        self.x, self.y = o.x, o.y

    @property
    def ratio(self):
        '''Get th aspect ratio as 2-tuple (width, height).
        '''
        return aspect_ratio(self.width, self.height)

    @ratio.setter  # PYCHOK property.setter
    def ratio(self, ratio):
        '''Adjust width and/or height to the given aspect ratio.

           @param ratio: New ratio (L{Size}, 2-tuple (width, height), str("w:h") or C{NSSize_t}).

           @raise valueError: Invalid I{ratio}.
        '''
        z = self.size
        z.ratio = ratio
        self.size = z

    @property
    def rect(self):
        '''Get x, y, width, height (C{4-tuple}).

           @see: Property C{rect4}.
        '''
        return self.x, self.y, self.width, self.height

    @rect.setter  # PYCHOK property.setter!
    def rect(self, rect):
        '''Set the rect (L{Rect}, C{2-list}, C{4-list},
           C{2-tuple}, C{4-tuple} or C{NSRect[4]_t}).
        '''
        if isinstance(rect, (tuple, list)):
            if len(rect) == 2:  # assume (w, h)
                rect = (self._x, self._y) + tuple(rect)
            elif len(rect) != 4:
                raise ValueError('invalid %s: %r' % ('rect', rect))
            self.NS = NSRect4_t(*rect)
        elif isinstance(rect, Rect):
            self.NS = rect.NS
        elif isinstanceOf(rect, NSRect_t, name='rect'):
            self.NS = rect

    @property_RO
    def rect4(self):
        '''Get left, bottom, right top (C{4-tuple}).

           @see: Property C{rect}.
        '''
        return self.x, self.y, self.right, self.top

    @property_RO
    def right(self):
        '''Get the upper x coordinate (C{float} or C{int}).
        '''
        return self.x + self.width

    @property
    def size(self):
        '''Get the size (L{Size}).
        '''
        return Size(self.NS.size)

    @size.setter  # PYCHOK property.setter
    def size(self, size):
        '''Set the size (L{Size}, C{list}, C{tuple} or C{NSSize_t}).
        '''
        if not isinstance(size, (Size, NSSize_t, Rect)):
            size = Size(size)
        self.width, self.height = size.width, size.height

    @property_RO
    def top(self):
        '''Get the upper y coordinate (C{float} or C{int}).
        '''
        return self.y + self.height

    @property_RO
    def topleft(self):
        '''Get the upper left (L{Point}).
        '''
        return Point((self.x, self.top))

    upperleft = topleft

    @property_RO
    def topright(self):
        '''Get the upper right (L{Point}).
        '''
        return Point((self.right, self.top))

    upperright = topright

    @property
    def width(self):
        '''Get the width (C{float} or C{int}).
        '''
        return self.NS.size.width

    @width.setter  # PYCHOK property.setter
    def width(self, width):
        '''Set the width (C{float} or C{int}).
        '''
        if width < 0:
            width = -width
            self.x -= width
        self.NS.size.width = width

    @property
    def x(self):
        '''Get the x coordinate (C{float} or C{int}).
        '''
        return self.NS.origin.x

    @x.setter  # PYCHOK property.setter
    def x(self, x):
        '''Set the x coordinate (C{float} or C{int}).
        '''
        self.NS.origin.x = x

    @property
    def y(self):
        '''Get the y coordinate (C{float} or C{int}).
        '''
        return self.NS.origin.y

    @y.setter  # PYCHOK property.setter
    def y(self, y):
        '''Set the y coordinate (C{float} or C{int}).
        '''
        self.NS.origin.y = y


class Rect4(Rect):
    '''Python Type, like L{Rect}, but signature as ObjC L{NSRect4_t}.
    '''
    def __init__(self, x=0, y=0, width=0, height=0):
        '''New L{Rect4} from keyword arguments.
        '''
        self.rect = x, y, width, height


class Size(_Type0):
    '''Python Type, wrapping an ObjC C{NSSize_t}.
    '''
    def __init__(self, size):
        '''New L{Size} from another L{Size}, C{list}, C{tuple} or C{NSSize_t}.
        '''
        self.size = size

    def __str__(self):
        return type2strepr(self, width=self.width, height=self.height)

    @property
    def height(self):
        '''Get the height (C{float} or C{int}).
        '''
        return self.NS.height

    @height.setter  # PYCHOK property.setter
    def height(self, height):
        '''Set the height (C{float} or C{int}).
        '''
        self.NS.height = height

    @property
    def ratio(self):
        '''Get the aspect ratio as 2-tuple (width, height).
        '''
        return aspect_ratio(self.size)

    @ratio.setter  # PYCHOK property.setter
    def ratio(self, ratio):
        '''Adjust width and/or height to the given aspect ratio.

           @param ratio: New ratio (L{Size}, 2-tuple (width, height), str("w:h") or C{NSSize_t}).

           @raise ValueError: Invalid I{ratio}.
        '''
        r = aspect_ratio(ratio)
        if r:  # adjust width or height to ratio
            w, h = self.size
            a, b = r
            if a > b:
                h = type(h)(w * b / float(a))
            elif b > a:
                w = type(w)(h * a / float(b))
            elif w > h:
                h = type(h)(w)
            else:
                w = type(w)(h)
            if (w, h) != self.size:
                self.size = w, h

    @property
    def size(self):
        '''Get the width, height (2-tuple) of (C{float} or C{int}).
        '''
        ns = self.NS
        return ns.width, ns.height

    @size.setter  # PYCHOK property.setter
    def size(self, size):
        '''Set the size (L{Size}, C{list}, C{tuple} or C{NSSize_t}).
        '''
        if isinstance(size, (tuple, list)):
            if len(size) != 2:
                raise ValueError('invalid %s: %r' % ('size', size))
            self.NS = NSSize_t(*size)
        elif isinstance(size, Size):
            self.NS = size.NS
        elif isinstanceOf(size, NSSize_t):
            self.NS = size
        else:  # NSConcreteValue, like screen.resolutions
            self.NS = nsValue2py(size)  # NSSize_t

    @property
    def width(self):
        '''Get the width (C{float} or C{int}).
        '''
        return self.NS.width

    @width.setter  # PYCHOK property.setter
    def width(self, width):
        '''Set the width (C{float} or C{int}).
        '''
        self.NS.width = width


class Size2(Size):
    '''Python Type, like L{Size}, different signature.
    '''
    def __init__(self, width=0, height=0):
        '''New L{Size2} from keyword arguments.
        '''
        self.size = width, height


if __name__ == '__main__':

    from pycocoa.utils import _all_listing

    _all_listing(__all__, locals())

# % python3 -m pycocoa.geometry
#
# pycocoa.geometry.__all__ = tuple(
#  pycocoa.geometry.Point is <class .Point>,
#  pycocoa.geometry.Point2 is <class .Point2>,
#  pycocoa.geometry.Rect is <class .Rect>,
#  pycocoa.geometry.Rect4 is <class .Rect4>,
#  pycocoa.geometry.Size is <class .Size>,
#  pycocoa.geometry.Size2 is <class .Size2>,
# )[6]
# pycocoa.geometry.version 21.11.04, .isLazy 1, Python 3.11.0 64bit arm64, macOS 13.0.1

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
