#!/usr/bin/python
# -*- coding: utf-8 -*-

class AbstractBox:
    def __init__(self):
        self.coords = None
        self.height = None
        self.width = None
        self.x_density = None
        self.y_density = None

    def _find_x_density(self, ):
        pass

    def _find_y_density(self, ):
        pass

    def _find_general_density(self, ):
        pass

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width
