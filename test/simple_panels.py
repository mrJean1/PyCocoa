
# -*- coding: utf-8 -*-

# Originally <http://GitHub.com/phillip-nguyen/cocoa-python/blob/master/examples/open_panel.py>

# Minimal example of displaying an NSOpenPanel.

# all imports listed explicitly to help PyChecker
from pycocoa import NSOpenPanel, NSPrintPanel, NSSavePanel, \
                    NSStr, nsString2str, nsLog, py2NS

__version__ = '18.04.26'


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
