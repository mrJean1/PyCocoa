
# -*- coding: utf-8 -*-

# Originally <http://GitHub.com/phillip-nguyen/cocoa-python>

u'''A basic, partial, U{ctypes
<http://Docs.Python.org/2.7/library/ctypes.html>}-based Python binding to
the I{macOS} Objective-C Cocoa runtime and several other I{macOS} libraries.

This is the U{cocoa-python<http://GitHub.com/phillip-nguyen/cocoa-python>}
package by I{Phillip Nguyen (C) 2011}, modified, extended, tested,
documented and published with permission under both the original
U{New BSD License<http://OpenSource.org/licenses/BSD-3-Clause>} and the
U{MIT License<http://OpenSource.org/licenses/MIT>}.

In addition to the U{pycocoa<http://PyPI.Python.org/pypi/PyCocoa>} package,
the distribution files contain several tests, examples and
U{documentation <http://mrJean1.GitHub.io/PyCocoa>} (generated by
U{Epydoc<http://PyPI.Python.org/pypi/epydoc>} using command line:
C{epydoc --html --no-private --no-source --name=PyCocoa --url=... -v pycocoa}).

Examples U{cocoavlc.py<http://GitHub.com/oaubert/python-vlc/tree/master/examples>}
and I{simple_VLCplayer.py} require installation of the U{VLC App
<http://www.VideoLan.org/vlc/download-macosx.html>} for I{macOS} and the corresponding
U{Python-VLC<http://PyPI.Python.org/pypi/python-vlc>} binding.

The tests and examples have only been run with 64-bit Python 2.7.14 and
3.6.5 (with U{VLC<http://PyPI.Python.org/pypi/python-vlc>} 2.2.6 and 3.0.1)
and only on macOS 10.13.4 High Sierra.  PyCocoa has I{not} been tested on
iOS nor with 32-bit Python.

All PyCocoa source code has been statically
U{checked<http://GitHub.com/ActiveState/code/tree/master/recipes/Python/546532_PyChecker_postprocessor>}
with U{PyChecker<http://PyPI.Python.org/pypi/pychecker>},
U{PyFlakes<http://PyPI.Python.org/pypi/pyflakes>},
U{PyCodeStyle<http://PyPI.Python.org/pypi/pycodestyle>} (formerly Pep8) and
U{McCabe<http://PyPI.Python.org/pypi/mccabe>} using 64-bit Python 2.7.14 and with
U{Flake8<http://PyPI.Python.org/pypi/flake8>} on 64-bit Python 3.6.5.

To install PyCocoa, type C{pip install PyCocoa} or C{easy_install PyCocoa}
in a terminal window.  Alternatively, download C{PyCocoa-} from
U{PyPI<http://PyPI.Python.org/pypi/PyCocoa/>} or
U{GitHub<http://GitHub.com/mrJean1/PyCocoa>}, C{unzip} the downloaded file,
C{cd} to directory C{PyCocoa-} and type C{python setup.py install}.  To
run the PyCocoa tests, type C{python setup.py test} before installation.

Some alternatives to PyCocoa are (a) U{PyObjC<http://PyPI.Python.org/pypi/pyobjc/>},
the most comprehensive Python to Objective-C bridge, (b)
U{Rubicon-ObjC<http://PyPI.Python.org/pypi/rubicon-objc/>} for Python 3.5+,
taking advantage of Python's new
U{typing<http://Docs.Python.org/3/library/typing.html>} annotations and (c)
U{PyGUI<http://www.cosc.canterbury.ac.nz/greg.ewing/python_gui>} for I{macOS}.

__

U{Copyright (C) 2011 -- Phillip Nguyen -- All Rights Reserved.
<http://OpenSource.org/licenses/BSD-3-Clause>}

C{Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:}

C{1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.}

C{2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.}

C{3. Neither the name of objective-ctypes nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.}

C{THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.}

__

U{Copyright (C) 2017-2018 -- mrJean1 at Gmail dot com
<http://OpenSource.org/licenses/MIT>}

C{Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:}

C{The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.}

C{THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.}

@newfield example: Example, Examples

@var libobjc: The macOS C{objc} library (C{ctypes.CDLL})
'''

from os.path import abspath, dirname
import sys

__version__ = '18.05.08'

p = sys.platform
if not p.startswith('darwin'):
    raise NotImplementedError('%s not supported, only %s' % (p, 'macOS'))
del p

# PyChecker chockes on .import
d = dirname(abspath(__file__))
if d not in sys.path:
    sys.path.insert(0, d)
del d, abspath, dirname, sys

from nstypes import *  # PYCHOK expected
from octypes import *  # PYCHOK expected
from oslibs  import *  # PYCHOK expected
from pytypes import *  # PYCHOK expected
from runtime import *  # PYCHOK expected

# Python Type wrappers
from apps     import *  # PYCHOK expected
from bases    import *  # PYCHOK expected
from dicts    import *  # PYCHOK expected
from fonts    import *  # PYCHOK expected
from getters  import *  # PYCHOK expected
from geometry import *  # PYCHOK expected
from lists    import *  # PYCHOK expected
from menus    import *  # PYCHOK expected
from panels   import *  # PYCHOK expected
from sets     import *  # PYCHOK expected
from strs     import *  # PYCHOK expected
from tables   import *  # PYCHOK expected
from tuples   import *  # PYCHOK expected
from utils    import *  # PYCHOK expected
from windows  import *  # PYCHOK expected

# if needed, for backward compatibility with cocoa-python:
# cfarray_to_list               = cfArray2list               # PYCHOK expected
# cfnumber_to_number            = cfNumber2num               # PYCHOK expected
# cfset_to_set                  = cfSet2set                  # PYCHOK expected
# CFSTR                         = CFStr                      # PYCHOK expected
# cfstring_to_string            = cfString2str               # PYCHOK expected
# cftype_to_value               = cfType2py                  # PYCHOK expected
# create_subclass               = add_subclass               # PYCHOK expected
# DeallocObserver               = deallocObserver            # PYCHOK expected
# get_cfunctype                 = get_c_func_t               # PYCHOK expected
# get_instance_variable         = get_ivar                   # PYCHOK expected
# get_NSString                  = NSStr                      # PYCHOK expected
# get_object_class              = get_classof                # PYCHOK expected
# get_superclass_of_object      = get_superclassof           # PYCHOK expected
# objc                          = libobjc                    # PYCHOK expected
# objc_id                       = Id_t                       # PYCHOK expected
# OBJC_SUPER                    = objc_super_t               # PYCHOK expected
# OBJC_SUPER_PTR                = objc_super_t_ptr           # PYCHOK expected
# ObjCClass.get_class_method    = ObjCClass.get_classmethod  # PYCHOK expected
# ObjCClass.get_instance_method = ObjCClass.get_method       # PYCHOK expected
# parse_type_encoding           = split_encoding             # PYCHOK expected
# set_instance_variable         = set_ivar                   # PYCHOK expected
# unichar                       = unichar_t                  # PYCHOK expected
# UniChar                       = UniChar_t                  # PYCHOK expected

# if needed, previous NS...WindowMask names, deprecated ones are marked with D?
# NSBorderlessWindowMask             = NSWindowStyleMaskBorderless              # PYCHOK D?
# NSClosableWindowMask               = NSWindowStyleMaskClosable                # PYCHOK expected
# NSFullScreenWindowMask             = NSWindowStyleMaskFullScreen              # PYCHOK D?
# NSFullSizeContentViewWindowMask    = NSWindowStyleMaskFullSizeContentView     # PYCHOK D?
# NSHUDWindowMask?                   = NSWindowStyleMaskHUDWindow               # PYCHOK D?
# NSMiniaturizableWindowMask         = NSWindowStyleMaskMiniaturizable          # PYCHOK expected
# NSMiniWindowMask                   = NSWindowStyleMaskNonactivatingPanel      # PYCHOK D?
# NSResizableWindowMask              = NSWindowStyleMaskResizable               # PYCHOK expected
# NSTexturedBackgroundWindowMask     = NSWindowStyleMaskTexturedBackground      # PYCHOK D?
# NSTitledWindowMask                 = NSWindowStyleMaskTitled                  # PYCHOK D?
# NSUtilityWindowMask                = NSWindowStyleMaskUtilityWindow           # PYCHOK D?
# NSUnifiedTitleAndToolbarWindowMask = NSWindowStyleMaskUnifiedTitleAndToolbar  # PYCHOK D?
# NSUnscaledWindowMask               = NSWindowStyleMaskUnscaled                # PYCHOK D? XXX

# filter locals() for .__init__.py
from utils import _exports  # PYCHOK expected
__all__ = _exports(locals(), not_starts=('_', 'CFUNCTION', 'c_', 'kC'))

if __name__ == '__main__':

    from utils import _allisting  # PYCHOK expected

    _allisting(__all__, locals(), __version__, 'pycocoa')
