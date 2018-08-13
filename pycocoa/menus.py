
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Types L{Item}, L{ItemSeparator}, L{Menu} and L{MenuBar}, wrapping ObjC C{NSMenuItem} and C{NSMenu}.
'''
# all imports listed explicitly to help PyChecker
from bases   import _Type2
from fonts   import Font
from getters import get_selector, get_selectornameof
from nstypes import NSMenu, NSMenuItem, nsOf, NSStr, nsString2str
from pytypes import int2NS
from octypes import SEL_t
from oslibs  import NO, NSAlternateKeyMask, NSCommandKeyMask, \
                    NSControlKeyMask, NSShiftKeyMask, YES  # PYCHOK expected
from runtime import isObjCInstanceOf, ObjCInstance
from utils   import bytes2str, _ByteStrs, _Globals, _Ints, isinstanceOf, \
                    missing, name2pymethod, printf, property2, _Types

from inspect import isfunction, ismethod
try:
    from inspect import getfullargspec as getargspec  # Python 3+
except ImportError:
    from inspect import getargspec  # Python 2

__all__ = ('Item', 'ItemSeparator',
           'Menu', 'MenuBar',
           'ns2Item',
           'title2action')
__version__ = '18.08.09'

# Method _NSApplicationDelegate.handleMenuItem_ in .apps.py
# is the handler ('selector') for all menu items specified
# with action as a string or None.  Method -.callMenuItem_
# ('selector') handles items with Python-callable actions.
# Both selectors are defined in .apps._NSApplicationDelegate,
# which is the default 'target' for ObjC menu item (unless
# a different target is set for the item).
_callMenuItem_name  = 'callMenuItem_'
_CALL_ = get_selector(_callMenuItem_name)

_handleMenuItem_name  = 'handleMenuItem_'
_HANDLE_ = get_selector(_handleMenuItem_name)

# keyEquivalentModifierMask: name and mask
_Modifiers2 = (('Alt',   NSAlternateKeyMask),
               ('Cmd',   NSCommandKeyMask),
               ('Ctrl',  NSControlKeyMask),
               ('Shift', NSShiftKeyMask))  # or NSAlphaShiftKeyMask?


def _finder(inst, title, action, dflt, items, kind):
    '''(INTERNAL) Handle menu.item, menuBar.menu lookup.
    '''
    if title:
        t = bytes2str(title)
        for item in items:
            if item.title.startswith(t):
                return item
    elif action:
        a = bytes2str(action)
        for item in items:
            if item.action.startswith(a):
                return item
    if dflt is missing:
        raise ValueError('no such %s.%s: %r' % (inst, kind, title or action))
    return dflt


def _indexer(inst, index, items, bytitle):
    '''(INTERNAL) Handle menu[], menuBar[] indexing.
    '''
    try:
        if isinstance(index, _Ints):
            if 0 <= index < len(items):
                return items[index]
        elif isinstance(index, slice):
            return [items[i] for i in range(*index.indices(len(items)))]
        elif isinstance(index, _ByteStrs):
            i = bytitle(title=index, dflt=None)
            if i:
                return i
    except (IndexError, TypeError, ValueError):
        pass
    raise IndexError('no such %s index [%r]' % (inst, index))


class _Item_Type2(_Type2):
    '''(INTERNAL) Base class for L{Item} and L{ItemSeparator}.
    '''
    _isSeparator = False

    @property
    def nsMenu(self):
        '''Get the I{menu} owning this item (C{NSMenu}) or C{None}.
        '''
        return self.NS.menu()

    @nsMenu.setter  # PYCHOK property.setter
    def nsMenu(self, ns_menu):
        '''Set the I{menu} owning this item (C{NSMenu} or L{Menu}).
        '''
        if isinstanceOf(ns_menu, Menu):
            ns_menu = ns_menu.NS  # PYCHOK getattr(self, 'NS')...
        if ns_menu:
            self.NS.setMenu_(ns_menu)

    @property
    def isSeparator(self):
        '''Is this a menu item (C{False}) or a menu item separator (C{True})?.
        '''
        return self._isSeparator  # isinstance(self, ItemSeparator)


class Item(_Item_Type2):
    '''Python menu C{Item} Type, wrapping ObjC C{NSMenuItem}.
    '''
    _action  = _handleMenuItem_name
    _mask    = 0
    _SEL_    = _HANDLE_
    _subMenu = None  # see also Item.hasSubmenu

    def __init__(self, title, action=None, key='',  # MCCABE 13
                                           alt=False,
                                           cmd=True,  # default
                                          ctrl=False,
                                         shift=False, **props):
        '''New menu L{Item}.

           @param title: Item title (C{str}).
           @keyword action: Callback method (C{str ending with ':' or _'},
                            C{callable} or C{SEL_t}) or C{None}, see note.
           @keyword key: The shortcut key, if any (C{str} or C{bytes}).
           @keyword alt: Hold C{alt} or C{option} down with I{key} (bool).
           @keyword cmd: Hold C{command} down with I{key} (bool).
           @keyword cntl: Hold C{control} down with I{key} (bool).
           @keyword shift: Hold C{shift} down with I{key} (bool).
           @keyword props: Optional, settable L{Item} I{property=value} pairs.

           @raise TypeError: Callable I{action} not a method or function.

           @raise ValueError: Invalid I{action} or I{title} for
                              C{None} I{action}.

           @note: A C{None} I{action} is set to the I{menu.<title>} with
                  spaces and dots removed, see function L{title2action}.
                  A callable I{action} must be a (bound) Python method
                  with signature C{(self, item, ...)} or a Python
                  function with signature C{(item, ...)}.
        '''
        self.title = title

        # XXX allow action to be any callable
        if action is None:
            a = title2action(self.title)
        elif callable(action):
            a = action  # bound method(self, item) or function(item)
            if not ((ismethod(a)   and len(getargspec(a).args) > 1) or
                    (isfunction(a) and len(getargspec(a).args) > 0)):
                raise TypeError('invalid %s: %r' % ('action', action))
            self._SEL_ = _CALL_
        elif isinstanceOf(action, SEL_t):  # or isObjCInstanceOf(sel, NSSelector)
            self._SEL_ = action
            a = name2pymethod(get_selectornameof(action))
        else:  # str or bytes
            a = name2pymethod(action)
            if a[-1:] not in ':_':
                raise ValueError('invalid %s: %r' % ('action', action))
        self._action = a

        # <http://Developer.Apple.com/documentation/appkit/
        #       nsmenuitem/1514858-initwithtitle>
        self.NS = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                             NSStr(self.title), self._SEL_, NSStr(key or ''))
        if key:  # allow capitalized Modifiers
            self._keyModifiers(Alt=alt, Cmd=cmd, Ctrl=ctrl, Shift=shift)
            if props:
                props = self._keyModifiers(**props)

        # self.NS.setEnabled_(YES) or self.isEnabled = True, is default
        for p, v in props.items():
            try:  # get property setter
                g, s = property2(self, p)
                if s and callable(s):
                    s(self, v)
                else:
                    g = 'non-settable' if g else 'invalid'
                    raise NameError('%s %s property: %r' % (g,
                                        self.__class__.__name__, p))
            except Exception as x:
                if _Globals.raiser:
                    x = x.__class__.__name__
                    printf('%s: %s(title=%r, ..., %s=%r) ...', x,
                                self.__class__.__name__, self.title, p, v)
                    raise

        r = int2NS(id(self))  # XXX use item.tag?
        _Globals.Items[r] = self
        self.NS.setRepresentedObject_(r)

    def __str__(self):
        k = '+'.join([M for M, ns in _Modifiers2 if (self._mask & ns)]
                   + [self.key.upper()])
        return '%s(%r, %r, %s)' % (self.__class__.__name__,
                                   self.title, self.action, k)

#   def copy(self, other):
#       '''Duplicate an item.
#       '''
#       if isinstance(other, Item):
#           self.title   = other.title
#           self._action = other._action
#           self.key     = other.key
#           self._mask   = other._mask
#           self._NS     = other.NS
#           self._SEL_   = other._SEL_
#
#       elif isObjCInstanceOf(other, NSMenuItem, name='other'):
#           self.title   = nsString2str(other.title())
#           self._action = get_selectornameof(other.action())
#           self.key     = nsString2str(other.keyEquivalent())
#           self._mask   = other.keyEquivalentModifierMask()
#           self._NS     = other
#           self._SEL_   = other.action()

    @property
    def action(self):
        '''Get the I{action} name (C{str}).
        '''
        return self._action

    @property
    def allowsKeyWhenHidden(self):
        '''Get the item's I{allows} property (C{bool}).
        '''
        return bool(self.NS.allowsKeyEquivalentWhenHidden())

    @allowsKeyWhenHidden.setter  # PYCHOK property.setter
    def allowsKeyWhenHidden(self, allows):
        '''Set the item's I{allows} property (C{bool}).
        '''
        b = bool(allows)
        if b != self.allowsKeyWhenHidden:
            self.NS.setAllowsKeyEquivalentWhenHidden_(YES if b else NO)

    @property
    def alt(self):
        '''Get the I{alt} or I{option} key modifier (C{bool}).
        '''
        return bool(self._mask & NSAlternateKeyMask)

    @property
    def cmd(self):
        '''Get the I{command} key modifier (C{bool}).
        '''
        return bool(self._mask & NSCommandKeyMask)

    @property
    def ctrl(self):
        '''Get the I{control} key modifier (C{bool}).
        '''
        return bool(self._mask & NSControlKeyMask)

    @property
    def font(self):
        '''Get the item's I{font} (L{Font}) or C{None}.
        '''
        ns = self.NS.font()
        return Font(ns) if ns else None

    @font.setter  # PYCHOK property.setter
    def font(self, font):
        '''Set the item's I{font} (L{Font}).
        '''
        if isinstanceOf(font, Font, name='font') and font != self.font:
            self.NS.setFont_(font.NS)

    @property
    def hasSubmenu(self):
        '''Has this item's a I{submenu} (C{bool}).
        '''
        return True if self.NS.hasSubmenu() else False

#   @property
#   def image(self):
#       '''Get the item's I{image} (L{Image}).
#       '''
#       return Image(self.NS.image())

#   @image.setter  # PYCHOK property.setter
#   def image(self, image):
#       '''Set the item's I{image} (L{Image}).
#       '''
#       if isinstanceOf(image, Image, name='image') and image != self.image:
#           self.NS.setImage_(image.NS)

    @property
    def indentationLevel(self):
        '''Get the item's I{indentation} (C{int}).
        '''
        return int(self.NS.indentationLevel())

    @indentationLevel.setter  # PYCHOK property.setter
    def indentationLevel(self, indent):
        '''Set the item's I{indentation} (C{int}).
        '''
        if isinstanceOf(indent, _Ints, name='indent') and indent != self.indentationLevel:
            if not 0 <= indent < 16:
                raise ValueError('%s: %r' % ('indent', indent))
            self.NS.setIndentationLevel_(indent)

    @property
    def isAlternate(self):
        '''Get the item's I{Altenate} property (C{bool}).
        '''
        return bool(self.NS.isAlternate())

    @isAlternate.setter  # PYCHOK property.setter
    def isAlternate(self, alternate):
        '''Set the item's I{Altenate} property (C{bool}).
        '''
        b = bool(alternate)
        if b != self.isAlternate:
            self.NS.setAlternate_(YES if b else NO)

    @property
    def isEnabled(self):
        '''Get the item's I{Enabled} property (C{bool}).
        '''
        return bool(self.NS.isEnabled())

    @isEnabled.setter  # PYCHOK property.setter
    def isEnabled(self, enable):
        '''Set the item's I{Enabled} property (C{bool}).
        '''
        b = bool(enable)
        if b != self.isEnabled:
            self.NS.setEnabled_(YES if b else NO)

    @property
    def isHidden(self):
        '''Get the item's I{Hidden} property (C{bool}).
        '''
        return bool(self.NS.isHidden())

    @isHidden.setter  # PYCHOK property.setter
    def isHidden(self, hidden):
        '''Set the item's I{Hidden} property (C{bool}).
        '''
        b = bool(hidden)
        if b != self.isHidden:
            self.NS.setHidden_(YES if b else NO)

    @property
    def isHighlighted(self):
        '''Get the item's I{Highlighted} property (C{bool}).
        '''
        return bool(self.NS.isHighlighted())

    @property
    def key(self):
        '''Get the item's shortcut key (C{str}).
        '''
        return nsString2str(self.NS.keyEquivalent())

    keyEquivalent = key

    @key.setter  # PYCHOK property.setter
    def key(self, key):
        '''Set the item's shortcut key (C{str}).
        '''
        if isinstanceOf(key, _ByteStrs, name='key') and key != self.key:
            self.NS.setKeyEquivalent_(NSStr(key))

    @property
    def keyModifiers(self):
        '''Get the item's shortcut key modifiers (C{dict}).
        '''
        return dict((M.lower(), bool(self._mask & ns)) for M, ns in _Modifiers2)

    keyEquivalentModifiers = keyModifiers

    @keyModifiers.setter  # PYCHOK property.setter
    def keyModifiers(self, modifiers):
        '''Get/set the item's shortcut key modifiers (C{dict}).

           @keyword alt: Hold C{alt} or C{option} down with I{key} (bool).
           @keyword cmd: Hold C{command} down with I{key} (bool).
           @keyword cntl: Hold C{control} down with I{key} (bool).
           @keyword shift: Hold C{shift} down with I{key} (bool).
           @keyword modifiers: Optional, additional I{modifier=}C{bool} pairs.

           @return: Previous modifiers (C{dict}).

           @raise KeyError: Invalid I{modifiers}.
        '''
        m = self._mask
        d = self._keyModifiers(**modifiers)
        if d:
            self._mask = m  # restore
            raise KeyError(', '.join('%s=%r' % t for t in sorted(d.items())))

    def _keyModifiers(self, **kwds):
        '''(INTERNAL) Set the item's shortcut key modifiers.
        '''
        mask = self._mask
        for M, ns in _Modifiers2:
            m = kwds.pop(M, kwds.pop(M.lower(), missing))
            if m is missing:
                pass
            elif m:  # set mask
                mask |= ns
            elif (mask & ns):  # clear
                mask -= ns

        if mask != self._mask:
            self.NS.setKeyEquivalentModifierMask_(mask)
            self._mask = mask

        return kwds  # return leftover

#   @property
#   def mixedStateImage(self):
#       '''Get the item's mixed-state I{image} (L{Image}).
#       '''
#       return Image(self.NS.mixedStateImage())
#
#   @mixedStateImage.setter  # PYCHOK property.setter
#   def mixedStateImage(self, image):
#       '''Set the item's mixed-state I{image} (L{Image}).
#       '''
#       if isinstanceOf(image, Image, name='image') and image != self.mixedStateImage:
#           self.NS.setMixedStateImage_(image.NS)

#   @property
#   def offStateImage(self):
#       '''Get the item's off-state I{image} (L{Image}).
#       '''
#       return Image(self.NS.offStateImage())
#
#   @offStateImage.setter  # PYCHOK property.setter
#   def offStateImage(self, image):
#       '''Set the item's off-state I{image} (L{Image}).
#       '''
#       if isinstanceOf(image, Image, name='image') and image != self.offStateImage:
#           self.NS.setOffStateImage_(image.NS)

#   @property
#   def onStateImage(self):
#       '''Get the item's on-state I{image} (L{Image}).
#       '''
#       return Image(self.NS.onStateImage())
#
#   @onStateImage.setter  # PYCHOK property.setter
#   def onStateImage(self, image):
#       '''Set the item's on-state I{image} (L{Image}).
#       '''
#       if isinstanceOf(image, Image, name='image') and image != self.onStateImage:
#           self.NS.setOnStateImage_(image.NS)

    @property
    def nsTarget(self):
        '''Get the item's target (C{NS...}) or C{None} for
        the default target, C{_NSApplicationDelegate}.
        '''
        return self.NS.target()

    @nsTarget.setter  # PYCHOK property.setter
    def nsTarget(self, ns_target):
        '''Set the item's I{target} (C{NS...}).
        '''
        if isinstanceOf(ns_target, ObjCInstance, name='ns_target'):
            self.NS.setTarget_(ns_target.NS)

    @property
    def parent(self):
        '''Get a I{submenu} item's parent item (L{Item}) or C{None}.
        '''
        ns = self.NS.parentItem()
        return ns2Item(ns) if ns else None

    @property
    def shift(self):
        '''Get the I{shift} key modifier (C{bool}).
        '''
        return bool(self._mask & NSShiftKeyMask)

    @property
    def state(self):
        '''Get the item's I{state} (C{int}).
        '''
        return int(self.NS.state())

    @state.setter  # PYCHOK property.setter
    def state(self, state):
        '''Set the item's I{state} (C{int}).
        '''
        if isinstanceOf(state, _Ints, name='state') and state != self.state:
            self.NS.setState_(state)

    @property
    def subMenu(self):
        '''Get the item's I{submenu} (C{Menu}) or C{None}.
        '''
        return self._subMenu

    @subMenu.setter  # PYCHOK property.setter
    def subMenu(self, submenu):
        '''Set the item's I{submenu} (L{Menu}).
        '''
        if isinstanceOf(submenu, Menu, name='submenu') and submenu != self.subMenu:
            self.NS.setSubmenu_(submenu.NS)
            self._subMenu = submenu

    @property
    def toolTip(self):
        '''Get the item's I{toolTip} (C{str}) or C{''}.
        '''
        ns = self.NS.toolTip()
        return nsString2str(ns) if ns else ''

    @toolTip.setter  # PYCHOK property.setter
    def toolTip(self, tip):
        '''Set the item's I{toolTip} (C{str}).
        '''
        if isinstanceOf(tip, _ByteStrs, name='tip') and tip != self.toolTip:
            self.NS.setToolTip_(NSStr(tip))


class ItemSeparator(_Item_Type2):
    '''Python menu C{ItemSeparator} Type, wrapping ObjC C{NSMenuItem.separatorItem}.
    '''
    _isSeparator = True

    def __init__(self):
        '''New L{ItemSeparator}.
        '''
        self.NS = NSMenuItem.separatorItem()  # XXX can't be singleton


class Menu(_Type2):
    '''Python L{Menu} Type, wrapping ObjC C{NSMenu}.
    '''
    _items = []

    def __init__(self, title):
        '''New L{Menu}.

           @param title: The menu title (C{str}).
        '''
        self._items = []
        self.NS = NSMenu.alloc().init()
        self.title = title  # sets self.NS...Title_

    def __len__(self):
        return len(self._items)  # self.NS.numberOfItems()

    def append(self, *items):
        '''Add one or more items or separators to this menu.

           @param items: The items (L{Item} or L{ItemSeparator}) to add.
        '''
        for item in items:
            if isinstanceOf(item, Item, ItemSeparator, name='item'):
                self._items.append(item)
                item.tag = len(self._items)  # default .tag
                self.NS.addItem_(nsOf(item))

#   def click(self):
#       self.NS.performActionForItemAtIndex_(...)

    def __getitem__(self, index):
        '''Yield an or several items by index, by slice or by title.

           @param index: Index (C{int}, C{str} or C{slice}).

           @return: Each item (L{Item} or L{ItemSeparator}).

           @raise IndexError: If I{index} out of range or if no item
                              titled I{index} exists.
        '''
        return _indexer(self, index, self._items, self.item)

    def item(self, title='', action='', dflt=missing):
        '''Find an item by title or by action.

           @keyword title: Item title to match (C{str}).
           @keyword action: Item action to match (C{str}).
           @keyword dflt: Optional, default return value.

           @return: The first matching item (L{Item}) or I{dflt}
                    if no I{title} or I{action} match found.

           @raise ValueError: No I{dflt} provided and no I{title} or
                              I{action} match.
        '''
        return _finder(self, title, action, dflt, self.items(), 'item')

    def items(self, separators=False):
        '''Yield the items in this menu.

           @keyword separators: Yield L{ItemSeparator}s (C{bool}),
                                skip otherwise.

           @return: Each L{Item} or L{ItemSeparator}.
        '''
        y = bool(separators)
        for item in self._items:
            if y or not item.isSeparator:
                yield item


# <http://Developer.Apple.com/library/content/qa/qa1420/_index.html
#      #//apple_ref/doc/uid/DTS10004127>
class MenuBar(_Type2):
    '''Python L{MenuBar} Type, wrapping ObjC C{NSMenu}.
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
        if app:  # type checked in app.setter
            self.app = app
            # XXX do not change self.NS...Title
            self._title = app.title
            # self.main(app)  # XXX trashes menu bar

    def __len__(self):
        '''Return the number of menus in this menu bar (C{int}).
        '''
        return len(self._menus)  # self.NS.numberOfItems()

    def append(self, *menus):
        '''Add one or more sub-menus to this menu bar.

           @param menus: The menus to add (L{Menu}).
        '''
        for menu in menus:
            isinstanceOf(menu, Menu, name='menu')
            self._menus.append(menu)
            menu.tag = len(self._menus)  # default .tag
            # ns = NSMenuItem.alloc().init(); ns.setTitle(NSStr(menu.title))
            ns = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                                    NSStr(menu.title), 0, NSStr(''))
            ns.setSubmenu_(menu.NS)
            self.NS.addItem_(ns)

    def __getitem__(self, index):
        '''Yield one or several menus by index, by slice or by title.

           @param index: Index (C{int}, C{str} or C{slice}).

           @return: Each menu (L{Menu}).

           @raise IndexError: If I{index} out of range or if no menu
                              titled I{index} exists.
        '''
        return _indexer(self, index, self._menus, self.menu)

    @property
    def height(self):
        '''Get this menu bar's height (C{float}).
        '''
        return self.NS.menuBarHeight()

    def main(self, app=None):
        '''Make this menu bar the app's main menu.

           @keyword app: The application (L{App} or C{None}).

           @raise TypeError: If I{app} not an L{App}.

           @raise ValueError: If I{app} missing.
        '''
        # type checked in app.setter
        self.app = app or _Globals.App
        if self.app:
            if not self.title:
                # XXX do not change self.NS...Title
                self._title = self.app.title
            self.app.NS.setMainMenu_(self.NS)

    def menu(self, title='', dflt=None):
        '''Find a menu by title.

           @keyword title: The menu title to match (C{str}).
           @keyword dflt: Optional, default return value.

           @return: The first matching menu (L{Menu}) or I{dflt}
                    if no I{title} match found.

           @raise ValueError: No I{dflt} provided and no I{title} match.
        '''
        return _finder(self, title, '', dflt, self.menus(), 'menu')

    def menus(self):
        '''Yield the menus of this menu bar.

           @return: Each menu (L{Menu}).
        '''
        for menu in self._menus:
            yield menu


def ns2Item(ns):
    '''Get the L{Item} instance for an C{NSMenuItem}.

       @param ns: The ObjC instance (C{NSMenuItem}).

       @return: The item instance (L{Item}).

       @raise TypeError: Invalid I{ns} type.
    '''
    if isObjCInstanceOf(ns, NSMenuItem, name='ns'):
        return _Globals.Items[ns.representedObject()]


def title2action(title):
    '''Convert a menu item title to a valid callback method name.

       @param title: The item's title (C{str}).

       @return: Name for the callback method (C{str}).

       @raise ValueError: Invalid method name for this I{title}.
    '''
    t = title.rstrip().rstrip('.').strip()
    return name2pymethod('menu' + ''.join(t.split()) + '_')


_Types.Item          = Item
_Types.ItemSeparator = ItemSeparator
_Types.Menu          = Menu
_Types.MenuBar       = MenuBar

if __name__ == '__main__':

    from utils import _allisting, properties

    _allisting(__all__, locals(), __version__, __file__)

    i = Item('Quit', 'menuTerminate_', key='q')
    print('\n%s properties:' % (i,))
    for p, v in sorted(properties(i).items()):
        print('  %s = %r' % (p, v))

    _ = '''

 menus.__all__ = tuple(
   menus.Item is <class .Item>,
   menus.ItemSeparator is <class .ItemSeparator>,
   menus.Menu is <class .Menu>,
   menus.MenuBar is <class .MenuBar>,
   menus.ns2Item is <function .ns2Item at 0x10713f5f0>,
   menus.title2action is <function .title2action at 0x107142f50>,
 )[6]
 menus.__version__ = '18.08.09'

Item('Quit', 'menuTerminate_', Cmd+Q) properties:
  NS = <ObjCInstance(NSMenuItem(<Id_t at 0x1040e4b90>) of 0x7fce19450af0) at 0x1040fee90>
  NSDelegate = 'AttributeError("use \'NSdelegate\' not \'NSD-\'",)'
  NSdelegate = 'AttributeError("no \'delegate\' [class]method or property: NSMenuItem(<Id_t at 0x1040e4b90>) of 0x7fce19450af0",)'
  action = 'menuTerminate_'
  allowsKeyWhenHidden = False
  alt = False
  app = None
  cmd = True
  ctrl = False
  font = None
  hasSubmenu = False
  indentationLevel = 0
  isAlternate = False
  isEnabled = True
  isHidden = False
  isHighlighted = False
  isSeparator = False
  key = 'q'
  keyEquivalent = 'q'
  keyEquivalentModifiers = {'shift': False, 'alt': False, 'cmd': True, 'ctrl': False}
  keyModifiers = {'shift': False, 'alt': False, 'cmd': True, 'ctrl': False}
  nsMenu = None
  nsTarget = None
  parent = None
  shift = False
  state = 0
  subMenu = None
  tag = 0
  title = 'Quit'
  toolTip = ''
'''
    del _

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
