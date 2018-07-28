
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Types L{Table} and L{TableWindow}, wrapping ObjC L{NSTableView}, L{NSWindow}.
'''
# <http://StackOverflow.com/questions/15519296/pyobjc-crashes-by-using-nstableview>
# <http://GitHub.com/versluis/Mac-TableViewCode/tree/master/Mac%20TableViewCode>

# all imports listed explicitly to help PyChecker
from bases    import _Type2
from fonts    import Font
from geometry import Rect4
from nstypes  import NSMain, NSScrollView, NSStr, NSTableColumn, \
                     NSTableView  # isNone, NSTextField
from octypes  import NSSize_t
from oslibs   import NSTableViewSolidHorizontalGridLineMask, \
                     NSTableViewSolidVerticalGridLineMask, \
                     NSTextAlignmentCenter, NSTextAlignmentJustified, \
                     NSTextAlignmentLeft, NSTextAlignmentNatural, \
                     NSTextAlignmentRight, YES
from runtime  import isInstanceOf, ObjCClass, ObjCInstance, \
                     ObjCSubclass, release, retain, send_super_init
from utils    import _Globals, isinstanceOf, _Types
from windows  import Screen, Window, WindowStyle

__all__ = ('NSTableViewDelegate',
           'Table', 'TableWindow',
           'closeTables')
__version__ = '18.07.27'

_Alignment = dict(center=NSTextAlignmentCenter,
               justified=NSTextAlignmentJustified,
                    left=NSTextAlignmentLeft,
                 natural=NSTextAlignmentNatural,
                   right=NSTextAlignmentRight)


class _NS(object):
    '''(INTERNAL) Singletons.
    '''
    BlankCell = retain(NSStr(''))
    EmptyCell = retain(NSStr('-'))


def _format(header, col):
    # format a table column from the header string
    # "title:<col_width>:left|center|right|justified:bold|italic"
    t = header.rstrip().split(':')
    while len(t) > 1:
        try:
            f = t.pop(1)
            if f.islower():
                c = col.dataCell()
            else:  # cap means title row
                c = col.headerCell()
                f = f.lower()

            ns = _Alignment.get(f, None)
            if ns:
                c.setAlignment_(ns)
            elif f in ('bold', 'italic'):
                ns = c.font()
                ns = Font(ns).traitsup(f).NS
                c.setFont_(ns)
            else:
                # col.sizeToFit()  # fits width of headerCell text!
                col.setWidth_(float(f))
        except (IndexError, TypeError, ValueError):
            raise ValueError('%s invalid: %s' % ('header', header))
    return t.pop()


def closeTables():
    '''Close all tables.
    '''
    n = len(_Globals.Tables)
    while _Globals.Tables:
        _Globals.Tables.pop().close()
    return n


class Table(_Type2):
    '''Python Type table of rows and columns, wrapping an ObjC L{NSTableView}.
    '''
    _Fonts   = None
    _headers = ()
    _rows    = []
    _window  = None

    def __init__(self, *headers):
        '''New L{Table}.

           @param headers: Column headers (C{str}), either just the "title"
                           or "title:width" to specify the column width
                           (C{int} or C{float}), ":bold" and/or :italic"
                           to specify the font trait and ":center",
                           ":justified", ":left", ":natural" or ":right"
                           to set the text alignment.

           @note: Capitalize font ":Trait" and text ":Alignment" to change
                  the header row.
        '''
        self._headers = tuple(map(str, headers))
        self._rows    = []

    def _release(self):
        # release all NSStr-s
        while self._rows:
            for s in (self._rows.pop() or ()):
                if isinstance(s, NSStr) and s is not _NS.BlankCell:
                    release(s)
        self.NSdelegate.release()
        self.NS.release()

    def append(self, *cols):
        '''Append another row of column values.
        '''
        def _nstr(col):
            return retain(NSStr(str(col))) if col else _NS.BlankCell

        self._rows.append(tuple(map(_nstr, cols)))

    def close(self):
        '''Close and release this table.
        '''
        if self._window:
            self._window.close()
            self._window = None
            self._release()
        self.NS = NSMain.Null

    def display(self, title, width=400, height=300):
        '''Show the table in a scrollable window.

           @param title: Window title (C{str}).
           @keyword width: Window frame width (C{int} or C{float}).
           @keyword height: Window frame height (C{int} or C{float}).

           @return: The window (L{TableWindow}).

           @raise ValueError: Invalid header column ":width", font
                              ":trait" or text ":alignment".
        '''
        f = Rect4(0, 0, width, height)
        v = NSTableView.alloc().initWithFrame_(f.NS)

        cols = []
        high = 0
        id2i = {}
        wide = f.width  # == v.frame().size.width
        # <http://Developer.Apple.com//documentation/appkit/nstablecolumn>
        for i, h in enumerate(self._headers):
            # note, the identifier MUST be an NSStr (to avoid warnings)
            t = retain(NSStr(str(i)))
            c = NSTableColumn.alloc().initWithIdentifier_(t)
            # simply map col.identifier to int, instead of frequent and
            # costly int(nsString2str(col.identifier())) conversions in
            # _NSTableViewDelegate.tableView_objectValueForTableColumn_row_
            id2i[c.identifier()] = i
            # <http://Developer.Apple.com//documentation/appkit/nscell>
            h = _format(h, c)
            cols.append(h)
            c.setTitle_(release(NSStr(h)))  # == c.headerCell().setStringValue_(NSStr(h))
            # <http://Developer.Apple.com//documentation/uikit/nstextalignment>
            v.addTableColumn_(c)
            high = max(high, Font(c.dataCell().font()).height)
            wide -= c.width()

        if wide > 0:  # stretch last col to frame edge
            c.setWidth_(float(wide + c.width()))
        if high > v.rowHeight():  # adjust the row height
            v.setRowHeight_(high + 1)

        # <http://Developer.Apple.com//library/content/documentation/
        #         Cocoa/Conceptual/TableView/VisualAttributes/VisualAttributes.html>
        v.setGridStyleMask_(NSTableViewSolidHorizontalGridLineMask |
                            NSTableViewSolidVerticalGridLineMask)
#       v.setDrawsGrid_(YES)  # XXX obsolete, not needed

        d = NSTableViewDelegate.alloc().init(cols, self._rows, id2i)
        v.setDelegate_(d)
        v.setDataSource_(d)
#       v.setEditing_(NSMain.NO_false)  # NO
        v.reloadData()

        self.NS = retain(v)
        self.NSdelegate = retain(d)

        self._window = w = TableWindow(title, self)
        # v.setDelegate_(w.delegate)
        return w

    def separator(self):
        '''Append a row separator, an empty row.
        '''
        self._rows.append(None)


class _NSTableViewDelegate(object):
    '''An ObjC-callable I{NSDelegate} class, conforming to ObjC
       protocols L{NSTableViewDelegate} and L{NSTableViewDataSource}.

       @see: The C{_NSApplicationDelegate} for more I{NSDelegate} details.
    '''
    # <http://Developer.Apple.com/documentation/appkit/nstableviewdatasource>
    # <http://Developer.Apple.com/documentation/appkit/nstableviewdelegate>
    _ObjC = ObjCSubclass('NSObject', '_NSTableViewDelegate')

    @_ObjC.method('@PPP')
    def init(self, cols, rows, id2i):
        '''Initialize the allocated L{NSTableViewDelegate}.

           @note: I{MUST} be called as C{.alloc().init(...)}.
        '''
        isinstanceOf(cols, list, tuple, name='cols')
        isinstanceOf(rows, list, tuple, name='rows')
#       self = ObjCInstance(send_message('NSObject', 'alloc'))
        self = ObjCInstance(send_super_init(self))
        self.cols = cols  # column headers/titles
        self.rows = rows
        self.id2i = id2i  # map col.identifier to number
        # self.id_s = NSStr(str(id(self)))
        return self

    @_ObjC.method('i@')
    def numberOfColumnsInTableView_(self, table):
        # table is the NSTableView created above,
        return len(self.cols)

    @_ObjC.method('i@')
    def numberOfRowsInTableView_(self, table):
        # table is the NSTableView created above,
        return len(self.rows)

    # XXX never called, NSCell_ vs NSView-based NSTableView?
#   @_ObjC.method('v@@i')
#   def tableView_didAddRowView_forRow_(self, table, view, row):
        # table is the NSTableView created in Table.display above,
        # <http://Developer.Apple.com/library/content/releasenotes/AppKit/RN-AppKit/index.html>
#       print('row %s height %s' % (row, view.fittingSize.height))

    @_ObjC.method('@@@i')  # using '*@@i' crashes **)
    def tableView_objectValueForTableColumn_row_(self, table, col, row):
        # table is the NSTableView created above,
        # row is the row number, but col is an
        # NSTableColumn instance, not an index
        # (and col.identifier must be an NSStr).
        try:
            r = self.rows[row]
            if r in (None, ()):
                # XXX reduce the height of row separator?
                # <http://Developer.Apple.com//library/content/samplecode/
                #       CocoaTipsAndTricks/Listings/TableViewVariableRowHeights_
                #       TableViewVariableRowHeightsAppDelegate_m.html>
                return _NS.BlankCell
            c = self.id2i[col.identifier()]
            # **) return an NSStr, always
            return r[c] if 0 <= c < len(r) else _NS.EmptyCell
        except (IndexError, KeyError):  # TypeError, ValueError
            c = col.identifier()
        return release(NSStr('[C%r, R%s]' % (c, row)))

    # XXX never called, NSCell- vs NSView-based NSTableView?
#   @_ObjC.method('@@i')
#   def tableView_rowViewForRow_(self, table, row):
        # table is the NSTableView created in Table.display,
        # return an NSTableRowView to use for the given row
        # <http://Developer.Apple.com/documentation/appkit/nstableviewdelegate/1532417-tableview>
#       return NSMain.nil  # means, use the default NSView

#   @_ObjC.method('@@@i')
#   def tableView_viewForTableColumn_row_(self, table, col, row):
        # table is the NSTableView created in Table.display above,
        # return a configurable NSTextField for this col and row
        # <http://Developer.Apple.com/documentation/appkit/nstableviewdelegate/1527449-tableview>
        # <http://Developer.Apple.com/library/content/documentation/Cocoa/Conceptual/TableView/
        #       PopulatingView-TablesProgrammatically/PopulatingView-TablesProgrammatically.html>
#       r = self.rows[row]
#       if r is _NS.Separator:
#           tf = NSMain.nil  # means, do not show
#       else:
#           tf = table.makeViewWithIdentifier_owner_(self.id_s, self)
#           if isNone(tf):
#               tf = NSTextField.alloc().initWithFrame_(table.frame())
#               tf.setIdentifier_(self.id_s)
#           c = self.id2i[col.identifier()]
#           tf.setStringValue_(r[c] if 0 <= c < len(r) else _NS.EmptyCell)
#       return tf

#   def tableView_viewForTableColumn_row_(self, table, col, row):  # perhaps from this Swift code?
        # <http://StackOverflow.com/questions/36634559/osx-view-based-nstableview-font-change>
#   func tableView(tableView: NSTableView, viewForTableColumn tableColumn: NSTableColumn?, row: Int) -> NSView? {
#       let cellView = tableView.makeViewWithIdentifier("myTableViewCell", owner: self) as! NSTableCellView
#       let textField = cellView.textField!
#       let fontDescriptor = textField.font!.fontDescriptor
#       textField.font = NSFont(descriptor: fontDescriptor, size: self.fontSize)
#       textField.stringValue = self.names[row]
#       textField.sizeToFit()
#       textField.setFrameOrigin(NSZeroPoint)
#       tableView.rowHeight = textField.frame.height + 2
#       return cellView }


NSTableViewDelegate = ObjCClass('_NSTableViewDelegate',  # the actual class
#                                'NSTableViewDelegate',  # protocol, ...
                                 'NSTableViewDataSource')
# XXX or NSTableViewDelegate.add_protocol('NSTableViewDelegate')
#   plus NSTableViewDelegate.add_protocol('NSTableViewDataSource')


class TableWindow(Window):
    '''Python Type for a vertically scrollable window, wrapping
       ObjC C{NSWindow/NSScrollView}.
    '''
    _table = None

    def __init__(self, title='', table=None, frame=None):
        '''New L{TableWindow}.

           @keyword title: Window name or title (C{str}).
           @keyword table: Table data (L{Table}).
           @keyword frame: Optional window frame (L{Rect}).
        '''
        isinstanceOf(table, Table, name='table')
        self._table = table

        tbl = getattr(table, 'NS', None)
        isInstanceOf(tbl, NSTableView, name='table')

        # <http://Developer.Apple.com//documentation/appkit/nswindow>
        n = tbl.dataSource().numberOfRowsInTableView_(tbl)
        # approximate height of the table content, also to
        # .setContentMaxSize_ of the window in self.limit
        h = tbl.rowHeight() * max(1, n * 1.1)
        # adjust frame to include all (or most) table rows
        f = tbl.frame() if frame is None else frame.NS
        if f.size.height < h:
            h = min(Screen().height, h)
            f.size = NSSize_t(f.size.width, h)
            tbl.setFrameSize_(f.size)

        super(TableWindow, self).__init__(title=title,
                                          frame=f,
                                          excl=WindowStyle.Miniaturizable,
                                          auto=True)  # XXX False?
        self.NSview = sv = NSScrollView.alloc().initWithFrame_(f)

        sv.setDocumentView_(tbl)
        sv.setHasVerticalScroller_(YES)

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
        '''Closing this window callback.
        '''
        try:
            _Globals.Tables.remove(self)
        except ValueError:
            pass
        self._table = None
#       self.close()
        super(TableWindow, self).windowClose_()


_Types.Table = NSTableView._Type = Table
_Types.TableWindow               = TableWindow

if __name__ == '__main__':

    from utils import _allisting

    _allisting(__all__, locals(), __version__, __file__)

# MIT License <http://OpenSource.org/licenses/MIT>
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
