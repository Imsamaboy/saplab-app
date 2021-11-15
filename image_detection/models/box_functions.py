#!/usr/bin/python
# -*- coding: utf-8 -*-
# from abc import ABCMeta, ABC, abstractmethod
import numpy as np


class BoxFunctions:
    """
    Класс с прописанными функциями для всех боксов
    Эти функции повторяются у всех боксов
    """
    def _find_x_density(self, thresholded_and_binarized_image) -> np.array:
        """
        :return: x_density[i] = the number of white pixels in each column of the thresholded_and_binarized_image image
        """
        x_density = np.zeros(self.width)
        for column in range(self.width):
            x_density[column] = np.count_nonzero(thresholded_and_binarized_image[:, column])
        return x_density

    def _find_y_density(self, thresholded_and_binarized_image) -> np.array:
        """
        :return: y_density[i] = the number of white pixels in each row of the thresholded_and_binarized_image image
        """
        y_density = np.zeros(self.height)
        for row in range(self.height):
            y_density[row] = np.count_nonzero(thresholded_and_binarized_image[row])
        return y_density

    def _find_general_density(self, thresholded_and_binarized_image) -> float:
        """
        :return: number of white pixels divided by all pixels
        """
        count = 0
        for line in thresholded_and_binarized_image:
            count += np.count_nonzero(line)
        return count / (self.height * self.width)   # thresholded_and_binarized_image.size
