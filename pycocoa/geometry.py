
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Types L{Point}, L{Rect} and L{Size}, wrapping ObjC C{NSPoint_t}, L{NSRect_t}, C{NSSize_t}.
'''
# all imports listed explicitly to help PyChecker
from bases   import _Type0
from octypes import NSPoint_t, NSRect_t, NSRect4_t, NSSize_t
from utils   import isinstanceOf

__all__ = ('Point', 'Point2',
           'Rect', 'Rect4',
           'Size', 'Size2')
__version__ = '18.06.28'


class Point(_Type0):
    '''Python Type, wrapping an ObjC C{NSPoint_t}.
    '''
    def __init__(self, point):
        '''New L{Point} from another L{Point}, C{list}, C{tuple} or C{NSPoint_t}.
        '''
        self.point = point

    @property
    def point(self):
        '''Get the 2-tuple (x, y) coordinate of (C{float} or C{int}).
        '''
        return self.x, self.y

    @point.setter  # PYCHOK property.setter
    def point(self, point):
        if isinstance(point, (tuple, list)):
            if len(point) != 2:
                raise ValueError('%s invalid: %r' % ('point', point))
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
        '''New L{Rect} from another L{Rect}, C{list}, C{tuple} or C{NSRect[4]_t}.
        '''
        self.rect = rect

    @property
    def rect(self):
        '''Get x, y, width, height (4-tuple).
        '''
        return self.x, self.y, self.width, self.height

    @rect.setter  # PYCHOK property.setter
    def rect(self, rect):
        '''Set the rect (L{Rect}, C{list}, C{tuple} or C{NSRect[4]_t}).
        '''
        if isinstance(rect, (tuple, list)):
            if len(rect) == 2:  # assume (w, h)
                rect = (self._x, self._y) + tuple(rect)
            elif len(rect) != 4:
                raise ValueError('%s invalid: %r' % ('rect', rect))
            self.NS = NSRect4_t(*rect)
        elif isinstance(rect, Rect):
            self.NS = rect.NS
        elif isinstanceOf(rect, NSRect_t, name='rect'):
            self.NS = rect

    @property
    def bottom(self):
        '''Get the lower y coordinate (C{float} or C{int}).
        '''
        return self.y

    @property
    def height(self):
        '''Get the height (float).
        '''
        return self.NS.size.height

    @height.setter  # PYCHOK property.setter
    def height(self, height):
        '''Set the height (float).
        '''
        if height < 0:
            height = -height
            self.y -= height
        self.NS.size.height = height

    @property
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
        origin = Point(origin)
        self.x, self.y = origin.x, origin.y

    @property
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
        size = Size(size)
        self.width, self.height = size.width, size.height

    @property
    def top(self):
        '''Get the upper y coordinate (C{float} or C{int}).
        '''
        return self.y + self.height

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

    @property
    def size(self):
        '''Get the width, height (2-tuple) of (C{float} or C{int}).
        '''
        return self.width, self.height

    @size.setter  # PYCHOK property.setter
    def size(self, size):
        '''Set the size (L{Size}, C{list}, C{tuple} or C{NSSize_t}).
        '''
        if isinstance(size, (tuple, list)):
            if len(size) != 2:
                raise ValueError('%s invalid: %r' % ('size', size))
            self.NS = NSSize_t(*size)
        elif isinstance(size, Size):
            self.NS = size.NS
        elif isinstanceOf(size, NSSize_t, name='size'):
            self.NS = size

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

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)

# MIT License <http://OpenSource.org/licenses/MIT>
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
