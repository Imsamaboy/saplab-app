#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import cv2 as cv

from image_detection.utils.utils import compare_contours, read_from_pdf, show_images
from image_detection.utils.utils import get_gray_image
from image_detection.utils.utils import get_thresholded_and_binarized_image
from image_detection.utils.utils import get_dilated_image
from image_detection.models.image_box import ImageBox
from image_detection.models.box_functions import BoxFunctions

PAGE_DENSITY_1 = 0.11
PAGE_DENSITY_2 = 0.2


class Page(BoxFunctions):
    def __init__(self, original_image: np.ndarray):
        self.original_image = original_image
        self.height = original_image.shape[0]
        self.width = original_image.shape[1]
        self.gray_page = get_gray_image(self.original_image)
        self.thresholded_and_binarized_page = get_thresholded_and_binarized_image(self.gray_page)
        self.dilated_page = get_dilated_image(self.thresholded_and_binarized_page)
        self.general_density = self._find_general_density(self.dilated_page)
        self.page_number = None     # Как устанавливаем?
        self.image_boxes = []

    def create_image_boxes(self) -> None:
        """
        :return:
        p. 21:	0.18044814298549072 - (13, 26) ok
        p. 22:  0.2085796070167479  - (10, 26) ok

        p. 24:  0.26957707886230065 - (10, 26)  +- ok

        p. 31:  0.2139964838654795  - (10, 26) ok   (13, 26) worse
        p. 32:  0.17601566440913718  - (13, 26) ok
        p. 83:  0.20564551513758592 -

        p. 5:	0.05770161807854292 -   (10, 40) ок
        p. 7:	0.09186543174132233 -   (10, 40) ок
        p. 145: 0.0873637050148197  -   (10, 40) ok, но большие боксы
        p. 340:	0.0959212242595373  -   (10, 40) ok, но выделяется ненужный "x" в 4. 4) интеграле
        ! p. 341:	0.10767311291328759 -   (10, 40) ok !
        p. 342:	0.09706083390293917 -   (10, 40) ok
        p. 367: 0.0991096240004537  -   (10, 40) ok (10, 26) worse
        p. 379:	0.03573861211185964 -   (10, 40) ok (10, 26) ok
        p. 467:	0.05587848143582458 -   (10, 40) терпимо, попадают лишние символы в боксы
        """
        if PAGE_DENSITY_2 <= self.general_density:
            dilation = (10, 26)
        elif PAGE_DENSITY_1 <= self.general_density < PAGE_DENSITY_2:
            dilation = (13, 26)
        else:
            dilation = (10, 40)
        gray_image = get_gray_image(self.original_image)
        inv_bin_image = get_thresholded_and_binarized_image(gray_image)
        dilated_image = get_dilated_image(inv_bin_image,
                                          dilation=dilation,
                                          iterations=1)
        # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
        contours, hierarchy = cv.findContours(image=dilated_image,
                                              mode=cv.RETR_EXTERNAL,
                                              method=cv.CHAIN_APPROX_NONE)
        # draw contours on the original image
        image_copy = self.original_image.copy()
        cv.drawContours(image=image_copy,
                        contours=contours,
                        contourIdx=-1,
                        color=(0, 0, 255),
                        thickness=1,
                        lineType=cv.LINE_AA)

        image_copy = inv_bin_image.copy()
        up_down_shift = dilation[0] // 2
        left_right_shift = dilation[1] // 2

        contours.sort(key=lambda x: compare_contours(x))
        count = 1
        for contour in contours:
            x, y, w, h = cv.boundingRect(contour)
            # Подрезаем лишние чёрные пиксели
            y_up = y + up_down_shift - 1
            y_down = y + h - up_down_shift
            x_up = x + left_right_shift - 1
            x_down = x + w - left_right_shift
            coords = (y_up, y_down, x_up, x_down)
            image_copy[y_up:y_down, x_up:x_down] = 0
            # Создаем и добавляем ImageBox в page.image_boxes
            self.image_boxes.append(ImageBox(self.original_image[y:y+h, x:x+w], coords=coords)) # y_up:y_down, x_up:x_down
            # cv.imwrite(f"/home/sfelshtyn/Python/SapLabApp/resources/pics/ImageBox{count}.png", self.original_image[y:y+h, x:x+w])
            # count += 1

    def create_latex_page(self, ):
        pass

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def get_image_boxes(self):
        return self.image_boxes


if __name__ == "__main__":
    page = Page(*read_from_pdf("/home/sfelshtyn/Python/SapLabApp/tom3.pdf", "20"))
    page.create_image_boxes()
    show_images("", page.get_image_boxes())
