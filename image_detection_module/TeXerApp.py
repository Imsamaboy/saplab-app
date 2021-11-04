#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2 as cv

from handler.type_handler import handle
from handler.split_handler import run
from models.page import Page
from utils.draw_utils import draw_x_density
from utils.utils import read_from_pdf
from utils.utils import show_images


class TeXerApp:
    def __init__(self):
        """
        !singleton class!
        Эксземпляр создаётся при заходе в приложение.
        Происходит подгрузка всех необходимых данных для других модулей.
        """
        pass

    def main(self, path="", pages="20"):
        pages = [Page(simple_image) for simple_image in read_from_pdf(path, pages)]
        for page in pages:
            page.create_image_boxes()
        handle(pages)
        for page in pages:
            images = []
            for image_box in page.get_image_boxes():
                images.append(image_box.original_image_box)
                # print(image_box)
                print(image_box.x_density)
                cv.imshow("", image_box.original_image_box)
                cv.waitKey(0)
                cv.destroyAllWindows()
                draw_x_density(image_box)
            # show_images("", images)
            run(page.get_image_boxes())


if __name__ == "__main__":
    TeXerApp().main(path="/home/sfelshtyn/Python/SapLabApp/tom3.pdf")
