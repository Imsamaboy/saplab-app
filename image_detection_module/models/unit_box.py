#!/usr/bin/python
# -*- coding: utf-8 -*-

from image_detection_module.models.abstract_box import AbstractBox


class UnitBox:
    def __init__(self, original_unit_image_box):
        self.original_unit_image_box = original_unit_image_box
        self.position_in_word_box_or_in_formula_box = None
