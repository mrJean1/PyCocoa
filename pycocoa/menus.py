
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Types L{Item}, L{Menu}, L{MenuBar} and L{Separator}, wrapping ObjC L{NSMenuItem} and L{NSMenu}.
'''
# all imports listed explicitly to help PyChecker
from bases   import _Type1, _Type2
from getters import get_selector, get_selectornameof
from nstypes import NSMenu, NSMenuItem, nsOf, NSStr
from pytypes import int2NS
from octypes import SEL_t
from oslibs  import NSAlternateKeyMask, NSCommandKeyMask, \
                    NSControlKeyMask, NSShiftKeyMask  # PYCHOK expected
from runtime import isInstanceOf
from utils   import _Globals, isinstanceOf, name2pymethod, _Types

__all__ = ('Item',
           'Menu', 'MenuBar',
           'Separator',
           'ns2Item',
           'title2action')
__version__ = '18.06.28'

_menuItemHandler_name = 'menuItemHandler_'


class Item(_Type2):
    '''Python menu C{Item} Type, wrapping ObjC L{NSMenuItem}.
    '''
    _action = _menuItemHandler_name
    _key    = ''
    _mask   = 0
    _SEL_   = get_selector(_menuItemHandler_name)

    def __init__(self, title, action=None, key='',
                                           alt=False,
                                           cmd=True,
                                          ctrl=False,
                                         shift=False):
        '''New menu L{Item}.

           @param title: Item title (C{str}).
           @keyword action: Callback, the method to be called (C{str
                            ending with ':' or _'}, C{SEL_t} or C{None}).
           @keyword key: The shortcut key, if any (C{str}).
           @keyword alt: Hold C{option} or C{alt} with I{key} (bool).
           @keyword cmd: Hold C{command} with I{key} (bool).
           @keyword cntl: Hold C{control} with I{key} (bool).
           @keyword shift: Hold C{shift} with I{key} (bool).

           @raise ValueError: Invalid I{title} for C{None} I{action}.

           @note: A C{None} I{action} is set to the I{title}, spaces and
                  dots removed, etc., see function L{title2action}.
        '''
        self.title = title

        if action is None:
            a = title2action(self.title)
            # self._SEL_ = get_selector(a)
        elif isinstanceOf(action, SEL_t):  # or isInstanceOf(sel, NSSelector)
            self._SEL_ = action
            a = name2pymethod(get_selectornameof(action))
        else:
            a = name2pymethod(action)
            if a[-1:] not in ':_':
                raise ValueError('%s invalid: %r' % ('action', action))
            # self._SEL_ = get_selector(a)
        self._action = a

        # <http://Developer.Apple.com//documentation/appkit/
        #       nsmenuitem/1514858-initwithtitle>
        self.NS = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                             NSStr(self.title), self._SEL_, NSStr(key or ''))
        if key:
            mask = 0
            if alt:
                mask |= NSAlternateKeyMask
            if cmd:
                mask |= NSCommandKeyMask
            if ctrl:
                mask |= NSControlKeyMask
            if shift:
                mask |= NSShiftKeyMask  # NSAlphaShiftKeyMask
            if mask:
                self.NS.setKeyEquivalentModifierMask_(mask)
            self._mask = mask
            self._key = key

        r = int2NS(id(self))
        _Globals.Items[r] = self
        self.NS.setRepresentedObject_(r)

    def __str__(self):
        k = '+'.join([m for m in ('Alt', 'Cmd', 'Ctrl', 'Shift')
                              if getattr(self, m.lower())] +
                     [self.key.upper()])
        return '%s(%r, %r, %s)' % (self.__class__.__name__,
                                   self.title, self.action, k)

#   def copy(self, other):
#       '''Duplicate an item.
#       '''
#       if isinstance(other, Item):
#           self.title   = other.title
#           self._action = other._action
#           self._key    = other._key
#           self._mask   = other._mask
#           self._NS     = other.NS
#           self._SEL_   = other._SEL_
#
#       elif isInstanceOf(other, NSMenuItem, name='other'):
#           self.title   = nsString2str(other.title())
#           self._action = get_selectornameof(other.action())
#           self._key    = nsString2str(other.keyEquivalent())
#           self._mask   = other.keyEquivalentModifierMask()
#           self._NS     = other
#           self._SEL_   = other.action()

    @property
    def action(self):
        return self._action

    @property
    def alt(self):
        return bool(self._mask & NSAlternateKeyMask)

    @property
    def cmd(self):
        return bool(self._mask & NSCommandKeyMask)

    @property
    def ctrl(self):
        return bool(self._mask & NSControlKeyMask)

    @property
    def key(self):
        return self._key

    @property
    def shift(self):
        return bool(self._mask & NSShiftKeyMask)


class Menu(_Type2):
    '''Menu Python Type, wrapping ObjC L{NSMenu}.
    '''
    _items = []

    def __init__(self, title=''):
        '''New L{Menu}.

           @keyword title: The menu title (C{str}).
        '''
        self._items = []
        self.NS = NSMenu.alloc().init()
        self.title = title

    def __len__(self):
        return len(self._items)  # self.NS.numberOfItems()

    def append(self, *items):
        '''Add one or more items or separators to this menu.

           @param items: The items to add (L{Item} or L{Separator}).
        '''
        for item in items:
            isinstanceOf(item, Item, Separator, name='item')
            self.NS.addItem_(nsOf(item))

#   def click(self):
#       self.NS.performActionForItemAtIndex_(...)

    def item(self, title, action=None, **kwds):
        '''New menu item with action and optional shortcut key.

           @param title: Item title (C{str}).
           @keyword action: See L{Item}C{.__init__}.
           @keyword kwds: See L{Item}C{.__init__}.

           @return: New item (L{Item}).
        '''
        return Item(title, action=action, **kwds)

    def items(self, separators=False):
        '''Yield each of the items in this menu (L{Item}).

           @keyword separators: Yield or skip L{Separator} items (C{bool}).
        '''
        if separators:
            for item in self._items:
                yield item
        else:
            for item in self._items:
                if not isinstance(item, Separator):
                    yield item

    def separator(self):
        '''New menu separator.

           @return: New item (L{Separator}).
        '''
        return Separator()


# <http://Developer.Apple.com//library/content/qa/qa1420/_index.html
#      #//apple_ref/doc/uid/DTS10004127>
class MenuBar(_Type2):
    '''Python C{MenuBar} Type, wrapping ObjC L{NSMenu}.
    '''
    _menus = []

    def __init__(self, app=None):
        '''New L{MenuBar}.

           @keyword app: The application (L{App} or C{None}).

           @raise TypeError: If I{app} not an L{App}.

           @see: Method L{MenuBar}C{.main}.
        '''
        self._menus = []
        self.NS = NSMenu.alloc().init()
        if app:
            self.app = app
            self._title = app.title
            # self.main(app)  # trashes menu bar

    def __len__(self):
        '''Return the number of menus in this menu bar.
        '''
        return len(self._menus)  # self.NS.numberOfItems()

    def append(self, *menus):
        '''Add one or more sub-menus to this menu bar.

           @param menus: The menus to add (L{Menu}).
        '''
        for menu in menus:
            isinstanceOf(menu, Menu, name='menu')
            self._menus.append(menu)

            # ns = NSMenuItem.alloc().init(); ns.setTitle(NSStr(menu.title))
            ns = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                                    NSStr(menu.title), 0, NSStr(''))
            ns.setSubmenu_(menu.NS)
            self.NS.addItem_(ns)

    @property
    def height(self):
        '''Get this menu bar's height (float).
        '''
        return self.NS.menuBarHeight()

    def main(self, app=None):
        '''Make this menu bar the app's main menu.

           @keyword app: The application (L{App} or C{None}).

           @raise TypeError: If I{app} not an L{App}.

           @raise ValueError: If I{app} missing.
        '''
        if app:
            self.app = app
            self._title = app.title
        if not self.app:
            raise ValueError('%s invalid: %s' % ('app', 'missing'))
        self.app.NS.setMainMenu_(self.NS)

    def menus(self):
        '''Yield each menu of this menu bar (L{Menu}).
        '''
        for menu in self._menus:
            yield menu


class Separator(_Type1):
    '''Python menu C{Separator} Type, wrapping ObjC C{NSMenuItem.separatorItem}.
    '''
    def __init__(self):
        '''New L{Separator}.

           @keyword kws: Optional, additional keyword arguments.
        '''
        self.NS = NSMenuItem.separatorItem()  # XXX can't be singleton


def ns2Item(ns):
    '''Get the L{Item} instance for an L{NSMenuItem}.

       @param ns: The ObjC instance (L{NSMenuItem}).

       @return: The item instance (L{Item}).

       @raise TypeError: Invalid I{ns} type.
    '''
    if isInstanceOf(ns, NSMenuItem, name='ns'):
        return _Globals.Items[ns.representedObject()]


def title2action(title):
    '''Convert a menu item title to a valid callback method name.

       @param title: The item's title (C{str}).

       @return: Name for the callback method (C{str}).

       @raise ValueError: Invalid method name for this I{title}.
    '''
    t = title.strip().rstrip('.')
    return name2pymethod('menu' + ''.join(t.split()) + '_')


_Types.Item      = Item
_Types.Menu      = Menu
_Types.MenuBar   = MenuBar
_Types.Separator = Separator

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
