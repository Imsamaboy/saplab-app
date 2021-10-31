#!/usr/bin/python
#-*- coding: utf-8 -*-

from models.AbstractBox import AbstractBox

class WordBox(AbstractBox):
    def __init__(self):
        self.original_word_image_box = None
        self.position_in_line_box = None
        self.unit_boxes = None
        self.Attribute2 = None
        self.Attribute3 = None
        self.Attribute4 = None

    def split_word_box_into_units(self, ):
        pass

