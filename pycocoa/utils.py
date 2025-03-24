
# -*- coding: utf-8 -*-

# License at the end of this file.

'''Private and public utility functions.
'''
from pycocoa.internals import bytes2str, _ByteStrs, _COLON_, _COMMA_, \
                             _COLONSPACE_, _COMMASPACE_, _Ddoc_, _Dmain_,\
                             _DOT_, _EQUALS_, _fmt, _fmt_invalid, _Globals, \
                             _instr, _int2, _Ints, _kwdstr, missing, _NL_, \
                             _NN_, _SPACE_, str2bytes, _TypeError, \
                             _UNDER_, _writef,  sys   # _Dall_, _Dfile_, _Dversion_
from pycocoa.lazily import _ALL_LAZY, isLazy, _Python_version

import os.path as _os_path
import platform as _platform
# import sys  # from .lazily

__all__ = _ALL_LAZY.utils
__version__ = '25.03.24'

_bCOL = b':'  # in .octypes


def _all_listing(alls, localls, libs=False, _file_=_NN_, argv0='#'):
    '''(INTERNAL) Print sorted __all__ names and values.
    '''
    from pycocoa.internals import _Dall_, _Dfile_, _Dversion_

    def _all_in(alls, inns, m, n):
        t = tuple(a for a in alls if a not in inns)
        if t:
            t = _COMMASPACE_.join(t)
            t = _COLONSPACE_(_DOT_(m, n), t)
            t = _SPACE_(missing, t)
            raise NameError(t)

    t =  alls.__class__.__name__
    f = _file_ or localls.get(_Dfile_, _NN_)
    m, n = _dirbasename2(f)
    printf('%s = %s(', _DOT_(m, _Dall_), t, argv0=argv0, nl=1)

    lazy = _ALL_LAZY.get(n, ())
    if lazy:
        _all_in(alls, lazy,   'lazily', n)
        _all_in(lazy, alls,    m, _Dall_)
        _all_in(lazy, localls, m, 'locals()')

    d = i = 0
    p = _NN_
    S = _SPACE_ * (len(m) + 2)
    for n in _asorted(alls):
        v = localls[n]
        r = repr(v)
        if isinstance(v, _Ints):
            r = '%s or 0x%X' % (r, v)
            v, s = _int2(v)
            if s > 2:
                r = _fmt('%s or %d<<%s', r, v, s)
        elif r.startswith('<class '):
            r = r.replace("'", _NN_)
        elif r.startswith('<function '):
            r = r[:10] + _DOT_(v.__module__, r[10:])
        r = r.replace(_Dmain_, _NN_)  # .replace(_Dmain_, m)
        if n == p:
            d += 1
            r += ' DUPLICATE'
        else:
            p = n
        if r.startswith(_DOT_(n, _NN_)):
            # increase indentation to align enums, constants, etc.
            t = _SPACE_ * len(n)
            r =  r.replace(t, t + S)
        else:
            r = _fmt('%s is %s', n, r)
        printf(' %s,', _DOT_(m, r), argv0=argv0)
        i += 1
    if d:
        d = _NN_(_SPACE_, d, ' DUPLICATE', 's' if d > 1 else _NN_)
    else:
        d = _NN_
    printf(')[%d]%s', i, d, argv0=argv0)
    v = localls.get(_Dversion_, _NN_).replace('.0', _DOT_)
    _all_versions(libs=libs, _file_=f, _version_=v, argv0=argv0)  # PYCHOK kwargs


def _all_versions(libs=False, _file_=_NN_, _version_=_NN_, argv0=_NN_):
    '''(INTERNAL) Print PyCocao, Python, macOS.
    '''
    printf(_all_versionstr(libs=libs, _file_=_file_, _version_=_version_), argv0=argv0)


def _all_versionstr(libs=False, _file_=_NN_, _version_=_NN_):
    '''(INTERNAL) PyCocao, Python, macOS, etc. versions as C{str}.
    '''
    from pycocoa import oslibs, _pycocoa_package, version as _version

    t = (('version', _version_ or _version),  # PYCHOK shadow
         ('.isLazy',  str(isLazy)),
         ('Python',  _Python_version, _platform.architecture()[0], machine()),
         ('macOS',    macOSver()))
    if libs:
        ls = _asorted(oslibs.Libs.keys())
        t += ('oslibs', str(ls).replace("'", _NN_)),

    m, _ = _dirbasename2(_file_ or _pycocoa_package)
    return _DOT_(m, _COMMASPACE_.join(map(_SPACE_.join, t)))


def _asorted(sortable):
    return sorted(sortable, key=str.lower)


def aspect_ratio(width, *height, **Error_kwds):
    '''Compute the smallest, integer aspect ratio.

       @param width: The width (C{float}, C{int}, L{Size}, 2-tuple
                     (width, height), str("w:h") or C{NSSize_t}).
       @param height: The height (C{float} or C{int}).

       @return: 2-Tuple (width, height) as (C{int}, C{int}) or C{None}.

       @example:

       >>> aspect_ratio(10, 15)
       (2, 3)
       >>> aspect_ratio(10.0, 15)
       (2, 3)
       >>> aspect_ratio(10, -15)
       (-2, 3)
       >>> aspect_ratio(-10, -15)
       (2, 3)
       >>> aspect_ratio(10.5, 15)
       (7, 10)
       >>> aspect_ratio(0, 15)
       ()
    '''
    if height:
        r = (width,) + height
    else:
        r =  width  # str
    try:
        if isinstance(r, _ByteStrs):
            s = bytes2str(r)
            w, h = map(int, s.split(_COLON_))
        elif islistuple(r) and len(r) == 2:
            w, h = map(flint, r)
        else:  # NSSize_t
            w, h = flint(r.width), flint(r.height)

        # video 4:3, 16:9, 21:9 [14:10, 19:10]
        # photo 1:1, 3:2, 4:3, 5:3, 5:4, 7:5, 16:9,
        #            2:3  3:4  3:5  4:5  5:7  9:16
        r = gcd(w, h)
        if r and w and h:
            r = float(r)
            return int(w / r), int(h / r)
        else:
            return None

    except (AttributeError, ValueError):
        pass  # to avoid chaining
    E = Error_kwds.get('Error', ValueError)
    raise E(_fmt_invalid(ratio=repr(r)))


def clipstr(bytestr, limit=50):
    '''Clip a string to the given length limit.

       @param bytestr: String (C{bytes} or C{str}).
       @keyword limit: Length limit (C{int}).

       @return: Clipped C{bytes} or C{str}.
    '''
    if bytestr and limit > 10:
        n = len(bytestr)
        if n > limit:
            h = limit // 2
            t = type(bytestr)
            bytestr = bytestr[:h] + t('....') + bytestr[-h:]
        #   if XXX:
        #       bytestr += t('[' + str(n) + ']')
    return bytestr


def _dirbasename2(filename, sep=_DOT_):
    '''(INTERNAL) get the dir and base name of a C{filename} without extension.
    '''
    f = _os_path.splitext(filename)[0]
    d, b = _os_path.split(f.strip())
    while d and not b:  # ended with '/'
        d, b = _os_path.split(d)
    _, d = _os_path.split(d)
    if d and b:
        m = sep.join((d, b)) if sep else _os_path.join(d, b)
        n = b
    else:
        m = n = d or b
    return m, n


def errorf(fmtxt, *args, **file_flush_nl_nt_argv0):
    '''Like I{printf}, but writing to I{file=sys.stderr}.
    '''
    return _writef(fmtxt, args, **_xkwds(file_flush_nl_nt_argv0,
                                         file=sys.stderr, flush=True))


def flint(f):
    '''Return C{int} for integer C{float}.
    '''
    try:
        if f.is_integer():
            return int(f)
    except AttributeError:
        if not isinstance(f, _Ints):
            raise
    return f


try:
    from math import gcd  # Python 3+
except ImportError:
    try:
        from fractions import gcd  # Python 2-
    except ImportError:

        def gcd(a, b):
            a, b = abs(a), abs(b)
            if a < b:
                a, b = b, a
            while b:
                a, b = b, (a % b)
            return a


def inst2strepr(inst, strepr, *attrs):
    '''Convert an instance's attributes, maintaining the order.

       @param inst: Instance (C{any}, incl. C{ctypes}).
       @param strepr: Conversion (C{repr} or C{str}).
       @param attrs: Instance attribute names (I{all positional}).

       @return: Instance representation (C{str}).
    '''
    def _a_v(a):
        v = getattr(inst, a)
        t = repr(v) if isinstance(v, _ByteStrs) else strepr(v)
        return _EQUALS_(a, t)

    return _instr(type(inst), *map(_a_v, attrs))


def isinstanceOf(inst, *classes, **raiser_name):
    '''Check a Python instance' class.

       @param inst: The instance to check (C{any}).
       @param classes: One or several classes (I{all positional}).
       @keyword raiser_name: Optional instance name (C{str}) to raise
                             C{TypeError}.

       @return: The C{type{B{inst}} if C{isinstance(B{inst}, classes}}
                else C{None}.

       @raise TypeError: If I{inst} does not match any of the I{classes}
                         but only if keyword C{raiser} is specified.

       @see: Function L{isObjCInstanceOf} for checking ObjC instances.
    '''
    # assert classes
    if isinstance(inst, classes):
        return type(inst)
    if raiser_name:
        n = _raiser_name(**raiser_name)
        if n:
            raise _TypeError(n, inst, isinstanceOf, *classes)
    return None


def islistuple(inst):
    '''Is B{C{inst}}ance a C{list} or C{tuple}?

       @param inst: The object (any C{type}).

       @return: C{True} if C{B{inst}} is a C{list} or
                C{tuple}, C{False} otherwise.
    '''
    return isinstance(inst, (tuple, list))


def logf(fmtxt, *args, **file_flush_nl_nt_argv0):
    '''Like I{printf}, but writing to I{file=NSMain.stdlog}.
    '''
    return _writef(fmtxt, args, **_xkwds(file_flush_nl_nt_argv0,
                                         file=_Globals.stdlog, flush=True))


def machine():
    '''Return the C{platform.machine} string, distinguishing Intel from
       I{emulating} Intel on Apple Silicon (on macOS).

       @return: Machine C{'arm64'} for Apple Silicon, C{"arm64_x86_64"} for
                Intel I{emulated}, C{'x86_64'} for Intel, etc. (C{str} with
                any C{comma}s replaced by C{underscore}).
    '''
    m = _platform.machine().replace(_COMMA_, _UNDER_)  # arm64 Apple Si, x86_64, other?
    if m == 'x86_64' and macOSver():  # only on Intel or Rosetta2
        # <https://Developer.Apple.com/forums/thread/659846>
        if _sysctl_uint('sysctl.proc_translated') == 1:  # and \
#          _sysctl_uint('hw.optional.arm64') == 1:  # PYCHOK indent
            m = _UNDER_('arm64', m)  # Apple Silicon emulating Intel x86
    return m


def macOSver():
    '''Return the macOS release as C{str}.

       @note: C{macOS 11 Big Sur} is C{'10.16'} before Python 3.9.6 and
              on Apple Si Intel-emulation, see function L{machine}.
    '''
    return _platform.mac_ver()[0]


def macOSver2(n=2):
    '''Return the macOS release as 1-, 2- or 3-tuple of C{int}s.

       @note: C{macOS 11 Big Sur} is C{(10, 16)} before Python 3.9.6 and
              on Apple Si Intel-emulation, see function L{machine}.
    '''
    v = macOSver() or '0'
    t = tuple(map(int, v.split(_DOT_)[:n])) + (0, 0, 0)
    return t[:n]


def name2objc(name_):
    '''Convert a (selector) name to C{bytes} and ObjC naming rules.

       @param name_: Name to convert (C{str} or C{bytes}).

       @return: Converted name (C{bytes}).

       @note: A I{name_} starting with an underscore is returned as-is.
    '''
    b = str2bytes(name_)
    if not b.startswith(b'_'):
        b = b.replace(b'_', _bCOL)
    return b


def name2py(name_):
    '''Convert a (selector) name C{str} and Python naming conventions.

       @param name_: Name to convert (C{str} or C{bytes}).

       @return: Converted name (C{str}).

       @note: A I{name_} starting with an underscore is returned as-is.
    '''
    s = bytes2str(name_)
    if not s.startswith(_UNDER_):
        s = s.replace(_COLON_, _UNDER_)
    return s


def name2pymethod(name_):
    '''Convert a (selector) name to a valid Python callback method.

       @param name_: Name to convert (C{str} or C{bytes}).

       @return: Converted name (C{str}).

       @raise ValueError: Invalid, non-alphanumeric I{name_}.
    '''
    m = name2py(name_)
    if m and m.replace(_UNDER_, _NN_).isalnum() and not m[:1].isdigit():
        return m
    raise ValueError(_fmt_invalid(name_=repr(name_)))


def printf(fmtxt, *args, **file_flush_nl_nt_argv0):
    '''Formatted print I{fmt % args} with optional keywords.

       @param fmtxt: Print-like format or plain string (C{str}).
       @param args: Optional arguments to format (I{all positional}).
       @keyword file: Alternate file to write to (C{file}-type),
                      default C{sys.stdout}.
       @keyword flush: Flush B{C{file}} after writing (C{bool}),
                       default C{False}.
       @keyword nl: Number of leading blank lines (C{int}).
       @keyword nt: Number of trailing blank lines (C{int}, default 1).
       @keyword argv0: Optional prefix (C{str}).

       @return: Number of bytes written (C{int}).
    '''
    return _writef(fmtxt, args, **file_flush_nl_nt_argv0)


def properties(inst):
    '''All property names and values.

       @param inst: An instance (C{any}).

       @return: The properties (C{dict}).
    '''
    pd, t = {}, type(inst)
    for a in dir(inst):  # dir(t), t.__mro__?
        if a[:1] != _UNDER_ and isinstance(getattr(t, a), property):
            try:
                pd[a] = getattr(inst, a)
            except Exception as x:
                pd[a] = repr(x)
    return pd


def _raiser_name(raiser=None, name=None):  # in .runtime
    return raiser or name


def _sysctl_uint(name):
    '''(INTERNAL) Get an unsigned int sysctl item by name (on macOS).
    '''
    from pycocoa.oslibs import byref, c_char_p, c_size_t, c_uint, Libs, sizeof
    C = Libs.C
    if C:  # <https://StackOverflow.com/questions/759892/python-ctypes-and-sysctl>
        n = name if str is bytes else bytes(name, 'utf_8')  # PYCHOK isPython2 = str is bytes
        u = c_uint(0)
        z = c_size_t(sizeof(u))
        r = C.sysctlbyname(c_char_p(n), byref(u), byref(z), None, c_size_t(0))
    else:  # could find or load 'libc'
        r = -2
    return int(r if r else u.value)  # -1 ENOENT error, -2 no libc


def terminating(app, timeout=None):
    '''Set up a separate thread to terminate an NSApplication I{app}
       by calling its C{.terminate_} method at the given I{timeout}
       in seconds.

       @return: Timeout in seconds (C{float}) or C{None}.

       @note: Similarly, the NSWindow could be closed, provided the
              NSWindow or NSApplication C{Delegate} instance includes
              the C{.windowWillClose_} method which in turn invokes
              the NSApplication's C{.terminate_} method.
    '''
    try:
        s = float(timeout)
        t = app.terminate_
    except AttributeError:
        raise ValueError(_fmt_invalid(app=repr(app)))
    except (TypeError, ValueError):
        return None

    def _t():
        from time import sleep
        sleep(s + 0.5)
        # <https://Developer.Apple.com/documentation/appkit/nsapplication/1428417-terminate>
        t(app)

    from threading import Thread
    Thread(target=_t).start()

    return s


def _text_title2(text_or_file, title=_NN_):
    '''(INTERNAL) Return 2-tuple (title, text).
    '''
    if isinstance(text_or_file, _ByteStrs):
        text, t = text_or_file, title
    else:
        try:
            text = text_or_file.read()
        except (AttributeError, IOError, OSError) as x:
            text = str(x)
        try:
            n = text_or_file.name
        except AttributeError:
            n = None
        t = _fmt('File %r', n)
    return text, t


def type2strepr(inst, strepr=str, **kwds):
    '''Represent a Python Type instance as L{str} or L{repr}.

       @param inst: Instance (C{any}).
       @keyword strepr: Representation function (C{repr} or C{str}).
       @keyword kwds: Optional, additional C{name=value} arguments.

       @return: Instance representation (C{str}).
    '''
    try:
        t =  inst.NS.objc_classname  # PYCHOK expected
    except AttributeError:
        t = _NN_
    try:
        t = _fmt('%s[%s]', t, len(inst))
    except TypeError:
        pass
    try:
        d = _xkwds(kwds, name=repr(inst.name))
    except AttributeError:
        d =  kwds
    if d:
        d = _kwdstr(d)
        t = _COMMASPACE_(strepr(t), d) if t else d
    else:
        t =  strepr(t)
    return _instr(type(inst), t)


def _varstr(constants, strepr=None):
    '''(INTERNAL) Return all C{@var Class.<name>: <doc>} lines as C{str}.
    '''
    def _doc1(c, n, f):
        # get class c's 1st __doc__ line or value from f(c)
        if callable(f):
            t = f(c)
        else:
            d = getattr(c, _Ddoc_) or _NN_
            t = d.split(_NL_)[0].strip()
            t = t.rstrip('.,;:') + _DOT_
        return _SPACE_('@var', _COLONSPACE_(n, t))

    C = constants.__class__
    N = C.__name__.lstrip(_UNDER_)
    v = [_NN_, _doc1(C, N, None)]
    for n in _asorted(constants.keys()):
        v.append(_doc1(getattr(C, n), _DOT_(N, n), strepr))
    return _NL_.join(v)


def _xkwds(kwds, **dflts):
    # return dict C{kwds.update(dflts)}
    d = dflts
    if kwds:
        d = d.copy()
        d.update(kwds)
    return d


def z1000str(size, sep=_UNDER_):
    '''Convert a size to string with 1_000's seperator.

       @param size: Value to convert (C{float} or C{int}).
       @keyword sep: 1_000's separator (C{str}).

       @return: "<1or2digits><sep><3digits>..." or "-" if
                I{size} is negative (C{str}).
    '''
    def _z(z, S, s):
        t = '{0:%s}' % (S,)
        t = t.format(z)
        if S != s:
            t = t.replace(S, s)
        return t

    z = int(size)
    if z < 0:
        return '-'
    try:  # '_' only in Python 3.6+
        t = _z(z, _UNDER_, sep)
    except ValueError:
        try:  # ',' only in Python 3.1+
            t = _z(z, _COMMA_, sep)
        except ValueError:
            t = str(z)
            n = len(t)
            while n > 3:
                n -= 3
                t = t[:n] + sep + t[n:]
    return t


def zfstr(flt, prec=3):
    '''Format a C{float} and strip trailing zero decimals.

       @param flt: Value (C{float}).
       @keyword prec: Number of decimals (C{int}).

       @return: Value (C{str}).
    '''
    fstr = _fmt('%.*f', prec, float(flt))
    if prec > 0:
        fstr = fstr.rstrip('0').rstrip(_DOT_)
    return fstr


def zSIstr(size, B='B', K=1024):
    '''Convert a size to string with SI-units suffix.

       @param size: Value to convert (C{float} or C{int}).
       @keyword B: The unit (C{str}).
       @keyword K: 1024 or 1000 (C{int}).

       @return: "<Size> <SI>[i]<B>" (C{str}).
    '''
    z, si, k = float(size), _NN_, float(K)
    if z > k:
        # Science Mag, vol 363, issue 6428, p 681, Feb 15, 2019
        # "Metric prefixes sought for extremely large numbers",
        # Ronna 10^27 and Quecca 10^30
        for si in iter('KMGTPEZYRQ'):
            z /= k
            if z < k:
                if k == 1024.0:
                    si += 'i'
                si = _fmt('%.1f %s%s', z, si, B)
                break
        else:
            si = _fmt('%.3e %s', float(size), B)
    else:
        si = _fmt('%d %s', int(size), B)
    return si


if __name__ == _Dmain_:

    _all_listing(__all__, locals())

# % python3 -m pycocoa.utils
#
# pycocoa.utils.__all__ = tuple(
#  pycocoa.utils.aspect_ratio is <function .aspect_ratio at 0x102574c20>,
#  pycocoa.utils.clipstr is <function .clipstr at 0x102574cc0>,
#  pycocoa.utils.errorf is <function .errorf at 0x102574e00>,
#  pycocoa.utils.flint is <function .flint at 0x102574ea0>,
#  pycocoa.utils.gcd is <built-in function gcd>,
#  pycocoa.utils.inst2strepr is <function .inst2strepr at 0x102574f40>,
#  pycocoa.utils.isinstanceOf is <function .isinstanceOf at 0x102575120>,
#  pycocoa.utils.islistuple is <function .islistuple at 0x1025751c0>,
#  pycocoa.utils.logf is <function .logf at 0x102575260>,
#  pycocoa.utils.machine is <function .machine at 0x102575300>,
#  pycocoa.utils.macOSver is <function .macOSver at 0x1025753a0>,
#  pycocoa.utils.macOSver2 is <function .macOSver2 at 0x102575440>,
#  pycocoa.utils.name2objc is <function .name2objc at 0x1025754e0>,
#  pycocoa.utils.name2py is <function .name2py at 0x102575580>,
#  pycocoa.utils.name2pymethod is <function .name2pymethod at 0x102575620>,
#  pycocoa.utils.printf is <function .printf at 0x1025756c0>,
#  pycocoa.utils.properties is <function .properties at 0x102575760>,
#  pycocoa.utils.terminating is <function .terminating at 0x102575940>,
#  pycocoa.utils.type2strepr is <function .type2strepr at 0x102575a80>,
#  pycocoa.utils.z1000str is <function .z1000str at 0x102575c60>,
#  pycocoa.utils.zfstr is <function .zfstr at 0x102575d00>,
#  pycocoa.utils.zSIstr is <function .zSIstr at 0x102575da0>,
# )[22]
# pycocoa.utils.version 25.3.24, .isLazy 1, Python 3.13.2 64bit arm64, macOS 15.3.2

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2017-2025 -- mrJean1 at Gmail -- All Rights Reserved.
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

# Originally <https://GitHub.com/phillip-nguyen/cocoa-python>

# objective-ctypes
#
# Copyright (C) 2011 -- Phillip Nguyen -- All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of objective-ctypes nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
