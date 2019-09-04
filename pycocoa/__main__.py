
# -*- coding: utf-8 -*-

u'''Print L{pycocoa} version, etc. using C{python -m pycocoa}.
'''

from pycocoa import __all__, __version__, _locals
from pycocoa.utils import _allisting  # PYCHOK expected

_allisting(__all__, _locals(), __version__, 'pycocoa')

from pycocoa.runtime import _nsDeallocObserverIvar1
_nsDeallocObserverIvar1()

__all__ = ()
__version__ = '19.07.21'

# **) MIT License
#
# Copyright (C) 2018-2019 -- mrJean1 at Gmail dot com
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
