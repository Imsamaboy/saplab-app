#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from typing import List

from image_detection_module.models import abstract_box


class ImageBox:
    def __init__(self, original_image_box: np.ndarray, coords: tuple):
        """
        :param original_image_box:
        :param coords:
        """
        self.original_image_box = original_image_box
        self.coords = coords
        self.height = original_image_box.shape[0]
        self.width = original_image_box.shape[1]
        self.number_of_image_box = None
        self.dilated_image_box = None
        self.laplacian_image_box = None
        self.x_density = self._find_x_density()
        self.y_density = self._find_y_density()
        self.general_density = self._find_general_density()
        self.position_of_the_equals_sign = None
        self.type = None
        self.line_boxes = None

    def _find_x_density(self) -> np.array:
        """
        :return:
        """
        x_density = np.zeros(self.width)
        for column in range(self.width):
            x_density[column] = np.count_nonzero(np.transpose(self.dilated_image_box)[column])
        return x_density

    def _find_y_density(self) -> np.array:
        """
        :return:
        """
        y_density = np.zeros(self.height)
        for row in range(self.height):
            y_density[row] = np.count_nonzero(self.image[row])
        return y_density

    def _find_general_density(self) -> float:
        """
        :return:
        """
        count = 0
        for line in self.dilated_image_box:
            count += np.count_nonzero(line)
        return count / (self.height * self.width)

    def _find_type_of_box(self):
        """
        :return:
        """
        # baseline_height = 10  # pix
        if self.find_general_density() > 0.4:
            return "text"
        else:
            return "not defined"

    def get_general_density(self) -> float:
        return self.general_density

    def set_type(self, type: str):
        """
        :param type:
        :return:
        """
        self.type = type

    def set_position_of_the_equals_sign(self, position: List[int]):
        """
        :param position:
        :return:
        """
        self.position_of_the_equals_sign = position

    def __str__(self):
        return f"Height={self.height}, Width={self.width}"

    def split_image_box_into_lines(self, ):
        pass
