
# -*- coding: utf-8 -*-

# Originally <https://GitHub.com/phillip-nguyen/cocoa-python>

u'''A basic, U{ctypes<https://Docs.Python.org/2.7/library/ctypes.html>}-based
Python binding to the I{macOS} Objective-C Cocoa runtime and several other
I{macOS} libraries.

This is the U{cocoa-python<https://GitHub.com/phillip-nguyen/cocoa-python>}
package by I{Phillip Nguyen (C) 2011}, modified, extended, tested, documented
and published with permission under both the U{MIT License
<https://OpenSource.org/licenses/MIT>} and the original U{New BSD License
<https://OpenSource.org/licenses/BSD-3-Clause>}.

Installation
============

To install C{pycocoa}, type C{pip install pycocoa} or C{easy_install pycocoa} in
a terminal window.  Alternatively, download C{pycocoa-y.m.d.zip} from U{PyPI
<https://PyPI.org/project/PyCocoa>} or U{GitHub
<https://GitHub.com/mrJean1/PyCocoa>}, C{unzip} the downloaded file, C{cd} to
directory C{pycocoa-y.m.d} and type C{python setup.py install}.  To run the
PyCocoa tests, type C{python setup.py test} or C{python test/run.py} before
or after installation.

Examples U{cocoavlc.py<https://GitHub.com/oaubert/python-vlc/tree/master/examples>}
and I{simple_VLCplayer.py} require installation of the U{VLC App
<https://www.VideoLan.org/vlc/download-macosx.html>} for I{macOS} and the
corresponding U{Python-VLC<https://PyPI.org/project/python-vlc>} binding.

Documentation
=============

In addition to the U{pycocoa<https://PyPI.org/project/PyCocoa>} package, the
distribution files contain several tests, some examples and the U{documentation
<https://mrJean1.GitHub.io/PyCocoa>} (generated by U{Epydoc
<https://PyPI.org/project/epydoc>} using command line
C{epydoc --html --no-private --no-source --name=pycocoa --url=... -v pycocoa}).

Tests
=====

The tests and examples have only been run with 64-bit Python 3.13.1, 3.12.7. 3.11.5
and 2.7.18 using U{Python-VLC<https://PyPI.org/project/python-vlc>} 3.0.21, 3.0.18,
3.0.16, 3.0.12, 3.0.11, 3.0.10, 3.0.8, 3.0.6, 3.0.4 and 2.2.8 (with the compatible
U{VLC App<https://www.VideoLan.org/vlc>}) on macOS 14.6.1 Sonoma, 13.2 Ventura,
12.0.1 Monterey, 11.6.1 and 11.5.2 Big Sur (aka 10.16), 10.15.7 Catalina, 10.14.6
Mojave or 10.13.6 High Sierra.  The tests run with and without C{lazy import} in
Python 3.

Python 3.13.1, 3.12.7 and 3.11.5 run on Apple Silicon (C{arm64} I{natively}), other
Python versions run on Intel (C{x86_64}) or Intel I{emulation} (C{"arm64_x86_64"},
see function L{pycocoa.machine}).

Previously, C{pycocoa} was tested with 64-bit Python 3.10.0, 3.9.6, 3.8.6, 3.8.3, 3.8.1,
3.7.4-6, 3.6.5, 2.7.17 and macOS' 2.7.16.  However, C{pycocoa} has I{not been tested} on
iOS nor with 32-bit Python and I{does not work} with U{PyPy<https://PyPy.org>} nor with
U{Intel(R) Python<https://Software.Intel.com/en-us/distribution-for-python>}.

Notes
=====

All C{pycocoa} source code has been statically U{checked
<https://GitHub.com/ActiveState/code/tree/master/recipes/Python/546532_PyChecker_postprocessor>}
with U{PyChecker<https://PyPI.org/project/pychecker>}, U{PyFlakes
<https://PyPI.org/project/pyflakes>}, U{PyCodeStyle<https://PyPI.org/project/pycodestyle>}
(formerly Pep8) and U{McCabe<https://PyPI.org/project/mccabe>} using 64-bit Python 2.7.18
and with U{Flake8<https://PyPI.org/project/flake8>} using 64-bit Python 3.12.01 on macOS
14.1.2 Sonoma.

Some alternatives to C{pycocoa} are (a) U{PyObjC<https://PyPI.org/project/pyobjc>}, the
most comprehensive Python to Objective-C bridge (no longer included in U{macOS' Python
<https://WikiPedia.org/wiki/PyObjC#History>}), (b) U{Rubicon-ObjC
<https://PyPI.org/project/rubicon-objc>} for Python 3.5+, taking advantage of Python's
U{typing<https://Docs.Python.org/3/library/typing.html>} annotations, (c) U{PyGUI
<https://CoSC.Canterbury.AC.NZ/greg.ewing/python_gui>} for I{macOS} and (d) U{wxPython
<https://wxPython.org/pages/overview/index.html>}.

Licenses
========

U{Copyright (C) 2017-2025 -- mrJean1 at Gmail -- All Rights Reserved
<https://OpenSource.org/licenses/MIT>}.

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

__

U{Copyright (C) 2011 -- Phillip Nguyen -- All Rights Reserved
<https://OpenSource.org/licenses/BSD-3-Clause>}.

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

@newfield example: Example, Examples

'''
import os.path as _pth
import sys as _sys

# <https://PyInstaller.ReadTheDocs.io/en/stable/runtime-information.html>
_isfrozen       = getattr(_sys, 'frozen', False)
pycocoa_abspath = _pth.dirname(_pth.abspath(__file__))  # _sys._MEIPASS + '/pycocoa'
_pycocoa        = __package__ or _pth.basename(pycocoa_abspath)

__version__ = '25.01.25'
# see setup.py for similar logic
version = '.'.join(map(str, map(int, __version__.split('.'))))

def _Error(what, only):  # PYCHOK expected
    return NotImplementedError('%s not supported by %s %s, only %s'
                               % (what, _pycocoa, version, only))

_ = _sys.platform  # PYCHOK iOS?
if not _.startswith('darwin'):
    raise _Error(_, 'macOS')
_ = 'PyPy'
if _ in _sys.version:
    raise _Error(_, 'CPython')

if _isfrozen:  # avoid lazy import
    _lazy_import2 = None
else:
    # setting __path__ should ...
    __path__ = [pycocoa_abspath]
    try:  # ... make this import work, ...
        import pycocoa.lazily as _
    except ImportError:  # ... if it doesn't, extend
        # _sys.path to include this very directory such
        # that all public and private sub-modules can
        # be imported (and checked by PyChecker, etc.)
        _sys.path.insert(0, pycocoa_abspath)  # XXX __path__[0]

    try:
        # lazily requires Python 3.7+, see lazily.__doc__
        from pycocoa.lazily import LazyImportError, _lazy_import2, _PY_FH  # PYCHOK expected
        _, __getattr__ = _lazy_import2(_pycocoa)  # PYCHOK expected

    except (ImportError, LazyImportError, NotImplementedError):
        _lazy_import2 = _PY_FH = None

    if _PY_FH == _pycocoa:  # override Python 3.3+ faulthandler
        import pycocoa.faults as _

del _, _Error, _pth, _sys  # exclude from globals(), __all__

if not _lazy_import2:  # import and set __all__

    import pycocoa.nstypes as nstypes  # PYCHOK exported
    import pycocoa.octypes as octypes  # PYCHOK exported
    import pycocoa.oslibs  as oslibs   # PYCHOK exported
    import pycocoa.pytypes as pytypes  # PYCHOK exported
    import pycocoa.runtime as runtime  # PYCHOK exported

    # Python Type wrappers
    import pycocoa.apps     as apps      # PYCHOK exported
    import pycocoa.bases    as bases     # PYCHOK exported
    import pycocoa.bases    as bases     # PYCHOK exported
    import pycocoa.colors   as colors    # PYCHOK exported
    import pycocoa.faults   as faults    # PYCHOK exported
    import pycocoa.fonts    as fonts     # PYCHOK exported
    import pycocoa.getters  as getters   # PYCHOK exported
    import pycocoa.geometry as geometry  # PYCHOK exported
    import pycocoa.lazily   as lazily    # PYCHOK exported
    import pycocoa.lists    as lists     # PYCHOK exported
    import pycocoa.menus    as menus     # PYCHOK exported
    import pycocoa.panels   as panels    # PYCHOK exported
    import pycocoa.printers as printers  # PYCHOK exported
    import pycocoa.screens  as screens   # PYCHOK exported
    import pycocoa.sets     as sets      # PYCHOK exported
    import pycocoa.strs     as strs      # PYCHOK exported
    import pycocoa.tables   as tables    # PYCHOK exported
    import pycocoa.tuples   as tuples    # PYCHOK exported
    import pycocoa.utils    as utils     # PYCHOK exported
    import pycocoa.windows  as windows   # PYCHOK exported

    # lift all public classes, constants, functions,
    # etc. (see also David Beazley's talk
    # <https://DaBeaz.com/modulepackage/index.html>)
    from pycocoa.nstypes import *  # PYCHOK __all__
    from pycocoa.octypes import *  # PYCHOK __all__
    from pycocoa.oslibs  import *  # PYCHOK __all__
    from pycocoa.pytypes import *  # PYCHOK __all__
    from pycocoa.runtime import *  # PYCHOK __all__

    # Python Type wrappers
    from pycocoa.apps     import *  # PYCHOK __all__
    from pycocoa.bases    import *  # PYCHOK __all__
    from pycocoa.colors   import *  # PYCHOK __all__
    from pycocoa.dicts    import *  # PYCHOK __all__
    from pycocoa.fonts    import *  # PYCHOK __all__
    from pycocoa.faults   import *  # PYCHOK __all__
    from pycocoa.getters  import *  # PYCHOK __all__
    from pycocoa.geometry import *  # PYCHOK __all__
    from pycocoa.lazily   import *  # PYCHOK __all__
    from pycocoa.lists    import *  # PYCHOK __all__
    from pycocoa.menus    import *  # PYCHOK __all__
    from pycocoa.panels   import *  # PYCHOK __all__
    from pycocoa.printers import *  # PYCHOK __all__
    from pycocoa.screens  import *  # PYCHOK __all__
    from pycocoa.sets     import *  # PYCHOK __all__
    from pycocoa.strs     import *  # PYCHOK __all__
    from pycocoa.tables   import *  # PYCHOK __all__
    from pycocoa.tuples   import *  # PYCHOK __all__
    from pycocoa.utils    import *  # PYCHOK __all__
    from pycocoa.windows  import *  # PYCHOK __all__

    # if needed, for backward compatibility with cocoa-python:
    # cfarray_to_list               = nsArray2listuple           # PYCHOK expected
    # cfnumber_to_number            = cfNumber2num               # PYCHOK expected
    # cfset_to_set                  = nsSet2set                  # PYCHOK expected
    # CFSTR                         = NSStr                      # PYCHOK expected
    # cfstring_to_string            = cfString2str               # PYCHOK expected
    # cftype_to_value               = ns2py                      # PYCHOK expected
    # create_subclass               = add_subclass               # PYCHOK expected
    # DeallocObserver               = _nsDeallocObserver         # PYCHOK expected
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
    __all__ = tuple(set(_ for _ in locals().keys() if  # _UNDER_
                          not _.startswith(('_', 'CFUNCTION', 'c_', 'kC')))) \
            + lazily._C_XTYPES  # export some extended C types


def _locals():
    '''(INTERNAL) For C{pycocoa.__main__.py} only'
    '''
    return globals()
