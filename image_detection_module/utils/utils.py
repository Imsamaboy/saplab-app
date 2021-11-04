import os
import re
import numpy as np
import cv2 as cv
from pdf2image import convert_from_path
from typing import List

DILATION_BLOCK_SIZE = (3, 25)


def read_from_pdf(pdf_file_path, *args) -> List[np.ndarray]:
    """
        Returns a list of numpy array images
        1 - просто первая страница
        1-5, 7 = страницы с 1 по 5 и страница 7
        5, 12-50, 67 = страница 5, страницы 12 - 50, 67
    """
    if not os.path.isfile(pdf_file_path):
        raise FileNotFoundError("Make sure your file path is correct")
    images_list = []
    for pages_arg in args:
        pages_arg = str(pages_arg)
        if '-' not in pages_arg:
            first_page = int(pages_arg)
            last_page = first_page
        else:
            first_page, last_page = map(int, re.split(r'-', pages_arg))
        images_list.extend(list(map(np.array,
                                    convert_from_path(pdf_file_path,
                                                      first_page=first_page,
                                                      last_page=last_page))))
    return images_list


def show_images(window_name: str, images: List) -> None:
    """
    :param images:
    :param window_name:
    :return:
    """
    for image in images:
        cv.imshow(window_name, image)
        cv.waitKey(0)
        cv.destroyAllWindows()


def compare_contours(contour):
    """
    :param contour:
    :return:
    """
    x, y, w, h = cv.boundingRect(contour)
    return h * w


def get_gray_image(image: np.ndarray, color=cv.COLOR_BGR2GRAY) -> np.ndarray:
    """
    :param image:
    :param color:
    :return:
    """
    return cv.cvtColor(image, color)


def get_thresholded_and_binarized_image(image: np.ndarray,
                                        binarization_border=(254, 255)) -> np.ndarray:
    """
    :param binarization_border:
    :param image:
    :return:
    """
    _, inv_bin_image = cv.threshold(image,
                                    binarization_border[0],
                                    binarization_border[1],
                                    cv.THRESH_BINARY_INV)
    return inv_bin_image


def get_dilated_image(image: np.ndarray, dilation=DILATION_BLOCK_SIZE):
    """
    :param image:
    :param dilation:
    :return:
    """
    kernel = np.ones(dilation,
                     np.uint8)

    dilated_image = cv.dilate(image,
                              kernel,
                              iterations=1)
    return dilated_image


def get_laplacian_image(image: np.ndarray, ddepth=cv.CV_16S, kernel=3):
    """
    :param image:
    :param ddepth:
    :param kernel:
    :return:
    """
    laplacian_image = cv.Laplacian(image, ddepth, kernel)
    show_images("laplacian&original image", [laplacian_image, image])
    return cv.Laplacian(image, ddepth, kernel)


if __name__ == "__main__":
    get_laplacian_image(
        get_thresholded_and_binarized_image(*read_from_pdf("/tom3.pdf", "20")))
