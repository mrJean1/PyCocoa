
# -*- coding: utf-8 -*-

# MIT License <http://opensource.org/licenses/MIT>
#
# Copyright (C) 2017-2018 mrJean1 at Gmail dot com
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

'''Type L{Font}, etc., wrapping ObjC C{NSFont}.
'''
# all imports listed explicitly to help PyChecker
from bases   import _Type0
from nstypes import isNone, NSFont, NSFontManager, nsIter, nsIter2, \
                    NSLayoutManager, NSStr, nsString2str, NSTableColumn
from oslibs  import NSFontBoldMask, NSFontItalicMask, NSFontCompressedMask, \
                    NSFontCondensedMask, NSFontExpandedMask, \
                    NSFontMonoSpaceMask, NSFontNarrowMask, NSFontPosterMask, \
                    NSFontSmallCapsMask, NSFontSansSerifClass, \
                    NSFontUnboldMask, NSFontUnitalicMask
from runtime import isInstanceOf
from strs    import Str
from utils   import bytes2str, _ByteStrs, _Constants, _exports, \
                    flint, instanceof, _Ints, _Types

__version__ = '18.05.16'

_NSFM = NSFontManager.sharedFontManager()
_NSLM = NSLayoutManager.alloc().init()
_NSTC = NSTableColumn.alloc().init()  # PYCHOK false

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


FontTrait = FontTrait()  #: Font trait constants (C{mask}).

# dict for Font.traitsup() to update traits with family traits
_familyTraits = dict((n.lower(), m) for n, m in FontTrait.items()
                                     if not n.startswith('Un'))
_familyTraits.update(dict(black=NSFontBoldMask,
                  #        book=0,
                  #    chancery=0,
                  #        demi=0,
                     extrablack=NSFontBoldMask,
                      extrabold=NSFontBoldMask,
                  #  extralight=0,
                          heavy=NSFontBoldMask,
                  #    inclined=0,
                  #      inline=0,
                  #       light=0,
                  #      medium=0,
                           mono=NSFontMonoSpaceMask,
                        oblique=NSFontItalicMask,
                  #     outline=0,  # Braille
                  #    pinpoint=0,  # Braille
                  #       plain=0,
                  #     regular=0,
                  #       roman=0,
                           sans=NSFontSansSerifClass,  # exception
                  #        semi=0,
                       semibold=NSFontBoldMask,
                  #       solid=0,
                  #        text=0,
                  #        thin=0,
                  #       ultra=0,
                  #  ultralight=0,
                      ultrabold=NSFontBoldMask))
# all valid traits
_maskTraits = 0
for _, m in FontTrait.items():
    _maskTraits |= m

_ = n = m = None; del _, n, m  # PYCHOK expected


def _traitex(traits, mask):
    # check exclusivity
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
    if _traitex(ts, NSFontCondensedMask | NSFontExpandedMask) or \
       _traitex(ts, NSFontItalicMask    | NSFontUnitalicMask) or \
       _traitex(ts, NSFontBoldMask      | NSFontUnboldMask):
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
    _family = ''
    _height = 0
    _name   = ''
    _size   = 0
    _traits = 0
    _weight = None

    def __init__(self, family, size=0, traits=0, weight=5):
        '''New L{Font}.

           @param family: Generic font name (C{str}, L{Str}, C{NSStr},
                          L{Font} or C{NSFont}), like "Times" or "Helvetica".
           @keyword size: Desired point size (C{int}), zero for any.
           @keyword traits: Desired font traits (C{str} or C{FontTrait}C{s mask}).
           @keyword weigth: Desired book weight (C{int}) in range 0..15, where
                            0=light, 5=regular, 9=bold and 15=heavy.

           @raise FontError: No such I{family} or font.

           @raise FontTraitError: Mutually exclusive I{traits}.

           @raise TypeError: Invalid I{family}.

           @raise ValueError: Invalid I{weight}.

           @note: The new L{Font} may not exhibit the desired I{traits}
                  and I{weight}.  The I{weight} is ignored if I{traits}
                  includes C{FontTrait.Bold}.

           @see: Function L{fontsof} to obtain all available fonts of
                 a particular font family.
        '''
        if isinstance(family, Str):
            ns, py = family.NS, str(family)
        elif isinstance(family, _ByteStrs):
            ns, py = NSStr(family), bytes2str(family)
        elif isinstance(family, NSStr):
            ns, py = family, nsString2str(family)
#       elif isInstanceOf(family, NSFontDescriptor):
#           ns, py = ..., ...
        elif isInstanceOf(family, NSFont, name='family'):
            ns, py = family, None
            if size == 0:
                size = ns.pointSize()
            if traits == 0:
                traits = _NSFM.traitsOfFont_(ns)
            if not (size == ns.pointSize() and
                    traits == _NSFM.traitsOfFont_(ns)):
                ns = ns.familyName()
                py = nsString2str(ns)

        if py is not None:
            # <http://Developer.Apple.com/documentation/appkit/
            #       nsfontmanager/1462332-fontwithfamily>
            self._traits = _traitsin(traits)
            self._weight = _weightin(weight)
            ns = _NSFM.fontWithFamily_traits_weight_size_(ns,
                                                    self._traits,
                                                    self._weight, size)
            if isNone(ns):
                self._family = py
                self._size   = flint(size)
                raise FontError('no such %s: %s' % ('font', self._argstr()))

        self.NS = ns
        # <http://Developer.Apple.com/library/content/documentation/
        #  TextFonts/Conceptual/CocoaTextArchitecture/FontHandling/FontHandling.html>
        self._family = nsString2str(ns.familyName())
        self._height = flint(_NSLM.defaultLineHeightForFont_(ns) + 1)
        self._name   = nsString2str(ns.fontName())
        self._size   = flint(ns.pointSize())
        # traits not always reflect actual traits
        self._traits = _NSFM.traitsOfFont_(ns) or 0
        # update with the family traits, if any
        self._traits |= _traitsin(self._family, raiser=False)
        if ns.isFixedPitch() and not self.isMonoSpace:
            self._traits |= NSFontMonoSpaceMask
        self._weight = _NSFM.weightOfFont_(ns)

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
        '''
        return flint(self._height)

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
            ns = NSStr(bstr)
        elif instanceof(bstr, NSStr, name='bstr'):
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


class Fonts(_Constants):
    '''Some pre-defined fonts.
    '''
    App         = Font(NSFont.userFontOfSize_(0))
    Bold        = Font(NSFont.boldSystemFontOfSize_(0))
    BoldItalic  = Font(NSFont.boldSystemFontOfSize_(0)).traitsup(FontTrait.Italic)
    Italic      = Font(NSFont.systemFontOfSize_(0)).traitsup(FontTrait.Italic)
    Label       = Font(NSFont.labelFontOfSize_(0))
    Menu        = Font(NSFont.menuFontOfSize_(0))
    MenuBar     = Font(NSFont.menuBarFontOfSize_(0))
    Message     = Font(NSFont.messageFontOfSize_(0))
    MonoSpace   = Font(NSFont.userFixedPitchFontOfSize_(0))
    Palette     = Font(NSFont.paletteFontOfSize_(0))
    System      = Font(NSFont.systemFontOfSize_(0))
    TableData   = Font(_NSTC.dataCell().font())
    TableHeader = Font(_NSTC.headerCell().font())
    Title       = Font(NSFont.titleBarFontOfSize_(0))


Fonts = Fonts()  #: Pre-defined system fonts (L{Font}).


def fontfamilies(*prefixes):
    '''Yield the installed font families.

       @param prefixes: No, one or more font family names to match (C{str}-s).

       @return: Each font family name (C{str}).
    '''
    # <http://Developer.Apple.com/documentation/appkit/
    #       nsfontmanager/1462323-availablefontfamilies>
    for ns in nsIter(_NSFM.availableFontFamilies()):
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
    for ns in nsIter(_NSFM.availableMembersOfFontFamily_(NSStr(family))):
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
    for (n, m, w, t), _ in nsIter2(_NSFM.availableMembersOfFontFamily_(NSStr(family))):
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
    for t4, _ in nsIter2(_NSFM.availableMembersOfFontFamily_(NSStr(family))):
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

    def _itemf(fmt, *args):
        t = fmt % args
        d = t.find('.App=')
        if d > 0:
            d = ' ' * (d + 1)
            t = t.replace('), .', ')\n' + d + '.')
        return t

    _allisting(__all__, locals(), __version__, __file__, itemf=_itemf)

_ = '''

 fonts.__all__ = tuple(
   fonts.Font is <class .Font>,
   fonts.FontError is <class .FontError>,
   fonts.fontfamilies is <function .fontfamilies at 0x1022c78c0>,
   fonts.fontnamesof is <function .fontnamesof at 0x1022ccb18>,
   fonts.Fonts is Fonts.App=Font(name='Helvetica', family='Helvetica', size=12, weight=5)
                       .Bold=Font(name='.SFNSText-Bold', family='.SF NS Text', size=13, traits='Bold', weight=9)
                       .BoldItalic=Font(name='.SFNSText-BoldItalic', family='.SF NS Text', size=13, traits='Bold Italic', weight=9)
                       .Italic=Font(name='.SFNSText-Italic', family='.SF NS Text', size=13, traits='Italic', weight=5)
                       .Label=Font(name='.AppleSystemUIFont', family='.AppleSystemUIFont', size=10, weight=5)
                       .Menu=Font(name='.AppleSystemUIFont', family='.AppleSystemUIFont', size=13, weight=5)
                       .MenuBar=Font(name='.AppleSystemUIFont', family='.AppleSystemUIFont', size=14, weight=5)
                       .Message=Font(name='.AppleSystemUIFont', family='.AppleSystemUIFont', size=13, weight=5)
                       .MonoSpace=Font(name='Monaco', family='Monaco', size=10, traits='MonoSpace', weight=5)
                       .Palette=Font(name='.AppleSystemUIFont', family='.AppleSystemUIFont', size=11, weight=5)
                       .System=Font(name='.SFNSText', family='.SF NS Text', size=13, weight=5)
                       .TableData=Font(name='.SFNSText', family='.SF NS Text', size=13, weight=5)
                       .TableHeader=Font(name='.SFNSText', family='.SF NS Text', size=11, weight=5)
                       .Title=Font(name='.AppleSystemUIFont', family='.AppleSystemUIFont', size=13, weight=5),
   fonts.fontsof is <function .fontsof at 0x1022ccb90>,
   fonts.fontsof4 is <function .fontsof4 at 0x1022ccc08>,
   fonts.FontTrait is FontTrait.Bold=2, .Compressed=1<<9, .Condensed=1<<6, .Expanded=1<<5, .Italic=1, .MonoSpace=1<<10, .Narrow=1<<4, .Poster=1<<8, .SansSerif=1<<31, .SmallCaps=1<<7, .UnBold=1<<2, .UnItalic=1<<24,
   fonts.FontTraitError is <class .FontTraitError>,
   fonts.fontTraits is <function .fontTraits at 0x1022ccc80>,
   fonts.fontTraitstrs is <function .fontTraitstrs at 0x1022cccf8>,
 )[11]
 fonts.__version__ = '18.05.15'
'''
del _
