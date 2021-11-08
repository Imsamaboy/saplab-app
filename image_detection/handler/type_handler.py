"""
Добавить сюда часть с машинным обучением и все проверки на тип бокса
"""
from typing import List

from image_detection.models.image_box import ImageBox


def equals_checker_in_the_image_box(image_box: ImageBox) -> bool:
    """
    :param image_box:
    :return:
    """
    indices_list = []
    temp = []
    for index in range(0, len(image_box.x_density)):
        if image_box.x_density[index] in range(4, 7):
            temp.append(index)
        else:
            if len(temp) in range(19, 22):
                indices_list += [temp]
            temp = []

    if len(indices_list) > 0:
        image_box.set_position_of_the_equals_sign(indices_list)
        return True
    else:
        return False


def define_type_of_image_box(image_box: ImageBox, threshold=0.15):
    """
    :param threshold:
    :param image_box:
    :return:
    Будет сделано после понедельника
    """
    # match function_that_defines_type(image_box.original_image_box):
    #     case r"text\text_with_formula":
    #         pass
    #     case r"formula":
    #         pass
    #     case r"figure":
    #         pass
    #     case r"trash":
    #         pass
    if image_box.get_general_density() > threshold:
        image_box.set_type("text")
    else:
        image_box.set_type("smt else")


def handle(pages):
    for page in pages:
        for image_box in page.get_image_boxes():
            define_type_of_image_box(image_box)
