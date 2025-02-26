
# -*- coding: utf-8 -*-

u'''Lazily import C{pycocoa} modules and attributes, based on
U{lazy_import<https://modutil.ReadTheDocs.io/en/latest/#lazy_import>}
from Brett Cannon's U{modutil<https://PyPI.org/project/modutil>}.

C{Lazy import} is I{supported only for U{Python 3.7+
<https://Snarky.CA/lazy-importing-in-python-3-7>}} and is I{enabled by
default in U{PyCocoa 20.01.30<https://PyPI.org/project/PyCocoa>}
and later}.

To disable C{lazy import}, set environment variable C{PYCOCOA_LAZY_IMPORT}
to C{0} or an empty string.  Use C{2} or higher to print a message for
each lazily imported module and attribute, similar to environment variable
C{PYTHONVERBOSE} showing imports.  Using C{3} or higher also shows the
importing file name and line number.

@note: C{Lazy import} applies only to top-level modules of C{pycocoa}.
A C{lazy import} of a top-level module also loads all sub-modules
imported by that top-level module.

@var isLazy: Lazy import setting (C{int} 0, 1, 2 or 3+) from environment
             variable C{PYCOCOA_LAZY_IMPORT}, or C{None} if C{lazy import}
             is not supported or not enabled, or C{False} if initializing
             C{lazy import} failed.
'''
from pycocoa.internals import __all__ as _internals_all_, _COMMASPACE_, _Dall_, \
                              _Dfile_, _Dmain_, _Dpackage_, _DOT_, _fmt_invalid, \
                              _fmt, _instr, _MutableConstants, _NA_, _NN_, _no, \
                              _NSObject_, _pycocoa_, property_RO, _sys, _UNDER_
from os import environ as _environ
from os.path import basename as _basename
# import sys as _sys  # from .internals

_C_XTYPES = 'c_ptrdiff_t', 'c_struct_t', 'c_void'  # exported
_FOR_DOCS = _environ.get('PYCOCOA_FOR_DOCS', None)
_PY_FH    = _environ.get('PYTHONFAULTHANDLER', None)  # PYCHOK .faults, .__init__

# @module_property[_RO?] <https://GitHub.com/jtushman/proxy_tools/>
isLazy          =  None  # see @var isLazy above
# _isPython2    = _sys.version_info.major < 3  # PYCHOK in .runtime
_isPython3      = _sys.version_info.major > 2  # PYCHOK in .utils, .windows
_None           =  object()   # NOT None!
_Python_version = _sys.version.split()[0]


class LazyAttributeError(AttributeError):
    '''Raised if a C{lazily imported} attribute is missing or invalid.
    '''
    def __init__(self, fmtxt, *args):
        AttributeError.__init__(self, _fmt(fmtxt, *args))


class LazyImportError(ImportError):
    '''Raised if C{lazy import} is not supported, disabled or failed.
    '''
    def __init__(self, fmtxt, *args):
        ImportError.__init__(self, _fmt(fmtxt, *args))


class _Dict(dict):
    '''(INTERNAL) Imports C{dict}.
    '''
    def add(self, key, value, *values):
        '''Add C{[key] = value}, typically C{[attr] = mod}.

           @raise AssertionError: The B{C{key}} already exists
                                  with different B{C{value}}.
        '''
        if key in self:
            val = self[key]  # duplicate OK
            if val != value and val not in values:
                t = _fmt('%s[%s]: %r vs %r', 'imports', key, val, value)
                raise AssertionError(t)
        else:
            self[key] = value


class _NamedEnum_RO(dict):
    '''(INTERNAL) C{Read_Only} enum-like C{dict} sub-class.
    '''
    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            t = _no('enum', _DOT_(self._name, attr))  # PYCHOK _name
            raise AttributeError(t)

    def __setattr__(self, attr, value):
        t = _DOT_(self._name, attr)  # PYCHOK _name
        t = _fmt('%s %s: %s = %r', 'Read_Only', 'enum', t, value)
        raise TypeError(t)

    def enums(self):
        for k, v in dict.items(self):
            if not k.startswith(_UNDER_):
                yield k, v


class _Types(_MutableConstants):
    '''Python Types, to avoid circular imports, lazily set.
    '''
    AlertPanel    = None  # set by .panels
    App           = None  # set by .apps
    Color         = None  # set by .colors
    Dict          = None  # set by .dicts
    ErrorPanel    = None  # set by .panels
    Font          = None  # sef by .fonts
    FrozenDict    = None  # set by .dicts
    FrozenSet     = None  # set by .sets
    Item          = None  # set by .menus
    ItemSeparator = None  # set by .menus
    List          = None  # set by .lists
    MediaWindow   = None  # set by .windows
    Menu          = None  # set by .menus
    MenuBar       = None  # set by .menus
    OpenPanel     = None  # set by .panels
    Paper         = None  # set by .printer
    PaperCustom   = None  # set by .printer
    PaperMargins  = None  # set by .printer
    Printer       = None  # set by .printer
    SavePanel     = None  # set by .panels
    Screen        = None  # set by .screens
    Set           = None  # set by .sets
    Str           = None  # set by .strs
    StrAttd       = None  # set by .strs
    Table         = None  # set by .tables
    TableWindow   = None  # set by .tables
    TextPanel     = None  # set by .panels
    TextWindow    = None  # set by .windows
    Tuple         = None  # set by .tuples
    Window        = None  # set by .windows

    def __getattr__(self, name):  # called when .__getattribute__ failed
        '''(INTERNAL) Lazily import missing _Types.
        '''
        return _MutableConstants.__getattr__(self, name) or _lazy_import(name)

    def __getattribute__(self, name):  # called when .name accessed
        '''(INTERNAL) Lazily import missing _Types.
        '''
        return _MutableConstants.__getattribute__(self, name)  # or _lazy_import(name)

    @property_RO
    def pycocoa(self):  # get pycocoa, I{once}
        pycocoa = _sys.modules[_pycocoa_]  # without re-import, isLazy=0?
        _Types.__class__.pycocoa = pycocoa  # overwrite property_RO
        return pycocoa

_Types = _Types()  # PYCHOK singleton

if _FOR_DOCS:
    def _ALL_DOCS(*exports):
        '''(INTERNAL) Only C{B{exports}.__name__} when make'ing docs to
           force C{epydoc} to include classes, methods, functions and
           other names in the documentation.  Using C{epydoc --private
           ...} tends to include far too much internal documentation.
        '''
        return tuple(x.__name__ for x in exports)
else:
    def _ALL_DOCS(*unused):  # PYCHOK expected
        return ()


_ALL_INIT = 'pycocoa_abspath', 'version'  # exported by pycocoa.__init__,py

# __all__ value for most modules, accessible as _ALL_LAZY.<module>
_ALL_LAZY = _NamedEnum_RO(_name='_ALL_LAZY',
                           apps=('App', 'app_title', 'ns2App', 'NSApplicationDelegate', 'Tile'),
                          bases=(),  # module only
                         colors=('CMYColor', 'CMYColors', 'Color', 'ColorError', 'Colors', 'GrayScaleColor', 'GrayScaleColors',
                                 'HSBColor', 'HSBColors', 'RGBColor', 'RGBColors', 'TintColor', 'TintColors', 'UIColor', 'UIColors'),
                     deprecated=('Cache2', 'module_property_RO',
                                 'get_libPC', 'get_libs', 'property2', 'sortuples',
                                 'libAppKit', 'libCF', 'libCG', 'libCT', 'libFoundation', 'libPC', 'libobjc',
                                 'OBJC_ASSOCIATION_ASSIGN', 'OBJC_ASSOCIATION_COPY', 'OBJC_ASSOCIATION_COPY_NONATOMIC',
                                 'OBJC_ASSOCIATION_RETAIN', 'OBJC_ASSOCIATION_RETAIN_NONATOMIC'),
                          dicts=('Dict', 'FrozenDict'),
                         faults=('getUncaughtExceptionHandler', 'setUncaughtExceptionHandler',),  # disable, enable, exiting, is_enabled, SIGs_enabled
                          fonts=('Font', 'FontError', 'fontfamilies', 'fontnamesof', 'Fonts',
                                 'fontsof', 'fontsof4', 'FontTrait', 'FontTraitError', 'fontTraits', 'fontTraitstrs'),
                       geometry=('Point', 'Point2', 'Rect', 'Rect4', 'Size', 'Size2'),
                        getters=('get_c_func_t', 'get_class', 'get_classes', 'get_classname', 'get_classnameof',
                                 'get_classof', 'get_inheritance', 'get_ivar', 'get_ivars', 'get_metaclass',
                                 'get_method', 'get_methods', 'get_properties', 'get_protocol', 'get_protocols',
                                 'get_selector', 'get_selectorname_permutations', 'get_selectornameof',
                                 'get_superclass', 'get_superclassnameof', 'get_superclassof'),
                      internals=_internals_all_,
                         lazily=('LazyAttributeError', 'LazyImportError', 'isLazy'),
                          lists=('List',),
                          menus=('Item', 'ItemSeparator', 'Keys', 'Menu', 'MenuBar', 'ns2Item', 'title2action'),
                        nstypes=('at', 'isAlias', 'isLink', 'isNone',
                                 'NSAlert', 'NSApplication',
                                 'NSArray', 'nsArray2listuple',  'nsArray2tuple', 'NSAttributedString', 'NSAutoreleasePool',
                                 'NSBezierPath', 'NSBoolean', 'nsBoolean2bool', 'NSBundle', 'nsBundleRename',
                                 'NSColor', 'NSConcreteNotification', 'NSConcreteValue', 'NSConstantString',
                                 'NSData', 'nsData2bytes', 'NSDate',
                                 'NSDecimal', 'nsDecimal2decimal', 'NSDecimalNumber', 'nsDescription2dict',
                                 'NSDictionary', 'nsDictionary2dict', 'nsDictionary2items',
                                 'NSDockTile', 'NSDouble',
                                 'NSEnumerator', 'NSError', 'NSException', 'nsException', 'NSExceptionError',
                                 'NSFloat', 'NSFont', 'NSFontDescriptor', 'NSFontManager', 'NSFontPanel',
                                 'NSImage', 'NSImageView', 'NSInt', 'nsIter', 'nsIter2',
                                 'NSLayoutManager', 'nsLog', 'nsLogf', 'NSLong', 'NSLongLong',
                                 'NSMain', 'NSMenu', 'NSMenuItem', 'NSMutableArray', 'NSMutableData',
                                 'NSMutableDictionary', 'NSMutableSet', 'NSMutableString',
                                 'NSNotification', 'NSNotificationCenter', 'ns2NSType2',
                                 'NSNull', 'nsNull2none', 'NSNumber', 'nsNumber2num',
                                 _NSObject_, 'nsOf', 'NSOpenPanel', 'ns2py', 'NSPageLayout',
                                 'NSPrinter', 'NSPrintInfo', 'NSPrintOperation', 'NSPrintPanel', 'nsRaise',
                                 'NSSavePanel', 'NSScreen', 'NSScrollView', 'NSSet', 'nsSet2set',
                                 'NSStatusBar', 'NSStr', 'NSString', 'nsString2str',
                                 'NSTableColumn', 'NSTableView',
                                 'NSTextField', 'nsTextSize3', 'nsTextView', 'NSTextView',
                                 'NSThread', 'nsThrow', 'ns2Type', 'ns2TypeID2',
                                 'NSURL', 'nsURL2str', 'NSValue', 'nsValue2py', 'NSView', 'NSWindow'),
                        octypes=('Allocator_t', 'Array_t', 'Block_t', 'BOOL_t',
                                 'CFIndex_t', 'CFRange_t',
                                 'CGBitmapInfo_t', 'CGDirectDisplayID_t', 'CGError_t', 'CGFloat_t',
                                 'CGGlyph_t', 'CGImageEncoding', 'CGPoint_t', 'CGPointEncoding',
                                 'CGRect_t', 'CGRectEncoding', 'CGSize_t', 'CGSizeEncoding', 'Class_t',
                                 'CTFontOrientation_t', 'CTFontSymbolicTraits_t',
                                 'Data_t', 'Dictionary_t', 'Id_t', 'IMP_t', 'Ivar_t', 'Method_t',
                                 'NSDouble_t', 'NSFloat_t', 'NSFloatEncoding', 'NSInteger_t', 'NSIntegerEncoding', 'NSIntegerMax',
                                 'NSMakePoint', 'NSMakeRange', 'NSMakeRect', 'NSMakeSize', 'NSNotFound',
                                 'NSPoint_t', 'NSPointEncoding', 'NSPointZero', 'NSRange_t', 'NSRangeEncoding',
                                 'NSRect4_t', 'NSRect_t', 'NSRectEncoding', 'NSSize_t', 'NSSizeEncoding', 'NSTimeInterval_t',
                                 'NSUInteger_t', 'NSUIntegerEncoding', 'NSZoneEncoding', 'Number_t', 'NumberType_t',
                                 'objc_method_description_t', 'objc_property_attribute_t', 'objc_property_t', 'objc_super_t',
                                 'ObjC_t', 'OptionFlags_t', 'Protocol_t', 'PyObjectEncoding', 'RunLoop_t', 'SEL_t',
                                 'Set_t', 'split_emcoding2', 'split_encoding', 'String_t', 'Struct_t',
                                 'TimeInterval_t', 'TypeCodeError', 'TypeID_t', 'TypeRef_t',
                                 'UniChar_t', 'unichar_t', 'Union_t', 'Unknown_t', 'UnknownPtr_t', 'URL_t',
                                 'VoidPtr_t') + _C_XTYPES,
                         oslibs=('get_lib', 'get_lib_framework', 'leaked2', 'Libs',
                                 'NO', 'NSAcknowledgeCharacter', 'NSAlphaShiftKeyMask', 'NSAlternateKeyMask', 'NSAnyEventMask',
                                 'NSApplicationActivationPolicyAccessory', 'NSApplicationActivationPolicyProhibited',
                                 'NSApplicationActivationPolicyRegular', 'NSApplicationDefined', 'NSApplicationDidHideNotification',
                                 'NSApplicationDidUnhideNotification', 'NSApplicationPresentationDefault', 'NSApplicationPresentationDisableHideApplication',
                                 'NSApplicationPresentationDisableProcessSwitching', 'NSApplicationPresentationHideDock', 'NSApplicationPresentationHideMenuBar',
                                 'NSBackingStoreBuffered', 'NSBackingStoreNonretained', 'NSBackingStoreRetained',
                                 'NSBackSpaceCharacter', 'NSBackTabCharacter', 'NSBellCharacter', 'NSCancelButton', 'NSCancelCharacter',
                                 'NSCarriageReturnCharacter', 'NSCenterTextAlignment', 'NSClearLineFunctionKey', 'NSCommandKeyMask', 'NSControlKeyMask',
                                 'NSDataLineEscapeCharacter', 'NSDefaultRunLoopMode', 'NSDeleteCharacter', 'NSDeleteFunctionKey',
                                 'NSDeviceControl1Character', 'NSDeviceControl2Character', 'NSDeviceControl3Character', 'NSDeviceControl4Character',
                                 'NSDownArrowFunctionKey', 'NSEndFunctionKey', 'NSEndOfMediumCharacter', 'NSEndOfTextCharacter', 'NSEndOfTransmitBlockCharacter',
                                 'NSEndOfTransmitCharacter', 'NSEnquiryCharacter', 'NSEnterCharacter', 'NSEscapeCharacter', 'NSEventTrackingRunLoopMode',
                                 'NSF19FunctionKey', 'NSF1FunctionKey', 'NSFileHandlingPanelCancelButton', 'NSFileHandlingPanelOKButton',
                                 'NSFileSeparatorCharacter', 'NSFlagsChanged', 'NSFontBoldMask', 'NSFontClarendonSerifsClass', 'NSFontClassMask',
                                 'NSFontColorGlyphsMask', 'NSFontCompositeMask', 'NSFontCompressedMask', 'NSFontCondensedMask', 'NSFontExpandedMask',
                                 'NSFontFreeformSerifsClass', 'NSFontItalicMask', 'NSFontModernSerifsClass', 'NSFontMonoSpaceMask', 'NSFontNarrowMask',
                                 'NSFontNonStandardCharacterSetMask', 'NSFontOldStyleSerifsClass', 'NSFontOrnamentalsClass', 'NSFontPosterMask',
                                 'NSFontSansSerifClass', 'NSFontScriptsClass', 'NSFontSlabSerifsClass', 'NSFontSmallCapsMask', 'NSFontSymbolicClass',
                                 'NSFontTransitionalSerifsClass', 'NSFontUIOptimizedMask', 'NSFontUnboldMask', 'NSFontUnitalicMask', 'NSFontUnknownClass',
                                 'NSFontVerticalMask', 'NSFormFeedCharacter', 'NSFunctionKeyMask', 'NSGroupSeparatorCharacter', 'NSHelpFunctionKey',
                                 'NSHelpKeyMask', 'NSHomeFunctionKey', 'NSHorizontalTabCharacter', 'NSJustifiedTextAlignment',
                                 'NSKeyDown', 'NSKeyUp', 'NSLeftArrowFunctionKey', 'NSLeftTextAlignment', 'NSLineFeedCharacter', 'NSLineSeparatorCharacter',
                                 'NSNaturalTextAlignment', 'NSNegativeAcknowledgeCharacter', 'NSNewLineCharacter', 'NSNullCharacter', 'NSNumericPadKeyMask',
                                 'NSOKButton', 'NSPageDownFunctionKey', 'NSPageUpFunctionKey', 'NSParagraphSeparatorCharacter', 'NSRecordSeparatorCharacter',
                                 'NSRightArrowFunctionKey', 'NSRightTextAlignment', 'NSShiftInCharacter', 'NSShiftKeyMask', 'NSShiftOutCharacter',
                                 'NSSpaceCharacter', 'NSSquareStatusItemLength', 'NSStartOfHeadingCharacter', 'NSStartOfTextCharacter', 'NSSubstituteCharacter',
                                 'NSSynchronousIdleCharacter', 'NSTabCharacter', 'NSTableViewDashedHorizontalGridLineMask', 'NSTableViewGridNone',
                                 'NSTableViewSolidHorizontalGridLineMask', 'NSTableViewSolidVerticalGridLineMask', 'NSTextAlignmentCenter',
                                 'NSTextAlignmentJustified', 'NSTextAlignmentLeft', 'NSTextAlignmentNatural', 'NSTextAlignmentRight',
                                 'NSTextWritingDirectionEmbedding', 'NSTextWritingDirectionOverride', 'NSTrackingActiveInActiveApp', 'NSTrackingCursorUpdate',
                                 'NSTrackingMouseEnteredAndExited', 'NSTrackingMouseMoved', 'NSUnitSeparatorCharacter', 'NSUpArrowFunctionKey',
                                 'NSVariableStatusItemLength', 'NSVerticalTabCharacter', 'NSWindowCloseButton', 'NSWindowDocumentIconButton',
                                 'NSWindowMiniaturizeButton', 'NSWindowStyleMaskClosable', 'NSWindowStyleMaskMiniaturizable', 'NSWindowStyleMaskResizable',
                                 'NSWindowStyleMaskTitled', 'NSWindowStyleMaskUsual', 'NSWindowStyleMaskUtilityWindow', 'NSWindowToolbarButton',
                                 'NSWindowZoomButton', 'OSlibError', 'YES'),
                         panels=('AlertPanel', 'AlertStyle', 'BrowserPanel', 'ErrorPanel', 'NSAlertDelegate', 'OpenPanel', 'PanelButton', 'SavePanel', 'TextPanel'),
                       printers=('get_papers', 'get_printer', 'get_printer_browser', 'get_printers', 'get_resolutions',
                                 'Paper', 'PaperCustom', 'PaperMargins', 'Printer'),
                        pytypes=('bool2NS', 'bytes2NS', 'decimal2NS', 'dict2NS', 'dicts2NS', 'float2NS', 'frozendict2NS', 'frozenset2NS',
                                 'generator2NS', 'int2NS', 'iterable2NS', 'list2NS', 'listuple2NS', 'map2NS', 'None2NS', 'py2NS', 'range2NS',
                                 'set2NS', 'sets2NS', 'str2NS', 'strs2NS', 'time2NS', 'tuple2NS', 'type2NS', 'unicode2NS', 'url2NS'),
                        runtime=('add_ivar', 'add_method', 'add_protocol', 'add_subclass', 'drain', 'OBJC_ASSOCIATION',
                                 'isClass', 'isImmutable', 'isMetaClass', 'isMutable', 'isObjCInstanceOf',
                                 'ObjCBoundClassMethod', 'ObjCBoundMethod', 'ObjCClass', 'ObjCClassMethod',
                                 'ObjCConstant', 'ObjCDelegate', 'ObjCInstance', 'ObjCMethod', 'ObjCSubclass',
                                 'register_subclass', 'release', 'retain', 'send_message', 'send_super', 'send_super_init', 'set_ivar'),
                        screens=('BuiltInScreen', 'DeepestScreen', 'ExternalScreen', 'Frame', 'MainScreen', 'Screen', 'Screens'),
                           sets=('FrozenSet', 'Set'),
                           strs=('Str', 'StrAttd'),
                         tables=('closeTables', 'NSTableViewDelegate', 'Table', 'TableWindow'),
                         tuples=('Tuple',),
                          utils=('aspect_ratio', 'clipstr', 'errorf', 'flint', 'gcd',
                                 'inst2strepr', 'isinstanceOf', 'islistuple', 'logf',
                                 'machine', 'name2objc', 'name2py', 'name2pymethod',
                                 'printf', 'properties',
                                 'terminating', 'type2strepr', 'z1000str', 'zfstr', 'zSIstr'),
                        windows=('AutoResize', 'AutoResizeError', 'autoResizes', 'BezelStyle', 'Border', 'MediaWindow', 'ns2Window',
                                 'NSWindowDelegate', 'TextWindow', 'Window', 'WindowError', 'WindowStyle', 'WindowStyleError', 'windowStyles'))

# DEPRECATED __all__ names overloading those in _ALL_LAZY.deprecated where
# the new name is fully backward compatible in signature and return value
_ALL_OVERRIDING = _NamedEnum_RO(_name='_ALL_OVERRIDING')  # all DEPRECATED

__all__ = _ALL_LAZY.lazily
__version__ = '25.02.25'


def _all_imports(**more):
    '''(INTERNAL) Build C{dict} of all lazy imports.
    '''
    # imports naming conventions stored below - [<key>] = <from>:
    #  import <module>                        - [<module>] = <module>
    #  from <module> import <attr>            - [<attr>] = <module>
    #  from pycocoa import <attr>             - [<attr>] = <attr>
    #  from <module> import <attr> as <name>  - [<name>] = <module>.<attr>
    imports = _Dict()
    imports_add = imports.add

    for _all_ in (_ALL_LAZY, _ALL_OVERRIDING, more):
        for mod, attrs in _all_.items():
            if isinstance(attrs, tuple) and not mod.startswith(_UNDER_):
                imports_add(mod, mod)
                for attr in attrs:
                    attr, _, _as_ = attr.partition(' as ')
                    if _as_:
                        imports_add(_as_, _DOT_(mod, attr))
                    else:
                        imports_add(attr, mod)
    return imports


def _all_missing(_all, _imp):
    '''(INTERNAL) Get deltas between C{_all} and C{_imp}.
    '''
    return _COMMASPACE_.join(a for a in _all if a not in _imp)


def _all_missing2(_all):
    '''(INTERNAL) Get deltas between pycocoa.__all__ and lazily._all_imports.
    '''
    _imp = _all_imports(**_NamedEnum_RO((a, ()) for a in _ALL_INIT))
    return ((_DOT_('lazily',  _all_imports.__name__), _all_missing(_all, _imp)),
            (_DOT_(_pycocoa_, _Dall_),                _all_missing(_imp, _all)))


def _caller3(up):  # in .named
    '''(INTERNAL) Get 3-tuple C{(caller name, file name, line number)}
       for the caller B{C{up}} stack frames in the Python call stack.
    '''
    # sys._getframe(1) ... 'importlib._bootstrap' line 1032,
    # may throw a ValueError('call stack not deep enough')
    f = _sys._getframe(up + 1)
    return (f.f_code.co_name,  # caller name
           _basename(f.f_code.co_filename),  # file name
            f.f_lineno)  # line number


def _lazy_import(name):  # overwritten below in Python 3.7+, in .internals
    '''(INTERNAL) Lazily import an attribute by C{name}.
    '''
    try:
        return getattr(_Types.pycocoa, name)  # XXX _None or missing?
    except (AttributeError, ImportError) as x:
        t = _instr(_lazy_import, name)
        raise LazyImportError('%s: %s', t, x)


def _lazy_import2(pack):  # MCCABE 15
    '''Check for and set up lazy importing.

       @arg pack: The name of the package (C{str}) performing the imports,
                  to resolve relative imports, usually C{__package__}.

       @return: 2-Tuple (package, getattr) of the importing package for
                easy reference within itself and the callable to be set
                to `__getattr__`.

       @raise LazyAttributeError: The package, module or attribute name
                                  is invalid or does not exist.

       @raise LazyImportError: Lazy import not supported or import failed.

       @note: This is the original function U{modutil.lazy_import
              <https://GitHub.com/brettcannon/modutil/blob/master/modutil.py>}
              modified to handle the C{__all__} and C{__dir__} attributes
              and call C{importlib.import_module(<module>.<name>, ...)}
              without causing a C{ModuleNotFoundError}.

       @see: The original U{modutil<https://PyPi.org/project/modutil>},
             U{PEP 562<https://www.Python.org/dev/peps/pep-0562>} and
             U{Werkzeug<https://GitHub.com/pallets/werkzeug/blob/master/werkzeug/__init__.py>}.
    '''
    global isLazy

    if _sys.version_info[:2] < (3, 7):  # not supported
        t = _no(_DOT_(pack, _lazy_import2.__name__), 'for')
        raise LazyImportError('%s Python %s', t, _Python_version)

    import_module, package, parent = _lazy_init3(pack)

    imports  = _all_imports()
    packages = (parent, _Dmain_, _NN_)

    def __getattr__(name):  # __getattr__ only for Python 3.7+
        # only called once for each undefined pycocoa attribute
        if name in imports:
            # importlib.import_module() implicitly sets sub-modules
            # on this module as appropriate for direct imports (see
            # note in the _lazy_import.__doc__ above).
            mod, _, attr = imports[name].partition(_DOT_)
            if mod not in imports:
                raise LazyImportError(_no('module', _DOT_(parent, mod)))
            imported = import_module(_DOT_(pack, mod), parent)
            pkg = getattr(imported, _Dpackage_, None)
            if pkg not in packages:
                raise LazyImportError('%s %r', _DOT_(mod, _Dpackage_), pkg)
            # import the module or module attribute
            if attr:
                imported = getattr(imported, attr, _None)
            elif name != mod:
                imported = getattr(imported, name, _None)
            if imported is _None:
                raise LazyAttributeError(_no('attribute', _DOT_(mod, attr or name)))

        elif name in (_Dall_,):  # XXX _Ddir_, _Dmembers_?
            imported = _ALL_INIT + tuple(imports.keys())
            mod = _NN_
        else:
            raise LazyAttributeError(_no('module', 'or', 'attribute', _DOT_(parent, name)))

        setattr(package, name, imported)
        if isLazy > 1:
            t = _NN_
            if mod and mod != name:
                t = _DOT_(' from ', mod)
            if isLazy > 2:
                try:  # see C{_caller3}
                    _, f, s = _caller3(2)
                    t = _fmt('%s by %s line %d', t, f, s)
                except ValueError:
                    pass
            t = _NN_('# lazily imported ', _DOT_(parent, name), t)
            print(t)

        return imported  # __getattr__

    global _lazy_import  # for _Types.__getattr[ibute]__
    _lazy_import = __getattr__

    return package, __getattr__  # _lazy_import2


def _lazy_init3(pack):
    '''(INTERNAL) Try to initialize lazy import.

       @arg pack: The name of the package (C{str}) performing the imports,
                  to resolve relative imports, usually C{__package__}.

       @return: 3-Tuple C{(import_module, package, parent)} of module
                C{importlib.import_module}, the importing C{package}
                for easy reference within itself and the package name,
                aka the C{package}'s C{parent}.

       @raise LazyImportError: Lazy import not supported or not enabled,
                               an import failed or the package name is
                               invalid or does not exist.

       @note: Global C{isLazy} is set accordingly.
    '''
    global isLazy

    if pack != _pycocoa_:  # assertion
        t = _fmt_invalid(repr(_pycocoa_), pack=repr(pack))
        raise LazyImportError(t)

    try:  # to initialize
        from importlib import import_module  # in Python 2.7+

        z = _environ.get('PYCOCOA_LAZY_IMPORT', '1')  # 1 default on 3.7
        z =  z.strip()  # like PYTHONVERBOSE et.al.
        isLazy = int(z) if z.isdigit() else (1 if z else 0)
        if isLazy < 1:  # not enabled
            raise LazyImportError('env %s=%r', 'PYCOCOA_LAZY_IMPORT', z)
        if _sys.flags.verbose:  # _environ.get('PYTHONVERBOSE', None)
            isLazy += 1

        package = import_module(pack)
        parent = package.__spec__.parent  # __spec__ only in Python 3.7+
        if parent != pack:  # assertion
            raise AttributeError(_fmt_invalid(pack, parent=parent))

    except (AttributeError, ImportError) as x:
        isLazy = False  # failed
        raise LazyImportError('init failed: %s', x)

    return import_module, package, parent


if __name__ == _Dmain_:

    # the following warning appears when running this module with Python 3.7 or later as ...
    #
    # % python3 -m pycocoa.lazily
    #
    # /Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/runpy.py:127: RuntimeWarning:
    # 'pycocoa.lazily' found in sys.modules after import of package 'pycocoa', but prior to execution
    #  of 'pycocoa.lazily'; this may result in unpredictable behaviour ... warn(RuntimeWarning(msg))
    #
    # <https://StackOverflow.com/questions/43393764/python-3-6-project-structure-leads-to-runtimewarning>

    for n, m in _sys.modules.items():  # show any pre-loaded modules
        if n in _ALL_LAZY or getattr(m, _Dpackage_, _NN_) == _pycocoa_:
            print(_fmt('pre-loaded %s: %s?', n, getattr(m, _Dfile_, _NA_)))

# % python3 -m pycocoa.lazily
#
# ... runpy.py:128: RuntimeWarning: ...
# pre-loaded __main__: .../PyCocoa/pycocoa/lazily.py?
# pre-loaded pycocoa.lazily: .../PyCocoa/pycocoa/lazily.py?
# pre-loaded pycocoa: .../PyCocoa/pycocoa/__init__.py?

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2018-2025 -- mrJean1 at Gmail -- All Rights Reserved.
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
