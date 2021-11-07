#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np

from image_detection_module.models.box_functions import BoxFunctions
from models.unit_box import UnitBox
from utils.utils import get_gray_image, get_thresholded_and_binarized_image, \
    get_dilated_image, get_laplacian_image, \
    merge_intervals


class WordBox(BoxFunctions):
    def __init__(self, original_word_image_box: np.ndarray, coords: tuple, line_number: int, position_in_line: int):
        """
        :param original_word_image_box:
        Изображение может содержать помимо слова знаки препинания ,.-? и др
        """
        self.original_word_image_box = original_word_image_box
        self.coords = coords
        self.height = self.original_word_image_box.shape[0]
        self.width = self.original_word_image_box.shape[1]
        self.line_number = line_number
        self.position_in_line_box = position_in_line
        self.thresholded_and_binarized_word_image_box = get_thresholded_and_binarized_image(self.original_word_image_box)
        self.dilated_word_image_box = get_dilated_image(self.thresholded_and_binarized_word_image_box, dilation=(2, 3))
        self.laplacian_word_image_box = get_laplacian_image(self.thresholded_and_binarized_word_image_box)
        self.x_density = self._find_x_density(self.thresholded_and_binarized_word_image_box)
        self.y_density = self._find_y_density(self.thresholded_and_binarized_word_image_box)
        self.general_density = self._find_general_density(self.thresholded_and_binarized_word_image_box)
        self.units = self.find_units_into_word()
        self.unit_boxes = []

    def find_units_into_word(self, ):
        """
        This function searches words by spaces in image
        :return: list of indices, where are words
        """
        units = []
        is_local_first, is_local_last = True, False
        begin, end = 0, 0
        # Находим индексы Unit's (begin - начало слова, end - конец слова)
        for index, density in enumerate(self.x_density):
            if density != 0 and is_local_first:
                begin = index
                is_local_first, is_local_last = False, True
            if density == 0 and is_local_last:
                end = index
                result = [begin, end - 1] if end - begin > 0 else [begin, end]
                units.append(result)
                is_local_first, is_local_last = True, False
        # Добавляем последний Unit
        units.append([begin, len(self.x_density)])
        # Сливаем пересекающиеся интервалы, если такие есть
        merged_units = merge_intervals(units)
        return merged_units

    def split_word_box_into_units(self, ):
        """
        Функция делит слово по пробелам на Unit'ы
        :return:
        """
        # TODO: сделать обрезание ненужных пикслей послабее!
        # IMPORTANT: если знак ;:=, то обрезание лишних пикслей работает неправильно!
        for position, unit in enumerate(self.units):
            unit_picture = self.thresholded_and_binarized_word_image_box[:, list(range(unit[0], unit[1]))]
            numbers = []
            # Очистка от ненужных пикселей
            for number, row in enumerate(unit_picture):
                if unit_picture.shape[1] - np.count_nonzero(row) != unit_picture.shape[1]:
                    numbers.append(number)
            # Добавим сверху один пиксель, чтобы не обрезались нужные детали
            numbers.append(numbers[0] - 1)
            numbers.sort()
            # Создаем изображение без лишних пикселей
            cleaned_unit_picture = self.thresholded_and_binarized_word_image_box[numbers, unit[0]:unit[1]]
            # Добавляем в unit_boxes
            self.unit_boxes.append(UnitBox(cleaned_unit_picture,
                                           coords=(self.coords[0] + numbers[0],
                                                   self.coords[0] + numbers[-1],
                                                   self.coords[2] + unit[0],
                                                   self.coords[2] + unit[1]
                                                   ),
                                           position_in_word=position))


    def __str__(self):
        return str({
            "original_word_image_box": self.original_word_image_box,
            "coords": self.coords,
            "height": self.height,
            "width": self.width,
            "position_in_line_box": self.position_in_line_box,
            "general_density": self.general_density,
            "unit_boxes": self.unit_boxes
        })
