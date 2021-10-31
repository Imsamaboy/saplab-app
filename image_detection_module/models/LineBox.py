#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import AbstractBox


class LineBox(AbstractBox):
    def __init__(self):
        self.original_line_image_box = None
        self.line_number = None
        self.word_boxes = None
        self.position_in_image_box = None

    def split_line_box_into_words(self, ):
        pass
