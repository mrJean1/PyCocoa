
# -*- coding: utf-8 -*-

from pycocoa import AlertPanel, AlertStyle, BrowserPanel, \
                    Fonts, PanelButton, TextPanel

__version__ = '18.05.28'


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
        b.open('http://www.Google.com')


if __name__ == '__main__':

    import sys

    if len(sys.argv) > 1:
        _timeout = sys.argv[1]
    else:
        _timeout = 2

    test(_timeout)
