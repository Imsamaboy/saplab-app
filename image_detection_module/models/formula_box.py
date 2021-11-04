#!/usr/bin/python
# -*- coding: utf-8 -*-

from image_detection_module.models.abstract_box import AbstractBox


class FormulaBox:
    def __init__(self):
        self.original_formula_image_box = None
        self.coords = None
        self.height = None
        self.width = None
        self.position_in_line_box = None


if __name__ == "__main__":
    f = FormulaBox()
    f.get_height()
