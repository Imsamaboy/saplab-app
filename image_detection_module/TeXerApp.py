#!/usr/bin/python
# -*- coding: utf-8 -*-

from image_detection_module.Pages import Pages


class TeXerApp:
    def __init__(self):
        pass

    def main(self, path=""):
        pages = Pages(path)
        print(pages)


if __name__ == "__main__":
    TeXerApp().main(path="/home/sfelshtyn/Python/SapLabApp/tom3.pdf")
