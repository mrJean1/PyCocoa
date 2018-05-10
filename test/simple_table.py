
# -*- coding: utf-8 -*-

# Example of using PyCocoa to create a Table

# all imports listed explicitly to help PyChecker
from pycocoa import App, Table

__version__ = '18.05.06'


def main(timeout=None):

    app = App()

    tbl = Table(' Name:bold:center', ' Value:200:Center')
    tbl.append('Abc', 12345)
    tbl.separator()
    tbl.append('Xyz', 67890)
    tbl.display('Table - Select Quit from Dock menu', width=400)

    app.run(timeout)


if __name__ == '__main__':

    import sys

    if len(sys.argv) > 1:
        main(sys.argv.pop(1))
    else:
        main()
