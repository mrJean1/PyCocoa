
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Types L{OpenPanel} and L{SavePanel}, wrapping ObjC C{NSOpenPanel} and C{NSSavePanel}.

@var AlertStyle: Alert level constants (C{int}).
@var AlertStyle.Critical: 2.
@var AlertStyle.Info: 1.
@var AlertStyle.Warning: 0.

@var PanelButton: Panel button kinds (C{int}).
@var PanelButton.Cancel: 0.
@var PanelButton.Close: 1.
@var PanelButton.Error: -3.
@var PanelButton.OK: 1.
@var PanelButton.Other: 2.
@var PanelButton.Suppressed: -2.
@var PanelButton.TimedOut: -1.
'''
# all imports listed explicitly to help PyChecker
from pycocoa.bases   import _Type2
from pycocoa.lazily  import _ALL_LAZY, _DOT_, _NN_
from pycocoa.nstypes import NSAlert, NSError, NSFont, NSMain, \
                            NSNotificationCenter, NSOpenPanel, \
                            NSSavePanel, NSStr, nsString2str, \
                            nsTextView
from pycocoa.pytypes import dict2NS, py2NS, url2NS
from pycocoa.oslibs  import NO, NSCancelButton, NSOKButton, YES
from pycocoa.runtime import isObjCInstanceOf, release
# from strs  import StrAttd
from pycocoa.utils   import _Constants, property_RO, _Strs, \
                            _text_title2, _Types

from os import linesep
from threading import Thread
from time import sleep
try:
    from urlparse import urlparse as _urlparse  # Python 2-
except ImportError:
    from urllib.parse import urlparse as _urlparse  # Python 3+
try:
    from webbrowser import get as _Browser, Error as _BrowserError
except ImportError:
    _Browser, _BrowserError = None, ImportError

__all__ = _ALL_LAZY.panels
__version__ = '21.11.04'


class AlertStyle(_Constants):  # Enum?
    '''Alert level constants (C{int}).
    '''
    Critical = 2  # NSAlertStyleCritical
    Info     = 1  # NSAlertStyleInformational
    Warning  = 0  # NSAlertStyleWarning

AlertStyle = AlertStyle()  # PYCHOK constants

_AlertStyleStr = {AlertStyle.Critical: 'Critical ',
                  AlertStyle.Info:     'Informational ',
                  AlertStyle.Warning:  'Warning '}


class AlertPanel(_Type2):
    '''Python Type to show an alert, wrapping ObjC C{NSAlert}.
    '''
    _cancel   = False
    _info     = _NN_
    _ok       = 'OK'
    _other    = False
    _style    = None
    _suppress = None

    def __init__(self, title=_NN_, info=_NN_, ok='OK', cancel=False, other=False,
                       style=AlertStyle.Info, suppressable=False):
        '''New L{AlertPanel}.

          @keyword title: The panel name and title (C{str}).
          @keyword info: Optional, informative message (C{str}).
          @keyword ok: First, OK button text (C{str}), other than 'OK'.
          @keyword cancel: Include a second, Cancel button (C{bool} or C{str}).
          @keyword other: Include a third, Other button (C{bool} or C{str}).
          @keyword style: Kind of alert (C{AlertStyle}), default C{.Info}.
          @keyword suppressable: Include suppress option (C{bool}).

          @raise ValueError: Multi-line I{info} or too long.

          @note: The first, C{OK} button is always shown.  The I{info}
                 text is limited to about 50 characters and must be
                 without C{linesep}arators.
        '''
        if info and isinstance(info, _Strs):
            if len(info) > 50 or linesep in info:
                raise ValueError('invalid %s: %r' % ('info', info))
            self._info = info

        self._ok = ok if isinstance(ok, _Strs) else 'OK'
        if cancel:
            self._cancel = cancel if isinstance(cancel, _Strs) else 'Cancel'
            if other:
                self._other = other if isinstance(other, _Strs) else 'Other'

        if suppressable:
            self._suppress = YES

        self._style = style
        s = _AlertStyleStr.get(style, _NN_)
        t = s or 'Alert '
        if title:
            t = '%s- %s' % (t, title)
        self.title = t

    def show(self, text=_NN_, font=None, timeout=None):
        '''Show alert message iff not suppressed.

           @keyword text: Optional, accessory text (C{str}).
           @keyword font: Optional font (L{Font}), default C{Fonts.System}.
           @keyword timeout: Optional time limit (C{float}).

           @return: The button clicked (C{PanelButton}).  If
                    C{PanelButton.Suppressed} is returned, the
                    alert panel was not shown since it was suppressed
                    due to a previous selection of the corresponding
                    check box.  C{PanelButton.TimedOut} is returned
                    if no button was clicked before the I{timeout}
                    expired.
        '''
        # <https://Developer.Apple.com/documentation/appkit/nsalert>
        ns = NSAlert.alloc().init()
        ns.setAlertStyle_(self._style)
        ns.setMessageText_(release(NSStr(self.title)))

        if self._info:
            # <https://Developer.Apple.com/library/content/documentation/
            #        Cocoa/Conceptual/Strings/Articles/stringsParagraphBreaks.html>
            ns.setInformativeText_(NSStr(self._info))

        ns.addButtonWithTitle_(release(NSStr(self._ok)))
        if self._cancel:
            ns.addButtonWithTitle_(release(NSStr(self._cancel)))
            if self._other:
                ns.addButtonWithTitle_(release(NSStr(self._other)))

        if self._suppress in (False, YES):
            self._suppress = False
            ns.setShowsSuppressionButton_(YES)
            s = _AlertStyleStr.get(self._style, _NN_)
            s = 'Do not show this %sAlert again' % (s,)
            ns.suppressionButton().setTitle_(release(NSStr(s)))

        # <https://Developer.Apple.com/library/content/documentation/
        #        Cocoa/Conceptual/Dialog/Tasks/DisplayAlertHelp.html>
        # ns.showsHelp_(YES)
        # ns.helpAnchor_(HTML?)

        if text:
            t = nsTextView(text, NSFont.systemFontOfSize_(0)
                                 if font is None else font.NS)
            ns.setAccessoryView_(t)

        # <https://Developer.Apple.com/documentation/appkit/
        #        nsalert/1535196-showssuppressionbutton>
        if self._suppress is None:
            r = _runModal(ns, timeout)
        elif self._suppress is False:
            s = ns.suppressionButton().state()
            r = _runModal(ns, timeout)
            # XXX value of NSOnState?
            if ns.suppressionButton().state() != s:
                self._suppress = True
        else:
            r = PanelButton.Suppressed

        # ns.release()  # XXX may crash
        return r


class BrowserPanel(_Type2):
    '''Python Type to show a URL or file.
    '''
    _browser = None

    def __init__(self, name=None, title=_NN_):
        '''New L{BrowserPanel}, a browser.

          @keyword name: Browser type (C{str} or C{None} for default).
          @keyword title: The panel name (C{str}).

          @raise ValueError: No browser type I{name}.

          @see: U{Browser types<https://Docs.Python.org/3.6/library/webbrowser.html>}.
        '''
        # <https://Developer.Apple.com/documentation/
        #        foundation/nsnotificationcenter>
        if _Browser:
            try:
                self._browser = _Browser(name)
            except _BrowserError:
                raise ValueError('no %s type %r' % ('browser', name))
        else:
            self.NS = NSNotificationCenter.defaultCenter()
        self.title = title or name or 'default'

    @property_RO
    def browser(self):
        '''Get the browser instance (C{browser type}).
        '''
        return self._browser

    def open(self, url, tab=False):
        '''Open a new window or tab in the browser.

           @param url: The URL to open (C{str}).
           @keyword tab: New tab (C{bool}), new window otherwise.

           @return: Parsed I{url} as C{ParseResult}.

           @raise ValueError: Scheme of I{url} not 'http', 'https' or 'file'.
        '''
        ns = url2NS(url)
        sc = nsString2str(ns.scheme())
        if sc.lower() not in ('http', 'https', 'file'):
            raise ValueError('%s scheme %r invalid: %r' % ('url', sc, url))
        if self._browser:
            self._browser.open(url, new=2 if tab else 1)
        elif self.NS:
            d = dict2NS(dict(URL=ns, reveal=True, newTab=bool(tab)), frozen=True)
            u = NSStr('WebBrowserOpenURLNotification')
            self.NS.postNotificationName_object_userInfo_(u, None, d)
            u.release()  # PYCHOK expected
        return _urlparse(nsString2str(ns.absoluteString()))


class ErrorPanel(AlertPanel):
    '''Python Type to show an C{NSError} alert, wrapping ObjC C{NSAlert}.
    '''

    def __init__(self, title='Error'):
        '''New L{AlertPanel}.

           @keyword title: The panel name and title (C{str}).
        '''
        self.title = title

    def show(self, ns_error, timeout=None):  # PYCHOK expected
        '''Show the error.

           @param ns_error: Error information (C{NSError}).
           @keyword timeout: Optional time limit (C{float}).

           @return: TBD.

           @raise TypeError: Invalid I{ns_error}.
        '''
        # <https://Developer.Apple.com/documentation/
        #        appkit/nsalert/1531823-alertwitherror>
        # <https://Developer.Apple.com/documentation/foundation/nserror>
        if isObjCInstanceOf(ns_error, NSError, name='ns_error'):
            ns = NSAlert.alloc().alertWithError_(ns_error)
            r = _runModal(ns, timeout)
            # ns.release()  # XXX may crash
        else:
            r = PanelButton.Error
        return r


class OpenPanel(_Type2):
    '''Python Type to select a file, wrapping ObjC C{NSOpenPanel}.
    '''

    def __init__(self, title=_NN_):
        '''New L{OpenPanel}, a file selection dialog.

          @keyword title: The panel name (C{str}).
        '''
        self.title = title

    def pick(self, filetypes, aliases=False,
                                 dirs=False,
                                files=True,
                               hidden=False,
                              hidexts=False,
                             multiple=False,
                             packages=False,
                               prompt=_NN_,
                              otherOK=False, dflt=None):
        '''Select a file from the panel.

           @param filetypes: The selectable file types (tuple of str-s).
           @keyword aliases: Allow selection of aliases (C{bool}).
           @keyword dirs: Allow selection of directories (C{bool}).
           @keyword hidden: Allow selection of hidden files (C{bool}).
           @keyword hidexts: Hide file extensions (C{bool}).
           @keyword multiple: Allow selection of multiple files (C{bool}).
           @keyword packages: Treat file packages as directories (C{bool}).
           @keyword prompt: The button label (C{str}), default "Open".
           @keyword otherOK: Allow selection of other file types (C{bool}).
           @keyword dflt: Return value, if cancelled, nothing selected (C{None}).

           @return: The selected file name path (C{str}) or I{dflt}.
        '''
        if multiple:  # setAllowsMultipleSelection_
            raise NotImplementedError('multiple %s' % (multiple,))

        ns = NSOpenPanel.openPanel()
#       ns.setTitleHidden_(NO)  # "does nothing now"

        ns.setResolvesAliases_(YES if aliases else NO)
        ns.setCanChooseDirectories_(YES if dirs else NO)
        ns.setCanChooseFiles_(YES if files else NO)
        ns.setShowsHiddenFiles_(YES if hidden else NO)
        # ns.setCanSelectHiddenExtension_(YES if hidden else NO)
        ns.setExtensionHidden_(YES if hidexts else NO)

        # ns.setRequiredFileType_(NSStr)
        if filetypes:  # an NSArray of file extension NSStr[ing]s without the '.'
            ns.setAllowedFileTypes_(py2NS(t.lstrip(_DOT_) for t in filetypes))

        ns.setAllowsOtherFileTypes_(YES if otherOK else NO)
        ns.setTreatsFilePackagesAsDirectories_(YES if packages else NO)

        if prompt:
            ns.setPrompt_(release(NSStr(prompt)))

        while True:
            # ns.orderFrontRegardless()  # only flashes
            # <https://Developer.Apple.com/documentation/
            #        appkit/nssavepanel/1525357-runmodal>
            if ns.runModal() == NSCancelButton:  # runModalForTypes_
                path = dflt  # nothing selected
                break
#           paths = ns.filenames()  # returns an NSArray
#           urls = ns.URLs()  # returns an NSArray
            path = nsString2str(ns.filename())  # == ns.URL().path()
            # mimick NSOpenPanel.setAllowedFileTypes_
            if path.lower().endswith(filetypes):
                break
        # ns.release()  # XXX crashes Cancel pick
        return path


class PanelButton(_Constants):  # Enum?
    '''Panel button kinds (C{int}).
    '''
    Error      = -3
    Suppressed = -2
    TimedOut   = -1
    Cancel     = 0  # NSCancelButton
    Close      = 1  # TextPanel, like OK
    OK         = 1  # NSOKButton
    Other      = 2

PanelButton = PanelButton()  # PYCHOK constants


def _runModal(ns, timeout=None):
    r = None
    try:
        s = float(timeout or 0)
    except (TypeError, ValueError):
        s = 0

    if s > 0:
        def _stopModal():
            sleep(s + 0.5)
            if r is None:
                NSMain.Application.stopModalWithCode_(1003)

        t = Thread(target=_stopModal)
        t.start()
    # NSAlert buttons values are 1000, 1001 and 1002
    # <https://Developer.Apple.com/documentation/appkit/
    #        nsapplication.modalresponse>
    r = ns.runModal()
    return {1000: PanelButton.OK,  # alertFirstButtonReturn
            1001: PanelButton.Cancel,  # alertSecondButtonReturn
            1002: PanelButton.Other,  # alertThirdButtonReturn
            1003: PanelButton.TimedOut}.get(r, PanelButton.Error)


# <https://PseudoFish.com/p/saving-a-file-using-nssavepanel.html>
# <https://PseudoFish.com/showing-a-nssavepanel-as-a-sheet.html>

class SavePanel(_Type2):
    '''Python Type to save a file, wrapping ObjC C{NSSavePanel}.
    '''
    def __init__(self, title=_NN_):
        '''New L{SavePanel}, a file save dialog.

           @keyword title: The panel name (C{str}).
        '''
        self.title = title

    def save_as(self, name=_NN_, filetype=_NN_,  # PYCHOK expected
                                      dir=_NN_,
                                   hidden=False,
                                  hidexts=False,
                                    label=_NN_,
                                 packages=False,
                                   prompt=_NN_,
                                     tags=(), dflt=None):
        '''Specify a file name in the panel.

           @keyword name: A suggested file name (C{str}), default "Untitled".
           @keyword filetype: The file type (C{str}).
           @keyword dir: The directory (C{str}).
           @keyword hidden: Show hidden files (C{bool}).
           @keyword hidexts: Hide file extensions (C{bool}).
           @keyword label: The name label (C{str}), default "Save As:".
           @keyword packages: Treat file packages as directories (C{bool}).
           @keyword prompt: The button label (C{str}), default "Save".
           @keyword tags: Suggested tag names (C{tuple} of C{str}-s).
           @keyword dflt: Return value, cancelled (C{None}).

           @return: The specified file name path (C{str}) or I{dflt}.
        '''
        ns = NSSavePanel.savePanel()
#       ns.setTitleHidden_(bool(False))  # "does nothing now"

        if name:
            ns.setNameFieldStringValue_(release(NSStr(name)))

        if dir:
            if dir.lower().startswith('file:///'):
                ns.setDirectoryURL_(release(NSStr(dir)))
            else:
                ns.setDirectory_(release(NSStr(dir)))

        if filetype:
            ns.setRequiredFileType_(release(NSStr(filetype.lstrip(_DOT_))))
            hidexts = False

        ns.setShowsHiddenFiles_(YES if hidden else NO)
        # ns.setCanSelectHiddenExtension_(bool(hidden))
        ns.setExtensionHidden_(YES if hidexts else NO)

        if label:
            ns.setNameFieldLabel_(release(NSStr(label)))

        ns.setTreatsFilePackagesAsDirectories_(YES if packages else NO)

        if prompt:
            ns.setPrompt_(release(NSStr(prompt)))

        if tags:
            ns.setTagNames_(py2NS(tags))
            ns.setShowsTagField_(True)
        else:
            ns.setShowsTagField_(False)

        while True:
            r = _runModal(ns)  # == runModalForDirectory_file_(None, None)
            if r == NSOKButton:
                r = nsString2str(ns.filename())  # == ns.URL().path()
                break
            elif r == NSCancelButton:
                r = dflt
                break
        # ns.release()  # XXX may crash on Cancel
        return r


class TextPanel(AlertPanel):
    '''Scrollable text panel Python Type, wrapping ObjC C{NSAlert}.
    '''
    def __init__(self, title='Text Panel'):
        '''Create a L{TextPanel}.

           @keyword title: The panel name and title (C{str}).
        '''
        self.title = title

    def show(self, text_or_file=_NN_, font=None, timeout=None):
        '''Show alert message iff not suppressed.

           @param text_or_file: The contents (C{str} or C{file}).
           @keyword font: Optional font (L{Font}), default C{Fonts.MonoSpace}.
           @keyword timeout: Optional time limit (C{float}).

           @return: The button clicked (C{PanelButton.Close}) or
                    C{PanelButton.TimedOut} if the I{timeout} expired.

           @raise ValueError: No I{text_or_file} given.
        '''
        ns = NSAlert.alloc().init()
        ns.setAlertStyle_(AlertStyle.Info)
        ns.addButtonWithTitle_(release(NSStr('Close')))

        if not text_or_file:
            raise ValueError('no %s: %r' % ('text_or_file', text_or_file))

        text, t = _text_title2(text_or_file, self.title)
        if t:
            ns.setMessageText_(release(NSStr(t)))

        t = nsTextView(text, NSFont.userFixedPitchFontOfSize_(0)
                             if font is None else font.NS)
        ns.setAccessoryView_(t)
        r = _runModal(ns, timeout)
        ns.release()
        return r


_Types.AlertPanel = AlertPanel
_Types.ErrorPanel = ErrorPanel
_Types.OpenPanel  = NSOpenPanel._Type = OpenPanel
_Types.SavePanel  = NSSavePanel._Type = SavePanel
_Types.TextPanel  = TextPanel

if __name__ == '__main__':

    from pycocoa.utils import _all_listing, _varstr

    print(_varstr(AlertStyle,  strepr=repr))
    print(_varstr(PanelButton, strepr=repr))

    _all_listing(__all__, locals())

# % python3 -m pycocoa.panels
#
# pycocoa.panels.__all__ = tuple(
#  pycocoa.panels.AlertPanel is <class .AlertPanel>,
#  pycocoa.panels.AlertStyle.Critical=2,
#                           .Info=1,
#                           .Warning=0,
#  pycocoa.panels.BrowserPanel is <class .BrowserPanel>,
#  pycocoa.panels.ErrorPanel is <class .ErrorPanel>,
#  pycocoa.panels.OpenPanel is <class .OpenPanel>,
#  pycocoa.panels.PanelButton.Cancel=0,
#                            .Close=1,
#                            .Error=-3,
#                            .OK=1,
#                            .Other=2,
#                            .Suppressed=-2,
#                            .TimedOut=-1,
#  pycocoa.panels.SavePanel is <class .SavePanel>,
#  pycocoa.panels.TextPanel is <class .TextPanel>,
# )[8]
# pycocoa.panels.version 21.11.04, .isLazy 1, Python 3.11.0 64bit arm64, macOS 13.0.1

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2023 -- mrJean1 at Gmail -- All Rights Reserved.
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
