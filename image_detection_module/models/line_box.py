#!/usr/bin/python
# -*- coding: utf-8 -*-
from typing import List

import numpy as np

from image_detection_module.models.box_functions import BoxFunctions
from models.word_box import WordBox
from utils.utils import get_gray_image, get_thresholded_and_binarized_image, get_dilated_image, get_laplacian_image


class LineBox(BoxFunctions):
    def __init__(self, original_line_image_box: np.ndarray, coords: tuple, line_number: int):
        """
        :param original_line_image_box: original LineBox image
        """
        self.original_line_image_box = original_line_image_box
        self.coords = coords
        self.height = self.original_line_image_box.shape[0]
        self.width = self.original_line_image_box.shape[1]
        self.line_number = line_number
        self.thresholded_and_binarized_line_image_box = get_thresholded_and_binarized_image(self.original_line_image_box)
        self.dilated_line_image_box = get_dilated_image(self.thresholded_and_binarized_line_image_box, dilation=(2, 3))
        self.laplacian_line_image_box = get_laplacian_image(self.dilated_line_image_box)
        self.x_density = self._find_x_density(self.thresholded_and_binarized_line_image_box)
        self.y_density = self._find_y_density(self.thresholded_and_binarized_line_image_box)
        self.general_density = self._find_general_density(self.thresholded_and_binarized_line_image_box)
        self.words = self.find_words_in_image_box()
        self.position_of_the_equals_sign = None
        self.word_boxes = []

    def find_words_in_image_box(self, ) -> List:
        """
        This function searches words by spaces in image
        :return: list of indices, where are words
        """
        laplacian_x_density = self._find_x_density(self.laplacian_line_image_box)
        words = []
        is_local_first, is_local_last = True, False
        begin, end = 0, 0
        # Находим индексы слов (begin - начало слова, end - конец слова)
        for index, density in enumerate(laplacian_x_density):
            if density != 0 and is_local_first:
                begin = index
                is_local_first, is_local_last = False, True
            if density == 0 and is_local_last:
                end = index
                result = (begin, end - 1) if end - begin > 0 else (begin, end)
                words.append(result)
                is_local_first, is_local_last = True, False
        # Добавляем последнее слово
        words.append((begin, len(laplacian_x_density)))
        return words

    def split_line_box_into_words(self, ):
        """
        This function creates WordBoxes
        :return: None
        """
        self.word_boxes = [WordBox(self.original_line_image_box[:, list(range(word[0], word[1]))],
                                   coords=(self.coords[0],
                                           self.coords[1],
                                           self.coords[2] + word[0],
                                           self.coords[2] + word[1],
                                           ),
                                   line_number=self.line_number,
                                   position_in_line=position)
                           for position, word in enumerate(self.words)]
