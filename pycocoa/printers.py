
# -*- coding: utf-8 -*-

# Originally <https://Gist.GitHub.com/pudquick/68707b07c8c2772337cfd6397e399d3f>

'''Types L{Printer}, L{Paper}, L{PaperCustom} and L{PaperMargins},
wrapping ObjC C{NSPrinter}, C{PMPrinter}, C{PMPaper} respectively
C{PMPaperMargins} plus several C{get_...} print functions.

@var libPC: The macOS C{PrintCore} framework library (C{ctypes.CDLL}) or C{None}.
'''
from pycocoa.bases   import _Type0
from pycocoa.lazily  import _ALL_LAZY, _DOT_, _NN_
from pycocoa.nstypes import nsDictionary2dict, NSImageView, NSMain, \
                            NSPrinter, NSPrintInfo, NSPrintOperation, \
                            ns2py, NSStr, NSTableView, NSTextView
from pycocoa.octypes import Array_t, BOOL_t, c_struct_t, Dictionary_t, \
                            Id_t, ObjC_t, String_t, URL_t
from pycocoa.oslibs  import cfNumber2bool, cfString, cfString2str, \
                            cfURL2str, _csignature, _free_memory, \
                            get_lib_framework, libCF, YES
from pycocoa.runtime import isObjCInstanceOf, send_message, _Xargs
from pycocoa.utils   import Adict, isinstanceOf, property_RO, \
                           _Strs, _Types, zfstr

from ctypes  import ArgumentError, byref, cast, c_char_p, c_double, \
                    c_int, c_void_p, POINTER, sizeof
import os

__all__ = _ALL_LAZY.printers
__version__ = '21.11.04'

libPC = None  # loaded on-demand
kPMServerLocal = None
kPMPPDDescriptionType = cfString('PMPPDDescriptionType')  # PYCHOK false
noErr = 0  # aka noErr


# <https://Developer.Apple.com/documentation/applicationservices/core_printing>
# <https://Developer.Apple.com/documentation/kernel/osstatus>
class OSStatus_t(c_int):  # 32-bit or NSInteger_t == Int_t
    '''Return code type.
    '''
    pass


class PM_t(ObjC_t):
    '''Any PM type.
    '''
    pass


class PMPaper_t(ObjC_t):
    '''Opaque paper type.
    '''
    pass


class PMPrinter_t(ObjC_t):
    '''Opaque printer type.
    '''
    pass


class PMRect_t(c_struct_t):
    '''ObjC C{struct} with fields C{bottom}, C{left}, C{right} and C{top} (C{c_double}-s).
    '''
    _fields_ = ('bottom', c_double), ('left', c_double), \
               ('right',  c_double), ('top',  c_double)


class PMResolution_t(c_struct_t):
    '''ObjC C{struct} with fields C{hRes} and C{vRes} (C{c_double}-s).
    '''
    _fields_ = ('hRes', c_double), ('vRes', c_double)


class PMServer_t(ObjC_t):
    '''Opaque local or remote print server type.
    '''
    pass


class PrintError(ValueError):  # SystemError
    '''Error from ObjC C{NSPrinter} or C{PM...}.
    '''
    pass


def _nsPrinter(name, pm):
    '''(INTERNAL) New C{NSPrinter} instance.
    '''
    if isinstanceOf(pm, PMPrinter_t, name='pm'):  # NSStr(name)
        ns = send_message('NSPrinter', 'alloc', restype=Id_t)
        # _initWithName:printer:(Id_t, Id_t, SEL_t, Id_t, LP_Struct_t)
        # requires special selector handling due to leading underscore
        ns = send_message(ns, '_initWithName:printer:', NSStr(name), pm,
                          restype=Id_t, argtypes=[Id_t, PMPrinter_t])
    else:
        ns = None
    return ns

# % python -m test.list_methods NSPrinter
# description @16@0:8 (Id_t, Id_t, SEL_t)  # JSON?
# deviceDescription @16@0:8 (Id_t, Id_t, SEL_t)
# domain @16@0:8 (Id_t, Id_t, SEL_t)  # DEPRECATED
# host @16@0:8 (Id_t, Id_t, SEL_t)  # DEPRECATED
# imageRectForPaper: {CGRect={CGPoint=dd}{CGSize=dd}}24@0:8@16 (NSRect_t, Id_t, SEL_t, Id_t)
# initWithCoder: @24@0:8@16 (Id_t, Id_t, SEL_t, Id_t)
# isColor c16@0:8 (c_byte, Id_t, SEL_t)  # DEPRECATED
# isFontAvailable: c24@0:8@16 (c_byte, Id_t, SEL_t, Id_t)
# isOutputStackInReverseOrder c16@0:8 (c_byte, Id_t, SEL_t)
# name @16@0:8 (Id_t, Id_t, SEL_t)
# note @16@0:8 (Id_t, Id_t, SEL_t)  # DEPRECATED
# pageSizeForPaper: {CGSize=dd}24@0:8@16 (NSSize_t, Id_t, SEL_t, Id_t)
# type @16@0:8 (Id_t, Id_t, SEL_t)  # == MakeAndModelName
# ...
# _allocatePPDStuffAndParse v16@0:8 (None, Id_t, SEL_t)
# _allocString: *24@0:8r*16 (c_char_p, Id_t, SEL_t, c_char_p)
# _deallocatePPDStuff v16@0:8 (None, Id_t, SEL_t)
# _initWithName:printer: @32@0:8@16^{OpaquePMPrinter=}24 (Id_t, Id_t, SEL_t, Id_t, LP_Struct_t)
# _printer ^{OpaquePMPrinter=}16@0:8 (LP_Struct_t, Id_t, SEL_t)
# _setUIConstraints: @24@0:8*16 (Id_t, Id_t, SEL_t, c_char_p)
# ...


class _PM_Type0(_Type0):
    '''(INTERNAL) Base type for ObjC C{PM...} objects.
    '''
    _PM = None

    def __init__(self, pm):
        self._PM = pm
        if not libPC:
            get_libPC()

    def __str__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)

    def _libPCcall(self, func, *args):  # like runtime._libobjcall
        try:
            e = func(self.PM, *args)
        except (ArgumentError, KeyError, TypeError) as x:
            raise _Xargs(x, func.__name__, func.argtypes, func.restype)
        e = e.value
        if e != noErr:
            raise _StatusError(e, func.__name__)
        return e

    def _2bool(self, libPC_func):
        b = BOOL_t()
        self._libPCcall(libPC_func, byref(b))
        return True if b.value else False

    def _2dict(self, libPC_func):
        D = Dictionary_t()
        self._libPCcall(libPC_func, byref(D))
        if D:  # usually Null
            d = nsDictionary2dict(D)
            _free_memory(D, len(d) * 2 * sizeof(ObjC_t))
        else:
            d = {}
        return d

    def _2float(self, libPC_func):
        d = c_double()
        self._libPCcall(libPC_func, byref(d))
        return d.value

    def _2int(self, libPC_func):
        i = c_int()  # c_int32?
        self._libPCcall(libPC_func, byref(i))
        return i.value

    def _2rect(self, libPC_func):
        r = PMRect_t()
        self._libPCcall(libPC_func, byref(r))
        return r

    def _2str(self, libPC_func, *args):
        s = c_char_p()
        if args:
            args += (byref(s),)
            self._libPCcall(libPC_func, *args)
        else:
            self._libPCcall(libPC_func, byref(s))
        return cfString2str(s)

    def _2tuple(self, libPC_func, ctype):
        a = Array_t()
        self._libPCcall(libPC_func, byref(a))
        # like nstypes.nsArray2listuple
        n = libCF.CFArrayGetCount(a)
        f = libCF.CFArrayGetValueAtIndex
        t = tuple(cast(f(a, i), ctype) for i in range(n))
        _free_memory(a, n * sizeof(ObjC_t))
        return t

    def _2ustr(self, libPC_func, *args):
        u = URL_t()
        if args:
            args += (byref(u),)
            self._libPCcall(libPC_func, *args)
        else:
            self._libPCcall(libPC_func, byref(u))
        return cfURL2str(u)

    @property_RO
    def PM(self):
        '''Get the ObjC C{PMobject}.
        '''
        return self._PM

    def release(self):
        '''Release this ObjC C{PMobject}.
        '''
        self._libPCcall(libPC.PMRelease)

    def retain(self):
        '''Release this ObjC C{PMobject}.
        '''
        self._libPCcall(libPC.PMRetain)


class Paper(_PM_Type0):
    '''Python C{Paper} Type, wrapping an opaque ObjC C{PMPaper}.

       @note: Paper sizes are measured in I{points}.
    '''
    # <https://Gist.GitHub.com/lv10/8547663#file-gistfile1-m>
    # <https://Developer.Apple.com/documentation/applicationservices/core_printing>
    _name = None
    _PM_t = PMPaper_t
    # <https://WikiPedia.org/wiki/Point_(typography)>
    _ppi  = 72  # points / inch
    _ppmm = 72 / 25.4  # points / millimeter

    def __init__(self, name_pm):
        '''New L{Paper} from a paper name (C{str}) or C{PMPaper}.

           @raise PrintError: No paper with name I{name_pm}.

           @raise TypeError: Invalid I{name_pm}.
        '''
        if isinstance(name_pm, _Strs):
            for p in get_papers():
                if p.name == name_pm:
                    pm = p.PM
                    break
            else:
                raise PrintError('no such %s: %r' % (Paper.__name__, name_pm))
        elif isinstanceOf(name_pm, PMPaper_t, name='name_pm'):
            pm = name_pm
        _PM_Type0.__init__(self, pm)

    @property_RO
    def height(self):
        '''Get the paper height in I{points} (C{float}).
        '''
        return self._2float(libPC.PMPaperGetHeight)

    @property_RO
    def ID(self):
        '''Get the paper IDentifier (C{str}).
        '''
        return self._2str(libPC.PMPaperGetID)

    @property_RO
    def isCustom(self):
        '''True if this is a custom paper (C{bool}).
        '''
        return cfNumber2bool(libPC.PMPaperIsCustom(self.PM), None)

    def localname(self, printer=None):
        '''Get the paper's localized name for a printer (C{str}).

           @raise TypeError: Invalid I{printer}.
        '''
        if not printer:
            pm = get_printer().PM
        elif isinstanceOf(printer, Printer, name='printer'):
            pm = printer.PM
        return self._2str(libPC.PMPaperCreateLocalizedName, pm)

    @property_RO
    def margins(self):
        '''Get the paper margins (L{PaperMargins}).
        '''
        return PaperMargins(self._2rect(libPC.PMPaperGetMargins))

    @property_RO
    def name(self):
        '''Get the paper name (C{str}).
        '''
        if self._name is None:
            self._name = self._2str(libPC.PMPaperGetName)
        return self._name

    @property_RO
    def PPD(self):
        '''Get the paper's PPD name (C{URL}).
        '''
        return self._2str(libPC.PMPaperGetPPDPaperName)

    @property_RO
    def printer(self):
        '''Get the printer corresponding to this paper (C{Printer}) or C{None}.
        '''
        ID = self._2str(libPC.PMPaperGetPrinterID)
        for p in get_printers(ID):
            if p.ID == ID:
                return p
        return None

    @property_RO
    def size2inch(self):
        '''Get 2-tuple (width, height) in I{inch} (C{float}s).
        '''
        return self.width / self._ppi, self.height / self._ppi

    @property_RO
    def size2mm(self):
        '''Get 2-tuple (width, height) in I{millimeter} (C{float}s).
        '''
        return self.width / self._ppmm, self.height / self._ppmm

    @property_RO
    def width(self):
        '''Get the paper width in I{points} (C{float}).
        '''
        return self._2float(libPC.PMPaperGetWidth)


class PaperCustom(Paper):
    '''Create a custom L{Paper}.
    '''
    def __init__(self, name='Custom', ID=_NN_, width=612, height=792, margins=None, printer=None):
        '''New L{PaperCustom} from paper attributes.

           @raise TypeError: Invalid I{margins} or I{printer}.
        '''
        h = float(height)
        w = float(width)

        z = 'x'.join(map(zfstr, (w, h)))
        if name:
            n = str(name)
            i = str(ID) or '%s %s' % (name, z)
        else:
            n = z
            i = str(ID) or z

        if margins is None:
            m = PaperMargins()
        elif isinstanceOf(margins, PaperMargins, name='margins'):
            m = PaperMargins(margins)

        if printer is None:
            p = get_printer()
        elif isinstanceOf(printer, Printer, name='printer'):
            p = printer

        pm = PMPaper_t()
        self._libPCcall(libPC.PMPaperCreateCustom, p, NSStr(n),
                              NSStr(i), w, h, m, byref(pm))
        Paper.__init__(self, pm)


class PaperMargins(PMRect_t):
    '''Python C{PaperMargins} Type, wrapping an ObjC C{PMPaperMargins}.
    '''
    _PM = None

    def __init__(self, margins_pm=None, bottom=0, left=0, right=0, top=0):
        '''New L{PaperMargins} from margin attributes.

           @raise TypeError: Invalid I{margins_pm}.
        '''
        if not margins_pm:
            self.bottom = float(bottom)
            self.left   = float(left)
            self.right  = float(right)
            self.top    = float(top)
        elif isinstanceOf(margins_pm, PaperMargins, PMRect_t, name='margins_pm'):
            self.bottom = float(margins_pm.bottom)
            self.left   = float(margins_pm.left)
            self.right  = float(margins_pm.right)
            self.top    = float(margins_pm.top)

        self._PM = self

    @property_RO
    def PM(self):
        return self._PM


class Printer(_PM_Type0):
    '''Python C{Printer} Type, wrapping ObjC C{NSPrinter} and C{PMPrinter}.
    '''
    _deviceDescription = None
    _name              = None
    _PM_t              = PMPrinter_t

    def __init__(self, name_ns_pm=None):
        '''New L{Printer} from a printer name (C{str}), C{NSPrinter} or C{PMPrinter}.

           @raise TypeError: Invalid I{name_ns_pm}.

           @raise PrintError: No printer with name I{name_ns_pm}.
        '''
        if not name_ns_pm:  # generic printer
            _PM_Type0.__init__(self, PMPrinter_t())
            self._libPCcall(libPC.PMCreateGenericPrinter)
            pm = self.PM
            ns = _nsPrinter('Generic', pm)

        elif isinstance(name_ns_pm, _Strs):
            for p in get_printers():
                if p.name == name_ns_pm:
                    pm = p.PM
                    ns = _nsPrinter(p.name, pm)
                    break
            else:
                raise PrintError('no such %s: %r' % (Printer.__name__, name_ns_pm))

        elif isinstanceOf(name_ns_pm, PMPrinter_t):
            pm = name_ns_pm
            ns = _nsPrinter(cfString2str(libPC.PMPrinterGetName(pm)), pm)

        elif isObjCInstanceOf(name_ns_pm, NSPrinter, name='name_ns_pm'):
            ns = name_ns_pm
            # special method name due to leading underscore
            pm = send_message(ns, '_printer', restype=PMPrinter_t)

        _PM_Type0.__init__(self, pm)
        self._NS = ns  # _RO

    @property_RO
    def description(self):
        '''Get printer description (C{json}).
        '''
        # XXX use send_message, avoiding printer.NS.description()
        d = send_message(self.NS, 'description', restype=Id_t)
        return ns2py(d)

    @property_RO
    def deviceDescription(self):
        '''Get the C{NSDevice} description (L{Adict}).
        '''
        if self._deviceDescription is None:
            # d = nsDescription2dict(self.NS.deviceDescription())
            # _ = d.NSDeviceIsPrinter  # preload
            self._deviceDescription = ns2py(self.NS.deviceDescription())
        return self._deviceDescription

    @property_RO
    def deviceURI(self):
        '''Get the printer device (C{URI}) or C{""}.
        '''
        try:
            return self._2ustr(libPC.PMPrinterCopyDeviceURI)
        except _StatusError:
            return _NN_

    @property_RO
    def ID(self):
        '''Get the printer IDentifier (C{str}) or C{""}.
        '''
        return cfString2str(libPC.PMPrinterGetID(self.PM)).strip()

    @property_RO
    def isColor(self):
        '''Is printer color (C{bool}).
        '''
        return True if (  # self.NS.isColor() or  # DEPRECATED
                       'color' in self.name.lower() or
                       'color' in self.makemodel.lower()) else False

    @property_RO
    def isDefault(self):
        '''Is this the default printer (C{bool}).
        '''
        return True if libPC.PMPrinterIsDefault(self.PM) else False

    @property_RO
    def isRemote(self):
        '''Is this a remote printer (C{bool}).
        '''
        return self._2bool(libPC.PMPrinterIsRemote)

#   @property_RO
#   def localname(self):
#       '''Get the printer's localized name (C{str}).
#       '''
#       return cfString2str(libPC.PMPrinterGetName(self.PM))

    @property_RO
    def location(self):
        '''Get the printer location (C{str}) or C{""}.
        '''
        s = libPC.PMPrinterGetLocation(self.PM)
        return cfString2str(s) if s else _NN_

    @property_RO
    def makemodel(self):
        '''Get the printer make and model (C{str}) or C{""}.
        '''
        try:
            return self._2str(libPC.PMPrinterGetMakeAndModelName)
        except _StatusError:
            return _NN_

    @property_RO
    def name(self):
        '''Get the printer name (C{str}) or C{""}.
        '''
        if self._name is None:
            self._name = cfString2str(libPC.PMPrinterGetName(self.PM)).strip()
        return self._name

    @property_RO
    def NS(self):
        '''Get the ObjC instance (C{NSPrinter}).
        '''
        return self._NS

    @property_RO
    def papers(self):
        '''Yield each paper available (L{Paper}).
        '''
        return get_papers(self)

    @property_RO
    def PPD(self):
        '''Get the printer PPD description (C{URL}).
        '''
        return self._2ustr(libPC.PMPrinterCopyDescriptionURL,
                                        kPMPPDDescriptionType)

    @property_RO
    def psCapable(self):
        '''Is the printer PostScript capable (C{bool}).
        '''
        return True if libPC.PMPrinterIsPostScriptCapable(self.PM) else False

    @property_RO
    def psLevel(self):
        '''Get the printer's PostScript language level (C{int}).
        '''
        return int(self.NS.languageLevel())

#     def printImage(self, image, toPDF=_NN_, wait=True):
#         '''Print an image file.
#
#            @param image: The image file name path (C{str}).
#            @keyword toPDF: Save as PDF file name (C{str}).
#            @keyword wait: Wait for print completion (C{bool}).
#
#            @return: C{True} if printing succeeded, C{False} otherwise.
#
#            @raise PrintError: If I{toPDF} file exists.
#         '''
#         # <https://StackOverflow.com/questions/6452144/
#         #        how-to-make-a-print-dialog-with-preview-for-printing-an-image-file>
#         if not os.access(image, os.R_OK):
#             raise PrintError('no such %s: %r' % ('image file', image))
#         im = NSImage.alloc().initWithContentsOfFile_(NSStr(image))
#         vw = NSImageView.alloc().initWithFrame_(NSRect4_t(width=nim.size.width,
#                                                          height=nim.size.height))
#         vw.setImage_(im)
#         return self.printView(vw, toPDF=toPDF, wait=wait)

    def printView(self, PMview, toPDF=_NN_, wait=True):
        '''Print an ObjC C{NSView} or C{PMview}.

           @param PMview: The ObjC view to print (C{NSView} or C{PMview}).
           @keyword toPDF: Save as PDF file name (C{str}).
           @keyword wait: Wait for print completion (C{bool}).

           @return: C{True} if printing succeeded, C{False} if
                    printing failed or C{None} if ignored.

           @raise PrintError: If I{toPDF} file exists.

           @raise TypeError: Invalid I{PMview}.
        '''
        if PMview and isObjCInstanceOf(PMview, NSImageView,
                                               NSTableView,
                                               NSTextView, name='PMview'):
            pi = NSMain.PrintInfo
            if not self.isDefault:
                pi = NSPrintInfo.alloc().initWithDictionary_(pi.dictionary())
                pi.setPrinter_(self.NS)  # NSPrinter

            if toPDF:
                if os.access(toPDF, os.F_OK):
                    raise PrintError('%s exists: %r' % ('PDF file', toPDF))
                # <https://Developer.Apple.com/documentation/appkit/
                #        nsprintoperation/1534130-pdfoperationwithview>
                po = NSPrintOperation.PDFOperationWithView_insideRect_toPath_printInfo_(
                                      PMview, PMview.frame(), NSStr(toPDF), pi)
            else:
                # <https://StackOverflow.com/questions/6452144/
                #        how-to-make-a-print-dialog-with-preview-for-printing-an-image-file>
                po = NSPrintOperation.printOperationWithView_printInfo_(PMview, pi)

            if not wait:
                po.setCanSpawnSeparateThread_(YES)
            return True if po.runOperation() else False
        else:
            return None

    @property_RO
    def resolution(self):
        '''Get the highest (horizontal, vertical) resolution supported by this printer (C{float}s, dots-per-inch).
        '''
        H = V = 0
        for h, v in get_resolutions(self):
            H, V = max(h, H), max(v, V)
        return H, V

    def setDefault(self):
        '''Make this printer the default printer (C{bool}).

           @return: C{True} if set, C{False} otherwise
        '''
        return self._libPCcall(libPC.PMPrinterSetDefault) == noErr


def get_libPC():
    '''Get the C{PrintCore} framework library.

       @return: The C{libPC} framework library (C{ctypes.CDLL}).
    '''
    global libPC
    if not libPC:
        libPC = get_lib_framework('PrintCore')

        _csignature(libPC.PMCreateGenericPrinter, OSStatus_t, POINTER(PMPrinter_t))

        _csignature(libPC.PMPaperCreateCustom, OSStatus_t, PMPrinter_t, String_t, String_t,
                                               c_double, c_double, PMRect_t, POINTER(PMPaper_t))
        _csignature(libPC.PMPaperCreateLocalizedName, OSStatus_t, PMPaper_t, PMPrinter_t, POINTER(c_char_p))
        _csignature(libPC.PMPaperGetHeight, OSStatus_t, PMPaper_t, POINTER(c_double))
        _csignature(libPC.PMPaperGetID, OSStatus_t, PMPaper_t, POINTER(c_char_p))
        _csignature(libPC.PMPaperGetMargins, OSStatus_t, PMPaper_t, POINTER(PMRect_t))
        _csignature(libPC.PMPaperGetName, OSStatus_t, PMPaper_t, POINTER(c_char_p))
        _csignature(libPC.PMPaperGetPPDPaperName, OSStatus_t, PMPaper_t, POINTER(c_char_p))
        _csignature(libPC.PMPaperGetPrinterID, OSStatus_t, PMPaper_t, POINTER(c_char_p))
        _csignature(libPC.PMPaperGetWidth, OSStatus_t, PMPaper_t, POINTER(c_double))
        _csignature(libPC.PMPaperIsCustom, BOOL_t, PMPaper_t)

        _csignature(libPC.PMPrinterCopyDescriptionURL, OSStatus_t, PMPrinter_t, String_t, POINTER(URL_t))
        _csignature(libPC.PMPrinterCopyDeviceURI, OSStatus_t, PMPrinter_t, POINTER(URL_t))
#       _csignature(libPC.PMPrinterCreateFromPrinterID, PMPrinter_t, c_char_p)
        _csignature(libPC.PMPrinterGetID, String_t, PMPrinter_t)
        _csignature(libPC.PMPrinterGetLocation, String_t, PMPrinter_t)
        _csignature(libPC.PMPrinterGetMakeAndModelName, OSStatus_t, PMPrinter_t, POINTER(c_char_p))
        _csignature(libPC.PMPrinterGetName, String_t, PMPrinter_t)
        _csignature(libPC.PMPrinterGetPaperList, OSStatus_t, PMPrinter_t, POINTER(c_void_p))
        _csignature(libPC.PMPrinterGetPrinterResolutionCount, OSStatus_t, PMPrinter_t, POINTER(c_int))
        _csignature(libPC.PMPrinterGetIndexedPrinterResolution, OSStatus_t, PMPrinter_t,
                                                                c_int, POINTER(PMResolution_t))
        _csignature(libPC.PMPrinterIsDefault, BOOL_t, PMPrinter_t)
        _csignature(libPC.PMPrinterIsPostScriptCapable, BOOL_t, PMPrinter_t)
        _csignature(libPC.PMPrinterIsRemote, OSStatus_t, PMPrinter_t, POINTER(BOOL_t))
        _csignature(libPC.PMPrinterSetDefault, OSStatus_t, PMPrinter_t)

        _csignature(libPC.PMRelease, OSStatus_t, PM_t)
        _csignature(libPC.PMRetain, OSStatus_t, PM_t)

        _csignature(libPC.PMServerCreatePrinterList, OSStatus_t, PMServer_t, POINTER(Array_t))
        _csignature(libPC.PMServerLaunchPrinterBrowser, OSStatus_t, PMServer_t, POINTER(Dictionary_t))

    return libPC


def _printers(printers):
    '''(INTERNAL) Printer generator.
    '''
    if not printers:
        printers = (get_printer(),)
    elif not libPC:
        get_libPC()
    for p in printers:
        if isinstanceOf(p, Printer, name='printers'):
            yield p


def get_papers(*printers):
    '''Yield the papers available at the given printer(s).

       @param printers: No, one or more printers (L{Printer}s).

       @return: Each paper (L{Paper}).
    '''
    for r in _printers(printers):
        # <https://Gist.GitHub.com/lv10/8547663#file-gistfile1-m>
        for p in r._2tuple(libPC.PMPrinterGetPaperList, PMPaper_t):
            yield Paper(p)


def get_printer(*prefixes):
    '''Find a printer by name or by ID or get the default printer.

       @param prefixes: No, one or more printer names or IDs to match (C{str}s).

       @return: The printer (L{Printer}) or C{None} if none found.
    '''
    if prefixes:
        for p in get_printers():
            if p.name.startswith(prefixes or p.name) or \
               p.ID.startswith(prefixes or p.ID):
                break
        else:
            p = None
    else:  # get the current printer
        p = Printer(NSMain.PrintInfo.printer())
    return p


def get_printer_browser(server=kPMServerLocal):  # kPMServerLocal only
    '''Show the printer browser for the given server.

       @keyword server: Print server (C{PMServer}) or C{None} for
                        this server, the localhost.

       @return: Printers (C{dict}) or C{None}.
    '''
    sv = _PM_Type0(server)
    return sv._2dict(libPC.PMServerLaunchPrinterBrowser) or None


def get_printers(server=kPMServerLocal):  # kPMServerLocal only
    '''Yield all printers available at the given server.

       @keyword server: Print server (C{PMServer}) or C{None} for
                        this server, the localhost.

       @return: Each printer (L{Printer}).
    '''
    sv = _PM_Type0(server)
    for p in sv._2tuple(libPC.PMServerCreatePrinterList, PMPrinter_t):
        yield Printer(p)


def get_resolutions(*printers):
    '''Yield the resolutions supported by the given printer(s).

       @param printers: No, one or more printers (L{Printer}s).

       @return: Each resolution 2-tuple (horizontal, vertical) in dots per inch (C{float}s).
    '''
    for p in _printers(printers):
        try:
            n = p._2int(libPC.PMPrinterGetPrinterResolutionCount)
        except _StatusError:  # kPMNotImplemented
            n = 0
        r = PMResolution_t()
        for i in range(n):
            p._libPCcall(libPC.PMPrinterGetIndexedPrinterResolution, i+1, byref(r))
            yield tuple(map(float, (r.hRes, r.vRes)))


class _StatusError(PrintError):
    '''C{OSStatus} error.
    '''
    def __init__(self, sts, name):
        for k, v in kPMErrors.items():
            if v == sts:
                break
        else:
            k = 'OSStatus'
        PrintError.__init__(self, '%s (%s) %s' % (k, sts, name))


# <https://www.OSStatus.com/search/results?platform=all&framework=all&search=0>
# <https://GitHub.com/phracker/MacOSX-SDKs/blob/master/MacOSX10.5.sdk/
#        System/Library/Frameworks/ApplicationServices.framework/Versions/
#        A/Frameworks/PrintCore.framework/Versions/A/Headers/PMErrors.h>
# Contains: Mac OS X Printing Manager Error Codes.
# Copyright: 2001-2006 by Apple Computer, Inc., all rights reserved
kPMErrors = Adict(
    # General error codes originally in PMDefinitions (-30870 to -30899)
    kPMNoError                   = noErr,   # no error
    kPMInvalidParameter          = -50,     # paramErr: parameter missing or invalid
    kPMAllocationFailure         = -108,    # memFullErr: out of memory error
#   kPMGeneralError              = -30870,  # general, internal error
    kPMInternalError             = -30870,  # internal printing error
    kPMOutOfScope                = -30871,  # an API call is out of scope
    kPMNoDefaultPrinter          = -30872,  # no default printer selected
    kPMNotImplemented            = -30873,  # this API call is not supported
    kPMNoSuchEntry               = -30874,  # no such entry
    kPMInvalidPrintSettings      = -30875,  # print settings reference is invalid
    kPMInvalidPageFormat         = -30876,  # pageformat reference is invalid
    kPMValueOutOfRange           = -30877,  # value passed in is out of range
    kPMLockIgnored               = -30878,  # lock value was ignored
    kPMInvalidPrintSession       = -30879,  # print session is invalid
    kPMInvalidPrinter            = -30880,  # printer reference is invalid
    kPMObjectInUse               = -30881,  # object is in use
    kPMInvalidIndex              = -30882,  # invalid index in array
    kPMStringConversionFailure   = -30883,  # error converting a string
    kPMXMLParseError             = -30884,  # error parsing XML data
    kPMInvalidJobTemplate        = -30885,  # invalid job template
    kPMInvalidPrinterInfo        = -30886,  # invalid printer info ticket
    kPMInvalidConnection         = -30887,  # invalid connection type
    kPMInvalidKey                = -30888,  # invalid key in ticket or template or dictionary
    kPMInvalidValue              = -30889,  # invalid value in ticket or template or dictionary
    kPMInvalidAllocator          = -30890,  # invalid memory allocator
    kPMInvalidTicket             = -30891,  # invalid job ticket
    kPMInvalidItem               = -30892,  # invalid item in ticket or template or dictionary
    kPMInvalidType               = -30893,  # invalid type in ticket or template or dictionary
    kPMInvalidReply              = -30894,  # invalid reply from a remote server/client
    kPMInvalidFileType           = -30895,  # invalid file type in queue
    kPMInvalidObject             = -30896,  # invalid object or internal error
    kPMInvalidPaper              = -30897,  # Invalid paper.
    kPMInvalidCalibrationTarget  = -30898,  # invalid dictionary specifying printer calibration target
    kPMInvalidPreset             = -30899,  # invalid preset
)
# Print Job Creator and Printing Dialog Extension error codes (-9500 to -9540)
#   kPMNoDefaultItem              = -9500,
#   kPMNoDefaultSettings          = -9501,  # unused; to be removed
#   kPMInvalidPDEContext          = -9530,  # invalid printing dialog extension context
#   kPMDontSwitchPDEError         = -9531,  # tells the pjc not to switch panels
#   kPMUnableToFindProcess        = -9532,  # unable to find the Finder.app process
#   kPMFeatureNotInstalled        = -9533,  # printer is feature capable, but not installed
# PrintCenter and Printer Browser error codes (-9540 to -9579)
#   kPMInvalidPBMRef              = -9540,  # invalid printer browser module reference
#   kPMNoSelectedPrinters         = -9541,  # no selected printers or error getting selection
#   kPMInvalidLookupSpec          = -9542,  # error retrieving lookup specification
#   kPMSyncRequestFailed          = -9543,  # error handling sync request
#   kPMEditRequestFailed          = -9544,  # error handling request to update Edit menu
#   kPMPrBrowserNoUI              = -9545,  # got UI function call with no UI present
# Job Ticket error codes (-9580 to -9619)
#   kPMTicketTypeNotFound         = -9580,  # we can't find the ticket type in our ticket.
#   kPMUpdateTicketFailed         = -9581,  # attempt to update ticket to current API failed
#   kPMValidateTicketFailed       = -9582,  # ticket has at least one key that's invalid
#   kPMSubTicketNotFound          = -9583,  # sub ticket requested is not stored in this ticket
#   kPMInvalidSubTicket           = -9584,  # unable to add the requested sub-ticket
#   kPMDeleteSubTicketFailed      = -9585,  #* sub ticket could not be deleted
#   kPMItemIsLocked               = -9586,  # item's locked flag was true when attempt made to update
#   kPMTicketIsLocked             = -9587,  # caller may not change a locked ticket
#   kPMTemplateIsLocked           = -9588,  # caller can't change the template
#   kPMKeyNotFound                = -9589,  # requested update is for a key that doesn't exist
#   kPMKeyNotUnique               = -9590,  # key passed in already exists in the ticket, can't make a new one
#   kPMUnknownDataType            = -9591,  # couldn't determine proper CF type for the value passed in
# ClientPrintingLib (-9620 to -9629)
#   kPMCreateMessageFailed        = -9620,  # could not create message
#   kPMServerCommunicationFailed  = -9621,  # communication with print server failed
#   kPMKeyOrValueNotFound         = -9623,  # missing required key or value
#   kPMMessagingError             = -9624,  # could not connect to message port or send a message to remote client
# Queue Manager (-9630 to -9659)
#   kPMServerNotFound             = -9630,  # print server not found
#   kPMServerAlreadyRunning       = -9631,  # print server is already running
#   kPMServerSuspended            = -9632,  # server suspended
#   kPMServerAttributeRestricted  = -9633,  # access to attribute restricted
#   kPMFileOrDirOperationFailed   = -9634,  # file/directory operation failed
#   kPMUserOrGroupNotFound        = -9635,  # specified user/group not found
#   kPMPermissionError            = -9636,  # permission related error
#   kPMUnknownMessage             = -9637,  # unknown message
#   kPMQueueNotFound              = -9638,  # queue not found
#   kPMQueueAlreadyExists         = -9639,  # queue already exists
#   kPMQueueJobFailed             = -9640,  # could not queue a new job
#   kPMJobNotFound                = -9641,  # job not found
#   kPMJobBusy                    = -9642,  # job is busy
#   kPMJobCanceled                = -9643,  # job has aborted
#   kPMDocumentNotFound           = -9644,  # document not found
# Job Manager (-9660 to -9699)
#   kPMPMSymbolNotFound           = -9660,  # required printer module symbol is missing
#   kPMIOMSymbolNotFound          = -9661,  # required IO module symbol is missing
#   kPMCVMSymbolNotFound          = -9662,  # required converter module symbol is missing
#   kPMInvalidPMContext           = -9663,  # printerModule context is invalid
#   kPMInvalidIOMContext          = -9664,  # IO Module context is invalid
#   kPMInvalidCVMContext          = -9665,  # converter module context is invalid
#   kPMInvalidJobID               = -9666,  # jobID passed from printer module is not valid
#   kPMNoPrinterJobID             = -9667,  # no jobID from target printer/connection
#   kPMJobStreamOpenFailed        = -9668,  # failed to open job stream
#   kPMJobStreamReadFailed        = -9669,  # failed to read from job stream
#   kPMJobStreamEndError          = -9670,  # reached end of job stream
#   kPMJobManagerAborted          = -9671,  # Job Manager is aborting
#   kPMJobGetTicketBadFormatError = -9672,  # XML for the printer module tickets could not be parsed.
#   kPMJobGetTicketReadError      = -9673,  # unknown error reading stdout from the PrintJobMgr
# Converters (-9700 to -9739)
#   kPMPluginNotFound             = -9701,  # converter plugin not found
#   kPMPluginRegisterationFailed  = -9702,  # converter Plugin error
#   kPMFontNotFound               = -9703,  # font not found
#   kPMFontNameTooLong            = -9704,  # font name too long
#   kPMGeneralCGError             = -9705,  # CoreGraphics returned error
#   kPMInvalidState               = -9706,  # invalid converter state
# Printer Modules (-9740 to -9779)
# IO Modules (-9780 to -9799)
#   kPMInvalidPrinterAddress      = -9780,  # file/connection could not be open
#   kPMOpenFailed                 = -9781,  # file/connection could not be open
#   kPMReadFailed                 = -9782,  # file/connection read failed
#   kPMWriteFailed                = -9783,  # file/connection write failed
#   kPMStatusFailed               = -9784,  # connection status failed
#   kPMCloseFailed                = -9785,  # close file/connection failed
#   kPMUnsupportedConnection      = -9786,  # connection type not supported
#   kPMIOAttrNotAvailable         = -9787,  # IO attribute not available on current connection type
#   kPMReadGotZeroData            = -9788,  # read got zero bytes, but no error
# End of list
#   kPMLastErrorCodeToMakeMaintenanceOfThisListEasier = -9799

_Types.Paper        = Paper
_Types.PaperCustom  = PaperCustom
_Types.PaperMargins = PaperMargins
_Types.Printer      = Printer

if __name__ == '__main__':

    from pycocoa.utils import _all_listing, _Globals, printf

    _Globals.argv0 = _NN_

    for i, p in enumerate(get_printers()):
        printf('%2s %s: ID %r, makemodel %r, URI %r', i + 1,
                     p, p.ID, p.makemodel, p.deviceURI)

    d = get_printer()
    if d:
        printf('default (%s) printer: %s...', d.isDefault, d, nl=1)
        for a in ('name', 'ID', 'makemodel', 'isColor', 'location',
                                'psCapable', 'psLevel', 'isRemote',
                                'deviceURI', 'deviceDescription',
                                'description', 'PPD', 'resolution'):
            printf(' %s: %r', _DOT_(d, a), getattr(d, a))

        printf(_NN_)
        for i, p in enumerate(get_papers(d)):
            t = tuple(map(zfstr, (p.width, p.height) + p.size2inch))
            printf('%2s %s: ID %r, %sx%s (%sX%s)', i + 1, p, p.ID, *t)

    p = Paper('A4')
    printf('paper: %s...', p, nl=1)
    for a in ('name', 'ID', 'height', 'width',
                            'size2inch', 'size2mm',
                            'PPD', 'printer'):
        printf(' %s: %r', _DOT_(p, a), getattr(p, a))
    printf(' %s: %r', _DOT_(p, 'localname'), p.localname(), nt=1)

    _all_listing(__all__, locals())

    # get_printer_browser()

# % python3 -m pycocoa.printers
#  1 Printer('Color'): ID 'Brother_MFC_...', makemodel 'Brother MFC-... CUPS', URI 'usb://...'

# default (True) printer: Printer('Color MFC-...')...
#  Printer('Color ...').name: 'Color MFC-...'
#  Printer('Color ...').ID: 'Brother_MFC_...'
#  Printer('Color ...').makemodel: 'Brother MFC-...CUPS'
#  Printer('Color ...').isColor: True
#  Printer('Color ...').location: '....'
#  Printer('Color ...').psCapable: True
#  Printer('Color ...').psLevel: 3
#  Printer('Color ...').isRemote: False
#  Printer('Color ...').deviceURI: 'usb://Brother/MFC-...?serial=...'
#  Printer('Color ...').deviceDescription: {'NSDeviceIsPrinter': 'YES'}
#  Printer('Color ...').description: '{\n    "Device Description" =     {\n        NSDeviceIsPrinter = YES;\n    };\n    "Language Level" = 3;\n    Name = "Color MFC-...";\n    Type = "Brother MFC-... CUPS";\n}'
#  Printer('Color ...').PPD: 'file:///var/folders/nx/.../...'
#  Printer('Color ...').resolution: (300.0, 300.0)
#
#  1 Paper('A4'): ID 'iso-a4', 595x842 (8.264X11.694)
#  2 Paper('US Letter'): ID 'na-letter', 612x792 (8.5X11)
#  3 Paper('US Legal'): ID 'na-legal', 612x1008 (8.5X14)
#  4 Paper('Executive'): ID 'executive', 522x756 (7.25X10.5)
#  5 Paper('A5'): ID 'iso-a5', 420x595 (5.833X8.264)
#  6 Paper('A5 Long Edge'): ID 'A5 Long Edge', 595x420 (8.264X5.833)
#  7 Paper('A6'): ID 'iso-a6', 297x420 (4.125X5.833)
#  8 Paper('B5'): ID 'iso-b5', 499x709 (6.931X9.847)
#  9 Paper('JIS B5'): ID 'jis-b5', 516x729 (7.167X10.125)
# 10 Paper('Envelope DL'): ID 'iso-designated', 312x624 (4.333X8.667)
# 11 Paper('Envelope C5'): ID 'iso-c5', 459x649 (6.375X9.014)
# 12 Paper('Envelope #10'): ID 'na-number-10-envelope', 297x684 (4.125X9.5)
# 13 Paper('Envelope Monarch'): ID 'monarch-envelope', 279x540 (3.875X7.5)
# 14 Paper('3 x 5'): ID '3 x 5', 216x360 (3X5)
# 15 Paper('8.5 x 13'): ID 'Folio', 612x936 (8.5X13)
# 16 Paper('Envelope PRC5 Long Edge'): ID 'DL Long Edge', 624x312 (8.667X4.333)
#
# paper: Paper('A4')...
#  Paper('A4').name: 'A4'
#  Paper('A4').ID: 'iso-a4'
#  Paper('A4').height: 842.0
#  Paper('A4').width: 595.0
#  Paper('A4').size2inch: (8.26388888888889, 11.694444444444445)
#  Paper('A4').size2mm: (209.90277777777774, 297.03888888888883)
#  Paper('A4').PPD: 'A4'
#  Paper('A4').printer: Printer('Color MFC-...') at 0x1034bd9d0
#  Paper('A4').localname: 'A4'


# pycocoa.printers.__all__ = tuple(
#  pycocoa.printers.get_libPC is <function .get_libPC at 0x100fa9ea0>,
#  pycocoa.printers.get_papers is <function .get_papers at 0x1014b05e0>,
#  pycocoa.printers.get_printer is <function .get_printer at 0x1014b0670>,
#  pycocoa.printers.get_printer_browser is <function .get_printer_browser at 0x1014b0700>,
#  pycocoa.printers.get_printers is <function .get_printers at 0x1014b0790>,
#  pycocoa.printers.get_resolutions is <function .get_resolutions at 0x1014b0820>,
#  pycocoa.printers.libPC is <CDLL '/System/Library/Frameworks/ApplicationServices.framework/Frameworks/PrintCore.framework/PrintCore', handle 46e129760 at 0x1014aca00>,
#  pycocoa.printers.Paper is <class .Paper>,
#  pycocoa.printers.PaperCustom is <class .PaperCustom>,
#  pycocoa.printers.PaperMargins is <class .PaperMargins>,
#  pycocoa.printers.Printer is <class .Printer>,
# )[11]
# pycocoa.printers.version 21.11.04, .isLazy 1, Python 3.11.0 64bit arm64, macOS 13.0.1

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

# Originally <https://Gist.GitHub.com/pudquick/68707b07c8c2772337cfd6397e399d3f>
