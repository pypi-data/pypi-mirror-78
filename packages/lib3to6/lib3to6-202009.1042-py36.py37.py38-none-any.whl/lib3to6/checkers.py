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
from . import utils
from . import common
from . import checker_base as cb
from .checkers_backports import NoUnusableImportsChecker


class NoStarImports(cb.CheckerBase):

    def __call__(self, ctx, tree):
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            for alias in node.names:
                if alias.name == '*':
                    raise common.CheckError('Prohibited from {0} import *.'
                        .format(node.module), node)


def _iter_scope_names(tree):
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            yield node.name, node
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            yield node.id, node
        elif isinstance(node, (ast.ImportFrom, ast.Import)):
            for alias in node.names:
                name = alias.name if alias.asname is None else alias.asname
                yield name, node
        elif isinstance(node, ast.arg):
            yield node.arg, node


class NoOverriddenFixerImportsChecker(cb.CheckerBase):
    """Don't override names that fixers may reference."""
    prohibited_import_overrides = {'itertools', 'six', 'builtins'}

    def __call__(self, ctx, tree):
        for name_in_scope, node in _iter_scope_names(tree):
            is_fixer_import = isinstance(node, ast.Import) and len(node.names
                ) == 1 and node.names[0].asname is None and node.names[0
                ].name == name_in_scope
            if is_fixer_import:
                continue
            if name_in_scope in self.prohibited_import_overrides:
                msg = "Prohibited override of import '{0}'".format(
                    name_in_scope)
                raise common.CheckError(msg, node)


class NoOverriddenBuiltinsChecker(cb.CheckerBase):
    """Don't override names that fixers may reference."""

    def __call__(self, ctx, tree):
        for name_in_scope, node in _iter_scope_names(tree):
            if name_in_scope in common.BUILTIN_NAMES:
                msg = "Prohibited override of builtin '{0}'".format(
                    name_in_scope)
                raise common.CheckError(msg, node)


PROHIBITED_OPEN_ARGUMENTS = {'encoding', 'errors', 'newline', 'closefd',
    'opener'}


class NoOpenWithEncodingChecker(cb.CheckerBase):
    version_info = common.VersionInfo(apply_until='2.7')

    def __call__(self, ctx, tree):
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func_node = node.func
            if not isinstance(func_node, ast.Name):
                continue
            if func_node.id != 'open' or not isinstance(func_node.ctx, ast.Load
                ):
                continue
            mode = 'r'
            if len(node.args) >= 2:
                mode_node = node.args[1]
                if not isinstance(mode_node, ast.Str):
                    msg = (
                        "Prohibited value for argument 'mode' of builtin.open. "
                         + 'Expected ast.Str node, got: {0}'.format(mode_node))
                    raise common.CheckError(msg, node)
                mode = mode_node.s
            if len(node.args) > 3:
                raise common.CheckError(
                    'Prohibited positional arguments to builtin.open', node)
            for keyword in node.keywords:
                if keyword.arg in PROHIBITED_OPEN_ARGUMENTS:
                    msg = ("Prohibited keyword argument '{0}' to builtin.open."
                        .format(keyword.arg))
                    raise common.CheckError(msg, node)
                if keyword.arg != 'mode':
                    continue
                mode_node = keyword.value
                if not isinstance(mode_node, ast.Str):
                    msg = (
                        "Prohibited value for argument 'mode' of builtin.open. "
                         + 'Expected ast.Str node, got: {0}'.format(mode_node))
                    raise common.CheckError(msg, node)
                mode = mode_node.s
            if 'b' not in mode:
                msg = (
                    "Prohibited value '{0}' for argument 'mode' of builtin.open. "
                    .format(mode) +
                    'Only binary modes are allowed, use io.open as an alternative.'
                    )
                raise common.CheckError(msg, node)


class NoAsyncAwait(cb.CheckerBase):
    version_info = common.VersionInfo(apply_until='3.4', works_since='3.5')

    def __call__(self, ctx, tree):
        async_await_node_types = (ast.AsyncFor, ast.AsyncWith, ast.
            AsyncFunctionDef, ast.Await)
        for node in ast.walk(tree):
            if not isinstance(node, async_await_node_types):
                continue
            if isinstance(node, ast.AsyncFor):
                keywords = 'async for'
            elif isinstance(node, ast.AsyncWith):
                keywords = 'async with'
            elif isinstance(node, ast.AsyncFunctionDef):
                keywords = 'async def'
            elif isinstance(node, ast.Await):
                keywords = 'await'
            else:
                keywords = 'async/await'
            msg = (
                "Prohibited use of '{0}', which is not supported for target_version='{1}'."
                .format(keywords, ctx.cfg.target_version))
            raise common.CheckError(msg, node)


class NoYieldFromChecker(cb.CheckerBase):
    version_info = common.VersionInfo(apply_until='3.2', works_since='3.3')

    def __call__(self, ctx, tree):
        for node in ast.walk(tree):
            if isinstance(node, ast.YieldFrom):
                msg = (
                    "Prohibited use of 'yield from', which is not supported for your target_version={0}"
                    .format(ctx.cfg.target_version))
                raise common.CheckError(msg, node)


class NoMatMultOpChecker(cb.CheckerBase):
    version_info = common.VersionInfo(apply_until='3.4', works_since='3.5')

    def __call__(self, ctx, tree):
        if not hasattr(ast, 'MatMult'):
            return
        for node in ast.walk(tree):
            if not isinstance(node, ast.BinOp):
                continue
            if not isinstance(node.op, ast.MatMult):
                continue
            msg = "Prohibited use of matrix multiplication '@' operator."
            raise common.CheckError(msg, node)


def _raise_if_complex_named_tuple(node):
    for subnode in node.body:
        if isinstance(subnode, ast.Expr) and isinstance(subnode.value, ast.Str
            ):
            continue
        if isinstance(subnode, ast.AnnAssign):
            if subnode.value:
                tgt = subnode.target
                assert isinstance(tgt, ast.Name)
                msg = ('Prohibited use of default value ' +
                    "for field '{0}' of class '{1}'".format(tgt.id, node.name))
                raise common.CheckError(msg, subnode, node)
        elif isinstance(subnode, ast.FunctionDef):
            msg = ('Prohibited definition of method ' +
                "'{0}' for class '{1}'".format(subnode.name, node.name))
            raise common.CheckError(msg, subnode, node)
        else:
            msg = 'Unexpected subnode defined for class {0}: {1}'.format(node
                .name, subnode)
            raise common.CheckError(msg, subnode, node)


class NoComplexNamedTuple(cb.CheckerBase):
    version_info = common.VersionInfo(apply_until='3.4', works_since='3.5')

    def __call__(self, ctx, tree):
        _typing_module_name = None
        _namedtuple_class_name = 'NamedTuple'
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == 'typing':
                        _typing_module_name = (alias.name if alias.asname is
                            None else alias.asname)
                continue
            if isinstance(node, ast.ImportFrom) and node.module == 'typing':
                for alias in node.names:
                    if alias.name == 'NamedTuple':
                        _namedtuple_class_name = (alias.name if alias.
                            asname is None else alias.asname)
                continue
            is_namedtuple_class = isinstance(node, ast.ClassDef) and (
                _typing_module_name or _namedtuple_class_name
                ) and utils.has_base_class(node, _typing_module_name,
                _namedtuple_class_name)
            if is_namedtuple_class:
                assert isinstance(node, ast.ClassDef
                    ), 'mypy is stupid sometimes'
                _raise_if_complex_named_tuple(node)


__all__ = ['NoStarImports', 'NoOverriddenFixerImportsChecker',
    'NoOverriddenBuiltinsChecker', 'NoOpenWithEncodingChecker',
    'NoAsyncAwait', 'NoComplexNamedTuple', 'NoUnusableImportsChecker',
    'NoYieldFromChecker', 'NoMatMultOpChecker']
