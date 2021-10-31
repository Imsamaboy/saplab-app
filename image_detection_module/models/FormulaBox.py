#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import AbstractBox


class FormulaBox(AbstractBox):
    def __init__(self):
        self.original_formula_image_box = None
        self.coords = None
        self.height = None
        self.width = None
        self.position_in_line_box = None
