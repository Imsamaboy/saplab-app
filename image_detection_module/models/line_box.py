#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np

from image_detection_module.models import abstract_box


class LineBox:
    def __init__(self, original_image_box: np.ndarray):
        self.original_line_image_box = original_image_box
        self.line_number = None
        self.word_boxes = None
        self.position_in_image_box = None

    def split_line_box_into_words(self, ):
        # Использовать фильтр Лапласа при делении на слова
        pass
