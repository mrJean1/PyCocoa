
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Type L{Font}, etc., wrapping ObjC L{NSFont}.

@var Fonts:     Pre-defined system fonts (L{Font}).
@var FontTrait: Font traits (C{mask}).
'''
# all imports listed explicitly to help PyChecker
from bases   import _Type0
from nstypes import isNone, NSFont, nsIter, nsIter2, NSMain, \
                    NSStr, nsString2str
from oslibs  import NSFontBoldMask, NSFontItalicMask, \
                    NSFontCompressedMask, NSFontCondensedMask, \
                    NSFontExpandedMask, NSFontMonoSpaceMask, \
                    NSFontNarrowMask, NSFontPosterMask, \
                    NSFontSmallCapsMask, NSFontSansSerifClass, \
                    NSFontUnboldMask, NSFontUnitalicMask
from runtime import isInstanceOf, release
from strs    import Str
from utils   import bytes2str, _ByteStrs, _Constants, _exports, \
                    flint, _Ints, isinstanceOf, _Singletons, _Types

__version__ = '18.07.15'

# <http://Developer.Apple.com/documentation/appkit/nsfont.weight>
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


FontTrait = FontTrait()  # overwrite class on purpose

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
    '''Python C{Font} Type, wrapping ObjC L{NSFont}.
    '''
    _family = ''
    _height = 0
    _name   = ''
    _size   = 0
    _traits = 0
    _weight = None

    def __init__(self, family_or_font, size=0, traits=0, weight=5):
        '''New L{Font}.

           @param family_or_font: Generic font name (C{str}, L{Str}, L{NSStr})
                                  like "Times" or "Helvetica" or a L{Font},
                                  L{NSFont} or L{NSFontDescriptor} instance.
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
                  are ignored if I{family_or_font} is L{NSFontDescriptor}.

           @see: Function L{fontsof} to obtain all available fonts of
                 a particular font family.
        '''
        if isinstance(family_or_font, Str):
            ns, py = family_or_font.NS, str(family_or_font)
        elif isinstance(family_or_font, _ByteStrs):
            ns, py = release(NSStr(family_or_font)), bytes2str(family_or_font)
        elif isinstance(family_or_font, NSStr):
            ns, py = family_or_font, nsString2str(family_or_font)
#       elif isInstanceOf(family_or_font, NSFontDescriptor):
            # <http://Developer.Apple.com/documentation/appkit/nsfont/1525386-init>
            # ignore traits and weight
#           ns, py = NSFont.alloc().init_(family_or_font, size), None
        elif isInstanceOf(family_or_font, NSFont, name='family_or_font'):
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
            # <http://Developer.Apple.com/documentation/appkit/
            #       nsfontmanager/1462332-fontwithfamily>
            self._traits = _traitsin(traits)
            self._weight = _weightin(weight)
            ns = NSMain.FontManager.fontWithFamily_traits_weight_size_(
                                 ns, self._traits, self._weight, size)
            if isNone(ns):
                self._family = py
                self._size   = flint(size)
                raise FontError('no such %s: %s' % ('font', self._argstr()))

        self.NS = ns
        # <http://Developer.Apple.com/library/content/documentation/
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

    def _argstr(self, name=''):
        ts = []
        if name:
            ts.append(('name', name))
        ts.append(('family', self.family))
        ts.append(('size', self.size))

        t = tuple(t[2:] for t in _isTraits if getattr(self, t))
        if t:
            ts.append(('traits', ' '.join(t)))

        if self.weight is not None:
            ts.append(('weight', self.weight))
        return ', '.join('%s=%r' % t for t in ts)

    def _isTrait(self, mask):
        return True if (self._traits & mask) else False

    @property
    def count(self):
        '''Get the number of glyphs (C{int}).
        '''
        return self.NS.numberOfGlyphs()

    @property
    def family(self):
        '''Get the font C{family} name (C{str}).
        '''
        return self._family

    @property
    def height(self):
        '''Get the C{line} height (C{float} or C{int}).

           @note: The C{height} is the sum of the tallest
                  ascender, tallest descender and leading.
        '''
        # <http://Developer.Apple.com/library/content/documentation/
        #       Cocoa/Conceptual/TextLayout/Tasks/StringHeight.html>
        return self._height

    @property
    def heightAscender(self):
        '''Get the C{ascender} height (C{float}).
        '''
        return self.NS.ascender()

    @property
    def heightCap(self):
        '''Get the C{cap} height (C{float} or C{int}).
        '''
        return flint(self.NS.capHeight())

    @property
    def heightDescender(self):
        '''Get the C{descender} height (C{float}).
        '''
        return self.NS.descender()

    @property
    def heightLeading(self):
        '''Get the C{leading} height (C{float} or C{int}).
        '''
        return flint(self.NS.leading())

    @property
    def heightUnderline(self):
        '''Get the C{underline} position (C{float}).
        '''
        return self.NS.underlinePosition()

    @property
    def heightX(self):
        '''Get the C{x} height (C{float} or C{int}).
        '''
        return flint(self.NS.xHeight())

    @property
    def isBold(self):
        '''Get the B{Bold} trait (C{bool}).
        '''
        return self._isTrait(NSFontBoldMask)

    @property
    def isCompressed(self):
        '''Get the C{Compressed} trait (C{bool}).
        '''
        return self._isTrait(NSFontCompressedMask)

    @property
    def isCondensed(self):
        '''Get the C{Condensed} trait (C{bool}).
        '''
        return self._isTrait(NSFontCondensedMask)

    @property
    def isExpanded(self):
        '''Get the C{Expanded} trait (C{bool}).
        '''
        return self._isTrait(NSFontExpandedMask)

    @property
    def isItalic(self):
        '''Get the I{Italic} trait (C{bool}).
        '''
        return self._isTrait(NSFontItalicMask)

    @property
    def isMonoSpace(self):
        '''Get the C{MonoSpace} trait (C{bool}).
        '''
        return self._isTrait(NSFontMonoSpaceMask)

    @property
    def isNarrow(self):
        '''Get the C{Narrow} trait (C{bool}).
        '''
        return self._isTrait(NSFontNarrowMask)

    @property
    def isPoster(self):
        '''Get the C{Poster} trait (C{bool}).
        '''
        return self._isTrait(NSFontPosterMask)

    @property
    def isSansSerif(self):
        '''Get the C{SansSerif} "trait" (C{bool}).
        '''
        return self._isTrait(NSFontSansSerifClass)

    @property
    def isSmallCaps(self):
        '''Get the C{SmallCaps} trait (C{bool}).
        '''
        return self._isTrait(NSFontSmallCapsMask)

    @property
    def isUnBold(self):
        '''Get the C{UnBold} "trait" (C{bool}).
        '''
        return self._isTrait(NSFontUnboldMask)

    @property
    def isUnItalic(self):
        '''Get the C{UnItalic} "trait" (C{bool}).
        '''
        return self._isTrait(NSFontUnitalicMask)

    @property
    def isVertical(self):
        '''Get the C{Vertical} "trait" (C{bool}).
        '''
        return (True if self.NS.isVertical() else False) if self.NS else None

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

#   @property
#   def NSfontDescriptor(self):
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

    @property
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

    @property
    def slant(self):
        '''Get the italic angle (C{float}, C{int} or C{None}).
        '''
        return flint(self.NS.italicAngle()) if self.NS else None

    @property
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

    @property
    def vertical(self):
        '''Get the C{vertical} version of this font (L{Font} or C{None}).
        '''
        if self.isVertical:
            return self
        f = self.NS.vertical()
        if f and isInstanceOf(f, NSFont):
            return Font(f)
        return None

    @property
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
    '''Some pre-defined fonts.
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

    @property
    def App(self):
        '''Get the C{UserFont}.
        '''
        if self._App is None:
            _Fonts._App = Font(NSFont.userFontOfSize_(0))
        return self._App

    @property
    def Bold(self):
        '''Get the C{BoldFont}.
        '''
        if self._Bold is None:
            _Fonts._Bold = Font(NSFont.boldSystemFontOfSize_(0))
        return self._Bold

    @property
    def BoldItalic(self):
        '''Get the C{BoldItalicFont}.
        '''
        if self._BoldItalic is None:
            _Fonts._BoldItalic = Font(NSFont.boldSystemFontOfSize_(0)).traitsup(FontTrait.Italic)
        return self._BoldItalic

    @property
    def Italic(self):
        '''Get the C{ItalicFont}.
        '''
        if self._Italic is None:
            _Fonts._Italic = Font(NSFont.systemFontOfSize_(0)).traitsup(FontTrait.Italic)
        return self._Italic

    @property
    def Label(self):
        '''Get the C{LabelFont}.
        '''
        if self._Label is None:
            _Fonts._Label = Font(NSFont.labelFontOfSize_(0))
        return self._Label

    @property
    def Menu(self):
        '''Get the C{MenuFont}.
        '''
        if self._Menu is None:
            _Fonts._Menu = Font(NSFont.menuFontOfSize_(0))
        return self._Menu

    @property
    def MenuBar(self):
        '''Get the C{MenuBarFont}.
        '''
        if self._MenuBar is None:
            _Fonts._MenuBar = Font(NSFont.menuBarFontOfSize_(0))
        return self._MenuBar

    @property
    def Message(self):
        '''Get the C{MessageFont}.
        '''
        if self._Message is None:
            _Fonts._Message = Font(NSFont.messageFontOfSize_(0))
        return self._Message

    @property
    def MonoSpace(self):
        '''Get the C{MonoSpaceFont}.
        '''
        if self._MonoSpace is None:
            _Fonts._MonoSpace = Font(NSFont.userFixedPitchFontOfSize_(0))
        return self._MonoSpace

    @property
    def Palette(self):
        '''Get the C{PaletteFont}.
        '''
        if self._Palette is None:
            _Fonts._Palette = Font(NSFont.paletteFontOfSize_(0))
        return self._Palette

    @property
    def System(self):
        '''Get the C{SystemFont}.
        '''
        if self._System is None:
            _Fonts._System = Font(NSFont.systemFontOfSize_(0))
        return self._System

    @property
    def TableData(self):
        '''Get the C{TableDataFont}.
        '''
        if self._TableData is None:
            _Fonts._TableData = Font(NSMain.TableColumn.dataCell().font())
        return self._TableData

    @property
    def TableHeader(self):
        '''Get the C{TableHeaderFont}.
        '''
        if self._TableHeader is None:
            _Fonts._TableHeader = Font(NSMain.TableColumn.headerCell().font())
        return self._TableHeader

    @property
    def Title(self):
        '''Get the C{TitleFont}.
        '''
        if self._Title is None:
            _Fonts._Title = Font(NSFont.titleBarFontOfSize_(0))
        return self._Title


Fonts = _Fonts()  # pre-defined system fonts as L{Font}s


def fontfamilies(*prefixes):
    '''Yield the installed font families.

       @param prefixes: No, one or more font family names to match (C{str}-s).

       @return: Each font family name (C{str}).
    '''
    # <http://Developer.Apple.com/documentation/appkit/
    #       nsfontmanager/1462323-availablefontfamilies>
    for ns in nsIter(NSMain.FontManager.availableFontFamilies()):
        f = nsString2str(ns)
        if f.startswith(prefixes or f):
            yield f


def fontnamesof(family):
    '''Yield the available font names of a family.

       @param family: Generic font name (C{str}), like "Times" or "Helvetica".

       @return: The name (C{str}) of each font.
    '''
    # <http://Developer.Apple.com/documentation/appkit/
    #       nsfontmanager/1462316-availablemembers>
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
    # <http://Developer.Apple.com/documentation/appkit/
    #       nsfontmanager/1462316-availablemembers>
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
    # <http://Developer.Apple.com/documentation/appkit/
    #       nsfontmanager/1462316-availablemembers>
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

# filter locals() for .__init__.py
__all__ = _exports(locals(), starts=('Font', 'font'))

if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)

_ = '''

 fonts.__all__ = tuple(
   fonts.Font is <class .Font>,
   fonts.FontError is <class .FontError>,
   fonts.fontfamilies is <function .fontfamilies at 0x106b93b18>,
   fonts.fontnamesof is <function .fontnamesof at 0x106b97488>,
   fonts.Fonts.App=Font(name='Helvetica', family='Helvetica', size=12, weight=5),
              .Bold=Font(name='.AppleSystemUIFontBold', family='.AppleSystemUIFont', size=13, traits='Bold', weight=9),
              .BoldItalic=Font(name='.AppleSystemUIFontEmphasizedItalic', family='.AppleSystemUIFont', size=13, traits='Bold Italic', weight=9),
              .Italic=Font(name='.AppleSystemUIFontItalic', family='.AppleSystemUIFont', size=13, traits='Italic', weight=5),
              .Label=Font(name='.AppleSystemUIFont', family='.AppleSystemUIFont', size=10, weight=5),
              .Menu=Font(name='.AppleSystemUIFont', family='.AppleSystemUIFont', size=13, weight=5),
              .MenuBar=Font(name='.AppleSystemUIFont', family='.AppleSystemUIFont', size=14, weight=5),
              .Message=Font(name='.AppleSystemUIFont', family='.AppleSystemUIFont', size=13, weight=5),
              .MonoSpace=Font(name='Menlo-Regular', family='Menlo', size=11, traits='MonoSpace', weight=5),
              .Palette=Font(name='.AppleSystemUIFont', family='.AppleSystemUIFont', size=11, weight=5),
              .System=Font(name='.AppleSystemUIFont', family='.AppleSystemUIFont', size=13, weight=5),
              .TableData=Font(name='.AppleSystemUIFont', family='.AppleSystemUIFont', size=13, weight=5),
              .TableHeader=Font(name='.AppleSystemUIFont', family='.AppleSystemUIFont', size=11, weight=5),
              .Title=Font(name='.AppleSystemUIFont', family='.AppleSystemUIFont', size=13, weight=5),
   fonts.fontsof is <function .fontsof at 0x106b97500>,
   fonts.fontsof4 is <function .fontsof4 at 0x106b97578>,
   fonts.FontTrait.Bold=2,
                  .Compressed=1<<9,
                  .Condensed=1<<6,
                  .Expanded=1<<5,
                  .Italic=1,
                  .MonoSpace=1<<10,
                  .Narrow=1<<4,
                  .Poster=1<<8,
                  .SansSerif=1<<31,
                  .SmallCaps=1<<7,
                  .UnBold=1<<2,
                  .UnItalic=1<<24,
   fonts.FontTraitError is <class .FontTraitError>,
   fonts.fontTraits is <function .fontTraits at 0x106b975f0>,
   fonts.fontTraitstrs is <function .fontTraitstrs at 0x106b97668>,
 )[11]
 fonts.__version__ = '18.07.15'
'''
del _

# MIT License <http://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2018 -- mrJean1 at Gmail dot com
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
