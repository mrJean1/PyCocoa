
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Handle I{uncaught} C{ObjC/NSExceptions} and other C{fault}s similar
to standard module C{faulthandler} available since Python 3.3.

By default, C{fault} handling is not enabled.  In Python 3.3 and
later, the U{faulthandler<https://Docs.Python.org/3/library/faulthandler.html>}
may be enabled by (a) calling function C{faulthandler.enable} or
(b) setting environment variable U{PYTHONFAULTHANDLER
<https://Docs.Python.org/3/using/cmdline.html#envvar-PYTHONFAULTHANDLER>}
to any no-empty string or (c) including option C{-X faulthandler}
on the python command line.

For other Python releases, C{fault} handling by this module L{pycocoa.faults}
is enabled by either (a) calling function L{faults.enable} or (b) setting
environment variable U{PYTHONFAULTHANDLER
<https://Docs.Python.org/3/using/cmdline.html#envvar-PYTHONFAULTHANDLER>}
to any no-empty string.  Command line option C{-X faulthandler} is not
available in older Python versions.

B{NOTE, if in Python 3.3 or later,} the environment variable is defined as
B{U{PYTHONFAULTHANDLER=pycocoa
<https://Docs.Python.org/3/using/cmdline.html#envvar-PYTHONFAULTHANDLER>}},
the Python C{faulthandler} will be overridden by this module L{pycocoa.faults}.

@note: Functions L{faults.disable}, L{faults.enable}, L{faults.exiting},
L{faults.is_enabled} and L{faults.SIGs_enabled} are not exported publicly
as C{pycocoa.disable}, C{pycocoa.enable}, C{pycocoa.exiting}, etc., only
function L{setUncaughtExceptionHandler} is.
'''
# all imports listed explicitly to help PyChecker
from pycocoa.lazily  import _ALL_DOCS, _ALL_LAZY
from pycocoa.nstypes import  NSExceptionError, NSMain
from pycocoa.oslibs  import _setUncaughtExceptionHandler, _UncaughtExceptionHandler_t
from pycocoa.runtime import  ObjCInstance  # release
from pycocoa.utils   import _Globals, logf

import os
import signal as _signal
import sys

__all__ = _ALL_LAZY.faults
__version__ = '20.11.15'

_exiting = -9  # default _exit and status
_PY_FH   =  os.environ.get('PYTHONFAULTHANDLER', None)
# SIGnals handled by Python 3 C{faulthandler}
_SIGnals = (_signal.SIGABRT,  # critical
            _signal.SIGBUS, _signal.SIGFPE,
            _signal.SIGILL, _signal.SIGSEGV)


def _bye(name):
    '''(INTERNAL) Time to go ...
    '''
    logf('%s(%s) from %s', exiting.__name__, _exiting, name, nl=1, nt=1)
    if _exiting < 0:
        os._exit(-_exiting)  # force exit
    else:
        sys.exit(_exiting)


def _SIGdict(sigs, enabled):
    '''(INTERNAL) Get a C{dict} of C{SIG*} name and I{value}.
    '''
    if not sigs:
        sigs = _SIGnals
    return dict((_SIGname(sig), sig) for sig in enabled if sig in sigs)


def _SIGname(sig):
    '''(INTERNAL) Get the name of signal B{C{sig}}.
    '''
    for S in dir(_signal):
        if S.isupper() and S.startswith('SIG') \
                       and getattr(_signal, S, None) == sig:
            return S
    return '%s%s' % ('SIG', sig)


try:  # MCCABE 27
    if _PY_FH == 'pycocoa':
        raise ImportError

    import faulthandler as _fh  # Python 3.3+

    def disable():
        _fh.disable()
    disable.__doc__ = _fh.disable.__doc__

    def enable(file=sys.stderr, **kwds):
        NSMain.stdlog = file
        _fh.enable(file=file, **kwds)
    enable.__doc__ = _fh.enable.__doc__

    def is_enabled(sig=None):
        '''Check whether the C{faulthandler} is enabled.

           @keyword sig: Check whether C{faulthandler}
                         includes this signal (C{signal.SIG*}).

           @return: C{True}, C{faulhandler} is currently enabled,
                    C{False} otherwise.
        '''
        r = False
        if _fh.is_enabled():
            r = (sig is None) or (sig in _SIGnals)
        return r

    def SIGs_enabled(*sigs):
        '''Return the signals handled by the C{faulthandler}.

           @return: A C{dict} with the C{SIG*} name and value
                    the currently handled signals, if any.
        '''
        return _SIGdict(sigs, _SIGnals if _fh.is_enabled() else ())

except ImportError:

    import traceback

    try:
        _SIGraise = _signal.raise_signal
    except AttributeError:

        def _SIGraise(sig):
            '''(INTERNAL) Mimick C{signal.raise_signal}.
            '''
            os.kill(os.getpid(), sig)

    _SIGenabled = {}  # C{fault} handling enabled if not empty

    def _SIGhandler(sig, frame):  # PYCHOK unused
        '''(INTERNAL) Handler for the C{signal}s enabled by C{fault}.
        '''
        logf('traceback (most recent call last):')
        for t in '\n'.join(traceback.format_stack(frame)).split('\n'):
            if t:
                logf(t)
        _bye(_SIGname(sig) + 'handler')

    def _unCatcher(error):
        '''(INTERNAL) Default handler for I{uncaught} C{ObjC/NSExceptions}
           wrapped as an L{NSExceptionError}.
        '''
        logf('handling %s', error, nl=1)
        _SIGraise(_signal.SIGABRT)
        return error  # throw error in case _SIGraise failed

    def disable():  # PYCHOK expected
        '''Disable C{fault} handling and uninstall the signal handlers
           installed by L{faults.enable}, like the U{faulthandler
           <https://Docs.Python.org/3/library/faulthandler.html>}
           module in Python 3.3 and later.

           @return: C{None}.
        '''
        while _SIGenabled:
            sig, h = _SIGenabled.popitem()
            if h is not None:
                _signal.signal(sig, h)
        NSMain.stdlog = sys.stdout  # initial _Globals.stdlog

    def enable(file=sys.stderr, **unused):  # PYCHOK expected
        '''Enable C{fault} handling similar to the U{faulthandler
           <https://Docs.Python.org/3/library/faulthandler.html>}
           module available in Python 3.3 and later.

           Try to install handlers for the C{SIGABRT}, C{SIGBUS},
           C{SIGFPE}, C{SIGILL} and C{SIGSEGV} signals to dump a
           an ObjC call stack and Python traceback to B{C{file}}.

           @raise TypeError: File B{C{file}} doesn't have callable
                             C{write} and C{flush} attributes.

           @see: C{NSMain.stdlog}.
        '''
        NSMain.stdlog = file

        if is_enabled():
            disable()
        for sig in _SIGnals:
            try:
                _SIGenabled[sig] = _signal.signal(sig, _SIGhandler)
            except (IOError, OSError):
                pass

        setUncaughtExceptionHandler(_unCatcher)

    def is_enabled(sig=None):  # PYCHOK expected
        '''Check whether C{fault} handling is enabled, similar to the
           U{faulthandler<https://Docs.Python.org/3/library/faulthandler.html>}
           module available in Python 3.3 and later.

           @keyword sig: Check whether C{fault} handling includes this
                         signal (C{signal.SIG*}).

           @return: C{True} if C{fault} handling is currently enabled,
                    C{False} otherwise.
        '''
        return bool(len(_SIGenabled)) if sig is None else (sig in _SIGenabled)

    def SIGs_enabled(*sigs):  # PYCHOK expected
        '''Return the signals currently handled as C{fault}.

           @return: A C{dict} with the C{SIG*} name and value of
                    the currently handled signals, if any.
        '''
        return _SIGdict(sigs, _SIGenabled.keys())


def exiting(status=None):
    '''Get/set the C{exit} and C{status} to use after C{fault}s or
       I{uncaught} C{ObjC/NSException}s.

       @keyword status: The exit "door" and status code to be used (C{small
                        int}) or C{None} to leave unchanged.  A I{negative}
                        B{C{status}} invokes C{os._exit(abs(status))} to
                        terminate without normal exit processing, while a
                        I{non-negative} B{C{status}} uses C{sys.exit(status)}
                        after a C{fault}.

       @return: The previously set B{C{exiting}} code (C{int}).

       @note: The C{faulthandler} module in Python 3.3 and later ignores
              all B{C{exiting}} settings.
    '''
    global _exiting
    s = _exiting
    if status is not None and isinstance(status, int) \
                          and -100 < status < 100:
        _exiting = status
    return s


def setUncaughtExceptionHandler(handler, log=True, raiser=False):
    '''Install a callback to handle I{uncaught} C{ObjC/NSException}s.

       The C{B{handler}(error)} is called with one argument C{error},
       an L{NSExceptionError} instance.  It should return either C{None}
       or that same C{error}.  In the latter case, that C{error} will
       subsequently be raised as Python exception.

       @param handler: A callable to be invoked with a single argument
                       C{error}, an L{NSExceptionError} instance and
                       returning C{None} or that very C{error}.
       @keyword log: Print the C{error}, time stamp, ObjC callstack
                     and Python traceback prior to invoking the
                     B{C{handler}} (C{bool}).
       @keyword raiser: Raise the L{NSExceptionError} B{C{error}},
                        regardless of the return value from the
                        B{C{handler}}.

       @return: The previously installed I{uncaught} C{ObjC/NSException}
                handler or C{None} if no handler was installed.

       @raise TypeError: The B{C{handler}} is not callable.

       @note: Faults like C{SIGILL}, C{SIGSEGV}, etc. do not throw
              I{uncaught} C{ObjC/NSException}s and will not invoke the
              given B{C{handler}}.  However, those and several other
              signals can be handled as C{fault}s, see L{faults.enable},
              L{faults.disable} and other functions module L{faults}.

       @see: Dgelessus' U{pythonista_startup.py<https://gist.GitHub.com/dgelessus>},
             U{Handling Exceptions<https://Developer.Apple.com/library/archive/
             documentation/Cocoa/Conceptual/Exceptions/Tasks/HandlingExceptions.html>}
             and U{Error Handling Programming Guide<https://Developer.Apple.com/
             library/archive/documentation/Cocoa/Conceptual/ErrorHandlingCocoa/
             ErrorHandling/ErrorHandling.html#//apple_ref/doc/uid/TP40001806>}.
    '''

    if not callable(handler):
        raise TypeError('non-callable %s: %r' % ('handler', handler))

    @_UncaughtExceptionHandler_t
    def _handler(nsException):
        e = NSExceptionError(ObjCInstance(nsException))
        if log:
            s = e.reason or '*** n/a'
            logf('uncaught ObjC/%s: %s', e.name, s, nl=1)
            logf('datetime %s (%s)', e.datetime, e.versionstr)
            if e.info:
                logf('info: %s', e.info)
            logf('callstack (most recent last):')
            for s in e.callstack:
                logf('  %s', s)  # argv0='', nt=1

        if handler(e) is e or raiser:
            raise e

        _bye(handler.__name__)

    _ = _setUncaughtExceptionHandler(_handler)
    h = None  # previous
    if _Globals.Xhandler2:
        h, _h = _Globals.Xhandler2
        del _h  # release(_h)
    _Globals.Xhandler2 = (handler, _handler)  # retain(_handler)
    return h


# enable like Python 3.3+
if _PY_FH and not is_enabled():
    enable()

__all__ += _ALL_DOCS(disable, enable, exiting, is_enabled, SIGs_enabled)

if __name__ == '__main__':

    if is_enabled() or '-X' in sys.argv[1:]:
        # test fault handling
        enable(sys.stdout)
        logf('%s: %s', SIGs_enabled.__name__, SIGs_enabled())

        from pycocoa.nstypes import NSColor
        r = NSColor.redColor()
        c = r.cyanComponent()  # bye ...

    from pycocoa.utils import _all_listing

    _all_listing(__all__, locals())

# % [env PYTHONFAULTHANDLER=pycocoa] python[3] -m pycocoa.faults [-X]
#
# pycocoa.faults.__all__ = tuple(
#  pycocoa.faults.exito is <function .exito at 0x7fe1efc8b0d0>,
#  pycocoa.faults.setUncaughtExceptionHandler is <function .setUncaughtExceptionHandler at 0x7fe1efc8b160>,
# )[2]
# pycocoa.faults.version 20.11.14, .isLazy 1, Python 3.9.0 64bit, macOS 10.15.7

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2020 -- mrJean1 at Gmail -- All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
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
