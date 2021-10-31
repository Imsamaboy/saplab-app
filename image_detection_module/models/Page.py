#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import cv2 as cv
from typing import List

from image_detection_module.utils import compare_contours
from image_detection_module.utils import get_dilated_image


class Page:
    def __init__(self, original_image: np.ndarray):
        self.original_image = original_image
        self.height = original_image.shape[0]
        self.width = original_image.shape[1]
        self.dilated_image = None
        self.page_number = None
        self.image_boxes = None

    def create_latex_page(self, ):
        pass

    def create_image_boxes(self, dilation=(10, 26), binarization_border=(254, 255)) -> List[np.ndarray]:
        gray_image = cv.cvtColor(self.original_image,
                                 cv.COLOR_BGR2GRAY)

        _, inv_bin_image = cv.threshold(gray_image,
                                        binarization_border[0],
                                        binarization_border[1],
                                        cv.THRESH_BINARY_INV)

        dilated_image = get_dilated_image(inv_bin_image.copy(),
                                          dilation=dilation)

        # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
        contours, hierarchy = cv.findContours(image=dilated_image,
                                              mode=cv.RETR_EXTERNAL,
                                              method=cv.CHAIN_APPROX_NONE)

        # draw contours on the original image
        image_copy = self.original_image.copy()
        cv.drawContours(image=image_copy,
                        contours=contours,
                        contourIdx=-1,
                        color=(0, 0, 255),
                        thickness=1,
                        lineType=cv.LINE_AA)

        image_boxes = []
        image_copy = inv_bin_image.copy()

        up_down_shift = dilation[0] // 2
        left_right_shift = dilation[1] // 2

        contours.sort(key=lambda x: compare_contours(x))
        for contour in contours:
            x, y, w, h = cv.boundingRect(contour)
            cur_image = image_copy[y + up_down_shift - 2:y + h - up_down_shift,
                        x + left_right_shift - 1:x + w - left_right_shift].copy()
            image_copy[y + up_down_shift - 1:y + h - up_down_shift,
            x + left_right_shift - 1:x + w - left_right_shift] = 0
            image_boxes.append(cur_image)
        return image_boxes
