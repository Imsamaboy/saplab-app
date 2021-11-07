#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np

from image_detection_module.models.box_functions import BoxFunctions


class UnitBox(BoxFunctions):
    def __init__(self, original_unit_image_box: np.ndarray, coords: tuple, position_in_word: int):
        self.original_unit_image_box = original_unit_image_box
        self.coords = coords
        self.height = self.original_unit_image_box.shape[0]
        self.width = self.original_unit_image_box.shape[1]
        self.position_in_word_box_or_in_formula_box = position_in_word

    def __str__(self):
        return str({
            "original_image_box": self.original_unit_image_box,
            "coords": self.coords,
            "height": self.height,
            "width": self.width,
            "position_in_word_box_or_in_formula_box": self.position_in_word_box_or_in_formula_box,
        })
