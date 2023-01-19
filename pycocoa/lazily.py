
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

from os import environ as _environ, linesep as _NL_  # PYCHOK expected
from os.path import basename as _basename
import sys as _sys

_C_XTYPES = 'c_ptrdiff_t', 'c_struct_t', 'c_void'  # exported
_FOR_DOCS = _environ.get('PYCOCOA_FOR_DOCS', None)
_N_A      =  object()
_pycocoa_ = 'pycocoa'
_PY_FH    = _environ.get('PYTHONFAULTHANDLER', None)  # PYCHOK .faults, .__init__

# @module_property[_RO?] <https://GitHub.com/jtushman/proxy_tools/>
isLazy = None  # see @var isLazy above


class LazyImportError(ImportError):
    '''Lazy import is not supported, disabled or failed some other way.
    '''
    def __init__(self, fmt, *args):
        ImportError.__init__(self, (fmt % args) if args else fmt)


class _Dict(dict):
    '''(INTERNAL) Imports C{dict}.
    '''
    def add(self, key, value, *values):
        '''Add C{[key] = value}, typically C{[attr] = mod}.

           @raise AssertionError: The B{C{key}} already
                                  exists with different
                                  B{C{value}}.
        '''
        if key in self:
            val = self[key]  # duplicate OK
            if val != value and val not in values:
                t = 'imports', key, val, value
                raise AssertionError('%s[%s]: %r, not %r' % t)
        else:
            self[key] = value


class _NamedEnum_RO(dict):
    '''(INTERNAL) C{Read_Only} enum-like C{dict} sub-class.
    '''
    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError("%s.%s doesn't exist" % (self._name, attr))  # PYCHOK expected

    def __setattr__(self, attr, value):
        raise TypeError('Read_Only %s = %r' % (self._name, _DOT_(attr, value)))  # PYCHOK expected

    def enums(self):
        for k, v in dict.items(self):
            if not k.startswith(_UNDER_):
                yield k, v


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
                         lazily=('LazyImportError', 'isLazy'),
                          lists=('List',),
                          menus=('Item', 'ItemSeparator', 'Keys', 'Menu', 'MenuBar', 'ns2Item', 'title2action'),
                        nstypes=('at', 'drain', 'isAlias', 'isLink', 'isNone',
                                 'NSAlert', 'NSApplication',
                                 'NSArray', 'nsArray2listuple', 'nsArray2tuple', 'NSAttributedString', 'NSAutoreleasePool',
                                 'NSBezierPath', 'NSBoolean', 'nsBoolean2bool', 'NSBundle', 'nsBundleRename',
                                 'NSColor', 'NSConcreteNotification', 'NSConcreteValue', 'NSConstantString',
                                 'NSData', 'nsData2bytes', 'NSDate',
                                 'NSDecimal', 'nsDecimal2decimal', 'NSDecimalNumber', 'nsDescription2dict',
                                 'NSDictionary', 'nsDictionary2dict', 'nsDictionary2items', 'NSDockTile', 'NSDouble',
                                 'NSEnumerator', 'NSError', 'NSException', 'nsException', 'NSExceptionError',
                                 'NSFloat', 'NSFont', 'NSFontDescriptor', 'NSFontManager', 'NSFontPanel',
                                 'NSImage', 'NSImageView', 'NSInt', 'nsIter', 'nsIter2',
                                 'NSLayoutManager', 'nsLog', 'nsLogf', 'NSLong', 'NSLongLong',
                                 'NSMain', 'NSMenu', 'NSMenuItem', 'NSMutableArray', 'NSMutableData',
                                 'NSMutableDictionary', 'NSMutableSet', 'NSMutableString',
                                 'NSNotification', 'NSNotificationCenter', 'NSNull', 'nsNull2none', 'NSNumber', 'nsNumber2num',
                                 'NSObject', 'nsOf', 'NSOpenPanel', 'ns2py', 'NSPageLayout',
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
                         oslibs=('get_lib', 'get_libs', 'get_lib_framework', 'leaked2',
                                 'libAppKit', 'libCF', 'libCG', 'libCT', 'libFoundation', 'libobjc', 'Libs',
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
                                 'NSWindowZoomButton', 'YES'),
                         panels=('AlertPanel', 'AlertStyle', 'BrowserPanel', 'ErrorPanel', 'OpenPanel', 'PanelButton', 'SavePanel', 'TextPanel'),
                       printers=('get_libPC', 'get_papers', 'get_printer', 'get_printer_browser', 'get_printers', 'get_resolutions', 'libPC',
                                 'Paper', 'PaperCustom', 'PaperMargins', 'Printer'),
                        pytypes=('bool2NS', 'bytes2NS', 'dict2NS', 'float2NS', 'frozenset2NS', 'generator2NS', 'int2NS', 'list2NS', 'map2NS',
                                 'None2NS', 'py2NS', 'range2NS', 'set2NS', 'str2NS', 'time2NS', 'tuple2NS', 'type2NS', 'unicode2NS', 'url2NS'),
                        runtime=('add_ivar', 'add_method', 'add_protocol', 'add_subclass', 'isClass', 'isImmutable',
                                 'isMetaClass', 'isObjCInstanceOf', 'OBJC_ASSOCIATION_COPY', 'OBJC_ASSOCIATION_COPY_NONATOMIC',
                                 'OBJC_ASSOCIATION_RETAIN', 'OBJC_ASSOCIATION_RETAIN_NONATOMIC', 'ObjCBoundClassMethod', 'ObjCBoundMethod',
                                 'ObjCClass', 'ObjCClassMethod', 'ObjCConstant', 'ObjCDelegate', 'ObjCInstance', 'ObjCMethod', 'ObjCSubclass',
                                 'register_subclass', 'release', 'retain', 'send_message', 'send_super', 'send_super_init', 'set_ivar'),
                        screens=('BuiltInScreen', 'DeepestScreen', 'ExternalScreen', 'Frame', 'MainScreen', 'Screen', 'Screens'),
                           sets=('FrozenSet', 'Set'),
                           strs=('Str', 'StrAttd'),
                         tables=('closeTables', 'NSTableViewDelegate', 'Table', 'TableWindow'),
                         tuples=('Tuple',),
                          utils=('Adict', 'aspect_ratio',
                                 'bytes2repr', 'bytes2str', 'Cache2', 'clipstr',
                                 'DEFAULT_UNICODE', 'flint', 'gcd',
                                 'inst2strepr', 'isinstanceOf', 'iterbytes',
                                 'lambda1', 'logf',
                                 'machine', 'missing', 'module_property_RO',
                                 'name2objc', 'name2py', 'name2pymethod',
                                 'printf', 'properties', 'property2', 'property_RO',
                                 'sortuples', 'str2bytes', 'terminating', 'type2strepr',
                                 'z1000str', 'zfstr', 'zSIstr'),
                        windows=('AutoResize', 'AutoResizeError', 'autoResizes', 'BezelStyle', 'Border', 'MediaWindow', 'ns2Window',
                                 'NSWindowDelegate', 'TextWindow', 'Window', 'WindowError', 'WindowStyle', 'WindowStyleError', 'windowStyles'))

# DEPRECATED __all__ names overloading those in _ALL_LAZY.deprecated where
# the new name is fully backward compatible in signature and return value
_ALL_OVERRIDING = _NamedEnum_RO(_name='_ALL_OVERRIDING')  # all DEPRECATED

__all__ = _ALL_LAZY.lazily
__version__ = '23.01.18'


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
    return ((_DOT_('lazily', _all_imports.__name__), _all_missing(_all, _imp)),
            (_DOT_(_pycocoa_, '__all__'),            _all_missing(_imp, _all)))


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


def _lazy_import(name):  # overwritten below
    '''(INTERNAL) Lazily import an attribute by C{name}.
    '''
    raise LazyImportError('unsupported: %s(%s)', _lazy_import.__name__, name)


def _lazy_import2(_package_):  # MCCABE 15
    '''Check for and set up lazy importing.

       @param _package_: The name of the package (C{str}) performing
                         the imports, to help facilitate resolving
                         relative imports.

       @return: 2-Tuple (package, getattr) of the importing package for
                easy reference within itself and the callable to be set
                to `__getattr__`.

       @raise LazyImportError: Lazy import not supported, an import
                               failed or a module name or attribute
                               name is invalid or does not exist.

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
        raise LazyImportError('no %s for Python %s', _DOT_(_package_,
                              _lazy_import2.__name__), _sys.version.split()[0])

    import_module, package, parent = _lazy_init3(_package_)

    imports  = _all_imports()
    packages = (parent, '__main__', _NN_)

    def __getattr__(name):  # __getattr__ only for Python 3.7+
        # only called once for each undefined pycocoa attribute
        if name in imports:
            # importlib.import_module() implicitly sets sub-modules
            # on this module as appropriate for direct imports (see
            # note in the _lazy_import.__doc__ above).
            mod, _, attr = imports[name].partition(_DOT_)
            if mod not in imports:
                raise LazyImportError('no %s %s', 'module', _DOT_(parent, mod))
            imported = import_module(_DOT_(_package_, mod), parent)
            pkg = getattr(imported, '__package__', None)
            if pkg not in packages:
                raise LazyImportError('%s %r' % (_DOT_(mod, '__package__'), pkg))
            # import the module or module attribute
            if attr:
                imported = getattr(imported, attr, _N_A)
            elif name != mod:
                imported = getattr(imported, name, _N_A)
            if imported is _N_A:
                raise LazyImportError('no %s %s', 'attribute', _DOT_(mod, attr or name))

        elif name in ('__all__',):  # XXX '__dir__', '__members__'?
            imported = _ALL_INIT + tuple(imports.keys())
            mod = _NN_
        else:
            raise LazyImportError('no %s %s', 'module or attribute', _DOT_(parent, name))

        setattr(package, name, imported)
        if isLazy > 1:
            z = _NN_
            if mod and mod != name:
                z = _DOT_(' from ', mod)
            if isLazy > 2:
                try:  # see C{_caller3}
                    _, f, s = _caller3(2)
                    z = '%s by %s line %d' % (z, f, s)
                except ValueError:
                    pass
            print('# lazily imported %s%s' % (_DOT_(parent, name), z))

        return imported  # __getattr__

    global _lazy_import  # for .utils._Types.__getattribute__
    _lazy_import = __getattr__

    return package, __getattr__  # _lazy_import2


def _lazy_init3(_package_):
    '''(INTERNAL) Try to initialize lazy import.

       @arg _package_: The name of the package (C{str}) performing
                       the imports, to help facilitate resolving
                       relative imports, usually C{__package__}.

       @return: 3-Tuple C{(import_module, package, parent)} of module
                C{importlib.import_module}, the importing C{package}
                for easy reference within itself and the package name,
                aka the C{parent}.

       @raise LazyImportError: Lazy import not supported or not enabled,
                               an import failed or the package name is
                               invalid or does not exist.

       @note: Global C{isLazy} is set accordingly.
    '''
    global isLazy

    if _package_ != _pycocoa_:
        raise LazyImportError('%s: %r, not %r', 'package', _package_, _pycocoa_)

    z = _environ.get('PYCOCOA_LAZY_IMPORT', None)
    if z is None:  # PYCOCOA_LAZY_IMPORT not set
        isLazy = 1  # on by default on 3.7
    else:
        z = z.strip()  # like PYTHONVERBOSE et.al.
        isLazy = int(z) if z.isdigit() else (1 if z else 0)
    if isLazy < 1:  # not enabled
        raise LazyImportError('env %s=%r', 'PYCOCOA_LAZY_IMPORT', z)
    if _environ.get('PYTHONVERBOSE', None):
        isLazy += 1

    try:  # to initialize in Python 3+
        from importlib import import_module

        package = import_module(_package_)
        parent = package.__spec__.parent  # __spec__ only in Python 3.7+
        if parent != _package_:  # assertion
            raise AttributeError('parent %r vs %r' % (parent, _package_))

    except (AttributeError, ImportError) as x:
        isLazy = False  # failed
        raise LazyImportError('init failed: %s', str(x))

    return import_module, package, parent


class _Str(str):
    '''(INTERNAL) Callable C{_Str(*args)} == C{_Str.join(map(str, args))}.
    '''
    def __call__(self, *args):
        '''Join C{args} as C{self.join(args)}.
        '''
        return self.join(map(str, args))

_bNN_        = b''        # PYCHOK bytes(_NN_)
_COLON_      = _Str(':')  # PYCHOK expected
_COMMASPACE_ = _Str(', ')
_DOT_        = _Str('.')
_EQUALS_     = _Str('=')  # PYCHOK expected
_NN_         = _Str('')   # empty string, I{Nomen Nescio}
_SPACE_      = _Str(' ')  # PYCHOK expected
_UNDER_      = _Str('_')

if __name__ == '__main__':

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
        if n in _ALL_LAZY or getattr(m, '__package__', None) == _pycocoa_:
            print('pre-loaded %s: %s?' % (n, getattr(m, '__file__', '?')))

# % python3 -m pycocoa.lazily
#
# /Library/.../python3.11/runpy.py:126: RuntimeWarning: ...
#   warn(RuntimeWarning(msg))
# pre-loaded __main__: .../PyCocoa/pycocoa/lazily.py?
# pre-loaded pycocoa.lazily: .../PyCocoa/pycocoa/lazily.py?
# pre-loaded pycocoa: .../PyCocoa/pycocoa/__init__.py?

# MIT License <https://OpenSource.org/licenses/MIT>
#
# Copyright (C) 2018-2023 -- mrJean1 at Gmail -- All Rights Reserved.
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
