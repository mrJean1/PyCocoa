
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

__all__ = ('OpenPanel',)
__version__ = '18.04.18'


class OpenPanel(_Type2):
    '''Python Type to select a file, wrapping ObjC C{NSOpenPanel}.
    '''

    def __init__(self, title=''):
        '''New L{OpenPanel}, a file selection dialog.

          @param title: The panel name (str).
        '''
        self.NS = NSOpenPanel.openPanel()
        self.title = title

    def pick(self, filetypes, aliases =False,
                              dirs    =False,
                              files   =True,
                              hidden  =False,
                              multiple=False,
                              dflt    =None):
        '''Select a file from the panel.

          @param filetypes: The selectable file types (tuple of str).
          @keyword aliases: Allow selection of aliases (bool).
          @keyword dirs: Allow selection of directories (bool).
          @keyword hidden: Allow selection of hidden files (bool).
          @keyword multiple: Allow selection of multiple files (bool).
          @keyword dflt: Return value if nothing is selected (None).

          @return: The selected file name (str) or I{dflt}.
        '''
        if multiple:  # setAllowsMultipleSelection_
            raise NotImplementedError('multiple %s' % (multiple,))
        ns = self.NS

        ns.setResolvesAliases_(bool(aliases))
        ns.setCanChooseDirectories_(bool(dirs))
        ns.setCanChooseFiles_(bool(files))
        ns.setShowsHiddenFiles_(bool(hidden))
#       ns.allowedFileTypes(NSStrings(*filetypes))

        while True:
            ns.orderFrontRegardless()  # only flashes
            if not ns.runModal():
                return dflt  # Cancel, nothing selected
#           paths = ns.filenames()  # returns an NSArray
#           urls = ns.URLs()  # returns an NSArray
            path = nsString2str(ns.URL().path())
            # mimick NSOpenPanel.allowedFileTypes_
            if path.lower().endswith(filetypes):
                return path


if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)
