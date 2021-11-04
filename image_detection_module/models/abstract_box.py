#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABCMeta, ABC, abstractmethod


class AbstractBox(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def _find_x_density(self, ):
        pass

    @abstractmethod
    def _find_y_density(self, ):
        pass

    @abstractmethod
    def _find_general_density(self, ):
        pass

    # @abstractmethod
    # def get_height(self):
    #     return self.height
    #
    # @abstractmethod
    # def get_width(self):
    #     return self.width
