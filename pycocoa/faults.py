
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
functions L{getUncaughtExceptionHandler} and L{setUncaughtExceptionHandler}
are.
'''
# all imports listed explicitly to help PyChecker
from pycocoa.lazily  import _ALL_DOCS, _ALL_LAZY, _NL_, _NN_, _pycocoa_, _PY_FH
from pycocoa.nstypes import _not_given_, NSExceptionError, NSMain
from pycocoa.oslibs  import _setUncaughtExceptionHandler, _UncaughtExceptionHandler_t
from pycocoa.runtime import  ObjCInstance  # release
from pycocoa.utils   import  Adict, _Globals, logf

import os
import signal as _signal
import sys

__all__ = _ALL_LAZY.faults
__version__ = '21.11.04'

_exiting = -9  # default _exit and status
# SIGnals handled by Python 3 C{faulthandler}
_SIGnals = (_signal.SIGABRT,  # critical
            _signal.SIGBUS, _signal.SIGFPE,
            _signal.SIGILL, _signal.SIGSEGV)


def _bye(name):
    '''(INTERNAL) Time to go ...
    '''
    logf('%s(%s) %s %s %s', exiting.__name__, _exiting,
                           'from', name, 'handler',
                            nl=1, nt=1)
    if _exiting < 0:
        os._exit(-_exiting)  # force exit
    else:
        sys.exit(_exiting)


def _SIGdict(sigs, enabled):
    '''(INTERNAL) Get a C{dict} of C{SIG*} name and C{sig} number.
    '''
    if not sigs:
        sigs = _SIGnals
    return Adict((_SIGname(sig), sig) for sig in enabled if sig in sigs)


def _SIGname(sig):
    '''(INTERNAL) Get the name of signal B{C{sig}}.
    '''
    for S in dir(_signal):
        if S.isupper() and S.startswith('SIG') \
                       and getattr(_signal, S) == sig:
            return S
    return _NN_('SIG', sig)


try:  # MCCABE 26
    if _setUncaughtExceptionHandler and _PY_FH == _pycocoa_:
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

           @return: An L{Adict} with the C{SIG*} name and value
                    the currently handled signals, if any.
        '''
        return _SIGdict(sigs, _SIGnals if _fh.is_enabled() else ())

except ImportError:  # and not macOS 12.0.1 Monterey

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
        for t in _NL_.join(traceback.format_stack(frame)).split(_NL_):
            if t:
                logf(t)
        _bye(_SIGname(sig))

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

           @return: An L{Adict} with the C{SIG*} name and value of
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


def getUncaughtExceptionHandler():
    '''Get the currently installed I{uncaught} C{ObjC/NSException}
       handler.

       @return: The installed handler (C{callable}) or C{None} if
                no handler was or couldn't be installed (like on
                macOS 12.0.1 Monterey, for example).
    '''
    if _Globals.Xhandler2:
        h, _ = _Globals.Xhandler2
    else:
        h = None
    return h


def setUncaughtExceptionHandler(handler, log=True, raiser=False):
    '''Install a callback to handle I{uncaught} C{ObjC/NSException}s.

       The C{B{handler}(error)} is called with one argument C{error},
       an L{NSExceptionError} instance.  It should return that same
       C{error}, an L{exiting} C{status} or C{None}.  In in former
       case, that C{error} will subsequently be raised as Python
       exception.

       @param handler: A callable to be invoked with a single argument
                       C{error}, an L{NSExceptionError} instance and to
                       return that same C{error}, an L{exiting} C{status}
                       or C{None}.
       @keyword log: Print the C{error}, an time stamp and -if avilable-
                     the ObjC callstack and Python traceback prior to
                     invoking the B{C{handler}} (C{bool}).
       @keyword raiser: Raise the L{NSExceptionError} B{C{error}},
                        regardless of the return value from the
                        B{C{handler}}.

       @return: The previously installed I{uncaught} C{ObjC/NSException}
                handler or C{None} if no handler was or couldn't be installed.

       @raise RuntimeError: Setting uncaught exception handlers unavailable,
                            but only thrown if B{C{raiser}=True}.

       @raise TypeError: The B{C{handler}} is not callable.

       @note: Faults like C{SIGILL}, C{SIGSEGV}, etc. do not throw
              I{uncaught} C{ObjC/NSException}s and will not invoke the
              given B{C{handler}}.  However, those and several other
              signals can be handled as C{fault}s, see L{faults.enable},
              L{faults.disable} and other functions module L{faults}.

       @note: An I{uncaught} C{ObjC/NSException} always results in
              (graceful) termination of the process.

       @note: I{Uncaught} C{ObjC/NSException}s are not U{reported
              <https://Developer.Apple.com/documentation/appkit/nsapplication/
              1428396-reportexception>} to an C{NSLog} file (yet).

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
            s = e.reason or _not_given_
            logf('uncaught ObjC/%s: %s', e.name, s, nl=1)
            logf('datetime %s (%s)', e.datetime, e.versionstr)
            if e.info:
                logf('info: %s', e.info)
            logf('callstack (most recent last):')
            for s in e.callstack:
                logf('  %s', s)  # argv0=_NN_, nt=1

        r = handler(e)
        if r is e or raiser:
            raise e
        elif isinstance(r, int):
            exiting(r)

        _bye(handler.__name__)

    h = None
    if _setUncaughtExceptionHandler:
        _ = _setUncaughtExceptionHandler(_handler)
        if _Globals.Xhandler2:
            h, _h = _Globals.Xhandler2
            del _h  # release(_h)
        _Globals.Xhandler2 = (handler, _handler)  # retain(_handler)
    elif raiser:
        raise RuntimeError('no %s' % (setUncaughtExceptionHandler.__name__,))
    return h  # previous


# enable like Python 3.3+
if _PY_FH and not is_enabled():
    enable()

__all__ += _ALL_DOCS(disable, enable, exiting, is_enabled, SIGs_enabled)

if __name__ == '__main__':

    if is_enabled() and '-X' in sys.argv[1:]:
        # test fault handling
        enable(sys.stdout)
        logf('%s: %s', SIGs_enabled.__name__, SIGs_enabled())

        from pycocoa.nstypes import NSColor
        r = NSColor.redColor()
        c = r.cyanComponent()  # bye ...

    elif _PY_FH and '-raise' in sys.argv[1:]:
        # throw an ObjC/NSException and catch it
        from pycocoa.nstypes import nsRaise
        logf('%s ...', nsRaise.__name__)

        nsRaise(reason='testing', _PY_FH=_PY_FH)

    elif _PY_FH and '-try' in sys.argv[1:]:
        # throw an ObjC/NSException, have the handler
        # raise the NSExceptionError and then try to
        # catch that as a regular Python exception:
        # - doesn't work, the exception never forces
        # return of control to Python, instead the
        # process terminates with Abrt
        # - even setting a SIGABRT handler inside the
        # uncaught ObjC/NSException handler to try to
        # override ObjC/NS does not help, same
        # result, terminated by Abrt
        from pycocoa.nstypes import nsRaise  # PYCHOK twice
        logf('%s ...', 'try:')

        def _h(x):
            # raise ValueError
            return 8  # x

        setUncaughtExceptionHandler(_h)
        try:
            nsRaise(reason='testing', _PY_FH=_PY_FH)
        except (NSExceptionError, SystemExit) as x:
            logf('except: %s', x)

    from pycocoa.utils import _all_listing

    _all_listing(__all__, locals())

# % [env PYTHONFAULTHANDLER=pycocoa] python[3] -m pycocoa.faults [-X]
#
# pycocoa.faults.__all__ = tuple(
#  pycocoa.faults.getUncaughtExceptionHandler is <function .getUncaughtExceptionHandler at 0x10541fe20>,
#  pycocoa.faults.setUncaughtExceptionHandler is <function .setUncaughtExceptionHandler at 0x10541feb0>,
# )[2]
# pycocoa.faults.version 21.11.04, .isLazy 1, Python 3.11.0 64bit arm64, macOS 13.0.1

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2023 -- mrJean1 at Gmail -- All Rights Reserved.
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
