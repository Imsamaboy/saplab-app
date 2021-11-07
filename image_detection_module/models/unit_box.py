#!/usr/bin/python
# -*- coding: utf-8 -*-

from image_detection_module.models.box_functions import BoxFunctions


class UnitBox(BoxFunctions):
    def __init__(self, original_unit_image_box, coords: tuple, position_in_word: int):
        self.original_unit_image_box = original_unit_image_box
        self.coords = coords
        self.position_in_word_box_or_in_formula_box = position_in_word
