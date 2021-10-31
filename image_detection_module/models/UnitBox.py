#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import AbstractBox


class UnitBox(AbstractBox):
    def __init__(self, original_unit_image_box):
        self.original_unit_image_box = original_unit_image_box
        self.position_in_word_box_or_in_formula_box = None
