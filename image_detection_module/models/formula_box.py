#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np

from image_detection_module.models.box_functions import BoxFunctions


class FormulaBox(BoxFunctions):
    def __init__(self, original_formula_image_box: np.ndarray):
        self.original_formula_image_box = original_formula_image_box
        self.coords = None
        self.height = self.original_formula_image_box.shape[0]
        self.width = self.original_formula_image_box.shape[1]
        self.position_in_line_box = None


if __name__ == "__main__":
    pass
