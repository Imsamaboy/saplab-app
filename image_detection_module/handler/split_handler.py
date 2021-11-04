import scipy.signal as ss
import numpy as np
from typing import List

from image_detection_module.models.image_box import ImageBox
from image_detection_module.models.line_box import LineBox


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
    # Деление и создание строк
    return [LineBox(image_box.original_image_box[dividing_lines[border]:dividing_lines[border + 1]])
            for border in range(len(dividing_lines) - 1)]


def split_image_box_into_formula_and_text(image_box: ImageBox):
    pass


def run(image_boxes):
    for image_box in image_boxes:
        if image_box.type == "text":
            image_box.line_boxes = split_image_box_into_lines(image_box)
        if image_box.type == "formula":
            pass
        if image_box.type == "text_with_formula":
            split_image_box_into_formula_and_text(image_box)
        if image_box.type == "figure":
            pass


if __name__ == "__main__":
    pass
