#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import re

import cv2 as cv

from image_detection.handler.type_handler import handle
from image_detection.handler.split_handler import run_split
from image_detection.models.page import Page
from image_detection.utils.draw_utils import draw_x_density
from image_detection.utils.utils import read_from_pdf


class TeXerApp:
    def __init__(self):
        """
        Происходит подгрузка всех необходимых данных для других модулей.
        """
        pass

    """Singleton class"""
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TeXerApp, cls).__new__(cls)
        return cls.instance

    """Убрать в другое место"""
    def parse_pages_string(self, pages):
        if '-' not in pages:
            first_page = int(pages)
            last_page = first_page
        else:
            first_page, last_page = map(int, re.split(r'-', pages))
        return first_page if first_page == last_page else (first_page, last_page)

    def main(self, path="", page_numbers="89"):

        page_numbers = self.parse_pages_string(page_numbers)
        if type(page_numbers) is tuple:
            first_page, last_page = page_numbers
            pages = [Page(simple_image, number) for simple_image, number in
                     zip(read_from_pdf(path, page_numbers), range(first_page, last_page + 1))]
        else:
            pages = [Page(simple_image, page_numbers) for simple_image in
                     read_from_pdf(path, page_numbers)]

        handle(pages)

        for page in pages:
            print("Page number: ", page.page_number)
            for image_box in page.get_image_boxes():
                print(image_box.coords)
                print(image_box.general_density)
                print(image_box.height)
                print(image_box.width)
                # cv.imshow("ImageBox", image_box.original_image_box)
                # cv.waitKey(0)
                # cv.destroyAllWindows()
            run_split(page.get_image_boxes())


if __name__ == "__main__":
    TeXerApp().main(path="/home/sfelshtyn/Python/SapLabApp/resources/static/tom3.pdf")
