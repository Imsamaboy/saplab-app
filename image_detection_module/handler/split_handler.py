import scipy.signal as ss
import numpy as np
from typing import List

from image_detection_module.models.image_box import ImageBox
from image_detection_module.models.line_box import LineBox


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


def split_image_box_into_lines(image_box: ImageBox, edge_value_parameter=0.2) -> List:
    """
    :param image_box:
    :param edge_value_parameter:
    :return:
    """
    # Установка порогов для деления на строки
    edge_value = edge_value_parameter * image_box.width
    y_density = image_box.y_density
    y_density_filt = ss.medfilt(y_density, 9)

    # Установка границ деления на строки
    up_bound, down_bound = 0, 0
    dividing_lines = set()
    for index in range(image_box.height - 1):
        if y_density_filt[index + 1] < edge_value <= y_density_filt[index]:
            up_bound = index + 1
        if y_density_filt[index + 1] > edge_value >= y_density_filt[index]:
            down_bound = index + 1
            dividing_lines.add(np.argmin(y_density[up_bound: down_bound + 1]) + up_bound)

    dividing_lines.add(image_box.height)
    dividing_lines = sorted(list(dividing_lines))
    # Деление и создание строк (y_up:y_down, x_up:x_down)
    return [LineBox(image_box.gray_image_box[dividing_lines[border]:dividing_lines[border + 1]],
                    coords=(image_box.coords[0] + dividing_lines[border],
                            image_box.coords[0] + dividing_lines[border + 1],
                            image_box.coords[2],
                            image_box.coords[3]),
                    line_number=line_number)
            for line_number, border in enumerate(range(len(dividing_lines) - 1))]


def split_image_box_into_formula_and_text(image_box: ImageBox):
    """
    :param image_box:
    :return:
    """
    pass


def run_split(image_boxes):
    for image_box in image_boxes:
        if image_box.type == "text":
            # print("SPLITTING")
            image_box.line_boxes = split_image_box_into_lines(image_box)
        if image_box.type == "formula":
            pass
        if image_box.type == "text_with_formula":
            split_image_box_into_formula_and_text(image_box)
        if image_box.type == "figure":
            pass
        if image_box.type == "smt else":
            pass


if __name__ == "__main__":
    pass
