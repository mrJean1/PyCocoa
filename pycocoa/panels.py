
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
from nstypes import NSOpenPanel, nsString2str
from pytypes import py2NS
from oslibs  import NSCancelButton
from utils   import _Types

__all__ = ('OpenPanel',)
__version__ = '18.04.24'


class OpenPanel(_Type2):
    '''Python Type to select a file, wrapping ObjC C{NSOpenPanel}.
    '''

    def __init__(self, title=''):
        '''New L{OpenPanel}, a file selection dialog.

          @param title: The panel name (str).
        '''
        self.NS = NSOpenPanel.openPanel()
        self.title = title
#       self.NS.setTitleHidden_(bool(True))

    def pick(self, filetypes, aliases =False,
                              dirs    =False,
                              files   =True,
                              hidden  =False,
                              hidexts =False,
                              multiple=False,
                              packages=False,
                              otherOK =False,
                              dflt    =None):
        '''Select a file from the panel.

          @param filetypes: The selectable file types (tuple of str-s).
          @keyword aliases: Allow selection of aliases (bool).
          @keyword dirs: Allow selection of directories (bool).
          @keyword hidden: Allow selection of hidden files (bool).
          @keyword hidexts: Hide file extensions (bool).
          @keyword multiple: Allow selection of multiple files (bool).
          @keyword packages: Treat file packages as directories (bool).
          @keyword otherOK: Allow selection of other file types (bool).
          @keyword dflt: Return value, cancelled, nothing selected (None).

          @return: The selected file name (str) or I{dflt}.
        '''
        if multiple:  # setAllowsMultipleSelection_
            raise NotImplementedError('multiple %s' % (multiple,))
        ns = self.NS

        ns.setResolvesAliases_(bool(aliases))
        ns.setCanChooseDirectories_(bool(dirs))
        ns.setCanChooseFiles_(bool(files))
        ns.setShowsHiddenFiles_(bool(hidden))
        ns.setExtensionHidden_(bool(hidexts))
        # ns.setRequiredFileType_(NSStr)
        # an NSArray of file extension NSStr[ing]s without the '.'
        ns.setAllowedFileTypes_(py2NS(t.lstrip('.') for t in filetypes))
        ns.setAllowsOtherFileTypes_(bool(otherOK))
        ns.setTreatsFilePackagesAsDirectories_(bool(packages))

        while True:
            ns.orderFrontRegardless()  # only flashes
            # <http://developer.apple.com/documentation/
            #       appkit/nssavepanel/1525357-runmodal>
            if ns.runModal() == NSCancelButton:
                return dflt  # nothing selected
#           paths = ns.filenames()  # returns an NSArray
#           urls = ns.URLs()  # returns an NSArray
            path = nsString2str(ns.URL().path())
            # mimick NSOpenPanel.setAllowedFileTypes_
            if path.lower().endswith(filetypes):
                return path


NSOpenPanel._Type = _Types.OpenPanel = OpenPanel

if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)
