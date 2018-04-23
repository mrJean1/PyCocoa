
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

'''Types L{Point}, L{Rect} and L{Size}, wrapping ObjC C{NSPoint_t}, C{NSRect_t}, C{NSSize_t}.
'''
# all imports listed explicitly to help PyChecker
from bases   import _Type0
from octypes import NSPoint_t, NSRect_t, NSRect4_t, NSSize_t
from utils   import instanceof

__all__ = ('Point', 'Point2',
           'Rect', 'Rect4',
           'Size', 'Size2')
__version__ = '18.04.21'


class Point(_Type0):
    '''Python Type, wrapping an ObjC C{NSPoint_t}.
    '''
    def __init__(self, point):
        '''New L{Point} from another L{Point}, C{list}, C{tuple} or C{NSPoint_t}.
        '''
        self.point = point

    @property
    def point(self):
        '''Get the x and y coordinate (2-tuple).
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
        elif instanceof(point, NSPoint_t, name='point'):
            self.NS = point

    @property
    def x(self):
        '''Get the x coordinate (float).
        '''
        return self.NS.x

    @x.setter  # PYCHOK property.setter
    def x(self, x):
        self.NS.x = x

    @property
    def y(self):
        '''Get the y coordinate (float).
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
    '''Python Type, wrapping an ObjC C{NSRect_t}.
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
        elif instanceof(rect, NSRect_t, name='rect'):
            self.NS = rect

    @property
    def bottom(self):
        '''Get the lower y coordinate (float).
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
        '''Get the lower x coordinate (float).
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
        '''Get the upper x coordinate (float).
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
        '''Get the upper y coordinate (float).
        '''
        return self.y + self.height

    @property
    def width(self):
        '''Get the width (float).
        '''
        return self.NS.size.width

    @width.setter  # PYCHOK property.setter
    def width(self, width):
        '''Set the width (float).
        '''
        if width < 0:
            width = -width
            self.x -= width
        self.NS.size.width = width

    @property
    def x(self):
        '''Get the x coordinate (float).
        '''
        return self.NS.origin.x

    @x.setter  # PYCHOK property.setter
    def x(self, x):
        '''Set the x coordinate (float).
        '''
        self.NS.origin.x = x

    @property
    def y(self):
        '''Get the y coordinate (float).
        '''
        return self.NS.origin.y

    @y.setter  # PYCHOK property.setter
    def y(self, y):
        '''Set the y coordinate (float).
        '''
        self.NS.origin.y = y


class Rect4(Rect):
    '''Python Type, like L{Rect}, but signature as ObjC C{NSRect4_t}.
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
        '''Get the width, height (2-tuple).
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
        elif instanceof(size, NSSize_t, name='size'):
            self.NS = size

    @property
    def height(self):
        '''Get the height (float).
        '''
        return self.NS.height

    @height.setter  # PYCHOK property.setter
    def height(self, height):
        '''Set the height (float).
        '''
        self.NS.height = height

    @property
    def width(self):
        '''Get the width (float).
        '''
        return self.NS.width

    @width.setter  # PYCHOK property.setter
    def width(self, width):
        '''Set the width (float).
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
