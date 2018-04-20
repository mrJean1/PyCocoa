
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

from bases   import _Type1, _Type2
from getters import get_selector, get_selectornameof
from nstypes import int2NS, NSMenu, NSMenuItem, nsOf, NSStr
from oclibs  import NSAlternateKeyMask, NSCommandKeyMask, \
                    NSControlKeyMask, NSShiftKeyMask  # PYCHOK expected
from octypes import SEL_t
from runtime import isInstanceOf
from utils   import _Globals, instanceof, name2pymethod

__all__ = ('Item',
           'Menu', 'MenuBar',
           'Separator',
           'ns2Item')
__version__ = '18.04.18'

_menuItemHandler_name = 'menuItemHandler_'


class Item(_Type2):
    '''Menu item class.
    '''
    _action = _menuItemHandler_name
    _key    = ''
    _mask   = 0
    _sel_   = get_selector(_menuItemHandler_name)

    def __init__(self, title, action=None, key='',
                                           alt=False,
                                           cmd=True,
                                          ctrl=False,
                                         shift=False):
        '''New menu item with action and optional shortcut key.

        @param title: Item title (string).
        @keyword action: Callback, the delegate method to be called
                         (string ending with ':' or _', C{SEL_t} or None).
        @keyword key: The shortcut key, if any (string).
        @keyword alt: Key modifier (bool).
        @keyword cmd: Key modifier (bool).
        @keyword cntl: Key modifier (bool).
        @keyword shift: Key modifier (bool).

        @note: A None I{action} is set to the I{title} with spaces
               removed, etc. see C{title2action}.
        '''
        self.title = title

        if action is None:
            a = self.title2action(self.title)
            # self._sel_ = get_selector(a)
        elif instanceof(action, SEL_t):  # or isInstanceOf(sel, NSSelector)
            self._sel_ = action
            a = name2pymethod(get_selectornameof(action))
        else:
            a = name2pymethod(action)
            if a[-1:] not in ':_':
                raise ValueError('%s invalid: %r' % ('action', action))
            # self._sel_ = get_selector(a)
        self._action = a

        # <http://developer.apple.com/documentation/appkit/
        #       nsmenuitem/1514858-initwithtitle>
        self.NS = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                                     NSStr(self.title), self._sel_, NSStr(key))
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

#     def _dup(self, item):
#         '''Duplicate an item.
#         '''
#         if isinstance(item, Item):
#             self.title   = item.title
#             self._action = item._action
#             self._key    = item._key
#             self._mask   = item._mask
#             self._sel_   = item._sel_
#             self._NS     = item.NS
#
#         elif isInstanceOf(item, NSMenuItem, name='item'):
#             self.title   = nsString2str(item.title())
#             self._action = get_selectornameof(item.action())
#             self._key    = nsString2str(item.keyEquivalent())
#             self._mask   = item.keyEquivalentModifierMask()
#             self._NS     = item
#             self._sel_   = item.action()

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

    def title2action(self, title):
        '''Convert item title to the action/method name.
        '''
        t = title.strip().rstrip('.')
        return 'menu' + ''.join(t.split()) + '_'


class Menu(_Type2):
    '''New menu, item and separator.
    '''
    _items = []

    def __init__(self, title=''):
        self._items = []
        self.NS = NSMenu.alloc().init()
        if title:
            self.title = title

    def __len__(self):
        return len(self._items)  # self.NS.numberOfItems()

    def append(self, *items):
        '''Add one or more items or separators.
        '''
        for item in items:
            instanceof(item, Item, Separator, name='item')
            self.NS.addItem_(nsOf(item))

#   def click(self):
#       self.NS.performActionForItemAtIndex_(...)

    def item(self, title, action=None, key='', alt  =False,
                                               cmd  =True,
                                               ctrl =False,
                                               shift=False):
        '''New menu item with action and optional shortcut key.

        A None I{action} is set to the I{title} with spaces
        removed and lowercase first letter.

        The I{action} is a string, usually the delegate method or
        C{SEL} to be called.  The I{action} string must end with
        ':' or '_'.
        '''
        return Item(title, action=action, key=key, alt=alt,
                           cmd=cmd, ctrl=ctrl, shift=shift)

    def items(self, separators=False):
        '''Yield this menu's items (L{Item}).

           @keyword separators: Yield or skip separator items (bool).
        '''
        if separators:
            for item in self._items:
                yield item
        else:
            for item in self._items:
                if not isinstance(item, Separator):
                    yield item

    def separator(self):
        '''A menu items separator.
        '''
        return Separator()


# <http://developer.apple.com/library/content/qa/qa1420/_index.html
#      #//apple_ref/doc/uid/DTS10004127>
class MenuBar(_Type2):
    '''New menu bar of sub-menus.
    '''
    _menus = []

    def __init__(self, app=None):
        self._menus = []
        self.NS = NSMenu.alloc().init()
        if app:
            self.app = app
            # self.main(app)  # trashes menu bar

    def __len__(self):
        return len(self._menus)  # self.NS.numberOfItems()

    def append(self, *menus):
        '''Add one or more sub-menus.
        '''
        for menu in menus:
            instanceof(menu, Menu, name='menu')
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
        '''
        if app:
            self.app = app
        self.app.NS.setMainMenu_(self.NS)

    def menus(self):
        '''Yield this menu bar's menus (L{Menu}).
        '''
        for menu in self._menus:
            yield menu


class Separator(_Type1):
    '''Menu items separator class.
    '''
    def __init__(self, **attrs):
        '''New menu items separator.
        '''
        self.NS = NSMenuItem.separatorItem()  # can't be singleton
        if attrs:
            super(Separator, self).__init__(**attrs)


def ns2Item(ns):
    '''Get the L{Item} instance for an C{NSMenuItem}.
    '''
    if isInstanceOf(ns, NSMenuItem, name='ns'):
        return _Globals.Items[ns.representedObject()]


if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)
