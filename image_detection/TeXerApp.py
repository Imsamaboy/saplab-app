#!/usr/bin/python
# -*- coding: utf-8 -*-
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

    def main(self, path="", pages="406"):
        """
        default - 20
        :param path:
        :param pages: много текста: 406
        :return:
        """
        pages = [Page(simple_image) for simple_image in read_from_pdf(path, pages)]
        for page in pages:
            page.create_image_boxes()
        handle(pages)
        for page in pages:
            print("IMAGEBOXES")
            for image_box in page.get_image_boxes():
                pass
                # print("ImageBox coords")
                # print(image_box.coords)
                # cv.imshow("", image_box.original_image_box)
                # cv.waitKey(0)
                # cv.destroyAllWindows()
            run_split(page.get_image_boxes())
        for page in pages:
            for count, image_box in enumerate(page.get_image_boxes()):
                # print(image_box.type, count + 1)
                # cv.imshow("ImageBox", image_box.original_image_box)
                # cv.waitKey(0)
                # cv.destroyAllWindows()
                if image_box.get_line_boxes():
                    print("LINEBOXES")
                    for line_box in image_box.get_line_boxes():
                        # print(line_box.line_number)
                        # cv.imshow("LineBox", line_box.original_line_image_box)
                        # cv.waitKey(0)
                        # cv.destroyAllWindows()
                        # print("LineBox coords")
                        # print(line_box.coords)
                        line_box.split_line_box_into_words()
                        # print("Words:")
                        for word_box in line_box.word_boxes:
                            # cv.imshow("word", word_box.original_word_image_box)
                            # cv.waitKey(0)
                            # cv.destroyAllWindows()
                            # draw_x_density(word)
                            # print("WordBox coords")
                            # print(word_box.coords)
                            # print("Units")
                            word_box.split_word_box_into_units()
                            for unit in word_box.unit_boxes:
                                pass
                                # print("Unit coords")
                                # print(unit.coords)
                                # cv.imshow("units", unit.original_unit_image_box)
                                # cv.waitKey(0)
                                # cv.destroyAllWindows()


                else:
                    pass
                    # print("else")


if __name__ == "__main__":
    TeXerApp().main(path="/resources/static/tom3.pdf")
