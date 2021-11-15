"""
Добавить сюда часть с машинным обучением и все проверки на тип бокса
"""
from typing import List

import joblib
import numpy as np
import pandas as pd
import cv2 as cv

from image_detection.models.image_box import ImageBox

PAGE_LINEOUT = -1
TEXT = 0
TEXT_WITH_FORMULA = 1
FORMULA = 2


def define_type_of_image_box(image_box: ImageBox):
    """
    :param threshold:
    :param image_box:
    :return:
        naming = {
            -1: "page lineout",
            0: "text",
            1: "text with formula inside",
            2: "formula"
        }
    """
    clf = joblib.load("/home/sfelshtyn/Python/SapLabApp/image_detection/handler/rfc_classifier")
    scaler = joblib.load("/home/sfelshtyn/Python/SapLabApp/image_detection/handler/scaler_final")
    # columns = (
    #     'density',
    #     'mean_density_by_x',
    #     'mean_density_by_y',
    #     'width',
    #     'height',
    #     'black_pixels_count',
    #     'white_pixels_count'
    # )
    data = np.asarray([
        [image_box.general_density,
         image_box.get_mean_density_by_x(),
         image_box.get_mean_density_by_y(),
         image_box.width,
         image_box.height,
         image_box.black_pixels,
         image_box.count_white_pixels()]
    ])
    data = scaler.transform(data)
    print(clf.predict(data))

    predicted = clf.predict(data)[0]
    if predicted == PAGE_LINEOUT:
        image_box.set_type("page_lineout")
        print("page_lineout")
    if predicted == TEXT:
        print("text")
        image_box.set_type("text")
    if predicted == TEXT_WITH_FORMULA:
        image_box.set_type("text_with_formula")
        print("text_with_formula")
    if predicted == FORMULA:
        image_box.set_type("formula")
        print("formula")

    # cv.imshow("ImageBox", image_box.thresholded_and_binarized_image_box)
    # cv.waitKey(0)
    # cv.destroyAllWindows()


def handle(pages):
    for page in pages:
        for image_box in page.get_image_boxes():
            define_type_of_image_box(image_box)

    # match function_that_defines_type(image_box.original_image_box):
    #     case r"text\text_with_formula":
    #         pass
    #     case r"formula":
    #         pass
    #     case r"figure":
    #         pass
    #     case r"trash":
    #         pass
