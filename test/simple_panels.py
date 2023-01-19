
# -*- coding: utf-8 -*-

# Originally <https://GitHub.com/phillip-nguyen/cocoa-python/blob/master/examples/open_panel.py>

# Minimal example of displaying an NSOpenPanel.

import run as _  # PYCHOK sys.path
# all imports listed explicitly to help PyChecker
from pycocoa import NSOpenPanel, NSPrintPanel, NSSavePanel, \
                    NSStr, nsString2str, nsLog, py2NS

__version__ = '23.01.18'


def open_panel():
    panel = NSOpenPanel.openPanel()

    panel.setPrompt_(NSStr('Set prompt...'))
#   panel.setResolvesAliases_(True)
    panel.setCanChooseDirectories_(True)
    panel.setCanChooseFiles_(True)
#   panel.allowedFileTypes(?)

    if panel.runModal():
        return nsString2str(panel.URL().path())
    return None


def print_panel():
    panel = NSPrintPanel.alloc().init()

    return panel.runModal()  # crashes


def save_panel():
    panel = NSSavePanel.savePanel()

#   panel.setTitleHidden_(False)  # "does nothing now"
    panel.setPrompt_(NSStr('Prompt...'))
    panel.setTitle_(NSStr('Title...'))
    panel.setCanChooseDirectories_(True)
    panel.setCanChooseFiles_(True)
#   panel.allowedFileTypes(?)

    panel.setNameFieldLabel_(NSStr('NameFieldLabel...'))
    panel.setNameFieldStringValue_(NSStr('NameFieldValue...'))

    panel.setDirectory_(NSStr('/Users'))
    panel.setTagNames_(py2NS('tagA tagB tagC'.split()))
    panel.setShowsTagField_(True)

    panel.orderFrontRegardless()

    if panel.runModal():  # == runModalForDirectory_file_(None, None)
        return ' or '.join((nsString2str(panel.directory()),
                            nsString2str(panel.filename()),
                          # nsString2str(panel.URL()),
                            nsString2str(panel.URL().path())))
    return None


if __name__ == '__main__':

    # Create and display an NSSavePanel.
    saved = save_panel()
    nsLog('saved: %s' % (saved,))

    # Create and display an NSOpenPanel.
    selected = open_panel()
    nsLog('selected: %s' % (selected,))

    # Create and display an NSPrintPanel.
#   printed = print_panel()
#   nsLog('printed: %s' % (printed,))

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
