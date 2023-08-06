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
import sys
try:
    import builtins
except ImportError:
    import __builtin__ as builtins
import itertools
import typing as typ
range = getattr(builtins, 'xrange', range)
zip = getattr(itertools, 'izip', zip)
from . import utils
from . import common
from . import fixer_base as fb
from .fixers_future import DivisionFutureFixer
from .fixers_future import GeneratorsFutureFixer
from .fixers_future import AnnotationsFutureFixer
from .fixers_future import NestedScopesFutureFixer
from .fixers_future import GeneratorStopFutureFixer
from .fixers_future import PrintFunctionFutureFixer
from .fixers_future import WithStatementFutureFixer
from .fixers_future import AbsoluteImportFutureFixer
from .fixers_future import UnicodeLiteralsFutureFixer
from .fixers_future import RemoveUnsupportedFuturesFixer
from .fixers_builtin_rename import UnichrToChrFixer
from .fixers_builtin_rename import UnicodeToStrFixer
from .fixers_builtin_rename import XrangeToRangeFixer
from .fixers_builtin_rename import RawInputToInputFixer
from .fixers_import_fallback import QueueImportFallbackFixer
from .fixers_import_fallback import DbmGnuImportFallbackFixer
from .fixers_import_fallback import PickleImportFallbackFixer
from .fixers_import_fallback import ThreadImportFallbackFixer
from .fixers_import_fallback import WinRegImportFallbackFixer
from .fixers_import_fallback import CopyRegImportFallbackFixer
from .fixers_import_fallback import ReprLibImportFallbackFixer
from .fixers_import_fallback import TkinterImportFallbackFixer
from .fixers_import_fallback import BuiltinsImportFallbackFixer
from .fixers_import_fallback import HtmlParserImportFallbackFixer
from .fixers_import_fallback import HttpClientImportFallbackFixer
from .fixers_import_fallback import TkinterDndImportFallbackFixer
from .fixers_import_fallback import TkinterTixImportFallbackFixer
from .fixers_import_fallback import TkinterTtkImportFallbackFixer
from .fixers_import_fallback import DummyThreadImportFallbackFixer
from .fixers_import_fallback import HttpCookiesImportFallbackFixer
from .fixers_import_fallback import TkinterFontImportFallbackFixer
from .fixers_import_fallback import UrllibErrorImportFallbackFixer
from .fixers_import_fallback import UrllibParseImportFallbackFixer
from .fixers_import_fallback import ConfigParserImportFallbackFixer
from .fixers_import_fallback import SocketServerImportFallbackFixer
from .fixers_import_fallback import XMLRPCClientImportFallbackFixer
from .fixers_import_fallback import XmlrpcServerImportFallbackFixer
from .fixers_import_fallback import EmailMimeBaseImportFallbackFixer
from .fixers_import_fallback import EmailMimeTextImportFallbackFixer
from .fixers_import_fallback import HttpCookiejarImportFallbackFixer
from .fixers_import_fallback import TkinterDialogImportFallbackFixer
from .fixers_import_fallback import UrllibRequestImportFallbackFixer
from .fixers_import_fallback import EmailMimeImageImportFallbackFixer
from .fixers_import_fallback import TkinterConstantsImportFallbackFixer
from .fixers_import_fallback import TkinterMessageboxImportFallbackFixer
from .fixers_import_fallback import UrllibRobotParserImportFallbackFixer
from .fixers_import_fallback import EmailMimeMultipartImportFallbackFixer
from .fixers_import_fallback import TkinterColorchooserImportFallbackFixer
from .fixers_import_fallback import TkinterCommonDialogImportFallbackFixer
from .fixers_import_fallback import TkinterScrolledTextImportFallbackFixer
from .fixers_import_fallback import EmailMimeNonmultipartImportFallbackFixer
from .fixers_unpacking_generalization import UnpackingGeneralizationsFixer
AstStr = getattr(ast, 'Str', ast.Constant)


def is_const_node(node):
    return node is None or any(isinstance(node, cntype) for cntype in
        common.ConstantNodeTypes)


Elt = typ.Union[ast.Name, ast.Constant, ast.Subscript]
Elts = typ.List[Elt]
AnnoNode = typ.Union[ast.arg, ast.AnnAssign, ast.FunctionDef]


class _FRAFContext(object):
    local_classes = None
    known_classes = None

    def __init__(self, local_classes):
        self.local_classes = local_classes
        self.known_classes = set()

    def is_forward_ref(self, name):
        return name in self.local_classes and name not in self.known_classes

    def update_index_elts(self, elts):
        for i in range(len(elts)):
            elt = elts[i]
            if is_const_node(elt) or isinstance(elt, ast.Attribute):
                continue
            if isinstance(elt, ast.Name):
                if self.is_forward_ref(elt.id):
                    elts[i] = ast.Constant(elt.id)
            elif isinstance(elt, ast.Subscript):
                idx = elt.slice
                assert isinstance(idx, ast.Index)
                self.update_index(idx)
            else:
                msg = (
                    'Error fixing index element with forward ref of type {0}'
                    .format(type(elt)))
                raise NotImplementedError(msg)

    def update_index(self, idx):
        val = idx.value
        if is_const_node(val) or isinstance(val, ast.Attribute):
            return
        if isinstance(val, ast.Name):
            if self.is_forward_ref(val.id):
                idx.value = AstStr(val.id)
        elif isinstance(val, ast.Subscript):
            sub_idx = val.slice
            assert isinstance(sub_idx, ast.Index)
            self.update_index(sub_idx)
        elif isinstance(val, ast.Tuple):
            elts = typ.cast(Elts, val.elts)
            self.update_index_elts(elts)
        else:
            msg = 'Error fixing index with forward ref of type {0}'.format(type
                (val))
            raise NotImplementedError(msg)

    def update_annotation_refs(self, node, attrname):
        anno = getattr(node, attrname)
        if is_const_node(anno) or isinstance(anno, ast.Attribute):
            return
        if isinstance(anno, ast.Name):
            if self.is_forward_ref(anno.id):
                setattr(node, attrname, AstStr(anno.id))
        elif isinstance(anno, ast.Subscript):
            idx = anno.slice
            assert isinstance(idx, ast.Index)
            self.update_index(idx)
        else:
            msg = ('Error fixing annotation of forward ref with type {0}'.
                format(type(anno)))
            raise NotImplementedError(msg)

    def remove_forward_references(self, node):
        for sub_node in ast.iter_child_nodes(node):
            if isinstance(sub_node, ast.FunctionDef):
                self.update_annotation_refs(sub_node, 'returns')
                for arg in sub_node.args.args:
                    self.update_annotation_refs(arg, 'annotation')
                for arg in sub_node.args.kwonlyargs:
                    self.update_annotation_refs(arg, 'annotation')
                kwarg = sub_node.args.kwarg
                if kwarg:
                    self.update_annotation_refs(kwarg, 'annotation')
                vararg = sub_node.args.vararg
                if vararg:
                    self.update_annotation_refs(vararg, 'annotation')
            elif isinstance(sub_node, ast.AnnAssign):
                self.update_annotation_refs(sub_node, 'annotation')
            if hasattr(sub_node, 'body'):
                self.remove_forward_references(sub_node)
            if isinstance(sub_node, ast.ClassDef):
                self.known_classes.add(sub_node.name)


class ForwardReferenceAnnotationsFixer(fb.FixerBase):
    version_info = common.VersionInfo(apply_since='3.0', apply_until='3.6')

    def __call__(self, ctx, tree):
        local_classes = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                local_classes.add(node.name)
        _FRAFContext(local_classes).remove_forward_references(tree)
        return tree


class RemoveFunctionDefAnnotationsFixer(fb.FixerBase):
    version_info = common.VersionInfo(apply_since='1.0', apply_until='2.7')

    def __call__(self, ctx, tree):
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                node.returns = None
                for arg in node.args.args:
                    arg.annotation = None
                for arg in node.args.kwonlyargs:
                    arg.annotation = None
                if node.args.kwarg:
                    node.args.kwarg.annotation = None
                if node.args.vararg:
                    node.args.vararg.annotation = None
        return tree


class RemoveAnnAssignFixer(fb.TransformerFixerBase):
    version_info = common.VersionInfo(apply_since='1.0', apply_until='3.5')

    @staticmethod
    def visit_AnnAssign(node):
        tgt_node = node.target
        if not isinstance(tgt_node, (ast.Name, ast.Attribute)):
            raise common.FixerError('Unexpected Node type', tgt_node)
        value = None
        if node.value is None:
            value = ast.NameConstant(value=None)
        else:
            value = node.value
        return ast.Assign(targets=[tgt_node], value=value)


class ShortToLongFormSuperFixer(fb.TransformerFixerBase):
    version_info = common.VersionInfo(apply_since='2.2', apply_until='2.7')

    @staticmethod
    def visit_ClassDef(node):
        for maybe_method in ast.walk(node):
            if not isinstance(maybe_method, ast.FunctionDef):
                continue
            method = maybe_method
            method_args = method.args
            if len(method_args.args) == 0:
                continue
            self_arg = method_args.args[0]
            for maybe_super_call in ast.walk(method):
                if not isinstance(maybe_super_call, ast.Call):
                    continue
                func_node = maybe_super_call.func
                if not (isinstance(func_node, ast.Name) and func_node.id ==
                    'super'):
                    continue
                super_call = maybe_super_call
                if len(super_call.args) > 0:
                    continue
                super_call.args = [ast.Name(id=node.name, ctx=ast.Load()),
                    ast.Name(id=self_arg.arg, ctx=ast.Load())]
        return node


class InlineKWOnlyArgsFixer(fb.TransformerFixerBase):
    version_info = common.VersionInfo(apply_since='1.0', apply_until='2.99')

    @staticmethod
    def visit_FunctionDef(node):
        if not node.args.kwonlyargs:
            return node
        if node.args.kwarg:
            kw_name = node.args.kwarg.arg
        else:
            kw_name = 'kwargs'
            node.args.kwarg = ast.arg(arg=kw_name, annotation=None)
        kwonlyargs = reversed(node.args.kwonlyargs)
        kw_defaults = reversed(node.args.kw_defaults)
        for arg, default in zip(kwonlyargs, kw_defaults):
            arg_name = arg.arg
            node_value = None
            if default is None:
                node_value = ast.Subscript(value=ast.Name(id=kw_name, ctx=
                    ast.Load()), slice=ast.Index(value=AstStr(s=arg_name)),
                    ctx=ast.Load())
            elif not isinstance(default, common.ConstantNodeTypes):
                msg = (
                    'Keyword only arguments must be immutable. Found: {0} for {1}'
                    .format(default, arg_name))
                raise common.FixerError(msg, node)
            else:
                node_value = ast.Call(func=ast.Attribute(value=ast.Name(id=
                    kw_name, ctx=ast.Load()), attr='get', ctx=ast.Load()),
                    args=[AstStr(s=arg_name), default], keywords=[])
            new_node = ast.Assign(targets=[ast.Name(id=arg_name, ctx=ast.
                Store())], value=node_value)
            node.body.insert(0, new_node)
        node.args.kwonlyargs = []
        return node


class NewStyleClassesFixer(fb.TransformerFixerBase):
    version_info = common.VersionInfo(apply_since='2.0', apply_until='2.7')

    def visit_ClassDef(self, node):
        self.generic_visit(node)
        if len(node.bases) == 0:
            node.bases.append(ast.Name(id='object', ctx=ast.Load()))
        return node


class ItertoolsBuiltinsFixer(fb.TransformerFixerBase):
    version_info = common.VersionInfo(apply_since='2.3', apply_until='2.7',
        works_until='3.99')

    def __call__(self, ctx, tree):
        new_tree = self.visit(tree)
        return typ.cast(ast.Module, new_tree)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load) and node.id in ('map', 'zip',
            'filter'):
            self.required_imports.add(common.ImportDecl('itertools', None,
                None))
            global_decl = "{0} = getattr(itertools, 'i{1}', {2})".format(node
                .id, node.id, node.id)
            self.module_declarations.add(global_decl)
        return node


class NamedTupleClassToAssignFixer(fb.TransformerFixerBase):
    version_info = common.VersionInfo(apply_since='2.6', apply_until='3.4')
    _typing_module_name = None
    _namedtuple_class_name = None

    def __init__(self):
        self._typing_module_name = None
        self._namedtuple_class_name = None
        super(NamedTupleClassToAssignFixer, self).__init__()

    def visit_ImportFrom(self, node):
        if node.module == 'typing':
            for alias in node.names:
                if alias.name == 'NamedTuple':
                    if alias.asname is None:
                        self._namedtuple_class_name = alias.name
                    else:
                        self._namedtuple_class_name = alias.asname
        return node

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name == 'typing':
                if alias.asname is None:
                    self._typing_module_name = alias.name
                else:
                    self._typing_module_name = alias.asname
        return node

    def visit_ClassDef(self, node):
        self.generic_visit(node)
        if len(node.bases) == 0:
            return node
        if not (self._typing_module_name or self._namedtuple_class_name):
            return node
        has_namedtuple_base = utils.has_base_class(node, self.
            _typing_module_name, self._namedtuple_class_name or 'NamedTuple')
        if not has_namedtuple_base:
            return node
        func = None
        if self._typing_module_name:
            func = ast.Attribute(value=ast.Name(id=self._typing_module_name,
                ctx=ast.Load()), attr='NamedTuple', ctx=ast.Load())
        elif self._namedtuple_class_name:
            func = ast.Name(id=self._namedtuple_class_name, ctx=ast.Load())
        else:
            raise RuntimeError('')
        elts = []
        for assign in node.body:
            if not isinstance(assign, ast.AnnAssign):
                continue
            tgt = assign.target
            if not isinstance(tgt, ast.Name):
                continue
            elts.append(ast.Tuple(elts=[AstStr(s=tgt.id), assign.annotation
                ], ctx=ast.Load()))
        return ast.Assign(targets=[ast.Name(id=node.name, ctx=ast.Store())],
            value=ast.Call(func=func, args=[AstStr(s=node.name), ast.List(
            elts=elts, ctx=ast.Load())], keywords=[]))


if sys.version_info >= (3, 6):
    from .fixers_fstring import FStringToStrFormatFixer
else:
    FStringToStrFormatFixer = None
if sys.version_info >= (3, 8):
    from .fixers_namedexpr import NamedExprFixer
else:
    NamedExprFixer = None
__all__ = ['AnnotationsFutureFixer', 'GeneratorStopFutureFixer',
    'UnicodeLiteralsFutureFixer', 'RemoveUnsupportedFuturesFixer',
    'PrintFunctionFutureFixer', 'WithStatementFutureFixer',
    'AbsoluteImportFutureFixer', 'DivisionFutureFixer',
    'GeneratorsFutureFixer', 'NestedScopesFutureFixer',
    'ConfigParserImportFallbackFixer', 'SocketServerImportFallbackFixer',
    'BuiltinsImportFallbackFixer', 'QueueImportFallbackFixer',
    'CopyRegImportFallbackFixer', 'WinRegImportFallbackFixer',
    'ReprLibImportFallbackFixer', 'ThreadImportFallbackFixer',
    'DummyThreadImportFallbackFixer', 'HttpCookiejarImportFallbackFixer',
    'UrllibParseImportFallbackFixer', 'UrllibRequestImportFallbackFixer',
    'UrllibErrorImportFallbackFixer',
    'UrllibRobotParserImportFallbackFixer',
    'XMLRPCClientImportFallbackFixer', 'XmlrpcServerImportFallbackFixer',
    'HtmlParserImportFallbackFixer', 'HttpClientImportFallbackFixer',
    'HttpCookiesImportFallbackFixer', 'PickleImportFallbackFixer',
    'DbmGnuImportFallbackFixer', 'EmailMimeBaseImportFallbackFixer',
    'EmailMimeImageImportFallbackFixer',
    'EmailMimeMultipartImportFallbackFixer',
    'EmailMimeNonmultipartImportFallbackFixer',
    'EmailMimeTextImportFallbackFixer', 'TkinterImportFallbackFixer',
    'TkinterDialogImportFallbackFixer',
    'TkinterScrolledTextImportFallbackFixer',
    'TkinterTixImportFallbackFixer', 'TkinterTtkImportFallbackFixer',
    'TkinterConstantsImportFallbackFixer', 'TkinterDndImportFallbackFixer',
    'TkinterColorchooserImportFallbackFixer',
    'TkinterCommonDialogImportFallbackFixer',
    'TkinterFontImportFallbackFixer',
    'TkinterMessageboxImportFallbackFixer', 'XrangeToRangeFixer',
    'UnicodeToStrFixer', 'UnichrToChrFixer', 'RawInputToInputFixer',
    'RemoveFunctionDefAnnotationsFixer', 'ForwardReferenceAnnotationsFixer',
    'RemoveAnnAssignFixer', 'ShortToLongFormSuperFixer',
    'InlineKWOnlyArgsFixer', 'NewStyleClassesFixer',
    'ItertoolsBuiltinsFixer', 'UnpackingGeneralizationsFixer',
    'NamedTupleClassToAssignFixer', 'FStringToStrFormatFixer',
    'NamedExprFixer', 'UnpackingGeneralizationsFixer']
