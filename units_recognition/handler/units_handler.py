import numpy as np
import cv2 as cv
from functools import partial
from itertools import groupby
import random
from PIL import Image
import csv
import os
import joblib

'''Всё для обработки изображения символа'''


def prepare_image(image):
    return np.array(image)


def all_blocks(arr):
    return [list(g) for k, g in groupby(arr) if k == 1]


def general_term(s, pic_height, lower_bound):
    blocks = all_blocks(s)
    return -1 if len(blocks) == 1 and len(blocks[0]) >= lower_bound * pic_height else len(blocks)


def x_lines(image, pic_height, lower_bound):
    return [general_term(i, pic_height, lower_bound) for i in image]


def y_lines(image, pic_height, lower_bound):
    return [general_term(i, pic_height, lower_bound) for i in image.T]


'''Приведение к одной размерности'''


def stretch(index, k, n):
    if k == 0:
        index = [0, 0, 0]
    elif k < 2:
        index = [index[0]] * 3
        k = len(index)
    for _ in range(n - k):
        i = random.randint(0, k - 2)
        index.insert(i, (index[i] + index[i + 1]) / 2)
        k = len(index)
    return index


def compress(index, k, n):
    for _ in range(k - n):
        i = random.randint(0, k - 2)
        index[i] = (index[i] + index[i + 1]) / 2
        index.pop(i + 1)
        k = len(index)
    return index


def normalise(n, index):
    index = np.trim_zeros(index, 'fb')
    k = len(index)
    if k > n:
        return compress(index, k, n)
    elif k < n:
        return stretch(index, k, n)
    else:
        return index


'''Главная функция. На вход принимает картинку (страницу) и координаты символа'''


def get_norm_seq(image, lower_bound=0.8, size=20):
    pic_height = image.shape()[0]
    return normalise(size, x_lines(image, pic_height, lower_bound)) + normalise(size,
                                                                                y_lines(image, pic_height, lower_bound))


clf = joblib.load('/home/sfelshtyn/Python/SapLabApp/units_recognition/handler/classifier')


def get_tex(image):
    """
    :param image: jpg image
    :return:
    """
    seq = get_norm_seq(image)
    return clf.predict(seq)


if __name__ == "__main__":
    image = Image.open("/home/sfelshtyn/Downloads/Telegram Desktop/e.jpg")
    result = get_tex(image)
    print(result)
