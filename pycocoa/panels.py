
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

'''Type L{OpenPanel}, wrapping ObjC C{NSOpenPanel}.
'''
# all imports listed explicitly to help PyChecker
from bases   import _Type2
from nstypes import NSOpenPanel, NSSavePanel, NSStr, nsString2str
from pytypes import py2NS
from oslibs  import NSCancelButton, NSOKButton
from utils   import _Types

__all__ = ('OpenPanel',
           'SavePanel')
__version__ = '18.04.26'


class OpenPanel(_Type2):
    '''Python Type to select a file, wrapping ObjC C{NSOpenPanel}.
    '''

    def __init__(self, title=''):
        '''New L{OpenPanel}, a file selection dialog.

          @keyword title: The panel name (str).
          @keyword prompt: The text of the button (str), default "Open".
        '''
        self.NS = NSOpenPanel.openPanel()
        self.title = title
#       self.NS.setTitleHidden_(bool(False))  # "does nothing now"

    def pick(self, filetypes, aliases=False,
                                 dirs=False,
                                files=True,
                               hidden=False,
                              hidexts=False,
                             multiple=False,
                             packages=False,
                               prompt='',
                              otherOK=False, dflt=None):
        '''Select a file from the panel.

           @param filetypes: The selectable file types (tuple of str-s).
           @keyword aliases: Allow selection of aliases (bool).
           @keyword dirs: Allow selection of directories (bool).
           @keyword hidden: Allow selection of hidden files (bool).
           @keyword hidexts: Hide file extensions (bool).
           @keyword multiple: Allow selection of multiple files (bool).
           @keyword packages: Treat file packages as directories (bool).
           @keyword prompt: The button label (str), default "Open".
           @keyword otherOK: Allow selection of other file types (bool).
           @keyword dflt: Return value, cancelled, nothing selected (C{None}).

           @return: The selected file name path (str) or I{dflt}.
        '''
        if multiple:  # setAllowsMultipleSelection_
            raise NotImplementedError('multiple %s' % (multiple,))
        ns = self.NS

        ns.setResolvesAliases_(bool(aliases))
        ns.setCanChooseDirectories_(bool(dirs))
        ns.setCanChooseFiles_(bool(files))
        ns.setShowsHiddenFiles_(bool(hidden))
        # ns.setCanSelectHiddenExtension_(bool(hidden))
        ns.setExtensionHidden_(bool(hidexts))

        # ns.setRequiredFileType_(NSStr)
        if filetypes:  # an NSArray of file extension NSStr[ing]s without the '.'
            ns.setAllowedFileTypes_(py2NS(t.lstrip('.') for t in filetypes))

        ns.setAllowsOtherFileTypes_(bool(otherOK))
        ns.setTreatsFilePackagesAsDirectories_(bool(packages))

        if prompt:
            ns.setPrompt_(NSStr(prompt))

        while True:
            ns.orderFrontRegardless()  # only flashes
            # <http://Developer.Apple.com//documentation/
            #       appkit/nssavepanel/1525357-runmodal>
            if ns.runModal() == NSCancelButton:  # runModalForTypes_
                return dflt  # nothing selected
#           paths = ns.filenames()  # returns an NSArray
#           urls = ns.URLs()  # returns an NSArray
            path = nsString2str(ns.filename())  # == ns.URL().path()
            # mimick NSOpenPanel.setAllowedFileTypes_
            if path.lower().endswith(filetypes):
                return path


# <http://pseudofish.com/p/saving-a-file-using-nssavepanel.html>
# <http://pseudofish.com/showing-a-nssavepanel-as-a-sheet.html>

class SavePanel(_Type2):
    '''Python Type to save a file, wrapping ObjC C{NSSavePanel}.
    '''
    def __init__(self, title=''):
        '''New L{SavePanel}, a file save dialog.

          @param title: The panel name (str).
        '''
        self.NS = NSSavePanel.savePanel()
        self.title = title
#       self.NS.setTitleHidden_(bool(False))  # "does nothing now"

    def save_as(self, name='', filetype='',  # PYCHOK expected
                                    dir='',
                                 hidden=False,
                                hidexts=False,
                                  label='',
                               packages=False,
                                 prompt='',
                                   tags=(), dflt=None):
        '''Specify a file name in the panel.

           @keyword name: A suggested file name (str), default "Untitled".
           @keyword filetype: The file type (str).
           @keyword dir: The directory (str).
           @keyword hidden: Show hidden files (bool).
           @keyword hidexts: Hide file extensions (bool).
           @keyword label: The name label (str), default "Save As:".
           @keyword packages: Treat file packages as directories (bool).
           @keyword prompt: The button label (str), default "Save".
           @keyword tags: Suggested tag names (tuple of str-s).
           @keyword dflt: Return value, cancelled (C{None}).

           @return: The specified file name path (str) or I{dflt}.
        '''
        ns = self.NS

        if name:
            ns.setNameFieldStringValue_(NSStr(name))

        if dir:
            if dir.lower().startswith('file:///'):
                ns.setDirectoryURL_(NSStr(dir))
            else:
                ns.setDirectory_(NSStr(dir))

        if filetype:
            ns.setRequiredFileType_(NSStr(filetype.lstrip('.')))
            hidexts = False

        ns.setShowsHiddenFiles_(bool(hidden))
        # ns.setCanSelectHiddenExtension_(bool(hidden))
        ns.setExtensionHidden_(bool(hidexts))

        if label:
            ns.setNameFieldLabel_(NSStr(label))

        ns.setTreatsFilePackagesAsDirectories_(bool(packages))

        if prompt:
            ns.setPrompt_(NSStr(prompt))

        if tags:
            ns.setTagNames_(py2NS(tags))
            ns.setShowsTagField_(True)
        else:
            ns.setShowsTagField_(False)

        while True:
            r = ns.runModal()  # == runModalForDirectory_file_(None, None)
            if r == NSOKButton:
                return nsString2str(ns.filename())  # == ns.URL().path()
            elif r == NSCancelButton:
                return dflt


NSOpenPanel._Type = _Types.OpenPanel = OpenPanel
NSSavePanel._Type = _Types.SavePanel = SavePanel

if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)
