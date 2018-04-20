
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

from bases   import _Type2
from nstypes import NSOpenPanel, nsString2str

__all__ = ('OpenPanel',)
__version__ = '18.04.18'


class OpenPanel(_Type2):

    def __init__(self, title=''):
        '''A file selection dialog.
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

# <http://pseudofish.com/p/saving-a-file-using-nssavepanel.html>
# <http://pseudofish.com/showing-a-nssavepanel-as-a-sheet.html>

# class SavePanel(_Type2):
#     pass

# <http://developer.apple.com/library/content/navigation/>

# <http://nullege.com/codes/show/src%40l%40i%40Lightningbeam-HEAD%40GUI%40Cocoa%40BaseFileDialogs.py/5/AppKit.NSOpenPanel/python>
#
#   Python GUI - File selection dialogs - Cocoa
#
_ = '''
from AppKit import NSOpenPanel, NSSavePanel, NSOKButton
from GUI.Files import FileRef
from GUI import application

#------------------------------------------------------------------

def _request_old(prompt, default_dir, file_types, dir, multiple):
    ns_panel = NSOpenPanel.openPanel()
    if prompt.endswith(":"):
        prompt = prompt[:-1]
    ns_panel.setTitle_(prompt)
    ns_panel.setCanChooseFiles_(not dir)
    ns_panel.setCanChooseDirectories_(dir)
    ns_panel.setAllowsMultipleSelection_(multiple)
    if default_dir:
        ns_dir = default_dir.path
    else:
        ns_dir = None
    if file_types:
        ns_types = []
        for type in file_types:
            ns_types.extend(type._ns_file_types())
    else:
        ns_types = None
    result = ns_panel.runModalForDirectory_file_types_(ns_dir, None, ns_types)
    if result == NSOKButton:
        if multiple:
            return [FileRef(path = path) for path in ns_panel.filenames()]
        else:
            return FileRef(path = ns_panel.filename())
    else:
        return None

#------------------------------------------------------------------

def _request_new(prompt, default_dir, default_name, file_type, dir):
    ns_panel = NSSavePanel.savePanel()
    #if prompt.endswith(":"):
    #   prompt = prompt[:-1]
    #if prompt.lower().endswith(" as"):
    #   prompt = prompt[:-3]
    #ns_panel.setTitle_(prompt)
    #print "_request_new: setting label to", repr(prompt) ###
    ns_panel.setNameFieldLabel_(prompt)
    if default_dir:
        ns_dir = default_dir.path
    else:
        ns_dir = None
    if file_type:
        suffix = file_type.suffix
        if suffix:
            ns_panel.setCanSelectHiddenExtension_(True)
            if not file_type.mac_type or file_type.mac_force_suffix:
                ns_panel.setRequiredFileType_(suffix)
    result = ns_panel.runModalForDirectory_file_(ns_dir, default_name)
    if result == NSOKButton:
        return FileRef(path = ns_panel.filename())
    else:
        return None

'''

# <http://nullege.com/codes/show/src%40v%40i%40virtaal-HEAD%40virtaal%40support%40native_widgets.py/233/AppKit.NSOpenPanel/python>
_ = '''
def darwin_open_dialog(window, title, directory):
    # http://developer.apple.com/library/mac/
    #      #documentation/Cocoa/Conceptual/AppFileMgmt/Concepts/SaveOpenPanels.html
    #      #//apple_ref/doc/uid/20000771-BBCFDGFC
    # http://scottr.org/blog/2008/jul/04/building-cocoa-guis-python-pyobjc-part-four/
    from objc import NO
    from AppKit import NSOpenPanel
    from translate.storage import factory
    from locale import strcoll
    file_types = []
    _sorted = sorted(factory.supported_files(), cmp=strcoll, key=lambda x: x[0])
    for name, extension, mimetype in _sorted:
        file_types.extend(extension)
    panel = NSOpenPanel.openPanel()
    panel.setCanChooseDirectories_(NO)
    panel.setTitle_(title or _("Choose a Translation File"))
    panel.setAllowsMultipleSelection_(NO)
    panel.setAllowedFileTypes_(file_types)
    panel.setDirectoryURL_(u"file:///%s" % directory)
    ret_value = panel.runModalForTypes_(file_types)
    if ret_value:
        return (panel.filenames()[0], panel.URLs()[0].absoluteString())
    else:
        return ()

def darwin_save_dialog(window, title, current_filename):
    from AppKit import NSSavePanel
    directory, filename = os.path.split(current_filename)
    panel = NSSavePanel.savePanel()
    panel.setTitle_(title or _("Save"))
    panel.setDirectoryURL_(u"file:///%s" % directory)
    panel.setNameFieldStringValue_(filename)
    ret_value = panel.runModal()
    if ret_value:
        return panel.filename()
    else:
        return u''
'''

del _
