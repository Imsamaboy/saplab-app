#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np

from image_detection_module.models.abstract_box import AbstractBox
from utils.utils import get_gray_image, get_thresholded_and_binarized_image, get_dilated_image


class LineBox:
    def __init__(self, original_line_image_box: np.ndarray):
        self.original_line_image_box = original_line_image_box
        self.line_number = None
        self.gray_line_image_box = get_gray_image(self.original_line_image_box)
        self.thresholded_and_binarized_line_image_box = get_thresholded_and_binarized_image(self.gray_line_image_box)
        self.dilated_line_image_box = get_dilated_image(self.thresholded_and_binarized_line_image_box)
        self.laplacian_image_box = None
        # self.x_density = self._find_x_density()
        # self.y_density = self._find_y_density()
        # self.general_density = self._find_general_density()
        self.position_of_the_equals_sign = None
        self.word_boxes = None
        self.position_in_image_box = None

    def split_line_box_into_words(self, ):
        # Использовать фильтр Лапласа при делении на слова
        pass
