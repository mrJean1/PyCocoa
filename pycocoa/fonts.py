
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
@var Fonts.TitleBar: Get the C{TitleBarFont}.

@var FontDesign: Font design constants (C{int}), arbitrary.
@var FontDesign.Default: 0
@var FontDesign.MonoSpaced: 1
@var FontDesign.Rounded: 2
@var FontDesign.Serif: 3

@var FontTextStyle: Font text style constants (C{int}), arbitrary.
@var FontTextStyle.Body: 11
@var FontTextStyle.Callout: 31
@var FontTextStyle.Caption: 21
@var FontTextStyle.Caption2: 22
@var FontTextStyle.Footnote: 41
@var FontTextStyle.Headline: 51
@var FontTextStyle.HeadlineSub: 50
@var FontTextStyle.SubHeadline: 50
@var FontTextStyle.Title: 61
@var FontTextStyle.Title2: 62
@var FontTextStyle.Title3: 63
@var FontTextStyle.TitleExtraLarge: 72
@var FontTextStyle.TitleExtraLarge2: 73
@var FontTextStyle.TitleLarge: 82

@var FontTrait: Font trait constants (C{mask}).
@var FontTrait.Bold: 0x2
@var FontTrait.Compressed: 0x200
@var FontTrait.Condensed: 0x40
@var FontTrait.Expanded: 0x20
@var FontTrait.Italic: 0x1
@var FontTrait.MonoSpace: 0x400
@var FontTrait.Narrow: 0x10
@var FontTrait.Poster: 0x100
@var FontTrait.SansSerif: 0x80000000
@var FontTrait.SmallCaps: 0x80
@var FontTrait.UnBold: 0x4
@var FontTrait.UnItalic: 0x1000000

@var FontWeight: Font weight constants (C{int}).
@var FontWeight.Black: 12
@var FontWeight.Bold: 9
@var FontWeight.BoldSemi: 8
@var FontWeight.Hairline: 0
@var FontWeight.Heavy: 15
@var FontWeight.Light: 0
@var FontWeight.Medium: 7
@var FontWeight.Normal: 5
@var FontWeight.Regular: 5
@var FontWeight.SemiBold: 8
@var FontWeight.Thin: 2
'''
from pycocoa.bases import _Type0
from pycocoa.internals import _Constants, _Dmain_, _DOT_, bytes2str, \
                              _ByteStrs, _fmt_invalid, _instr, _Ints, \
                              _NN_, property_RO, _Singletons, _SPACE_
from pycocoa.lazily import _ALL_LAZY, _Types
from pycocoa.nstypes import isNone, NSFont, nsIter, NSMain, NSStr, \
                           _NSStr, nsString2str, ns2Type
from pycocoa.oslibs import NSFontBoldMask, NSFontItalicMask, \
                           NSFontCompressedMask, NSFontCondensedMask, \
                           NSFontExpandedMask, NSFontMonoSpaceMask, \
                           NSFontNarrowMask, NSFontPosterMask, \
                           NSFontSmallCapsMask, NSFontSansSerifClass, \
                           NSFontUnboldMask, NSFontUnitalicMask
from pycocoa.runtime import isObjCInstanceOf
from pycocoa.strs import Str
from pycocoa.utils import flint, isinstanceOf

__all__ = _ALL_LAZY.fonts
__version__ = '25.03.18'

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


class Font(_Type0):
    '''Python C{Font} Type, wrapping ObjC C{NSFont}.
    '''
    _family = _NN_
    _height =  0
    _name   = _NN_
    _size   =  0
    _traits =  0
    _weight =  None

    def __init__(self, family_or_font, size=0, traits=0, weight=5):  # MCCABE 13
        '''New L{Font}.

           @param family_or_font: Generic font name (C{str}, L{Str}, L{NSStr})
                                  like "Times" or "Helvetica" or a L{Font},
                                  C{NSFont} or C{NSFontDescriptor} instance.
           @keyword size: Desired point size (C{int}), zero for any.
           @keyword traits: Desired font traits (C{str} or C{FontTrait}C{s mask}).
           @keyword weigth: Desired book weight (C{FontWeigt}, C{int}) in range
                            0..15, where 0=Light, 5=Regular, 9=Bold and 15=Heavy.

           @raise FontError: No such I{family_or_font}.

           @raise FontTraitError: Mutually exclusive I{traits}.

           @raise TypeError: Invalid I{family_or_font}.

           @raise ValueError: Invalid I{weight}.

           @note: The new L{Font} may not exhibit the desired I{traits} and I{weight}.
                  The I{weight} is ignored if I{traits} include C{FontTrait.Bold},
                  both I{traits} and I{weight} are ignored if I{family_or_font} is
                  C{NSFontDescriptor}.

           @see: Function L{fontsOf} to obtain all available fonts of a particular
                 font family.
        '''
        f, FM = family_or_font, NSMain.FontManager
        if isinstance(f, Str):
            ns, py =  f.NS, str(f)
        elif isinstance(f, _ByteStrs):
            ns, py = _NSStr(f), bytes2str(f)
        elif isinstance(f, NSStr):
            ns, py =  f, nsString2str(f)
#       elif isObjCInstanceOf(f, NSFontDescriptor):
            # <https://Developer.Apple.com/documentation/appkit/nsfont/1525386-init>
            # ignore traits and weight
#           ns, py = NSFont.alloc().init_(f, size), None
        elif isinstance(f, Font):
            ns, py =  f.NS, None
        elif isObjCInstanceOf(f, NSFont, raiser='family_or_font'):
            ns, py =  f,    None

        if py is None:
            if not size:
                size = ns.pointSize()
            if not traits:
                traits = FM.traitsOfFont_(ns)
            if size   != ns.pointSize() or \
               traits != FM.traitsOfFont_(ns):
                ns = ns.familyName()
                py = nsString2str(ns)

        if py is not None:
            # <https://Developer.Apple.com/documentation/appkit/
            #        nsfontmanager/1462332-fontwithfamily>
            self._traits = FontTrait(traits)
            self._weight = FontWeight(weight)
            ns = FM.fontWithFamily_traits_weight_size_(
                    ns, self._traits, self._weight, size)
            if isNone(ns):
                self._family, self._size = py, flint(size)
                t = _fmt_invalid(font=str(self._kwds()))
                raise FontError(t)

        self._NS = ns  # _RO
        # <https://Developer.Apple.com/library/content/documentation/
        #  TextFonts/Conceptual/CocoaTextArchitecture/FontHandling/FontHandling.html>
        self._name   = nsString2str(ns.fontName())
        self._family = nsString2str(ns.familyName())
        self._size   = flint(ns.pointSize())
        self._height = flint(NSMain.LayoutManager.defaultLineHeightForFont_(ns) + 1)
        # traits not always reflect actual, family traits
        self._traits = FontTrait(self._family, FM.traitsOfFont_(ns), raiser=False)
        if ns.isFixedPitch() and not self.isMonoSpace:
            self._traits |= FontTrait.MonoSpace
        self._weight = FM.weightOfFont_(ns)

    def __str__(self):
        t, n = self.typename, self.name
        if n:
            t = _DOT_(t, n)
        return _instr(t, **self._kwds())

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
        b = NSMain.LayoutManager.defaultBaselineOffsetForFont_(self.NS)
        return flint(b)

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

    def _isTrait(self, mask):
        return bool(self._traits & mask)  # XXX == mask?

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
        '''Get the C{Vertical} "trait" (C{bool} or C{None} if unknown).
        '''
        return bool(self.NS.isVertical()) if self.NS else None

    def _kwds(self):
        d = dict(family=self.family, size=self.size)
        t = tuple(FontTrait._traitsOf(self))
        if t:
            d.update(traits=repr(_SPACE_(*t)))
        if self.weight is not None:
            d.update(weight=self.weight)
        return d

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
        if size != self.size:
            ns = self.family
            if size:
                f = self.NS.fontWithSize_(size)
                if not isNone(f):
                    ns = f
            f = Font(ns, size=size, traits=self.traits,
                                    weight=self.weight)
        else:
            f = self  # XXX copy?
        return f

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
            ns =  bstr.NS
        elif isinstance(bstr, _ByteStrs):
            ns = _NSStr(bstr)
        elif isinstanceOf(bstr, NSStr, raiser='bstr'):
            ns =  bstr
        w = self.NS.widthOfString_(ns)
        return flint(w), self.height

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
        M = self._traits
        for t in traits:
            M = FontTrait(t, M)
        return Font(self.NS, traits=M)

    @property_RO
    def vertical(self):
        '''Get the C{vertical} version of this font (L{Font} or C{None}).
        '''
        if self.isVertical:
            f = self
        else:
            f = self.NS.vertical()
            if f and isObjCInstanceOf(f, NSFont):
                f = Font(f)
            else:
                f = None
        return f

    @property_RO
    def weight(self):
        '''Get the book C{weight} of the font (C{int} or C{None}).
        '''
        return self._weight


class FontDesign(_Constants):
    '''Font design constants (C{int}), I{arbitrary}.
    '''
    Default    = 0  # arbitrary
    MonoSpaced = 1
    Rounded    = 2
    Serif      = 3

FontDesign = FontDesign()  # PYCHOK constants


class FontError(ValueError):
    '''Font selection error.
    '''
    pass


class FontTraitError(FontError):
    '''Font traits error.
    '''
    pass


class FontTextStyle(_Constants):
    '''Font text style constants (C{int}), I{arbitrary}.
    '''
    Body             = 11
    Caption          = 21
    Caption2         = 22
    Callout          = 31
    Footnote         = 41
    Headline         = 51
    HeadlineSub      = \
    SubHeadline      = 50
    Title            = 61
    Title2           = 62
    Title3           = 63
    TitleExtraLarge  = 72
    TitleExtraLarge2 = 73
    TitleLarge       = 82

FontTextStyle = FontTextStyle()  # PYCHOK constants


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

    @property_RO
    def _familyTraits(self):
        '''(INTERNAL) Get a C{dict} of traits, I{once}.
        '''
        d = dict((n.lower(), m) for n, m in self.items() if
                                not n.startswith('Un'))
        T = self  # FontTrait
        d.update(black=T.Bold,
        #         book=0,
        #     chancery=0,
        #         demi=0,
            extrablack=T.Bold,
             extrabold=T.Bold,
        #   extralight=0,
                 heavy=T.Bold,
        #     inclined=0,
        #        inline=0,
        #        light=0,
        #       medium=0,
                  mono=T.MonoSpace,
               oblique=T.Italic,
        #      outline=0,  # Braille
        #     pinpoint=0,  # Braille
        #        plain=0,
        #      regular=0,
        #        roman=0,
                  sans=T.SansSerif,  # exception
        #         semi=0,
              semibold=T.Bold,
        #        solid=0,
        #         text=0,
        #         thin=0,
        #        ultra=0,
        #   ultralight=0,
             ultrabold=T.Bold)
        self.__dict__.update(_familyTraits=d)  # cached
        return d

    def __call__(self, traits, mask=0, raiser=True):
        # Convert and check traits
        if isinstance(traits, _ByteStrs):
            M  = 0
            _g = self._familyTraits.get
            for t in bytes2str(traits).strip().split():
                m = _g(t.lower(), None)
                if m:
                    M |= m
                elif raiser and m is None:
                    t = _fmt_invalid(trait=repr(t))
                    raise FontTraitError(t)
        elif isinstance(traits, _Ints):
            M  = int(traits)
        else:
            t = _fmt_invalid(traits=repr(traits))
            raise FontTraitError(t)

        if mask:
            M |= mask
        # check for some mutually-exclusive traits
        for m in self._mutexTraits:
            if (M & m) == m:
                t = ' | '.join(fontTraitstrs(m))
                t = _fmt_invalid('compatible', traits=t)
                raise FontTraitError(t)
        return M & self._traitsMask

    @property_RO
    def _mutexTraits(self):
        '''(INTERNAL) Some mutually-exclusive trait masks, I{once}.
        '''
        T =  self  # FontTrait
        t = (T.Condensed | T.Expanded,
             T.Italic    | T.UnItalic,
             T.Bold      | T.UnBold)
        self.__dict__.update(_mutexTraits=t)  # cached
        return t

    @property_RO
    def _traitsMask(self):
        '''(INTERNAL) Get the combined traits mask, I{once}.
        '''
        M = 0
        for _, m in self.items():
            M |= m
        self.__dict__.update(_traitsMask=M)  # cached
        return M

    def _traitsNames(self, mask):
        '''(INTERNAL) Yield the trait names in I{mask}.
        '''
        for n, m in self.items():
            if (m & mask):
                yield n

    def _traitsOf(self, font):
        '''(INTERNAL) Yield the trait names of a C{font}.
        '''
        for n in self.keys():
            if getattr(font, 'is' + n, 0):
                yield n

FontTrait = FontTrait()  # PYCHOK contants


class FontWeight(_Constants):
    '''Font weight constants (C{int}) from C{UltraLight} to C{Heavy}.
    '''
    Black      = 12
    Bold       = 9
    BoldSemi   = \
    SemiBold   = 8
    Hairline   = \
    Light      = 1
    Heavy      = 15
    Medium     = 7
    Normal     = \
    Regular    = 5
    Thin       = 3
    UltraLight = 0

    def __call__(self, weight):
        # check and return I{weight}
        try:
            return int(weight) if (isinstance(weight, _Ints) and
                           self.UltraLight <= weight <= self.Heavy) else \
                   self.iget(bytes2str(weight))
        except (AttributeError, TypeError, ValueError):
            pass
        t = _fmt_invalid(weight=repr(weight))
        raise ValueError(t)

FontWeight = FontWeight()  # PYCHOK constants


class _Fonts(_Singletons):
    '''Pre-defined system fonts, all L{Font} instances.
    '''

    @property_RO
    def App(self):
        '''Get the C{UserFont}.
        '''
        return self._setFont0(App=NSFont.userFontOfSize_)

    @property_RO
    def Bold(self):
        '''Get the C{BoldFont}.
        '''
        return self._setFont0(Bold=NSFont.boldSystemFontOfSize_)

    @property_RO
    def BoldItalic(self):
        '''Get the C{BoldItalicFont}.
        '''
        return self._set(BoldItalic=self.Bold.traitsup(FontTrait.Italic))

    def _fonts(self, prefixes, NS_):
        for ns in nsIter(NS_()):
            f = nsString2str(ns)
            if f.startswith(prefixes or f):
                yield f

    def _fontsOf(self, family, ns_):
        fn = NSStr(family)
        ns = NSMain.FontManager.availableMembersOfFontFamily_(fn)
        fn.release()  # PYCHOK expected
        for ns in nsIter(ns):
            yield ns_(ns)

    @property_RO
    def Italic(self):
        '''Get the C{ItalicFont}.
        '''
        return self._set(Italic=self.System.traitsup(FontTrait.Italic))

    @property_RO
    def Label(self):
        '''Get the C{LabelFont}.
        '''
        return self._setFont0(Label=NSFont.labelFontOfSize_)

    @property_RO
    def Menu(self):
        '''Get the C{MenuFont}.
        '''
        return self._setFont0(Menu=NSFont.menuFontOfSize_)

    @property_RO
    def MenuBar(self):
        '''Get the C{MenuBarFont}.
        '''
        return self._setFont0(MenuBar=NSFont.menuBarFontOfSize_)

    @property_RO
    def Message(self):
        '''Get the C{MessageFont}.
        '''
        return self._setFont0(Message=NSFont.messageFontOfSize_)

    @property_RO
    def MonoSpace(self):
        '''Get the C{MonoSpaceFont}.
        '''
        return self._setFont0(MonoSpace=NSFont.userFixedPitchFontOfSize_)

    @property_RO
    def Palette(self):
        '''Get the C{PaletteFont}.
        '''
        return self._setFont0(Palete=NSFont.paletteFontOfSize_)

    def _setFont(self, **name_NS):
        name, NS = name_NS.popitem()
        # assert self._isAlnum(name)
        return self._set(**{name: Font(NS)})

    def _setFont0(self, **name_NS_):
        name, NS_ = name_NS_.popitem()
        # assert self._isAlnum(name) and NS_.name.endswith('FontOfSize_')
        return self._set(**{name: Font(NS_(0))})

    @property_RO
    def System(self):
        '''Get the C{SystemFont}.
        '''
        return self._setFont0(System=NSFont.systemFontOfSize_)

    @property_RO
    def TableData(self):
        '''Get the C{TableDataFont}.
        '''
        return self._setFont(TableData=NSMain.TableColumn.dataCell().font())

    @property_RO
    def TableHeader(self):
        '''Get the C{TableHeaderFont}.
        '''
        return self._setFont(TableHeader=NSMain.TableColumn.headerCell().font())

    @property_RO
    def Title(self):
        '''Get the C{TitleFont}.
        '''
        return self._set(Title=self.TitleBar)

    @property_RO
    def TitleBar(self):
        '''Get the C{TitleBarFont}.
        '''
        return self._setFont0(TitleBar=NSFont.titleBarFontOfSize_)

Fonts = _Fonts()  # PYCHOK singletons


def fontFamilies(*prefixes):
    '''Yield the installed font families.

       @param prefixes: No, one or more font family names to match (C{str}-s).

       @return: Each font family name (C{str}).
    '''
    # <https://Developer.Apple.com/documentation/appkit/
    #        nsfontmanager/1462323-availablefontfamilies>
    return Fonts._fonts(prefixes, NSMain.FontManager.availableFontFamilies)


def fontNamesOf(family):
    '''Yield the available font names of a family.

       @param family: Generic font name (C{str}), like "Times" or "Helvetica".

       @return: The name (C{str}) of each font.
    '''
    def _ns2str(ns):
        return nsString2str(ns.objectAtIndex_(0))

    # <https://Developer.Apple.com/documentation/appkit/
    #        nsfontmanager/1462316-availablemembers>
    return Fonts._fontsOf(family, _ns2str)


def fonts(*prefixes):
    '''Yield all available fonts.

       @param prefixes: No, one or more font family names to match (C{str}-s).

       @return: Each font name (C{str}).
    '''
    # <https://Developer.Apple.com/documentation/appkit/
    #        nsfontmanager/1462323-availablefontfamilies>
    return Fonts._fonts(prefixes, NSMain.FontManager.availableFonts)


def fontsOf(family, size=0, weight=None):
    '''Yield the available fonts of a family.

       @param family: Generic font name (C{str}), like "Times" or "Helvetica".
       @keyword size: The point size (C{int}), zero for any.
       @keyword weight: The book weight (C{int}), C{None} for any.

       @return: A (L{Font}) instance for each family font.

       @raise ValueError: Invalid I{weight}.
    '''
    if weight is None:
        lw,  hw = FontWeight.UltraLight, FontWeight.Heavy
    else:
        lw = hw = FontWeight(weight)
    # <https://Developer.Apple.com/documentation/appkit/
    #        nsfontmanager/1462316-availablemembers>
    for n, m, w, t in Fonts._fontsOf(family, ns2Type):
        # each item is [name, trait-like attributes, weight, traits]
        if lw <= w <= hw:
            try:
                f = Font(family, size=size, traits=t, weight=w)
                f.name = n
            except (FontError, FontTraitError):
                continue
            f._traits = FontTrait(m, f._traits, raiser=False)  # family traits
            yield f


def fontsOf4(family):
    '''Yield the available fonts of a family.

       @param family: Generic font name (C{str}), like "Times" or "Helvetica".

       @return: 4-Tuple (fontname, attributes, weight, traits) of (C{str},
                C{str}, C{int}, C{mask}) for each family font.
    '''
    # <https://Developer.Apple.com/documentation/appkit/
    #        nsfontmanager/1462316-availablemembers>
    for t4 in Fonts._fontsOf(family, ns2Type):
        # each item is [fontname, trait-like-attributes, weight, traits]
        yield tuple(t4)


def fontTraits(*traits):
    '''Return the traits mask for the named traits.

       @param traits: Trait names (C{str}s), case-insensitive.

       @return: Combined traits (C{mask}).

       @raise FontTraitError: One or more I{traits} are invalid
                              or incompatible, mutually exclusive.
    '''
    M = 0
    for t in traits:
        M |= FontTrait(t)
    return M


def fontTraitstrs(traits):
    '''Return the font trait names for a traits mask.

       @param traits: The traits (C{mask}).

       @return: Tuple of trait names (C{str}s).
    '''
    return tuple(sorted(FontTrait._traitsNames(traits)))


NSFont._Type = _Types.Font = Font

if __name__ == _Dmain_:

    from pycocoa.utils import _all_listing, _varstr

    print(_varstr(Fonts))
    print(_varstr(FontDesign, strepr=str))
    print(_varstr(FontTextStyle, strepr=str))
    print(_varstr(FontTrait, strepr=hex))
    print(_varstr(FontWeight, strepr=str))

    _all_listing(__all__, locals())

# % python3 -m pycocoa.fonts
#
# pycocoa.fonts.__all__ = tuple(
#  pycocoa.fonts.Font is <class .Font>,
#  pycocoa.fonts.FontDesign.Default=0,
#                          .MonoSpaced=1,
#                          .Rounded=2,
#                          .Serif=3,
#  pycocoa.fonts.FontError is <class .FontError>,
#  pycocoa.fonts.fontFamilies is <function .fontFamilies at 0x104f7c900>,
#  pycocoa.fonts.fontNamesOf is <function .fontNamesOf at 0x1052d1ee0>,
#  pycocoa.fonts.Fonts.App=Font.Helvetica(family=Helvetica, size=12, weight=5),
#                     .Bold=Font..AppleSystemUIFontBold(family=.AppleSystemUIFont, size=13, traits=Bold, weight=9),
#                     .BoldItalic=Font..AppleSystemUIFontEmphasizedItalic(family=.AppleSystemUIFont, size=13, traits=Bold Italic, weight=9),
#                     .Italic=Font..AppleSystemUIFontItalic(family=.AppleSystemUIFont, size=13, traits=Italic, weight=5),
#                     .Label=Font..AppleSystemUIFont(family=.AppleSystemUIFont, size=10, weight=5),
#                     .Menu=Font..AppleSystemUIFont(family=.AppleSystemUIFont, size=13, weight=5),
#                     .MenuBar=Font..AppleSystemUIFont(family=.AppleSystemUIFont, size=13, weight=5),
#                     .Message=Font..AppleSystemUIFont(family=.AppleSystemUIFont, size=13, weight=5),
#                     .MonoSpace=Font.Menlo-Regular(family=Menlo, size=11, traits=MonoSpace, weight=5),
#                     .Palette=Font..AppleSystemUIFont(family=.AppleSystemUIFont, size=11, weight=5),
#                     .System=Font..AppleSystemUIFont(family=.AppleSystemUIFont, size=13, weight=5),
#                     .TableData=Font..AppleSystemUIFont(family=.AppleSystemUIFont, size=13, weight=5),
#                     .TableHeader=Font..SFNS-Regular(family=.AppleSystemUIFont, size=11, weight=5),
#                     .Title=Font..AppleSystemUIFaceHeadline(family=.AppleSystemUIFont, size=13, traits=Bold, weight=8),
#                     .TitleBar=Font..AppleSystemUIFaceHeadline(family=.AppleSystemUIFont, size=13, traits=Bold, weight=8),
#  pycocoa.fonts.fontsOf is <function .fontsOf at 0x1052d1f80>,
#  pycocoa.fonts.fontsOf4 is <function .fontsOf4 at 0x1052d2020>,
#  pycocoa.fonts.FontTextStyle.Body=11,
#                             .Callout=31,
#                             .Caption=21,
#                             .Caption2=22,
#                             .Footnote=41,
#                             .Headline=51,
#                             .HeadlineSub=50,
#                             .SubHeadline=50,
#                             .Title=61,
#                             .Title2=62,
#                             .Title3=63,
#                             .TitleExtraLarge=72 or 9<<3,
#                             .TitleExtraLarge2=73,
#                             .TitleLarge=82,
#  pycocoa.fonts.FontTrait.Bold=2,
#                         .Compressed=512 or 1<<9,
#                         .Condensed=64 or 1<<6,
#                         .Expanded=32 or 1<<5,
#                         .Italic=1,
#                         .MonoSpace=1024 or 1<<10,
#                         .Narrow=16 or 1<<4,
#                         .Poster=256 or 1<<8,
#                         .SansSerif=2147483648 or 1<<31,
#                         .SmallCaps=128 or 1<<7,
#                         .UnBold=4 or 1<<2,
#                         .UnItalic=16777216 or 1<<24,
#  pycocoa.fonts.FontTraitError is <class .FontTraitError>,
#  pycocoa.fonts.fontTraits is <function .fontTraits at 0x1052d20c0>,
#  pycocoa.fonts.fontTraitstrs is <function .fontTraitstrs at 0x1052d2160>,
#  pycocoa.fonts.FontWeight.Black=12 or 3<<2,
#                          .Bold=9,
#                          .BoldSemi=8 or 1<<3,
#                          .Hairline=0,
#                          .Heavy=15,
#                          .Light=0,
#                          .Medium=7,
#                          .Normal=5,
#                          .Regular=5,
#                          .SemiBold=8 or 1<<3,
#                          .Thin=2,
# )[14]
# pycocoa.fonts.version 25.3.18, .isLazy 1, Python 3.13.2 64bit arm64, macOS 15.3.2

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2025 -- mrJean1 at Gmail -- All Rights Reserved.
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
