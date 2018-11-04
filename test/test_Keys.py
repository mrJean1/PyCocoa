
# -*- coding: utf-8 -*-

# Show all shortcut Keys in a menu.

from pycocoa import App, Item, ItemSeparator, Keys, Menu

__version__ = '18.11.02'


class KeysApp(App):

    def appLaunched_(self, app):  # PYCHOK app unused

        menu = Menu('Keys')
        menu.append(
            Item('Special Keys'),
            ItemSeparator(),
            Item('Backspace',      self.menuKey_, key=Keys.BS),
            Item('CarriageReturn', self.menuKey_, key=Keys.CR),
            Item('Delete',         self.menuKey_, key=Keys.DEL),
            Item('Enter',          self.menuKey_, key=Keys.ETX),
            Item('Escape',         self.menuKey_, key=Keys.ESC),
            Item('FormFeed',       self.menuKey_, key=Keys.FF),
            # Item('LineFeed',     self.menuKey_, key=Keys.LF),
            Item('Newline',        self.menuKey_, key=Keys.NL),
            Item('Space',          self.menuKey_, key=Keys.SP),
            Item('Tab',            self.menuKey_, key=Keys.HT))

        # self.append(menu)
        menu.popUp()

    def menuKey_(self, item):
        print('    %s clicked' % (item,))

    def menuSpecialKeys_(self, item):  # PYCHOK item unused
        pass  # ignore


if __name__ == '__main__':

    from sys import argv

    if len(argv) > 1:
        _timeout = float(argv[1])
    else:
        _timeout = 1

    app = KeysApp()
    app.run(timeout=_timeout)
