
# -*- coding: utf-8 -*-

# Show all shortcut Keys in a menu.

from pycocoa import App, Item, ItemSeparator, Keys, Menu

__version__ = '18.11.06'


class KeysApp(App):

    def appLaunched_(self, app):  # PYCHOK app unused

        menu = Menu('Keys')
        menu.append(
            Item('Special Keys'),  # ObjC specials
            ItemSeparator(),
            Item('BackSpace',           self.menuKey_, key=Keys.BS),   # Delete <x] key
            Item('BackTab',             self.menuKey_, key=Keys.BT, alt=True),
# no icon   Item('Cancel',              self.menuKey_, key=Keys.CAN),
            Item('CarriageReturn',      self.menuKey_, key=Keys.CR),   # Return key
            Item('Delete',              self.menuKey_, key=Keys.DEL),  # Delete [x> key
            Item('Enter',               self.menuKey_, key=Keys.ETX),
            Item('Escape',              self.menuKey_, key=Keys.ESC),  # Enter on keypad
            Item('FormFeed',            self.menuKey_, key=Keys.FF),   # Page Down key
            Item('NewLine',             self.menuKey_, key=Keys.NL),
            Item('Space',               self.menuKey_, key=Keys.SP, alt=True, ctrl=True),
            Item('Tab',                 self.menuKey_, key=Keys.HT, alt=True),
            ItemSeparator(),  # other ASCII Ctrl+Alpha characters
# no icon   Item('Acknowledge',         self.menuKey_, key=Keys.ACK),
# no icon   Item('Bell',                self.menuKey_, key=Keys.BEL),
# no icon   Item('DataLineEscape',      self.menuKey_, key=Keys.DLE),
# no icon   Item('DeviceControl1',      self.menuKey_, key=Keys.DC1),
# no icon   Item('DeviceControl2',      self.menuKey_, key=Keys.DC2),
# no icon   Item('DeviceControl3',      self.menuKey_, key=Keys.DC3),
# no icon   Item('DeviceControl4',      self.menuKey_, key=Keys.DC4),
# no icon   Item('EndOfMedium',         self.menuKey_, key=Keys.EM),
            Item('EndOfText',           self.menuKey_, key=Keys.ETX, alt=True),
            Item('EndOfTransmit',       self.menuKey_, key=Keys.EOT),  # End key
# no icon   Item('EndOfTransmitBlock',  self.menuKey_, key=Keys.ETB),
            Item('Enquiry',             self.menuKey_, key=Keys.ENQ),
            Item('FileSeparator',       self.menuKey_, key=Keys.FS),
            Item('GroupSeparator',      self.menuKey_, key=Keys.GS),
            Item('HorizontalTab',       self.menuKey_, key=Keys.HT, alt=True),
            Item('LineFeed',            self.menuKey_, key=Keys.LF, alt=True),
# no icon   Item('NegativeAcknowledge', self.menuKey_, key=Keys.NAK),
            Item('RecordSeparator',     self.menuKey_, key=Keys.RS),
# no icon   Item('ShiftIn',             self.menuKey_, key=Keys.SI),
# no icon   Item('ShiftOut',            self.menuKey_, key=Keys.SO),
# no icon   Item('StartOfHeading',      self.menuKey_, key=Keys.SOH),
# no icon   Item('StartOfText',         self.menuKey_, key=Keys.STX),
# no icon   Item('SynchronousIdle',     self.menuKey_, key=Keys.SYN),
# no icon   Item('Substitute',          self.menuKey_, key=Keys.SUB),
            Item('UnitSeparator',       self.menuKey_, key=Keys.US),
            Item('VerticalTab',         self.menuKey_, key=Keys.VT, alt=True))

        self.append(menu)
        menu.popUp()

    def menuKey_(self, item):
        print('    %s clicked' % (item,))

    def menuSpecialKeys_(self, item):  # PYCHOK item unused
        pass  # ignore


if __name__ == '__main__':

    from sys import argv

    app = KeysApp()

    if len(argv) > 1:
        _timeout = float(argv[1])
    else:
        _timeout = None

        from threading import Thread
        from time import sleep

        def _activate():
            while True:
                app.activate(True)
                sleep(1)

        t = Thread(target=_activate)
        t.start()

    app.run(timeout=_timeout)
