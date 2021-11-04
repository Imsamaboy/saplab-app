#!/usr/bin/python
# -*- coding: utf-8 -*-

from image_detection_module.models import abstract_box


class WordBox(abstract_box):
    def __init__(self):
        self.original_word_image_box = None
        self.position_in_line_box = None
        self.unit_boxes = None

    def split_word_box_into_units(self):
        pass
