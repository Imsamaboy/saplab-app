#!/usr/bin/python
# -*- coding: utf-8 -*-

from models.AbstractBox import AbstractBox


class UnitBox(AbstractBox):
    def __init__(self):
        self.original_unit_image_box = None
        self.position_in_word_box_or_in_formula_box = None
        self.Attribute3 = None
        self.Attribute4 = None
        self.Attribute5 = None
        self.Attribute6 = None
