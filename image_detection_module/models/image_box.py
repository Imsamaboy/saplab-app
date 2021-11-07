#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import cv2 as cv
from typing import List
import zope.interface

from image_detection_module.models.box_functions import BoxFunctions
from utils.utils import get_dilated_image, get_thresholded_and_binarized_image, get_gray_image


class ImageBox(BoxFunctions):

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
        self.gray_image_box = get_gray_image(self.original_image_box)
        self.thresholded_and_binarized_image_box = get_thresholded_and_binarized_image(self.gray_image_box)
        self.dilated_image_box = get_dilated_image(self.thresholded_and_binarized_image_box)
        self.laplacian_image_box = None
        self.x_density = self._find_x_density(self.thresholded_and_binarized_image_box)
        self.y_density = self._find_y_density(self.thresholded_and_binarized_image_box)
        self.general_density = self._find_general_density(self.thresholded_and_binarized_image_box)
        self.position_of_the_equals_sign = None
        self.type = None
        self.line_boxes = None

    def get_general_density(self) -> float:
        """
        :return: getter
        """
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

    def set_line_boxes(self, line_boxes: List):
        """
        :param line_boxes:
        :return:
        """
        self.line_boxes = line_boxes

    def get_line_boxes(self):
        """
        :return:
        """
        return self.line_boxes

    def __str__(self):
        return str({
            "original_image_box": self.original_image_box,
            "coords": self.coords,
            "height": self.height,
            "width": self.width,
            "number_of_image_box": self.number_of_image_box,
            # "thresholded_and_binarized_image_box": self.thresholded_and_binarized_image_box,
            "general_density": self.general_density,
            "type": self.type,
            "line_boxes": self.line_boxes
        })
