import scipy.signal as ss
import numpy as np
from typing import List
import cv2 as cv

from image_detection.models.image_box import ImageBox
from image_detection.models.line_box import LineBox
from image_detection.utils.draw_utils import *


def split_box_into_header_and_line(line_boxes) -> List:
    """
    :return:
    """
    # split_line_boxes = []
    # borders = []
    # deleting_line = None
    # for number_of_line_box, line_box in enumerate(line_boxes):
    #     for row_number, row in enumerate(line_box.thresholded_and_binarized_line_image_box):
    #         if row.tolist().count(0) == line_box.width:
    #             deleting_line = number_of_line_box
    #             borders.append((0, row_number - 1))
    #             borders.append((row_number, line_box.height))
    #     # Удаляем LineBox с header и добавляем отдельно Line и Header
    #     if deleting_line:
    #         del line_boxes[deleting_line]
    #         # Не Header
    #         line_boxes.append(LineBox(line_box.original_line_image_box[borders[0][0]:borders[0][1]],
    #                                   coords=(0,0,0,0),
    #                                   line_number=line_box.number))
    #         # Header
    #         line_boxes.append(LineBox(line_box.original_line_image_box[borders[1][0]:borders[1][1]],
    #                                   coords=(0, 0, 0, 0),
    #                                   line_number=1))
    #         # LineBox(image_box.gray_image_box[dividing_lines[border]:dividing_lines[border + 1]],
    #         #         coords=(image_box.coords[0] + dividing_lines[border],
    #         #                 image_box.coords[0] + dividing_lines[border + 1],
    #         #                 image_box.coords[2],
    #         #                 image_box.coords[3]),
    #         #         line_number=line_number)
    #         # Обновляем borders
    #         borders = []
    #         # Смотрим следующий LineBox
    # return line_boxes


def create_dividing_lines(image_box: ImageBox) -> List:
    flag = True
    dividing_lines = set()
    dividing_lines.add(0)
    for index in range(len(image_box.y_density)):
        if image_box.y_density[index] == 0 and flag:
            dividing_lines.add(index)
            flag = False
        if image_box.y_density[index] != 0:
            flag = True
    if image_box.height not in dividing_lines:
        dividing_lines.add(image_box.height)
    dividing_lines = sorted(list(dividing_lines))

    indices_that_must_delete = [index + 1 for index in range(len(dividing_lines) - 1) if
                                dividing_lines[index + 1] - dividing_lines[index] <= 15]
    for index in indices_that_must_delete:
        del dividing_lines[index]

    return dividing_lines


def clear_unnecessary_black_lines(image: np.ndarray) -> List:
    return sorted(
        [number for number, row in enumerate(image) if image.shape[1] - np.count_nonzero(row) != image.shape[1]])


def split_image_box_into_lines(image_box: ImageBox) -> List:
    """
    :param image_box:
    :return:
    """
    line_boxes = []
    dividing_lines = create_dividing_lines(image_box)
    for line_number, index in enumerate(range(len(dividing_lines) - 1)):
        # img = image_box.thresholded_and_binarized_image_box[dividing_lines[index]:dividing_lines[index + 1], :]
        numbers = clear_unnecessary_black_lines(
            image_box.thresholded_and_binarized_image_box[dividing_lines[index]:dividing_lines[index + 1], :])
        # Деление и создание строк (y_up:y_down, x_up:x_down)
        # TODO: Сейчас я не учитываю numbers, когда сую координаты в LineBox
        line_boxes.append(LineBox(
            gray_line_image_box=image_box.gray_image_box[dividing_lines[index]:dividing_lines[index + 1], :],
            coords=(image_box.coords[0] + dividing_lines[index],
                                          image_box.coords[0] + dividing_lines[index + 1],
                                          image_box.coords[2],
                                          image_box.coords[3]),
            line_number=line_number))
    return line_boxes
    # return [
    #     LineBox(original_line_image_box=image_box.gray_image_box[dividing_lines[border]:dividing_lines[border + 1]],
    #             coords=(image_box.coords[0] + dividing_lines[border],
    #                     image_box.coords[0] + dividing_lines[border + 1],
    #                     image_box.coords[2],
    #                     image_box.coords[3]),
    #             line_number=line_number)
    #     for line_number, border in enumerate(range(len(dividing_lines) - 1))
    # ]


def split_image_box_into_formula_and_text(image_box: ImageBox):
    """
    :param image_box:
    :return:
    """
    # print(image_box.height, image_box.width)
    # cv.imshow("ImageBox", image_box.thresholded_and_binarized_image_box)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    #
    # dividing_lines = create_dividing_lines(image_box)
    # print(dividing_lines)
    # draw_y_density(image_box)
    # draw_x_density(image_box)
    # return dividing_lines
    pass


def check_image_box_for_splitting(image_box: ImageBox):
    """
    :param image_box:
    :return:
    p. 77 - system
    p. 467
    """
    # print(image_box.height, image_box.width)
    # cv.imshow("ImageBox", image_box.thresholded_and_binarized_image_box)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    #
    # dividing_lines = create_dividing_lines(image_box)
    # print("Lines", dividing_lines)
    pass


def run_split(image_boxes):
    # Переписать на match case
    """
    :param image_boxes:
    :return:
    """
    for image_box in image_boxes:
        if image_box.type == "page_lineout":
            pass

        if image_box.type == "text":
            # print("text")
            image_box.line_boxes = split_image_box_into_lines(image_box)

        if image_box.type == "formula":
            pass
            # print("formula")
            # check_image_box_for_splitting(image_box)

        if image_box.type == "text_with_formula":
            pass
            # print("text_with_formula")
            # print("mean", image_box.get_mean_density_by_y())
            # dividing_lines = split_image_box_into_formula_and_text(image_box)

            # cv.imshow("ImageBox",
            #           image_box.thresholded_and_binarized_image_box[0:82, :])
            # cv.waitKey(0)
            # cv.destroyAllWindows()
            #
            # for index in range(len(dividing_lines) - 1):
            #     cv.imshow("ImageBox", image_box.thresholded_and_binarized_image_box[dividing_lines[index]:dividing_lines[index + 1], :])
            #     cv.waitKey(0)
            #     cv.destroyAllWindows()

        if image_box.type == "figure":
            pass

        if image_box.type == "smt else":
            pass


if __name__ == "__main__":
    pass
