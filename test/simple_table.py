
# -*- coding: utf-8 -*-

# Example of using PyCocoa to create a Table

# all imports listed explicitly to help PyChecker
from pycocoa import App, Table

__version__ = '18.04.18'


def main(timeout=None):

    app = App()

    tbl = Table(' Name', ' Value:200')
    tbl.append('Abc', 12345)
    tbl.separator()
    tbl.append('Xyz', 67890)
    tbl.display('Table - Close window to Quit', width=400)

    app.run(timeout)


if __name__ == '__main__':

    import sys

    if len(sys.argv) > 1:
        main(sys.argv.pop(1))
    else:
        main()