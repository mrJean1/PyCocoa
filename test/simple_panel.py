
# -*- coding: utf-8 -*-

# Originally <http://GitHub.com/phillip-nguyen/cocoa-python/blob/master/examples/open_panel.py>

# Minimal example of displaying an NSOpenPanel.

# all imports listed explicitly to help PyChecker
from pycocoa import NSLog, NSOpenPanel, nsString2str

__version__ = '17.11.18'


def show_open_panel():
    panel = NSOpenPanel.openPanel()

#   panel.setResolvesAliases_(True)
    panel.setCanChooseDirectories_(True)
    panel.setCanChooseFiles_(True)
#   panel.allowedFileTypes(?)

    if panel.runModal():
        return nsString2str(panel.URL().path())
    return None


if __name__ == '__main__':

    # Create and display an NSOpenPanel.
    selected = show_open_panel()
    NSLog('selected: %s' % (selected,))
