# -*- coding: utf-8 -*-
# This file is part of the lib3to6 project
# https://gitlab.com/mbarkhau/lib3to6
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import ast
import typing as typ
try:
    import builtins
except ImportError:
    import __builtin__ as builtins
str = getattr(builtins, 'unicode', str)
PackageName = str
PackageDirectory = str
PackageDir = typ.Dict[PackageName, PackageDirectory]
InstallRequires = typ.Optional[typ.Set[str]]
ConstantNodeTypes = ast.Constant,
if hasattr(ast, 'Num'):
    ConstantNodeTypes += (ast.Num, ast.Str, ast.Bytes, ast.NameConstant,
        ast.Ellipsis)
LeafNodeTypes = ConstantNodeTypes + (ast.Name, ast.cmpop, ast.boolop, ast.
    operator, ast.unaryop, ast.expr_context)
ContainerNodes = ast.List, ast.Set, ast.Tuple
BuildConfig = typ.NamedTuple('BuildConfig', [('target_version', str), (
    'cache_enabled', bool), ('default_mode', str), ('fixers', str), (
    'checkers', str), ('install_requires', InstallRequires)])
BuildContext = typ.NamedTuple('BuildContext', [('cfg', BuildConfig), (
    'filepath', str)])


def init_build_context(target_version='2.7', cache_enabled=True,
    default_mode='enabled', fixers='', checkers='', install_requires=None,
    filepath='<filepath>'):
    cfg = BuildConfig(target_version=target_version, cache_enabled=
        cache_enabled, default_mode=default_mode, fixers=fixers, checkers=
        checkers, install_requires=install_requires)
    return BuildContext(cfg=cfg, filepath=filepath)


class InvalidPackage(Exception):
    pass


def get_node_lineno(node=None, parent=None):
    if isinstance(node, (ast.stmt, ast.expr)):
        return node.lineno
    if isinstance(parent, (ast.stmt, ast.expr)):
        return parent.lineno
    return -1


class CheckError(Exception):
    lineno = None

    def __init__(self, msg, node=None, parent=None):
        self.lineno = get_node_lineno(node, parent)
        super(CheckError, self).__init__(msg)


class FixerError(Exception):
    msg = None
    node = None
    module = None

    def __init__(self, msg, node, module=None):
        self.msg = msg
        self.node = node
        self.module = module
        super(FixerError, self).__init__(msg)


class VersionInfo(object):
    """Compatibility info for Fixer and Checker classes.

    Used as a class attribute (not an instance attribute) of a fixer or checker.
    The compatability info relates to the fixer/checker rather than the feature
    it deals with. The question that is being ansered is: "should this
    fixer/checker be exectued for this (src_version, tgt_version) pair"
    """
    apply_since = None
    apply_until = None
    works_since = None
    works_until = None

    def __init__(self, apply_since='1.0', apply_until=None, works_since=
        None, works_until=None):
        self.apply_since = [int(part) for part in apply_since.split('.')]
        if apply_until is None:
            self.apply_until = None
        else:
            self.apply_until = [int(part) for part in apply_until.split('.')]
        if works_since is None:
            self.works_since = self.apply_since
        else:
            self.works_since = [int(part) for part in works_since.split('.')]
        if works_until is None:
            self.works_until = None
        else:
            self.works_until = [int(part) for part in works_until.split('.')]

    def is_required_for(self, version):
        version_num = [int(part) for part in version.split('.')]
        apply_until = self.apply_until
        if apply_until and apply_until < version_num:
            return False
        return self.apply_since <= version_num

    def is_compatible_with(self, version):
        version_num = [int(part) for part in version.split('.')]
        works_since = self.works_since
        works_until = self.works_until
        if works_since and version_num < works_since:
            return False
        if works_until and works_until < version_num:
            return False
        return True

    def is_applicable_to(self, source_version, target_version):
        return self.is_required_for(target_version
            ) and self.is_compatible_with(source_version)


ImportDecl = typ.NamedTuple('ImportDecl', [('module_name', str), (
    'import_name', typ.Optional[str]), ('py2_module_name', typ.Optional[str])])
BUILTIN_NAMES = {'ArithmeticError', 'AssertionError', 'AttributeError',
    'BaseException', 'BlockingIOError', 'BrokenPipeError', 'BufferError',
    'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError',
    'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError',
    'DeprecationWarning', 'EOFError', 'Ellipsis', 'EnvironmentError',
    'Exception', 'False', 'FileExistsError', 'FileNotFoundError',
    'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError',
    'ImportError', 'ImportWarning', 'IndentationError', 'IndexError',
    'InterruptedError', 'IsADirectoryError', 'KeyError',
    'KeyboardInterrupt', 'LookupError', 'MemoryError',
    'ModuleNotFoundError', 'NameError', 'None', 'NotADirectoryError',
    'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError',
    'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError',
    'RecursionError', 'ReferenceError', 'ResourceWarning', 'RuntimeError',
    'RuntimeWarning', 'StopAsyncIteration', 'StopIteration', 'SyntaxError',
    'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError',
    'TimeoutError', 'True', 'TypeError', 'UnboundLocalError',
    'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError',
    'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError',
    'Warning', 'ZeroDivisionError', 'abs', 'all', 'any', 'ascii', 'bin',
    'bool', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod',
    'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir',
    'display', 'divmod', 'enumerate', 'eval', 'exec', 'filter', 'float',
    'format', 'frozenset', 'get_ipython', 'getattr', 'globals', 'hasattr',
    'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass',
    'iter', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview',
    'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print',
    'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr',
    'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple',
    'type', 'vars', 'zip', 'StandardError', 'apply', 'basestring', 'buffer',
    'cmp', 'coerce', 'dreload', 'execfile', 'file', 'intern', 'long',
    'raw_input', 'reduce', 'reload', 'unichr', 'unicode', 'xrange'}
BUILTIN_NAMES.update([name for name in dir(builtins) if not name.startswith
    ('__')])
