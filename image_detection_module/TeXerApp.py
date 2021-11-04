#!/usr/bin/python
# -*- coding: utf-8 -*-

from handler.type_handler import handle
from handler.split_handler import run
from models.page import Page
from utils.utils import read_from_pdf


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
            print(page.image_boxes)
        handle(pages)
        for page in pages:
            run(page.get_image_boxes())


if __name__ == "__main__":
    TeXerApp().main(path="/home/sfelshtyn/Python/SapLabApp/tom3.pdf")
