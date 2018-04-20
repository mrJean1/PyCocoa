
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

# <http://stackoverflow.com/questions/15519296/pyobjc-crashes-by-using-nstableview>
# <http://github.com/versluis/Mac-TableViewCode/tree/master/Mac%20TableViewCode>
from bases   import _Type2
from nstypes import NSNone, NSScrollView, NSStr, nsString2str, \
                    NSTableColumn, NSTableView, NSTrue
from oclibs  import NSTableViewSolidHorizontalGridLineMask, \
                    NSTableViewSolidVerticalGridLineMask
from octypes import NSSize_t
from runtime import isInstanceOf, ObjCClass, ObjCInstance, \
                    ObjCSubclass, send_super
from utils   import _Globals, instanceof
from windows import Frame4, Screen, Style, Window

__all__ = ('Table', 'TableWindow', 'TableDataDelegate',
           'closeTables')
__version__ = '18.04.18'

_EmptyCell = NSStr('-', auto=False)  # PYCHOK false
_Separator = NSStr('',  auto=False)


def closeTables():
    '''Close all tables.
    '''
    n = len(_Globals.Tables)
    while _Globals.Tables:
        _Globals.Tables.pop().close()
    return n


class Table(_Type2):
    '''A table display of rows and columns.
    '''
    _headers = ()
    _rows    = []
    _window  = None

    def __init__(self, *headers):
        self._headers = tuple(map(str, headers))
        self._rows    = []

    def append(self, *cols):
        '''Append another row of column values.
        '''
        def _nstr(col):
            # NSStr can't be auto-released
            return NSStr(str(col), auto=False)

        self._rows.append(tuple(map(_nstr, cols)))

    def close(self):
        '''Close and release this table.
        '''
        if self._window:
            self._window.close()
            self._window = None
        self.NS = NSNone

    def display(self, title, width=600, height=400):
        '''Show the table in a scrollable window.
        '''
        f = Frame4(0, 0, width, height)
        self.NS = vuw = NSTableView.alloc().initWithFrame_(f.NS)

        cols = []
        wide = width  # == view.frame().size.width
        # <http://developer.apple.com/documentation/appkit/nstablecolumn>
        for i, h in enumerate(self._headers):
            # note, the Identifier MUSt be an NSStr (to avoid warnings)
            c = NSTableColumn.alloc().initWithIdentifier_(NSStr(i))
            # print(i, h, c.identifier(), c.headerCell(),
            #             c.width(), c.minWidth(), c.maxWidth())
            # <http://developer.apple.com/documentation/appkit/nscell>
            t = h.split(':')  # split column title:width
            if len(t) == 2:
                h, w = t
                c.setWidth_(float(w))
            c.setTitle_(NSStr(h))  # == c.headerCell().setStringValue_(NSStr(h))
            # c.sizeToFit()  # fits width of title, headerCell text!
            # <http://developer.apple.com/documentation/uikit/nstextalignment>
            # c.headerCell().setAlignment_(NSTextAlignment.wraps) .left, etc.
            # c.headerCell().fontBold_()  # c.fontBold_() ?
            vuw.addTableColumn_(c)
            cols.append(h)
            wide -= c.width()

        if wide > 0:  # stretch last col to frame edge
            c.setWidth_(float(wide + c.width()))

        # <http://developer.apple.com/library/content/documentation/
        #         Cocoa/Conceptual/TableView/VisualAttributes/VisualAttributes.html>
        vuw.setGridStyleMask_(NSTableViewSolidHorizontalGridLineMask |
                              NSTableViewSolidVerticalGridLineMask)
#       vuw.setDrawsGrid_(NSTrue)  # XXX obsolete, not needed

        self.delegate = TableDataDelegate.alloc().init(cols, self._rows)
        vuw.setDataSource_(self.delegate)
#       vuw.setEditing_(NSFalse)
        vuw.reloadData()

        self._window = w = TableWindow(title, self)
        # vuw.setDelegate_(w.delegate)
        return w

    def separator(self):
        '''Append a row separator.
        '''
        self._rows.append(_Separator)


class _TableDataDelegate(object):
    '''An ObjC Delegate class with an C{NSTableViewDataSource} protocol.
       See the C{_AppDelegate} for more Delegate details.
    '''
    # <http://developer.apple.com/documentation/appkit/nstableviewdatasource>
    _ObjC = ObjCSubclass('NSObject', '_TableDataDelegate')

    @_ObjC.method('@PP')
    def init(self, cols, rows):
        instanceof(cols, list, tuple, name='cols')
        instanceof(rows, list, tuple, name='rows')
#       self = ObjCInstance(send_message('NSObject', 'alloc'))
        self = ObjCInstance(send_super(self, 'init'))
        self.cols = cols  # column titles
        self.rows = rows
        return self

    @_ObjC.method('i@')
    def numberOfColumnsInTableView_(self, table):
        return len(self.cols)

    @_ObjC.method('i@')
    def numberOfRowsInTableView_(self, table):
        return len(self.rows)

    @_ObjC.method('@@@i')  # using '*@@i' crashes
    def tableView_objectValueForTableColumn_row_(self, table, col, row):
        # row is the row number, but col is an
        # NSTableColumn instance, not an index
        # and col.identifier must be an NSStr.
        c = col.identifier()
        try:
            r = self.rows[row]
            if r is _Separator:
                # XXX vary row height of row separato?
                # <http://developer.apple.com/library/content/samplecode/
                #       CocoaTipsAndTricks/Listings/TableViewVariableRowHeights_
                #       TableViewVariableRowHeightsAppDelegate_m.html>
                return _Separator
            c = int(nsString2str(c))
            return r[c] if 0 <= c < len(r) else _EmptyCell
        except (IndexError, TypeError, ValueError):
            pass
        return NSStr('[C%r, R%d]' % (c, row))


TableDataDelegate = ObjCClass('_TableDataDelegate',  # the actual class
                              'NSTableViewDataSource')
# XXX or TableDataDelegate.add_protocol('NSTableViewDataSource')


class TableWindow(Window):
    '''An ObjC Delegate class for vertically scrollable window.
    '''
    _table = None

    def __init__(self, title='', table=None, frame=None):
        instanceof(table, Table, name='table')
        self._table = table

        tbl = getattr(table, 'NS', None)
        isInstanceOf(tbl, NSTableView, name='table')

        # <http://developer.apple.com/documentation/appkit/nswindow>
        n = tbl.dataSource().numberOfRowsInTableView_(tbl)
        # approximate height of the table content, also to
        # .setContentMaxSize_ of the window further below
        h = tbl.rowHeight() * max(1, (n + 1.5) * 1.15)
        # adjust frame to include all (or most) table rows
        f = tbl.frame() if frame is None else frame.NS
        if f.size.height < h:
            h = min(Screen().height, h)
            f.size = NSSize_t(f.size.width, h)
            tbl.setFrameSize_(f.size)

        Window.__init__(self, title=title, frame=f,
                                           excl=Style.Miniaturizable,
                                           auto=True)
        self.NSview = vuw = NSScrollView.alloc().initWithFrame_(f)

        vuw.setDocumentView_(tbl)
        vuw.setHasVerticalScroller_(NSTrue)  # XXX or True or 1

        self.cascade()
        self.limit(height=h)
        self.front(False)

        _Globals.Tables.append(self)

    @property
    def table(self):
        '''Get the table (L{Table}).
        '''
        return self._table

    def windowClose_(self):
        try:
            _Globals.Tables.remove(self)
        except ValueError:
            pass
        self._table = None
#       self.close()
        Window.windowClose_(self)  # super(Window, self)...


if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)
