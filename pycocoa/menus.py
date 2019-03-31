
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Types L{Item}, L{ItemSeparator}, L{Menu} and L{MenuBar},
wrapping ObjC C{NSMenuItem} and C{NSMenu} and L{Keys}.

@var Keys: Menu L{Item} shortcut keys (C{chr}).
'''
# all imports listed explicitly to help PyChecker
from bases    import _Type2
from fonts    import Font
from geometry import Size
from getters  import get_selector, get_selectornameof
from nstypes  import isNone, NSMain, NSMenu, NSMenuItem, nsOf, \
                     NSStr, nsString2str
from pytypes  import int2NS
from octypes  import SEL_t
from oslibs   import NO, NSAlternateKeyMask, NSCommandKeyMask, \
                     NSControlKeyMask, NSShiftKeyMask, YES  # PYCHOK expected
from oslibs   import NSAcknowledgeCharacter, NSBackSpaceCharacter, \
                     NSBackTabCharacter, NSBellCharacter, NSCancelCharacter, \
                     NSCarriageReturnCharacter, NSDataLineEscapeCharacter, \
                     NSDeleteCharacter, NSDeviceControl1Character, \
                     NSDeviceControl2Character, NSDeviceControl3Character, \
                     NSDeviceControl4Character, NSEndOfMediumCharacter, \
                     NSEndOfTextCharacter, NSEndOfTransmitCharacter, \
                     NSEndOfTransmitBlockCharacter, NSEnquiryCharacter, \
                     NSEnterCharacter, NSEscapeCharacter, \
                     NSFileSeparatorCharacter, NSFormFeedCharacter, \
                     NSGroupSeparatorCharacter, NSHorizontalTabCharacter, \
                     NSLineFeedCharacter, NSNegativeAcknowledgeCharacter, \
                     NSNewLineCharacter, NSRecordSeparatorCharacter, \
                     NSShiftInCharacter, NSShiftOutCharacter, \
                     NSSpaceCharacter, NSStartOfHeadingCharacter, \
                     NSStartOfTextCharacter, NSSubstituteCharacter, \
                     NSSynchronousIdleCharacter, NSTabCharacter, \
                     NSUnitSeparatorCharacter, NSVerticalTabCharacter
from runtime  import isObjCInstanceOf  # , ObjCInstance
from utils    import bytes2str, _ByteStrs, _Constants, _Globals, \
                     _Ints, isinstanceOf, missing, name2pymethod, \
                     printf, property2, property_RO, _Strs, _Types

try:
    from inspect import getfullargspec as getargspec  # Python 3+
except ImportError:
    from inspect import getargspec  # Python 2
from inspect import isfunction, ismethod
# from types import FunctionType, MethodType

__all__ = ('Item', 'ItemSeparator',
           'Keys',
           'Menu', 'MenuBar',
           'ns2Item',
           'title2action')
__version__ = '18.11.06'

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
_NoKey = NSStr('')


def _bindM(inst, parent):
    '''(INTERNAL) Bind item or menu to parent menu, menu bar or item.
    '''
    # check that the item or menu is not already bound to (a 'child' of)
    # a menu or menu bar (ObjC's properties like hasSubmenu, owner,
    # parent, supermenu, etc. are non-trivial and rather inconsistent)
    # <http://Developer.Apple.com/documentation/appkit/nsmenu/1518204-supermenu>
    # <http://Developer.Apple.com/documentation/appkit/nsmenuitem/1514817-hassubmenu>
    # <http://Developer.Apple.com/documentation/appkit/nsmenuitem/1514845-submenu>
    if inst.parent:
        raise ValueError('%r bound to: %r' % (inst, inst.parent))
    inst._parent = parent


def _modifiedMask2(mask, kwds):
    '''(INTERNAL) Update modifier mask.
    '''
    # kwds = kwds.copy()
    for M, ns in _Modifiers2:
        m = kwds.pop(M, kwds.pop(M.lower(), missing))
        if m is missing:
            if not kwds:
                break
        elif m:  # set mask
            mask |= ns
        elif (mask & ns):  # clear
            mask -= ns
    return mask, kwds  # mask and "leftovers"


def _nsKey2(key):
    '''(INTERNAL) Check a shortcut key.
    '''
    if not key:
        return _NoKey, ''
    k = bytes2str(key, name='key')
    if len(k) == 1 and 32 < ord(k[0]) < 127:  # k.isprintable() and not k.ispace()
        return NSStr(k), k
    u = k.upper()
    for n, v in Keys.items():
        if k in (n, v) or u in (n.upper(), v):
            return NSStr(v), n
    raise ValueError('invalid %s: %r' % ('key', key))


def _nsMenuItem(inst, sel=0, nskey=_NoKey):
    '''(INTERNAL) New menu item or new menu bar menu item.
    '''
    # <http://Developer.Apple.com/documentation/appkit/
    #       nsmenuitem/1514858-initwithtitle>
    ns = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                            NSStr(inst.title), sel, nskey)
    r = int2NS(id(inst))
    _Globals.Items[r] = inst  # see ns2Item() below
    ns.setRepresentedObject_(r)
    return ns


def _setTag(inst, tag, ns=None):
    '''(INTERNAL) Check and set the tag.
    '''
    if isinstanceOf(tag, _Ints, name='tag'):
        if not tag:  # XXX zero tag invalid
            raise ValueError('invalid %s: %r' % ('tag', tag))
        inst._tag = tag
        if ns:
            ns.setTag_(tag)


class _Item_Type2(_Type2):
    '''(INTERNAL) Base class for L{Item} and L{ItemSeparator}.
    '''
    _isSeparator = False
    _parent      = None  # see _Menu_Type2._validM

    @property_RO
    def isSeparator(self):
        '''Is this a menu item (C{False}) or a menu item separator (C{True})?.
        '''
        return self._isSeparator  # isinstance(self, ItemSeparator)

    @property_RO
    def parent(self):
        '''Get the item's I{parent} (L{Menu} or L{MenuBar}) or C{None}.
        '''
        # like self.NS.parentItem() but for all Item, ItemSeparator,
        # Menu and MenuBar types, not only for NSItem like ObjC
        return self._parent  # see _Menu_Type2._validM


class Item(_Item_Type2):
    '''Python menu L{Item} Type, wrapping ObjC C{NSMenuItem}.
    '''
    _action  = _handleMenuItem_name
    _key     = ''
    _mask    = 0  # used in Menu.item below
    _SEL_    = _HANDLE_
    _subMenu = None
    _tag     = 0

    def __init__(self, title, action=None, key='',  # MCCABE 13
                                           alt=False,
                                           cmd=True,  # default
                                          ctrl=False,
                                         shift=False, **props):
        '''New menu L{Item}.

           @param title: The item's title (C{str}).
           @keyword action: Callback name (C{str} ending with ':' or '_'),
                            a Python C{callable}, an ObjC C{selector}
                            (C{SEL_t}) or C{None}, see B{Notes}.
           @keyword key: The shortcut key, if any (C{str}, C{bytes} or a L{Keys}).
           @keyword alt: Hold C{alt} or C{option} key down with I{key} (bool).
           @keyword cmd: Hold C{command} key down with I{key} (bool).
           @keyword cntl: Hold C{control} key down with I{key} (bool).
           @keyword shift: Hold C{shift} key down with I{key} (bool).
           @keyword props: Additional, settable L{Item} I{property=value} pairs.

           @raise TypeError: Invalid I{action} or invalid Python C{callable}
                             I{action} or C{callable} signature, see B{Notes}.

           @raise ValueError: Invalid I{action} or invalid I{title} for
                              C{None} I{action}.

           @note: A C{None} I{action} is set to the method name C{menu<title>_},
                    see function L{title2action}.

           @note: A Python C{callable} I{action} must be a (bound) Python method
                  with signature C{(self, item, ...)} or a Python function with
                  signature C{(item, ...)}.
        '''
        self.title = title

        # XXX allow action to be any callable
        if action is None:
            a = title2action(self.title)
        elif callable(action):
            a = action  # bound method(self, item) or function(item)
            self._SEL_ = _CALL_
        elif isinstanceOf(action, SEL_t):  # or isObjCInstanceOf(sel, NSSelector)
            self._SEL_ = action
            a = name2pymethod(get_selectornameof(action))
        else:  # str or bytes
            a = name2pymethod(action)
            if a[-1:] not in ':_':
                raise ValueError('invalid %s: %r' % ('action', action))
        self.action = a  # double checked in .action.setter below

        ns, key = _nsKey2(key)
        self.NS = _nsMenuItem(self, self._SEL_, ns)
        if key:  # allow capitalized Modifiers
            self._key = key
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
                    g = 'read-only' if g else 'invalid'
                    raise NameError('%s %s property: %s' % (g,
                                        self.__class__.__name__, p))
            except Exception as x:
                if _Globals.raiser:
                    x = x.__class__.__name__
                    printf('%s: %s(title=%r, ..., %s=%r) ...', x,
                                self.__class__.__name__, self.title, p, v)
                    raise

    def __str__(self):
        k = '+'.join([M for M, ns in _Modifiers2 if (self._mask & ns)]
                   + [self.key])
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
        '''Get the item's C{action} (C{str} or Python C{callable}).
        '''
        return self._action

    @action.setter  # PYCHOK property.setter
    def action(self, action):
        '''Set the item's C{action} (C{str} or Python C{callable}), see C{Item.__init__} B{Notes}.
        '''
        # type(action) in (types.FunctionType, types.MethodType ...
        if (isinstanceOf(action, _Strs) or
           (ismethod(action)   and len(getargspec(action).args) > 1) or
           (isfunction(action) and len(getargspec(action).args) > 0)):
            self._action = action
        else:
            raise TypeError('invalid %s: %r' % ('action', action))

    @property
    def allowsKeyWhenHidden(self):
        '''Get the item's C{allowsKeysWhenHidden} property (C{bool}).
        '''
        return bool(self.NS.allowsKeyEquivalentWhenHidden())

    @allowsKeyWhenHidden.setter  # PYCHOK property.setter
    def allowsKeyWhenHidden(self, allows):
        '''Set the item's C{allowsKeysWhenHidden} property (C{bool}).
        '''
        b = bool(allows)
        if b != self.allowsKeyWhenHidden:
            self.NS.setAllowsKeyEquivalentWhenHidden_(YES if b else NO)

    @property_RO
    def alt(self):
        '''Get the C{alt} or C{option} key modifier (C{bool}).
        '''
        return bool(self._mask & NSAlternateKeyMask)

    @property_RO
    def cmd(self):
        '''Get the C{command} key modifier (C{bool}).
        '''
        return bool(self._mask & NSCommandKeyMask)

    @property_RO
    def ctrl(self):
        '''Get the C{control} key modifier (C{bool}).
        '''
        return bool(self._mask & NSControlKeyMask)

    @property
    def font(self):
        '''Get the item's C{font} (L{Font}) or C{None}.
        '''
        ns = self.NS.font()
        return Font(ns) if ns else None

    @font.setter  # PYCHOK property.setter
    def font(self, font):
        '''Set the item's C{font} (L{Font}).
        '''
        if isinstanceOf(font, Font, name='font') and font != self.font:
            self.NS.setFont_(font.NS)

    @property_RO
    def hasSubmenu(self):
        '''Has this item a C{submenu} (C{bool}).
        '''
        return True if self.NS.hasSubmenu() else False

#   @property
#   def image(self):
#       '''Get the item's C{image} (L{Image}).
#       '''
#       return Image(self.NS.image())

#   @image.setter  # PYCHOK property.setter
#   def image(self, image):
#       '''Set the item's C{image} (L{Image}).
#       '''
#       if isinstanceOf(image, Image, name='image') and image != self.image:
#           self.NS.setImage_(image.NS)

    @property
    def indentationLevel(self):
        '''Get the item's C{indentation} (C{int}).
        '''
        return int(self.NS.indentationLevel())

    @indentationLevel.setter  # PYCHOK property.setter
    def indentationLevel(self, indent):
        '''Set the item's C{indentation} (C{int}).
        '''
        if isinstanceOf(indent, _Ints, name='indent') and indent != self.indentationLevel:
            if not 0 <= indent < 16:
                raise ValueError('%s: %r' % ('indent', indent))
            self.NS.setIndentationLevel_(indent)

    @property
    def isAlternate(self):
        '''Get the item's C{Alternate} property (C{bool}).
        '''
        return bool(self.NS.isAlternate())

    @isAlternate.setter  # PYCHOK property.setter
    def isAlternate(self, alternate):
        '''Set the item's C{Alternate} property (C{bool}).
        '''
        b = bool(alternate)
        if b != self.isAlternate:
            self.NS.setAlternate_(YES if b else NO)

    @property
    def isEnabled(self):
        '''Get the item's C{Enabled} property (C{bool}).
        '''
        return bool(self.NS.isEnabled())

    @isEnabled.setter  # PYCHOK property.setter
    def isEnabled(self, enable):
        '''Set the item's C{Enabled} property (C{bool}).
        '''
        b = bool(enable)
        if b != self.isEnabled:
            self.NS.setEnabled_(YES if b else NO)

    @property
    def isHidden(self):
        '''Get the item's C{Hidden} property (C{bool}).
        '''
        return bool(self.NS.isHidden())

    @isHidden.setter  # PYCHOK property.setter
    def isHidden(self, hidden):
        '''Set the item's C{Hidden} property (C{bool}).
        '''
        b = bool(hidden)
        if b != self.isHidden:
            self.NS.setHidden_(YES if b else NO)

    @property_RO
    def isHighlighted(self):
        '''Get the item's C{isHighlighted} property (C{bool}).
        '''
        return bool(self.NS.isHighlighted())

    @property
    def key(self):
        '''Get the item's shortcut C{key} (C{str}).
        '''
        return self._key  # nsString2str(self.NS.keyEquivalent())

    @key.setter  # PYCHOK property.setter
    def key(self, key):
        '''Set the item's shortcut C{key} and {keyEquivalent} (C{str}).
        '''
        ns, key = _nsKey2(key)
        if key != self.key:
            self.NS.setKeyEquivalent_(ns)
            self._key = key

    @property
    def keyEquivalent(self):
        '''Get the ObjC item's shortcut C{keyEquivalent} (C{str}).
        '''
        return nsString2str(self.NS.keyEquivalent())

    @keyEquivalent.setter  # PYCHOK property.setter
    def keyEquivalent(self, key):
        '''Set the ObjC item's shortcut C{keyEquivalent} (C{str}).
        '''
        ns = NSStr(bytes2str(key, name='key'))
        self.NS.setKeyEquivalent_(ns)

    @property
    def keyModifiers(self):
        '''Get the item's shortcut key C{modifiers} (C{dict}), see C{Item.__init__}.
        '''
        return dict((M.lower(), bool(self._mask & ns)) for M, ns in _Modifiers2)

    keyEquivalentModifiers = keyModifiers

    @keyModifiers.setter  # PYCHOK property.setter
    def keyModifiers(self, modifiers):
        '''Set the item's shortcut key C{modifiers} (C{dict}), see C{Item.__init__}.

           @keyword modifiers: One or more C{key} I{modifier=}C{bool} pairs (C{dict}).

           @return: Previous modifiers (C{dict}).

           @raise KeyError: Invalid I{modifiers}.
        '''
        m = self._mask
        d = self._keyModifiers(**modifiers)
        if d:
            self._mask = m  # restore
            raise KeyError('%s(%s)' % (self,
                           ', '.join('%s=%r' % _ for _ in sorted(d.items()))))

    def _keyModifiers(self, **kwds):
        '''(INTERNAL) Set the item's shortcut key modifiers.
        '''
        mask, kwds = _modifiedMask2(self._mask, kwds)

        if mask != self._mask:
            self.NS.setKeyEquivalentModifierMask_(mask)
            self._mask = mask

        return kwds  # "leftovers"

#   @property
#   def mixedStateImage(self):
#       '''Get the item's mixed-state C{image} (L{Image}).
#       '''
#       return Image(self.NS.mixedStateImage())
#
#   @mixedStateImage.setter  # PYCHOK property.setter
#   def mixedStateImage(self, image):
#       '''Set the item's mixed-state C{image} (L{Image}).
#       '''
#       if isinstanceOf(image, Image, name='image') and image != self.mixedStateImage:
#           self.NS.setMixedStateImage_(image.NS)

#   @property
#   def offStateImage(self):
#       '''Get the item's off-state C{image} (L{Image}).
#       '''
#       return Image(self.NS.offStateImage())
#
#   @offStateImage.setter  # PYCHOK property.setter
#   def offStateImage(self, image):
#       '''Set the item's off-state C{image} (L{Image}).
#       '''
#       if isinstanceOf(image, Image, name='image') and image != self.offStateImage:
#           self.NS.setOffStateImage_(image.NS)

#   @property
#   def onStateImage(self):
#       '''Get the item's on-state C{image} (L{Image}).
#       '''
#       return Image(self.NS.onStateImage())
#
#   @onStateImage.setter  # PYCHOK property.setter
#   def onStateImage(self, image):
#       '''Set the item's on-state C{image} (L{Image}).
#       '''
#       if isinstanceOf(image, Image, name='image') and image != self.onStateImage:
#           self.NS.setOnStateImage_(image.NS)

    @property_RO
    def nsTarget(self):
        '''Get the item's target (C{NS...}) or C{None} for
        the default target, C{_NSApplicationDelegate}.
        '''
        return self.NS.target()

#   @nsTarget.setter  # PYCHOK property.setter
#   def nsTarget(self, ns_target):
#       '''Set the item's C{target} (C{NS...}).
#       '''
#       if isinstanceOf(ns_target, ObjCInstance, name='ns_target'):
#           self.NS.setTarget_(ns_target)

    @property_RO
    def shift(self):
        '''Get the C{shift} key modifier (C{bool}).
        '''
        return bool(self._mask & NSShiftKeyMask)

    @property
    def state(self):
        '''Get the item's C{state} (C{int}).
        '''
        return int(self.NS.state())

    @state.setter  # PYCHOK property.setter
    def state(self, state):
        '''Set the item's C{state} (C{int}).
        '''
        if isinstanceOf(state, _Ints, name='state') and state != self.state:
            self.NS.setState_(state)

    @property
    def subMenu(self):
        '''Get the item's C{submenu} (C{Menu}) or C{None}.
        '''
        return self._subMenu

    @subMenu.setter  # PYCHOK property.setter
    def subMenu(self, submenu):
        '''Set the item's C{submenu} (L{Menu}).
        '''
        if isNone(submenu):
            m = self.subMenu
            if m:
                m._parent = None
            self.NS.setSubmenu_(0)
            self._subMenu = None

        elif isinstanceOf(submenu, Menu, name='submenu') and submenu != self.subMenu:
            _bindM(submenu, self)
            self.NS.setSubmenu_(nsOf(submenu))
            self._subMenu = submenu

    @property
    def tag(self):
        '''Get the L{Item} tag (C{int}) or C{None}.
        '''
        return self._tag

    @tag.setter  # PYCHOK property.setter
    def tag(self, tag):
        '''Set the L{Item} tag (C{int}).
        '''
        _setTag(self, tag, self.NS)

    @property
    def toolTip(self):
        '''Get the item's C{toolTip} (C{str}) or C{''}.
        '''
        ns = self.NS.toolTip()
        return nsString2str(ns) if ns else ''

    @toolTip.setter  # PYCHOK property.setter
    def toolTip(self, tip):
        '''Set the item's C{toolTip} (C{str}).
        '''
        if bytes2str(tip, name='tip') != self.toolTip:
            self.NS.setToolTip_(NSStr(tip))


class ItemSeparator(_Item_Type2):
    '''Python menu L{ItemSeparator} Type, wrapping ObjC C{NSMenuItem.separatorItem}.
    '''
    _isSeparator = True

    def __init__(self):
        '''New L{ItemSeparator}.
        '''
        self.NS = NSMenuItem.separatorItem()  # XXX can't be singleton

    @property_RO
    def action(self):
        '''Get the separator's C{action} (C{None} always).
        '''
        return None

    @property_RO
    def tag(self):
        '''Get the separator's C{tag} (C{0} always).
        '''
        return 0


class Keys(_Constants):
    '''Menu L{Item} shortcut keys (C{chr}).
    '''
    BackSpace           = BS  = chr(NSBackSpaceCharacter)  # Cmd+delete <x]
    BackTab             = BT  = chr(NSBackTabCharacter)
    Cancel              = CAN = chr(NSCancelCharacter)
    CarriageReturn      = CR  = chr(NSCarriageReturnCharacter)
    Delete              = DEL = chr(NSDeleteCharacter)  # Cmd+delete [x>
    Enter               = ETX = chr(NSEnterCharacter)
    Escape              = ESC = chr(NSEscapeCharacter)
    FormFeed            = FF  = chr(NSFormFeedCharacter)  # Cmd+page down
    NewLine             = NL  = chr(NSNewLineCharacter)
    Tab                 = HT  = chr(NSTabCharacter)

    Acknowledge         = ACK = chr(NSAcknowledgeCharacter)
    Bell                = BEL = chr(NSBellCharacter)
    DataLineEscape      = DLE = chr(NSDataLineEscapeCharacter)
    DeviceControl1      = DC1 = chr(NSDeviceControl1Character)
    DeviceControl2      = DC2 = chr(NSDeviceControl2Character)
    DeviceControl3      = DC3 = chr(NSDeviceControl3Character)
    DeviceControl4      = DC4 = chr(NSDeviceControl4Character)
    EndOfMedium         = EM  = chr(NSEndOfMediumCharacter)
    EndOfText           = ETX = chr(NSEndOfTextCharacter)
    EndOfTransmit       = EOT = chr(NSEndOfTransmitCharacter)  # Cmd+end
    EndOfTransmitBlock  = ETB = chr(NSEndOfTransmitBlockCharacter)
    Enquiry             = ENQ = chr(NSEnquiryCharacter)
    FileSeparator       = FS  = chr(NSFileSeparatorCharacter)
    GroupSeparator      = GS  = chr(NSGroupSeparatorCharacter)
    HorizontalTab       = HT  = chr(NSHorizontalTabCharacter)
    LineFeed            = LF  = chr(NSLineFeedCharacter)
    NegativeAcknowledge = NAK = chr(NSNegativeAcknowledgeCharacter)
    RecordSeparator     = RS  = chr(NSRecordSeparatorCharacter)
    ShiftIn             = SI  = chr(NSShiftInCharacter)
    ShiftOut            = SO  = chr(NSShiftOutCharacter)
    Space               = SP  = chr(NSSpaceCharacter)
    StartOfHeading      = SOH = chr(NSStartOfHeadingCharacter)
    StartOfText         = STX = chr(NSStartOfTextCharacter)
    SynchronousIdle     = SYN = chr(NSSynchronousIdleCharacter)
    Substitute          = SUB = chr(NSSubstituteCharacter)
    UnitSeparator       = US  = chr(NSUnitSeparatorCharacter)
    VerticalTab         = VT  = chr(NSVerticalTabCharacter)

    def __repr__(self):
        def _fmt(n, v):
            return '%s=%s' % (n, hex(ord(v)))
        return self._strepr(_fmt)


Keys = Keys()  # overwrite class on purpose


# % python -m test.list_methods NSMenu

# attachedMenu @16@0:8 (Id_t, Id_t, SEL_t)
# setTearOffMenuRepresentation: v24@0:8@16 (None, Id_t, SEL_t, Id_t)
# sizeToFit v16@0:8 (None, Id_t, SEL_t)                   XXX add?
# storyboard @16@0:8 (Id_t, Id_t, SEL_t)                  XXX add?
# tearOffMenuRepresentation @16@0:8 (Id_t, Id_t, SEL_t)
# update v16@0:8 (None, Id_t, SEL_t)                      XXX add?
# ...
# 502 NSMenu methods total (2, 4040)

class _Menu_Type2(_Type2):
    '''(INTERNAL) Base class for L{Menu} and L{MenuBar}.
    '''
    _listM  = []  # see ._initM()
    _nameM  = 'n/a'
    _parent = None  # see _Menu_Type2._validM
    _tagNr  = 0  # for L{Item}s only

    def __contains__(self, inst):
        return inst in self._listM

    def __len__(self):
        n = len(self._listM)
        self._assertM(n, self.NS.numberOfItems())
        return n

    def _alistM2(self, *classes):
        for inst in self._listM:
            a = inst.action
            if a and isinstance(a, classes):
                yield a, inst

    def _appendM(self, insts, *classes):
        for inst in insts:
            if isinstanceOf(inst, *classes, name=self._nameM):
                ns, m = self._validM(inst), len(self) + 1
                self.NS.addItem_(ns)
                self._listM.append(inst)
                self._tagM(inst, ns)
                self._assertM(len(self), m)

    def _assertM(self, n, m):
        if n != m:
            raise RuntimeError('len(%s) %r vs %r' % (self, n, m))

    def _find(self, inst, *classes):
        if isinstanceOf(inst, *classes, name=self._nameM):
            try:
                return self._listM.index(inst)
            except ValueError:
                pass
        return -1

    def _findM(self, title, action, tag, dflt):  # MCCABE 15
        # find item or menu
        if title:
            t = bytes2str(title, name='title')
            for inst in self._listM('title'):
                if inst.title.startswith(t):
                    return inst
            t = '%s=%r' % ('title', title)

        elif action:
            if isinstance(action, _ByteStrs):
                t = bytes2str(action)
                for a, inst in self._alistM2(type(t)):
                    if a.startswith(t):
                        return inst
            elif callable(action):
                for a, inst in self._alistM2(type(action)):
                    if a == action:
                        return inst
            t = '%s=%r' % ('action', action)

        elif isinstance(tag, _Ints):
            # only L{Item}s have non-zero tags
            for inst in self._listM:
                if inst.tag == tag:
                    return inst
            t = '%s=%r' % ('tag', tag)

        else:
            t = ''

        if dflt is missing:
            raise ValueError('no such %s.%s(%s)' % (self, self._nameM, t))
        return dflt

    def _getiteM(self, index, bytitle=None):
        try:
            if isinstance(index, slice):
                return [self._listM[i] for i in range(*index.indices(len(self)))]
            elif bytitle and isinstance(index, _ByteStrs):
                inst = bytitle(title=index, dflt=None)
                if inst:
                    return inst
            else:
                return self._listM[self._indexM(index)]
        except (IndexError, TypeError, ValueError):
            pass
        raise IndexError('invalid %s[%r]' % (self, index))

    def _index(self, inst, *classes):
        if isinstanceOf(inst, *classes, name=self._nameM):
            try:
                return self._listM.index(inst)
            except ValueError:
                pass
        raise ValueError('invalid %s: %r' % (self._nameM, inst))

    def _indexM(self, index):
        if isinstance(index, _Ints):
            i = index
            if i < 0:  # allow neg index ...
                i += len(self)
            # ... but not out of range, like list.append
            if 0 <= i < len(self):
                return i
        raise IndexError('invalid %s: %r' % ('index', index))

    def _initM(self):
        self._listM = []
        self.NS = NSMenu.alloc().init()

    def _insertM(self, index, insts, *classes):
        i = self._indexM(index)
        for inst in reversed(insts):
            if isinstanceOf(inst, *classes, name=self._nameM):
                ns, m = self._validM(inst), len(self) + 1
                self.NS.insertItem_atIndex_(ns, i)
                self._listM.insert(i, inst)
                self._tagM(inst, ns)
                self._assertM(len(self), m)

    def _popM(self, index):
        try:
            i, m = self._indexM(index), len(self) - 1
            inst = self._listM.pop(i)
            inst._parent = None
            self.NS.removeItemAtIndex_(i)
            self._assertM(len(self), m)
            return inst
        except (IndexError, TypeError):
            raise IndexError('%s.%s(%r)' % (self, 'pop', index))

    def _removeM(self, insts, *classes):
        for inst in insts:
            if isinstanceOf(inst, *classes, name=self._nameM):
                try:
                    self._popM(self._listM.index(inst))
                except (IndexError, ValueError):
                    raise ValueError('%s.%s(%s)' % (self, 'remove', inst))

    def _tagM(self, inst, ns):
        # only L{Item} tags are settable
        if isinstance(inst, (Item, Menu)):
            if inst.tag:
                pass  # preset
            else:
                _Menu_Type2._tagNr += 1
                inst.tag = _Menu_Type2._tagNr
            ns.setTag_(inst.tag)  # always an NSMenuItem
        elif not isinstance(inst, ItemSeparator):
            raise RuntimeError('set %s.%s in %s' % (inst, 'tag', self))

    def _validM(self, inst):
        if inst in self._listM:
            raise ValueError('duplicate %s %s: %r' % (self, self._nameM, inst))
        _bindM(inst, self)
        if isinstance(inst, Menu):
            inst._NSiMI = ns = _nsMenuItem(inst)
            ns.setSubmenu_(nsOf(inst))
        else:
            ns = nsOf(inst)
        return ns

    @property_RO
    def action(self):
        '''Get the menu[Bar]'s C{action} (C{None} always).
        '''
        return None

    @property
    def autoEnables(self):
        '''Get the menu's C{autoEnablesItems} property (C{bool}).
        '''
        return True if self.NS.autoenablesItems() else False

    @autoEnables.setter  # PYCHOK property.setter
    def autoEnables(self, enable):
        '''Set the menu's C{autoEnablesItems} property (C{bool}).
        '''
        b = bool(enable)
        if b != self.autoEnables:
            self.NS.setAutoenablesItems_(YES if b else NO)

    @property_RO
    def isAttached(self):
        '''Get the menu's C{isAttached} property (C{bool}).
        '''
        return True if self.NS.isAttached() else False

    @property_RO
    def isTornOff(self):
        '''Get the menu's C{isTornOff} property (C{bool}).
        '''
        return True if self.NS.isTornOff() else False

    @property
    def minWidth(self):
        '''Get the menu bar's C{minimumWidth} property (C{float} screen coordinates).
        '''
        return float(self.NS.minimumWidth())

    @minWidth.setter  # PYCHOK property.setter
    def minWidth(self, width):
        '''set the menu bar's C{minimumWidth} property (C{float} screen coordinates).
        '''
        if isinstanceOf(width, float, *_Ints, name='width'):
            self.NS.setMinimumWidth_(float(width))

    @property_RO
    def parent(self):
        '''Get the menu[Bar]'s C{parent} (L{Item}, L{Menu} or L{MenuBar}) or C{None}.
        '''
        return self._parent

    def removeAll(self):
        '''Clear this menu or menu bar.
        '''
        while self._listM:
            self._popM(0)

    @property
    def showsState(self):
        '''Get the menu's C{showsStateColumn} property (C{bool}).
        '''
        return True if self.NS.showsStateColumn() else False

    @showsState.setter  # PYCHOK property.setter
    def showsState(self, enable):
        '''Set the menu's C{showsStateColumn} property (C{bool}).
        '''
        b = bool(enable)
        if b != self.showsState:
            self.NS.setShowsStateColumn_(YES if b else NO)

    @property
    def size(self):
        '''Get the menu bar's C{size} property (L{Size} screen coordinates).
        '''
        return self.NS.size()

    @size.setter  # PYCHOK property.setter
    def size(self, size):
        '''set the menu bar's C{size} property (L{Size} screen coordinates).
        '''
        self.NS.setSize_(Size(size).NS)

    @property_RO
    def tags(self):
        '''Get the number of C{tag}s issued so far (C{int}).
        '''
        return _Menu_Type2._tagNr


class Menu(_Menu_Type2):
    '''Python L{Menu} Type, wrapping ObjC C{NSMenu}.
    '''
    _nameM = 'item'  # instances held
    _NSiMI =  None   # intermediate NSMenuItem, holding the NSMenu
    _tag   =  0

    def __init__(self, title):
        '''New L{Menu}.

           @param title: The menu title (C{str}).
        '''
        self._initM()
        self.title = title  # sets self.NS...Title_

    def append(self, *items):
        '''Add one or more items or separators to this menu.

           @param items: The items (L{Item} or L{ItemSeparator}) to add.

           @raise TypeError: An I{item} is not L{Item} nor L{ItemSeparator}.
        '''
        self._appendM(items, Item, ItemSeparator)

    def click(self, item, highlight=False):
        '''Mimick clicking a menu item.

           @param item: The item to click (L{Item}).
           @keyword highlight: Highlight the clicked item (C{bool}).

           @raise ValueError: No I{item} in this menu.
        '''
#       i = self._index(item, Item)
#       assert self.NS.itemAtIndex_(i) is item.NS
#       if highlight:  # XXX does not exist?
#           self.NS._performActionWithHighlightingForItemAtIndex_(i)  # leading _!
#       else:  # XXX causes segfault, threading?
#           self.NS.performActionForItemAtIndex_(i)

        # mimick behavior of performAction...ForItemAtIndex_
        # <http://Stackoverflow.com/questions/31989979/
        #         nsmenu-highlight-specific-nsmenuitem>
        if highlight:
            self.highlight(item)
        else:
            self._index(item, Item)
        # see _NSApplicationDelegate...
        if item._SEL_ is _CALL_:  # .callMenuItem_
            item._action(item)
        else:  # if item._SEL_ is _HANDLE_:  # .handleMenuItem_
            raise NotImplementedError('%s(%s)' % ('click', item))
        if highlight:
            # <http://Stackoverflow.com/questions/6169930/
            #         remove-highlight-from-nsmenuitem-after-click>
            # for item in (item, self):  # XXX segfaults
                h = item.isHidden  # un-highlight by ...
                item.isHidden = True  # ... hiding or removing and
                item.isHidden = h  # ... un-hiding or re-inserting

    def clickKey(self, key, highlight=False, **modifiers):
        '''Mimick clicking a menu item by the shortcut key, see C{Item.__init__}.

           @param key: The shortcut key (C{str}).
           @keyword modifiers: Optional, key I{modifier=}C{bool} pairs.
           @keyword highlight: Highlight the clicked item (C{bool}).

           @raise KeyError: If I{key} with I{modifiers} is not a
                            shortcut of this menu.
        '''
        # XXX self.NS.performKeyEquivalent_(e) is too tricky
        item = self.item(key=key, dflt=missing, **modifiers)
        self.click(item, highlight=highlight)

    def find(self, item):
        '''Return the index of a menu item in this menu.

           @param item: The item to locate (L{Item}).

           @return: The index (C{int}) or C{-1} if not found.
        '''
        return self._find(item, Item, ItemSeparator)

    def __getitem__(self, index):
        '''Return the item at index or with title or several by slice.

           @param index: The index (C{int}, C{str} or C{slice}).

           @return: The item (L{Item} or L{ItemSeparator}) or items.

           @raise IndexError: If I{index} out of range or if no item
                              titled I{index} exists.
        '''
        return self._getiteM(index, self.item)

    def highlight(self, item):
        '''Highlight a menu item.

           @param item: The item to hightlight (L{Item}).

           @raise ValueError: No I{item} in this menu.
        '''
        self._index(item, Item)
        self.NS.highlightItem_(item.NS)
#       if self._parent:  # highlight this very menu also
#           self._parent.highlight(self)

    @property_RO
    def highlightedItem(self):
        '''Get the menu's C{highlightedItem} property (C{Item} or C{None}).
        '''
        ns = self.NS.highlightedItem()
        return ns2Item(ns) if ns else None

    def index(self, item):
        '''Return the index of an item in this menu.

           @param item: The item to locate (L{Item} or L{ItemSeparator}).

           @return: Index (C{int}).

           @raise ValueError: If I{item} not found.
        '''
        return self._index(item, Item, ItemSeparator)

    @property_RO
    def isVisible(self):
        '''Get the menu's C{isVisible} property (C{bool}) or C{None}.
        '''
        try:  # mimick, not an NSMenu property
            return self.superMenu.isVisible
        except AttributeError:
            return None

    def insert(self, index, *items):
        '''Insert one or more items or separators into this menu.

           @param index: Insert items before this index (C{int}).
           @param items: The items (L{Item} or L{ItemSeparator}) to insert.

           @raise IndexError: If I{index} out of range.

           @raise TypeError: If I{index} not C{int} or an I{item} not
                             L{Item} nor L{ItemSeparator}.
        '''
        self._insertM(index, items, Item, ItemSeparator)

    @property
    def isEnabled(self):
        '''Get the menu's C{Enabled} property (C{bool}).
        '''
        return bool(self._NSiMI and self._NSiMI.isEnabled())

    @isEnabled.setter  # PYCHOK property.setter
    def isEnabled(self, enable):
        '''Set the menu's C{Enabled} property (C{bool}).
        '''
        b = bool(enable)
        if b != self.isEnabled and self._NSiMI:
            self._NSiMI.setEnabled_(YES if b else NO)

    @property
    def isHidden(self):
        '''Get the menu's C{Hidden} property (C{bool}).
        '''
        return bool(self._NSiMI and self._NSiMI.isHidden())

    @isHidden.setter  # PYCHOK property.setter
    def isHidden(self, hidden):
        '''Set the menu's C{Hidden} property (C{bool}).
        '''
        b = bool(hidden)
        if b != self.isHidden and self._NSiMI:
            print(b)
            self._NSiMI.setHidden_(YES if b else NO)

    @property_RO
    def isHighlighted(self):
        '''Get the menu's C{isHighlighted} property (C{bool}).
        '''
        return bool(self._NSiMI and self._NSiMI.isHighlighted())

    def item(self, title='', action=None, tag=None, dflt=missing, key='', **modifiers):
        '''Find an item by title, by action, by tag or by key.

           @keyword title: The item title to match (C{str}).
           @keyword action: The item action to match (C{str} or C{callable}).
           @keyword tag: The item tag to match (C{unsigned int}).
           @keyword dflt: Optional, default return value.
           @keyword key: The item shortcut key to match (C{str}).
           @keyword modifiers: Optional, key I{modifier=}C{bool} pairs, see C{Item.__init__}.

           @return: The first matching item (L{Item}) or I{dflt} if
                    no I{title}, I{action}, I{key} or I{tag} match found.

           @raise ValueError: No I{dflt} provided and no I{title},
                              I{action} nor I{tag} match.
        '''
        def _raise(Error, prefix, kwds):
            t = [('key', key)] + sorted(kwds.items())
            raise Error('%s%s.item(%s)' % (prefix, self,
                        ', '.join('%s=%r' % _ for _ in t)))

        if key:  # find by key and modifiers
            m, d = _modifiedMask2(0, modifiers)
            if d:  # can't have leftovers
                _raise(ValueError, '', d)

            try:
                _, k = _nsKey2(bytes2str(key))
                for item in self.items():  # non-separators
                    if item._mask == m and item.key == k:
                        return item
            except ValueError:
                pass

            if dflt is missing:
                _raise(KeyError, 'no such ', modifiers)
            return dflt

        elif modifiers:  # can't have modifiers
            _raise(ValueError, '', modifiers)

        return self._findM(title, action, tag, dflt)

    def items(self, separators=False):
        '''Yield the items in this menu.

           @keyword separators: Yield L{ItemSeparator}s (C{bool}),
                                skip otherwise.

           @return: Each L{Item} or L{ItemSeparator}.
        '''
        y = bool(separators)
        for item in self._listM:
            if y or not item.isSeparator:
                yield item

    @property_RO
    def nsMenuItem(self):
        '''Get the menu's intermediate (C{NSMenuItem}) or C{None} if
        the menu hasn't been added or inserted into a L{MenuBar}.
        '''
        ns = self._NSiMI
        if ns:
            m = ns2Item(ns)
            if m is not self:  # or m.NS != ns.subMenu()
                raise RuntimeError('%s(%s): %r' % ('ns2Item', self, m))
        return ns or None

    def pop(self, index=-1):
        '''Remove an item by index.

           @keyword index: The item's index (C{int}) or default,
                           the last item.

           @return: The removed item (L{Item}).

           @raise IndexError: Invalid I{index}.

           @raise TypeError: Invalid I{index}.
        '''
        return self._popM(index)

    def popUp(self, fraction=0.1):
        '''Show this menu on the screen.

           @param fraction: Cascade off the upper left corner (C{float}).

           @return: C{True} if an item was selected, C{False} otherwise.
        '''
        p = NSMain.ScreenCascade(fraction)
        t = self.NS.popUpMenuPositioningItem_atLocation_inView_(NSMain.nil, p, NSMain.nil)
        return bool(t)

    def remove(self, *items):
        '''Remove one or more items from this menu.

           @param items: The items to remove (C{Item}).

           @raise TypeError: Invalid I{item}.

           @raise ValueError: If I{item} not present.
        '''
        return self._removeM(items, Item, ItemSeparator)

    def separator(self, index=missing):
        '''Add or insert an item separator.

           @keyword index: Insert separator before this index (C{int})
                           or default, append separator.
        '''
        if index is missing:
            self._appendM(ItemSeparator())
        else:
            self._insertM(index, (ItemSeparator(),), ItemSeparator)

    @property
    def tag(self):
        '''Get the L{Menu} tag (C{int}).
        '''
        return self._tag

    @tag.setter  # PYCHOK property.setter
    def tag(self, tag):
        '''Set the L{Menu} tag (C{int}).
        '''
        _setTag(self, tag, self._NSiMI)


# <http://Developer.Apple.com/library/content/qa/qa1420/_index.html
#      #//apple_ref/doc/uid/DTS10004127>
class MenuBar(_Menu_Type2):
    '''Python L{MenuBar} Type, wrapping ObjC C{NSMenu}.
    '''
    _nameM = 'menu'  # instances held

    def __init__(self, app=None):
        '''New L{MenuBar}.

           @keyword app: The application (L{App} or C{None}).

           @raise TypeError: If I{app} not an L{App}.

           @see: Method L{MenuBar}C{.main}.
        '''
        self._initM()
        if app:  # type checked in app.setter
            self.app = app
            # XXX do not change self.NS...Title
            self._title = app.title
            # self.main(app)  # XXX trashes menu bar
        if not _Globals.MenuBar:
            _Globals.MenuBar = self

    def append(self, *menus):
        '''Add one or more sub-menus to this menu bar.

           @param menus: The menus to add (L{Menu}).
        '''
        self._appendM(menus, Menu)

    def find(self, menu):
        '''Return the index of a menu in this menu bar.

           @param menu: The menu to locate (L{Menu}).

           @return: The index (C{int}) or -1 if not found.
        '''
        return self._find(menu, Menu)

    def __getitem__(self, index):
        '''Return the menu at index or with title or several by slice.

           @param index: The index (C{int}, C{str} or C{slice}).

           @return: The menu (L{Menu}) or menus.

           @raise IndexError: If I{index} out of range or if no menu
                              titled I{index} exists.
        '''
        return self._getiteM(index, self.menu)

    @property_RO
    def height(self):
        '''Get this menu bar's height (C{float}).
        '''
        return self.NS.menuBarHeight()

    def highlight(self, menu):
        '''Highlight a menu.

           @param menu: The menu to hightlight (L{Menu}).

           @raise ValueError: No I{menu} in this menu bar.
        '''
        _ = self._index(menu, Menu)  # PYCHOK expected
        if menu._NSiMI:
            self.NS.highlightItem_(menu._NSiMI)

    @property_RO
    def highlightedMenu(self):
        '''Get the menu's C{highlightedMenu} property (C{Menu} or C{None}).
        '''
        ns = self.NS.highlightedItem()
        return ns2Item(ns) if ns else None

    def index(self, menu):
        '''Return the index of a menu in this menu bar.

           @param menu: The menu to locate (L{Menu}).

           @return: The index (C{int}).

           @raise ValueError: If I{menu} not found.
        '''
        return self._index(menu, Menu)

    @property
    def isVisible(self):
        '''Get the menu bar's C{menuBarVisible} property (C{bool}).
        '''
        return bool(self.NS.menuBarVisible())

    @isVisible.setter  # PYCHOK property.setter
    def isVisible(self, visible):
        '''Set the menu bar's C{menuBarVisible} property (C{bool}).
        '''
        b = bool(visible)
        if b != self.isVisible:
            self.NS.setMenuBarVisible_(YES if b else NO)

    def insert(self, index, *menus):
        '''Insert one or more menus into this menu bar.

           @param index: Insert menus before this index (C{int}).
           @param menus: The menus (L{Menu}) to insert.

           @raise IndexError: If I{index} out of range.

           @raise TypeError: If I{index} not C{int} or a I{menu} not
                             L{Menu}.
        '''
        self._insertM(index, menus, Menu)

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

    def menu(self, title='', dflt=missing):
        '''Find a menu by title.

           @keyword title: The menu title to match (C{str}).
           @keyword dflt: Optional, default return value.

           @return: The first matching menu (L{Menu}) or I{dflt}
                    if no I{title} match found.

           @raise ValueError: No I{dflt} provided and no I{title} match.
        '''
        return self._findM(title, None, None, dflt)

    def menus(self):
        '''Yield the menus of this menu bar.

           @return: Each menu (L{Menu}).
        '''
        for menu in self._listM:
            yield menu

    def pop(self, index=-1):
        '''Remove a menu by index.

           @keyword index: The menu's index (C{int}) or default,
                           the last menu.

           @return: The removed menu (L{Menu}).

           @raise IndexError: Invalid I{index}.

           @raise TypeError: Invalid I{index}.
        '''
        return self._popM(index)

    def remove(self, *menus):
        '''Remove one or several menus from this menu bar.

           @param menus: The menus to remove (C{Menu}).

           @raise TypeError: Invalid I{menu}.

           @raise ValueError: If I{menu} not present.
        '''
        return self._removeM(menus, Menu)

    @property_RO
    def tag(self):
        '''Get the L{MenuBar} C{tag} (C{None} always).
        '''
        return None  # XXX or ... raise AttributeError?


# TODO StatusBar & -Item
# <http://Developer.Apple.com/library/archive/documentation/
#         Cocoa/Conceptual/StatusBar/Tasks/creatingitems.html>
# class StatusBar():
#    pass


def ns2Item(ns):
    '''Get the Python instance for an C{NSMenuItem}.

       @param ns: The ObjC instance (C{NSMenuItem}).

       @return: The instance (L{Item} or L{Menu}).

       @raise TypeError: Invalid I{ns} type.

       @note: A L{Menu} instance is returned if I{ns} was an
              intermediate C{NSMenuItem}, created internally
              to append or insert a L{Menu} to a L{MenuBar}.
    '''
    if isObjCInstanceOf(ns, NSMenuItem, name='ns'):
        return _Globals.Items[ns.representedObject()]


def title2action(title):
    '''Convert a menu item C{title} to a Python callback method name.

       @param title: The item's title (C{str}).

       @return: Name for the Python callback method (C{str}), the
                I{title} with all non-alphanumeric characters except
                colon and underscore removed, with prefixed C{"menu"}
                and suffix C{"_"} added.

       @raise ValueError: If I{title} can not be converted.
    '''
    t = ''.join(_ for _ in bytes2str(title).strip().rstrip('.')
                        if _.isalnum() or _ in '_:')
    return name2pymethod('menu' + t + '_')


_Types.Item          = Item
_Types.ItemSeparator = ItemSeparator
_Types.Menu          = Menu
_Types.MenuBar       = MenuBar

if __name__ == '__main__':

    from utils import _allisting, properties

    _allisting(__all__, locals(), __version__, __file__)

    bar  = MenuBar()
    menu = Menu('Test')
    item = Item('Quit', 'menuTerminate_', key='q')

    menu.append(item)
    bar.append(menu)

    assert len(bar) == 1, len(bar)
    assert len(menu) == 1, len(menu)
    assert menu in bar, (menu, bar)
    assert item in menu, (item, menu)
    assert menu.parent is bar, menu.parent
    assert item.parent is menu, item.parent

    for x in (item, menu, bar):
        print('\n%s properties:' % (x,))
        for p, v in sorted(properties(x).items()):
            print('  %s = %r' % (p, v))

    bar.remove(menu)
    menu.remove(item)

    assert len(bar) == 0, len(bar)
    assert len(menu) == 0, len(menu)
    assert menu not in bar, (menu, bar)
    assert item not in menu, (item, menu)
    assert menu.parent is None, menu.parent
    assert item.parent is None, item.parent

    assert item.subMenu is None, item.subMenu

    item.subMenu = menu
    assert item.subMenu is menu, item.subMenu

    item.subMenu = None
    assert item.subMenu is None, item.subMenu

_ = '''

 menus.__all__ = tuple(
   menus.Item is <class .Item>,
   menus.ItemSeparator is <class .ItemSeparator>,
   menus.Menu is <class .Menu>,
   menus.MenuBar is <class .MenuBar>,
   menus.ns2Item is <function .ns2Item at 0x10c781320>,
   menus.title2action is <function .title2action at 0x10c789050>,
 )[6]
 menus.__version__ = '18.08.15'

Item('Quit', 'menuTerminate_', Cmd+Q) properties:
  NS = <ObjCInstance(NSMenuItem(<Id_t at 0x10c798170>) of 0x7fce5449c590) at 0x10c78e490>
  NSDelegate = 'AttributeError("use \'NSd-\' not \'NSD-\'",)'
  NSdelegate = None
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
  nsTarget = None
  parent = Menu('Test') at 0x10c78e1d0
  shift = False
  state = 0
  subMenu = None
  tag = 1
  title = 'Quit'
  toolTip = ''

Menu('Test') properties:
  NS = <ObjCInstance(NSMenu(<Id_t at 0x10c790560>) of 0x7fce54499bc0) at 0x10c78e290>
  NSDelegate = 'AttributeError("use \'NSd-\' not \'NSD-\'",)'
  NSdelegate = None
  action = None
  app = None
  autoEnables = True
  highlightedItem = None
  isAttached = False
  isEnabled = True
  isHidden = False
  isHighlighted = False
  isTornOff = False
  isVisible = None
  minWidth = 0.0
  parent = MenuBar(None) at 0x10c786ed0
  showsState = True
  size = <NSSize_t(width=100.0, height=29.0) at 0x10c7af5f0>
  tag = 2
  tags = 2
  title = 'Test'

MenuBar(None) properties:
  NS = <ObjCInstance(NSMenu(<Id_t at 0x10c719b00>) of 0x7fce54499580) at 0x10c78e110>
  NSDelegate = 'AttributeError("use \'NSd-\' not \'NSD-\'",)'
  NSdelegate = None
  action = None
  app = None
  autoEnables = True
  height = 0.0
  highlightedMenu = None
  isAttached = False
  isTornOff = False
  isVisible = True
  minWidth = 0.0
  parent = None
  showsState = True
  size = <NSSize_t(width=107.0, height=29.0) at 0x10c7af950>
  tag = None
  tags = 2
  title = None
'''
del _

# MIT License <http://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2019 -- mrJean1 at Gmail dot com
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
