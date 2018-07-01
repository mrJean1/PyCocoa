
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Type L{Str}, wrapping ObjC C{NSStr[ing]}.
'''
# all imports listed explicitly to help PyChecker
from bases   import _Type0
from nstypes import NSAttributedString, NSConstantString, \
                    NSStr, NSString, nsString2str
from pytypes import dict2NS, str2NS
from utils   import isinstanceOf, _Strs, _Types

__all__ = ('Str', 'StrAttd')
__version__ = '18.06.28'


class Str(str, _Type0):  # str, first to maintain str behavior
    '''Python C{str} Type, wrapping (immutable) ObjC C{NSStr[ing]}.
    '''

    def __new__(cls, ns_str=''):
        '''New L{Str} from C{str}, L{Str} or C{NSStr[ing]}.
        '''
        if isinstance(ns_str, Str):
            return ns_str
        elif isinstance(ns_str, _Strs):
            ns, py = str2NS(ns_str), ns_str
        elif isinstanceOf(ns_str, NSStr, name='ns_str'):
            ns, py = ns_str, nsString2str(ns_str)

        self = super(Str, cls).__new__(cls, py)
        self._NS = ns  # immutable
        return self

    def copy(self, *ranged):
        '''Return a copy of this string.

          @param ranged: Optional index range.

          @return: The copy (L{Str}).
        '''
        if ranged:
            s = self[slice(*ranged)]
        else:
            s = self
        return self.__class__(s)


class StrAttd(Str, _Type0):
    '''Python C{str} Type, wrapping (immutable) ObjC L{NSAttributedString}.
    '''
    _attachment      = None
    _backgroundColor = None
    _baselineOffset  = 0
    _font            = None  # Font('Helvetica', size=12)
    _foregroundColor = None  # Color.Black
    _kern            = None  # 0
    _ligature        = None  # Ligature.Std, .Min or .All
    _link            = None
    _paragraphStyle  = None
    _Str_NS          = None
    _superscript     = 0
    _underlineStyle  = 0  # Underline.None, .Single, .StrikeThrough, .Word

    # <http://Developer.Apple.com/library/content/documentation/
    #       Cocoa/Conceptual/AttributedStrings/Articles/standardAttributes.html>
    def __new__(cls, ns_str='', **attrs):
        self = Str.__new__(cls, ns_str)
        self._Str_NS = self._NS
        for a, v in attrs.items():
            setattr(self, a, v)
        return self

    @property
    def attachment(self):
        '''Get the baselineOffset (C{str}).
        '''
        return self._attachment

    @attachment.setter  # PYCHOK property.setter
    def attachment(self, attachment):
        self._attachment = attachment  # NSTextAttachment None

    @property
    def backgroundColor(self):
        '''Get the background fill color (C{Color}).
        '''
        return self._backgroundColor

    @backgroundColor.setter  # PYCHOK property.setter
    def backgroundColor(self, backgroundColor):  # PYCHOK property.setter
        self._backgroundColor = backgroundColor  # NSColor None

    @property
    def baselineOffset(self):
        '''Get the baselineOffset (C{int} or C{float}).

           @note: The baseline offset attribute is a literal distance,
                  in pixels, by which the characters should be shifted
                  above the baseline (for positive offsets) or below
                  (for negative offsets).
        '''
        return self._baselineOffset

    @baselineOffset.setter  # PYCHOK property.setter
    def baselineOffset(self, baselineOffset):
        self._baselineOffset = baselineOffset  # NSNumber flint 0 pixels

    @property
    def font(self):
        '''Get the font (C{Font}).
        '''
        return self._font

    @font.setter  # PYCHOK property.setter
    def font(self, font):
        self._font = font  # NSFont

    @property
    def foregroundColor(self):
        '''Get the text color (C{Color}).
        '''
        return self._foregroundColor

    @foregroundColor.setter  # PYCHOK property.setter
    def foregroundColor(self, foregroundColor):
        self._foregroundColor = foregroundColor  # NSColor Black

    @property
    def kern(self):
        '''Get the kerning (C{int} or C{float}).

           @note: The kerning attribute indicates how much the following
                  character should be shifted from its default offset as
                  defined by the current character’s font; a positive
                  kern indicates a shift farther along and a negative
                  kern indicates a shift closer to the current character.
        '''
        return self._kern

    @kern.setter  # PYCHOK property.setter
    def kern(self, kern):
        self._kern = kern  # NSNumber flint 0

    @property
    def ligature(self):
        '''Get the underline style (C{int}).

           @note: The ligature attribute determines what kinds of
                  ligatures should be used when displaying the string:
                  0 indicates that only ligatures essential for proper
                  rendering of text should be used, 1 indicates that
                  standard ligatures should be used, and 2 indicates
                  that all available ligatures should be used.
                  Which ligatures are standard depends on the script
                  and possibly the font.  Arabic text, for example,
                  requires ligatures for many character sequences, but
                  has a rich set of additional ligatures that combine
                  characters.  English text has no essential ligatures,
                  and typically has only two standard ligatures, those
                  for “fi” and “fl”—all others being considered more
                  advanced or fancy.
        '''
        return self._ligature

    @ligature.setter  # PYCHOK property.setter
    def ligature(self, ligature):
        self._ligature = ligature  # NSNumber int 1 (0, 1, 2)

    @property
    def link(self):
        '''Get the underline style (C{NS...}).

           @note: The link attribute specifies an arbitrary object that
                  is passed to the NSTextView method clickedOnLink:atIndex:
                  when the user clicks in the text range associated with
                  the NSLinkAttributeName attribute.  The text view’s
                  delegate object can implement textView:clickedOnLink:atIndex:
                  or textView:clickedOnLink: to process the link object.
                  Otherwise, the default implementation checks whether
                  the link object is an NSURL object and, if so, opens
                  it in the URL’s default application.
        '''
        return self._link

    @link.setter  # PYCHOK property.setter
    def link(self, link):
        self._link = link  # Id_t None

    @property
    def NS(self):
        ns_attrs = dict2NS({}, frozen=True)
        return NSAttributedString.alloc(). \
               initWithString_attributes_(self._Str_NS, ns_attrs)

    @property
    def paragraphStyle(self):
        '''Get the paragraph style (C{...}).
        '''
        return self._paragraphStyle

    @paragraphStyle.setter  # PYCHOK property.setter
    def paragraphStyle(self, paragraphStyle):
        # <http://Developer.Apple.com/documentation/appkit/
        #       nsparagraphstyle/1532681-defaultparagraphstyle>
        self._paragraphStyle = paragraphStyle  # .defaultParagraphStyle

    @property
    def superScript(self):
        '''Get the underline style (C{int} or C{float}).

           @note: The superscript attribute indicates an abstract level
                  for both super- and subscripts.  The user of the
                  attributed string can interpret this as desired,
                  adjusting the baseline by the same or a different
                  amount for each level, changing the font size, or both.
        '''
        return self._superScript

    @superScript.setter  # PYCHOK property.setter
    def superScript(self, superScript):
        self._superScript = superScript  # NSNumber int 0

    @property
    def underlineStyle(self):
        '''Get the underline style (C{UnderlineStyle}).

           @note: The underline attribute has only two values defined,
                  NSNoUnderlineStyle and NSSingleUnderlineStyle, but
                  these can be combined with NSUnderlineByWordMask and
                  NSUnderlineStrikethroughMask to extend their behavior.
                  By bitwise-ORing these values in different combinations,
                  you can specify no underline, a single underline, a
                  single strikethrough, both an underline and a strikethrough,
                  and whether the line is drawn for whitespace or not.
           '''
        return self._underlineStyle

    @underlineStyle.setter  # PYCHOK property.setter
    def underlineStyle(self, underlineStyle):
        self._underlineStyle = underlineStyle  # NSNumber int None


NSAttributedString._Type                              = _Types.StrAttd = StrAttd
NSConstantString._Type = NSString._Type = NSStr._Type = _Types.Str     = Str

if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)

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
