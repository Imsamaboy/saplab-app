import numpy as np

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


def create_deviation_array(image_box: ImageBox, step=100) -> (list, list):
    amount = len(image_box.x_density) // step
    deviation_array = []
    borders = []
    for count in range(amount):
        i, j = count * step, (count + 1) * step
        deviation = np.std(image_box.x_density[i:j])
        if deviation >= 6:
            deviation_array.append(deviation)
            borders.append([i, j])

    last_deviation_element = np.std(image_box.x_density[amount * step:])
    if last_deviation_element >= 6:
        deviation_array.append(last_deviation_element)
        borders.append([amount * step, len(image_box.x_density)])

    return deviation_array, borders


def merge_intervals(borders_array) -> list:
    merged = []
    for border in borders_array:
        if not merged or merged[-1][1] < border[0]:
            merged.append(border)
        else:
            merged[-1][1] = max(merged[-1][1], border[1])
    return list(map(tuple, merged))


def find_formula_borders(image_box, border_array, window=20) -> list:
    borders = []
    for array in border_array:
        if array[0] != 0:
            border = [index for index in range(array[0] - window, array[1] + window)
                      if np.std(image_box.x_density[index:index + window]) >= 6]
            borders.append((border[0], border.pop()))
        else:
            border = [index for index in range(array[0], array[1] - window)
                      if np.std(image_box.x_density[index:index + window]) >= 6]
            borders.append((border[0], border.pop()))
    return borders


def make_points(borders, image_box):
    points = []
    for border in borders:
        points.append(((border[0], 0), (border[0], image_box.height)))
        points.append(((border[1], 0), (border[1], image_box.height)))
    return points


def count_peaks_that_are_not_in_borders(borders, peaks) -> (int, list):
    count = 0
    out_ranged_peaks = []
    for index in range(len(borders) - 1):
        for peak in peaks:
            if borders[index][1] < peak < borders[index + 1][0] or peak > borders[-1][1]:
                count += 1
                out_ranged_peaks.append(peak)
    return count, out_ranged_peaks
