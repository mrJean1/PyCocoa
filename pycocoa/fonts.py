
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Type L{Font}, etc., wrapping ObjC C{NSFont}.

@var Fonts: Pre-defined system fonts, all L{Font} instances.
@var Fonts.App: Get the C{UserFont}.
@var Fonts.Bold: Get the C{BoldFont}.
@var Fonts.BoldItalic: Get the C{BoldItalicFont}.
@var Fonts.Italic: Get the C{ItalicFont}.
@var Fonts.Label: Get the C{LabelFont}.
@var Fonts.Menu: Get the C{MenuFont}.
@var Fonts.MenuBar: Get the C{MenuBarFont}.
@var Fonts.Message: Get the C{MessageFont}.
@var Fonts.MonoSpace: Get the C{MonoSpaceFont}.
@var Fonts.Palette: Get the C{PaletteFont}.
@var Fonts.System: Get the C{SystemFont}.
@var Fonts.TableData: Get the C{TableDataFont}.
@var Fonts.TableHeader: Get the C{TableHeaderFont}.
@var Fonts.Title: Get the C{TitleFont}.

@var FontTrait: Font trait constants (C{mask}).
@var FontTrait.Bold: int([x]) -> integer.
@var FontTrait.Compressed: int([x]) -> integer.
@var FontTrait.Condensed: int([x]) -> integer.
@var FontTrait.Expanded: int([x]) -> integer.
@var FontTrait.Italic: int([x]) -> integer.
@var FontTrait.MonoSpace: int([x]) -> integer.
@var FontTrait.Narrow: int([x]) -> integer.
@var FontTrait.Poster: int([x]) -> integer.
@var FontTrait.SansSerif: int([x]) -> integer.
@var FontTrait.SmallCaps: int([x]) -> integer.
@var FontTrait.UnBold: int([x]) -> integer.
@var FontTrait.UnItalic: int([x]) -> integer.
'''
# all imports listed explicitly to help PyChecker
from pycocoa.bases   import _Type0
from pycocoa.lazily  import _ALL_LAZY, _NN_, _SPACE_
from pycocoa.nstypes import isNone, NSFont, nsIter, nsIter2, NSMain, \
                            NSStr, nsString2str
from pycocoa.oslibs  import NSFontBoldMask, NSFontItalicMask, \
                            NSFontCompressedMask, NSFontCondensedMask, \
                            NSFontExpandedMask, NSFontMonoSpaceMask, \
                            NSFontNarrowMask, NSFontPosterMask, \
                            NSFontSmallCapsMask, NSFontSansSerifClass, \
                            NSFontUnboldMask, NSFontUnitalicMask
from pycocoa.runtime import isObjCInstanceOf, release
from pycocoa.strs    import Str
from pycocoa.utils   import Adict, bytes2str, _ByteStrs, _Constants, flint, \
                           _Ints, isinstanceOf, property_RO, _Singletons, \
                           _Types

__all__ = _ALL_LAZY.fonts
__version__ = '21.11.04'

# <https://Developer.Apple.com/documentation/appkit/nsfont.weight>
# _NSFontWeigthHeavy      = 13 ?
# _NSFontWeigthBlack      = 11 ?
# _NSFontWeigthBold       =  9
# _NSFontWeigthSemibold   =  8 ?
# _NSFontWeigthMedium     =  6 ?
# _NSFontWeigthRegular    =  5
# _NSFontWeigthThin       =  3 ?
# _NSFontWeigthLight      =  2 ?
# _NSFontWeigthUltraLight =  1 ?


def _nsFontsOf(family):
    t = NSStr(family)
    r = NSMain.FontManager.availableMembersOfFontFamily_(t)
    t.release()  # PYCHOK expected
    return r


# XXX dict _familyTraits and class FontTrait
#     MUST be defined before class Font
class FontTrait(_Constants):
    '''Font trait constants (C{mask}).
    '''
    Bold       = NSFontBoldMask
    Compressed = NSFontCompressedMask
    Condensed  = NSFontCondensedMask
    Expanded   = NSFontExpandedMask
    Italic     = NSFontItalicMask
    MonoSpace  = NSFontMonoSpaceMask
    Narrow     = NSFontNarrowMask
    Poster     = NSFontPosterMask
    SansSerif  = NSFontSansSerifClass  # exception
    SmallCaps  = NSFontSmallCapsMask
    UnBold     = NSFontUnboldMask
    UnItalic   = NSFontUnitalicMask

FontTrait = FontTrait()  # PYCHOK contants

# dict for Font.traitsup() to update traits with family traits
_familyTraits = dict((n.lower(), m) for n, m in FontTrait.items()
                                     if not n.startswith('Un'))
_familyTraits.update(dict(black=FontTrait.Bold,
                  #        book=0,
                  #    chancery=0,
                  #        demi=0,
                     extrablack=FontTrait.Bold,
                      extrabold=FontTrait.Bold,
                  #  extralight=0,
                          heavy=FontTrait.Bold,
                  #    inclined=0,
                  #      inline=0,
                  #       light=0,
                  #      medium=0,
                           mono=FontTrait.MonoSpace,
                        oblique=FontTrait.Italic,
                  #     outline=0,  # Braille
                  #    pinpoint=0,  # Braille
                  #       plain=0,
                  #     regular=0,
                  #       roman=0,
                           sans=FontTrait.SansSerif,  # exception
                  #        semi=0,
                       semibold=FontTrait.Bold,
                  #       solid=0,
                  #        text=0,
                  #        thin=0,
                  #       ultra=0,
                  #  ultralight=0,
                      ultrabold=FontTrait.Bold))
# all valid traits
_maskTraits = 0
for _, m in FontTrait.items():
    _maskTraits |= m

_ = n = m = None; del _, n, m  # PYCHOK expected


def _traitex(traits, mask):
    # check mask exclusivity
    return (traits & mask) == mask


def _traitsin(traits, raiser=True):
    # Convert and check traits
    if isinstance(traits, _Ints):
        ts = traits & _maskTraits
    elif isinstance(traits, _ByteStrs):
        ts = 0
        for t in bytes2str(traits).strip().split():
            m = _familyTraits.get(t.lower(), None)
            if m:
                ts |= m
            elif raiser and m is None:
                raise FontTraitError('invalid %s: %r' % ('trait', t))
    else:
        raise FontTraitError('invalid %s: %r' % ('traits', traits))
    # check for mutually exclusive traits
    if _traitex(ts, FontTrait.Condensed | FontTrait.Expanded) or \
       _traitex(ts, FontTrait.Italic    | FontTrait.UnItalic) or \
       _traitex(ts, FontTrait.Bold      | FontTrait.UnBold):
        raise FontTraitError('incompatible %s: %r' % ('traits', traits))
    return ts


def _weightin(weight):
    # check weight
    try:
        if 0 <= weight <= 15:
            return int(weight)
    except (TypeError, ValueError):
        pass
    raise ValueError('invalid %s: %r' % ('weight', weight))


class Font(_Type0):
    '''Python C{Font} Type, wrapping ObjC C{NSFont}.
    '''
    _family = _NN_
    _height =  0
    _name   = _NN_
    _size   =  0
    _traits =  0
    _weight =  None

    def __init__(self, family_or_font, size=0, traits=0, weight=5):
        '''New L{Font}.

           @param family_or_font: Generic font name (C{str}, L{Str}, L{NSStr})
                                  like "Times" or "Helvetica" or a L{Font},
                                  C{NSFont} or C{NSFontDescriptor} instance.
           @keyword size: Desired point size (C{int}), zero for any.
           @keyword traits: Desired font traits (C{str} or C{FontTrait}C{s mask}).
           @keyword weigth: Desired book weight (C{int}) in range 0..15, where
                            0=light, 5=regular, 9=bold and 15=heavy.

           @raise FontError: No such I{family_or_font}.

           @raise FontTraitError: Mutually exclusive I{traits}.

           @raise TypeError: Invalid I{family_or_font}.

           @raise ValueError: Invalid I{weight}.

           @note: The new L{Font} may not exhibit the desired I{traits}
                  and I{weight}.  The I{weight} is ignored if I{traits}
                  include C{FontTrait.Bold}, both I{traits} and I{weight}
                  are ignored if I{family_or_font} is C{NSFontDescriptor}.

           @see: Function L{fontsof} to obtain all available fonts of
                 a particular font family.
        '''
        if isinstance(family_or_font, Str):
            ns, py = family_or_font.NS, str(family_or_font)
        elif isinstance(family_or_font, _ByteStrs):
            ns, py = release(NSStr(family_or_font)), bytes2str(family_or_font)
        elif isinstance(family_or_font, NSStr):
            ns, py = family_or_font, nsString2str(family_or_font)
#       elif isObjCInstanceOf(family_or_font, NSFontDescriptor):
            # <https://Developer.Apple.com/documentation/appkit/nsfont/1525386-init>
            # ignore traits and weight
#           ns, py = NSFont.alloc().init_(family_or_font, size), None
        elif isObjCInstanceOf(family_or_font, NSFont, name='family_or_font'):
            ns, py = family_or_font, None
            if size == 0:
                size = ns.pointSize()
            if traits == 0:
                traits = NSMain.FontManager.traitsOfFont_(ns)
            if not (size == ns.pointSize() and
                    traits == NSMain.FontManager.traitsOfFont_(ns)):
                ns = ns.familyName()
                py = nsString2str(ns)

        if py is not None:
            # <https://Developer.Apple.com/documentation/appkit/
            #        nsfontmanager/1462332-fontwithfamily>
            self._traits = _traitsin(traits)
            self._weight = _weightin(weight)
            ns = NSMain.FontManager.fontWithFamily_traits_weight_size_(
                                 ns, self._traits, self._weight, size)
            if isNone(ns):
                self._family = py
                self._size   = flint(size)
                raise FontError('no such %s: %s' % ('font', self._argstr()))

        self._NS = ns  # _RO
        # <https://Developer.Apple.com/library/content/documentation/
        #  TextFonts/Conceptual/CocoaTextArchitecture/FontHandling/FontHandling.html>
        self._family = nsString2str(ns.familyName())
        self._height = flint(NSMain.LayoutManager.defaultLineHeightForFont_(ns) + 1)
        self._name   = nsString2str(ns.fontName())
        self._size   = flint(ns.pointSize())
        # traits not always reflect actual traits
        self._traits = NSMain.FontManager.traitsOfFont_(ns) or 0
        # update with the family traits, if any
        self._traits |= _traitsin(self._family, raiser=False)
        if ns.isFixedPitch() and not self.isMonoSpace:
            self._traits |= FontTrait.MonoSpace
        self._weight = NSMain.FontManager.weightOfFont_(ns)

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__,
                           self._argstr(name=self.name))

    def _argstr(self, name=_NN_):
        td = Adict(family=self.family, size=self.size)
        if name:
            td(name=name)
        t = tuple(t[2:] for t in _isTraits if getattr(self, t))
        if t:
            td(traits=_SPACE_.join(t))
        if self.weight is not None:
            td(weight=self.weight)
        return str(td)

    def _isTrait(self, mask):
        return True if (self._traits & mask) else False

    @property_RO
    def count(self):
        '''Get the number of glyphs (C{int}).
        '''
        return self.NS.numberOfGlyphs()

    @property_RO
    def family(self):
        '''Get the font C{family} name (C{str}).
        '''
        return self._family

    @property_RO
    def height(self):
        '''Get the C{line} height (C{float} or C{int}).

           @note: The C{line} height is the sum of the tallest
                  ascender, tallest descender and leading heights.
        '''
        # <https://Developer.Apple.com/library/content/documentation/
        #        Cocoa/Conceptual/TextLayout/Tasks/StringHeight.html>
        return self._height

    @property_RO
    def heightAscender(self):
        '''Get the C{ascender} height (C{float}).
        '''
        return self.NS.ascender()

    @property_RO
    def heightBaseline(self):
        '''Get the C{baseline} offset (C{float} or C{int}).
        '''
        return flint(NSMain.LayoutManager.defaultBaselineOffsetForFont_(self.NS))

    @property_RO
    def heightCap(self):
        '''Get the C{cap} height (C{float} or C{int}).
        '''
        return flint(self.NS.capHeight())

    @property_RO
    def heightDescender(self):
        '''Get the C{descender} height (C{float}).
        '''
        return self.NS.descender()

    @property_RO
    def heightLeading(self):
        '''Get the C{leading} height (C{float} or C{int}).
        '''
        return flint(self.NS.leading())

    @property_RO
    def heightUnderline(self):
        '''Get the C{underline} position (C{float}).
        '''
        return self.NS.underlinePosition()

    @property_RO
    def heightX(self):
        '''Get the C{x} height (C{float} or C{int}).
        '''
        return flint(self.NS.xHeight())

    @property_RO
    def isBold(self):
        '''Get the B{Bold} trait (C{bool}).
        '''
        return self._isTrait(NSFontBoldMask)

    @property_RO
    def isCompressed(self):
        '''Get the C{Compressed} trait (C{bool}).
        '''
        return self._isTrait(NSFontCompressedMask)

    @property_RO
    def isCondensed(self):
        '''Get the C{Condensed} trait (C{bool}).
        '''
        return self._isTrait(NSFontCondensedMask)

    @property_RO
    def isExpanded(self):
        '''Get the C{Expanded} trait (C{bool}).
        '''
        return self._isTrait(NSFontExpandedMask)

    @property_RO
    def isItalic(self):
        '''Get the I{Italic} trait (C{bool}).
        '''
        return self._isTrait(NSFontItalicMask)

    @property_RO
    def isMonoSpace(self):
        '''Get the C{MonoSpace} trait (C{bool}).
        '''
        return self._isTrait(NSFontMonoSpaceMask)

    @property_RO
    def isNarrow(self):
        '''Get the C{Narrow} trait (C{bool}).
        '''
        return self._isTrait(NSFontNarrowMask)

    @property_RO
    def isPoster(self):
        '''Get the C{Poster} trait (C{bool}).
        '''
        return self._isTrait(NSFontPosterMask)

    @property_RO
    def isSansSerif(self):
        '''Get the C{SansSerif} "trait" (C{bool}).
        '''
        return self._isTrait(NSFontSansSerifClass)

    @property_RO
    def isSmallCaps(self):
        '''Get the C{SmallCaps} trait (C{bool}).
        '''
        return self._isTrait(NSFontSmallCapsMask)

    @property_RO
    def isUnBold(self):
        '''Get the C{UnBold} "trait" (C{bool}).
        '''
        return self._isTrait(NSFontUnboldMask)

    @property_RO
    def isUnItalic(self):
        '''Get the C{UnItalic} "trait" (C{bool}).
        '''
        return self._isTrait(NSFontUnitalicMask)

    @property_RO
    def isVertical(self):
        '''Get the C{Vertical} "trait" (C{bool}).
        '''
        if self.NS:
            return True if self.NS.isVertical() else False
        else:
            return None

    @property
    def name(self):
        '''Get the font name (C{str}).
        '''
        return self._name

    @name.setter  # PYCHOK property.setter
    def name(self, name):
        '''Set the font name (C{str}).
        '''
        self._name = bytes2str(name)

    @property_RO
    def NS(self):
        '''Get the ObjC instance (C{NSFont}).
        '''
        return self._NS

#   @property_RO
#   def NSfontDescriptor(self):
#       '''Get the C{FontDecriptor} (C{NSDescriptor?}).
#       return self.NS.fontDescriptor()

    def resize(self, size):
        '''Get this font in an other point size.

           @keyword size: Desired point size (C{int}).

           @return: The other or this font (L{Font}).

           @see: L{Font}C{.__init__} for errors raised.
        '''
        ns = None
        if size == self.size:
            return self
        elif size:
            ns = self.NS.fontWithSize_(size)
            if isNone(ns):
                ns = None
        return Font(ns or self.family, size=size, traits=self.traits,
                                                  weight=self.weight)

    @property_RO
    def size(self):
        '''Get the C{point size} of the font (C{float} or C{int}).
        '''
        return self._size

    def size2(self, bstr):
        '''Get the size of a string.

           @param bstr: The string (C{str}, C{bytes} or L{Str}).

           @return: 2-Tuple (width, height) in (C{float} or C{int}).
        '''
        if isinstance(bstr, Str):
            ns = bstr.NS
        elif isinstance(bstr, _ByteStrs):
            ns = release(NSStr(bstr))
        elif isinstanceOf(bstr, NSStr, name='bstr'):
            ns = bstr
        return flint(self.NS.widthOfString_(ns)), self.height

    def sizedup(self, points):
        '''Return a font with increased point C{size}.

           @param points: Point size to add (C{int}).

           @return: The other or this font (L{Font}).

           @see: L{Font}C{.__init__} for errors raised.
        '''
        return self.resize(self.size + points)

    @property_RO
    def slant(self):
        '''Get the italic angle (C{float}, C{int} or C{None}).
        '''
        return flint(self.NS.italicAngle()) if self.NS else None

    @property_RO
    def traits(self):
        '''Get all font traits (C{FontTrait}s mask).
        '''
        return self._traits

    def traitsup(self, *traits):
        '''Return a font with updated C{traits}.

           @param traits: Traits to update (C{str} or C{FontTrait}C{s mask}).

           @return: The other or this font (L{Font}).

           @see: L{Font}C{.__init__} for errors raised.
        '''

        ts = self._traits
        for t in traits:
            ts |= _traitsin(t)
        return Font(self.NS, traits=ts)

    @property_RO
    def vertical(self):
        '''Get the C{vertical} version of this font (L{Font} or C{None}).
        '''
        if self.isVertical:
            return self
        f = self.NS.vertical()
        if f and isObjCInstanceOf(f, NSFont):
            return Font(f)
        return None

    @property_RO
    def weight(self):
        '''Get the book C{weight} of the font (C{int} or C{None}).
        '''
        return self._weight


# get all Font.isXyz... property names
_isTraits = tuple(sorted(_ for _ in dir(Font) if _.startswith('is')))  # PYCHOK false


class FontError(ValueError):
    '''Font selection error.
    '''
    pass


class FontTraitError(FontError):
    '''Font traits error.
    '''
    pass


class _Fonts(_Singletons):
    '''Pre-defined system fonts, all L{Font} instances.
    '''
    _App         = None
    _Bold        = None
    _BoldItalic  = None
    _Italic      = None
    _Label       = None
    _Menu        = None
    _MenuBar     = None
    _Message     = None
    _MonoSpace   = None
    _Palette     = None
    _System      = None
    _TableData   = None
    _TableHeader = None
    _Title       = None

    @property_RO
    def App(self):
        '''Get the C{UserFont}.
        '''
        if self._App is None:
            _Fonts._App = Font(NSFont.userFontOfSize_(0))
        return self._App

    @property_RO
    def Bold(self):
        '''Get the C{BoldFont}.
        '''
        if self._Bold is None:
            _Fonts._Bold = Font(NSFont.boldSystemFontOfSize_(0))
        return self._Bold

    @property_RO
    def BoldItalic(self):
        '''Get the C{BoldItalicFont}.
        '''
        if self._BoldItalic is None:
            _Fonts._BoldItalic = Font(NSFont.boldSystemFontOfSize_(0)).traitsup(FontTrait.Italic)
        return self._BoldItalic

    @property_RO
    def Italic(self):
        '''Get the C{ItalicFont}.
        '''
        if self._Italic is None:
            _Fonts._Italic = Font(NSFont.systemFontOfSize_(0)).traitsup(FontTrait.Italic)
        return self._Italic

    @property_RO
    def Label(self):
        '''Get the C{LabelFont}.
        '''
        if self._Label is None:
            _Fonts._Label = Font(NSFont.labelFontOfSize_(0))
        return self._Label

    @property_RO
    def Menu(self):
        '''Get the C{MenuFont}.
        '''
        if self._Menu is None:
            _Fonts._Menu = Font(NSFont.menuFontOfSize_(0))
        return self._Menu

    @property_RO
    def MenuBar(self):
        '''Get the C{MenuBarFont}.
        '''
        if self._MenuBar is None:
            _Fonts._MenuBar = Font(NSFont.menuBarFontOfSize_(0))
        return self._MenuBar

    @property_RO
    def Message(self):
        '''Get the C{MessageFont}.
        '''
        if self._Message is None:
            _Fonts._Message = Font(NSFont.messageFontOfSize_(0))
        return self._Message

    @property_RO
    def MonoSpace(self):
        '''Get the C{MonoSpaceFont}.
        '''
        if self._MonoSpace is None:
            _Fonts._MonoSpace = Font(NSFont.userFixedPitchFontOfSize_(0))
        return self._MonoSpace

    @property_RO
    def Palette(self):
        '''Get the C{PaletteFont}.
        '''
        if self._Palette is None:
            _Fonts._Palette = Font(NSFont.paletteFontOfSize_(0))
        return self._Palette

    @property_RO
    def System(self):
        '''Get the C{SystemFont}.
        '''
        if self._System is None:
            _Fonts._System = Font(NSFont.systemFontOfSize_(0))
        return self._System

    @property_RO
    def TableData(self):
        '''Get the C{TableDataFont}.
        '''
        if self._TableData is None:
            _Fonts._TableData = Font(NSMain.TableColumn.dataCell().font())
        return self._TableData

    @property_RO
    def TableHeader(self):
        '''Get the C{TableHeaderFont}.
        '''
        if self._TableHeader is None:
            _Fonts._TableHeader = Font(NSMain.TableColumn.headerCell().font())
        return self._TableHeader

    @property_RO
    def Title(self):
        '''Get the C{TitleFont}.
        '''
        if self._Title is None:
            _Fonts._Title = Font(NSFont.titleBarFontOfSize_(0))
        return self._Title

Fonts = _Fonts()  # PYCHOK singletons


def fontfamilies(*prefixes):
    '''Yield the installed font families.

       @param prefixes: No, one or more font family names to match (C{str}-s).

       @return: Each font family name (C{str}).
    '''
    # <https://Developer.Apple.com/documentation/appkit/
    #        nsfontmanager/1462323-availablefontfamilies>
    for ns in nsIter(NSMain.FontManager.availableFontFamilies()):
        f = nsString2str(ns)
        if f.startswith(prefixes or f):
            yield f


def fontnamesof(family):
    '''Yield the available font names of a family.

       @param family: Generic font name (C{str}), like "Times" or "Helvetica".

       @return: The name (C{str}) of each font.
    '''
    # <https://Developer.Apple.com/documentation/appkit/
    #        nsfontmanager/1462316-availablemembers>
    for ns in nsIter(_nsFontsOf(family)):
        yield nsString2str(ns.objectAtIndex_(0))


def fontsof(family, size=0, weight=None):
    '''Yield the available fonts of a family.

       @param family: Generic font name (C{str}), like "Times" or "Helvetica".
       @keyword size: The point size (C{int}), zero for any.
       @keyword weight: The book weight (C{int}), None for any.

       @return: A (L{Font}) instance for each font.

       @raise ValueError: Invalid I{weight}.
    '''
    if weight is None:
        lw, hw = 0, 15
    else:
        lw = hw = _weightin(weight)
    # <https://Developer.Apple.com/documentation/appkit/
    #        nsfontmanager/1462316-availablemembers>
    for (n, m, w, t), _ in nsIter2(_nsFontsOf(family)):
        # each item is [name, trait-like attributes, weight, traits]
        if lw <= w <= hw:
            try:
                f = Font(family, size=size, traits=t, weight=w)
            except (FontError, FontTraitError):
                continue
            f._traits |= _traitsin(m, raiser=False)  # family traits
            f.name = n
            yield f


def fontsof4(family):
    '''Yield the available fonts of a family.

       @param family: Generic font name (C{str}), like "Times" or "Helvetica".

       @return: 4-Tuple (name, attributes, weight, traits) of (C{str},
                C{str}, C{int}, C{int}) for each font.
    '''
    # <https://Developer.Apple.com/documentation/appkit/
    #        nsfontmanager/1462316-availablemembers>
    for t4, _ in nsIter2(_nsFontsOf(family)):
        # each item is [name, trait-like attributes, weight, traits]
        yield tuple(t4)


def fontTraits(*traits):
    '''Return a font traits mask for the named traits.

       @param traits: Trait names (C{str}s), case-insensitive.

       @return: Combined traits (C{FontTrait}C{s mask}).

       @raise FontTraitError: One or more I{traits} are invalid.
    '''
    ts = 0
    for t in traits:
        ts |= _traitsin(t)
    return ts


def fontTraitstrs(traits):
    '''Return font traits as names.

       @param traits: Traits (C{FontTrait}C{s mask}).

       @return: Tuple of trait names (C{str}s).
    '''
    return tuple(n for n, m in sorted(FontTrait.items())
                            if traits & m)


NSFont._Type = _Types.Font = Font

if __name__ == '__main__':

    from pycocoa.utils import _all_listing, _varstr

    print(_varstr(Fonts))
    print(_varstr(FontTrait))

    _all_listing(__all__, locals())

# % python3 -m pycocoa.fonts
#
# pycocoa.fonts.__all__ = tuple(
#  pycocoa.fonts.Font is <class .Font>,
#  pycocoa.fonts.FontError is <class .FontError>,
#  pycocoa.fonts.fontfamilies is <function .fontfamilies at 0x100c27a30>,
#  pycocoa.fonts.fontnamesof is <function .fontnamesof at 0x100c2b130>,
#  pycocoa.fonts.Fonts.App=Font({family='Helvetica', name='Helvetica', size=12, weight=5}),
#                     .Bold=Font({family='.AppleSystemUIFont', name='.AppleSystemUIFontBold', size=13, traits='Bold', weight=9}),
#                     .BoldItalic=Font({family='.AppleSystemUIFont', name='.AppleSystemUIFontEmphasizedItalic', size=13, traits='Bold Italic', weight=9}),
#                     .Italic=Font({family='.AppleSystemUIFont', name='.AppleSystemUIFontItalic', size=13, traits='Italic', weight=5}),
#                     .Label=Font({family='.AppleSystemUIFont', name='.AppleSystemUIFont', size=10, weight=5}),
#                     .Menu=Font({family='.AppleSystemUIFont', name='.AppleSystemUIFont', size=13, weight=5}),
#                     .MenuBar=Font({family='.AppleSystemUIFont', name='.AppleSystemUIFont', size=13, weight=5}),
#                     .Message=Font({family='.AppleSystemUIFont', name='.AppleSystemUIFont', size=13, weight=5}),
#                     .MonoSpace=Font({family='Menlo', name='Menlo-Regular', size=11, traits='MonoSpace', weight=5}),
#                     .Palette=Font({family='.AppleSystemUIFont', name='.AppleSystemUIFont', size=11, weight=5}),
#                     .System=Font({family='.AppleSystemUIFont', name='.AppleSystemUIFont', size=13, weight=5}),
#                     .TableData=Font({family='.AppleSystemUIFont', name='.AppleSystemUIFont', size=13, weight=5}),
#                     .TableHeader=Font({family='.AppleSystemUIFont', name='.SFNS-Regular', size=11, weight=5}),
#                     .Title=Font({family='.AppleSystemUIFont', name='.AppleSystemUIFaceHeadline', size=13, traits='Bold', weight=8}),
#  pycocoa.fonts.fontsof is <function .fontsof at 0x100c2b1c0>,
#  pycocoa.fonts.fontsof4 is <function .fontsof4 at 0x100c2b250>,
#  pycocoa.fonts.FontTrait.Bold=2,
#                         .Compressed=1<<9,
#                         .Condensed=1<<6,
#                         .Expanded=1<<5,
#                         .Italic=1,
#                         .MonoSpace=1<<10,
#                         .Narrow=1<<4,
#                         .Poster=1<<8,
#                         .SansSerif=1<<31,
#                         .SmallCaps=1<<7,
#                         .UnBold=1<<2,
#                         .UnItalic=1<<24,
#  pycocoa.fonts.FontTraitError is <class .FontTraitError>,
#  pycocoa.fonts.fontTraits is <function .fontTraits at 0x100c2b2e0>,
#  pycocoa.fonts.fontTraitstrs is <function .fontTraitstrs at 0x100c2b370>,
# )[11]
# pycocoa.fonts.version 21.11.04, .isLazy 1, Python 3.11.0 64bit arm64, macOS 13.0.1

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2023 -- mrJean1 at Gmail -- All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
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
