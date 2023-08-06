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
from . import common


class FixerBase(object):
    version_info = None
    required_imports = None
    module_declarations = None

    def __init__(self):
        self.required_imports = set()
        self.module_declarations = set()

    def __call__(self, ctx, tree):
        raise NotImplementedError()


class TransformerFixerBase(FixerBase, ast.NodeTransformer):

    def __call__(self, ctx, tree):
        try:
            new_tree = self.visit(tree)
            return typ.cast(ast.Module, new_tree)
        except common.FixerError as ex:
            if ex.module is None:
                ex.module = tree
            raise
