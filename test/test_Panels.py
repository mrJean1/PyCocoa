
# -*- coding: utf-8 -*-

import run as _  # PYCHOK sys.path
from pycocoa import AlertPanel, AlertStyle, BrowserPanel, \
                    Fonts, PanelButton, TextPanel

__version__ = '23.01.18'


def test(timeout):

    x = PanelButton.TimedOut

    a = AlertPanel(info='Informative text 1')
    assert(a.show('Main text 2', timeout=timeout) is x)
    assert(a.show('Main text 3', timeout=timeout) is x)

    a = AlertPanel(title='Title 1', style=AlertStyle.Warning, suppressable=True)
    assert(a.show('Main text 4', timeout=timeout) is x)
    assert(a.show('Main text 5', timeout=timeout) is x)

    t = TextPanel()
    assert(t.show('Main text 7', timeout=timeout) is x)
    assert(t.show(open('test/__init__.py'), timeout=timeout) is x)
    assert(t.show(open('test/__init__.py'), font=Fonts.Italic, timeout=timeout) is x)

    b = BrowserPanel()
    # XXX there is no good way to kill or close the
    # browser, since it runs as separate process or
    # new page opens in an already running browser
    if False:
        b.open('https://www.Google.com')


if __name__ == '__main__':

    import sys

    if len(sys.argv) > 1:
        _timeout = sys.argv[1]
    else:
        _timeout = 2

    test(_timeout)

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
