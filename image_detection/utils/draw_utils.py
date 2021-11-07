from typing import Union

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import scipy.signal as ss


def draw_x_density_with_filter(box, kernel=9):
    plt.plot(np.arange(box.width),
             ss.medfilt(box.x_density, kernel),
             # np.gradient(ss.medfilt(ss.medfilt(ss.medfilt(self.x_density, 15), 15), 15)),
             np.arange(box.width),
             np.full_like(np.arange(len(box.x_density)), np.average(box.x_density)), "r--",
             np.arange(box.width),
             np.full_like(np.arange(len(box.x_density)), np.max(box.x_density)), "g:")
    plt.title("X-density with median filtering")
    plt.xlabel("X-axis")
    plt.ylabel("Density")
    plt.legend(["Real value", "Average value", "Max value"])
    # plt.text(10, np.average(self.x_density), 'percents',)
    plt.axis([0, box.width, 0, box.height])
    plt.show()


def draw_x_density(box, middle_line=10):
    plt.plot(np.arange(box.width), box.x_density,
             np.arange(box.width), np.full_like(np.arange(len(box.x_density)), middle_line),
             np.arange(box.width), np.full_like(np.arange(len(box.x_density)), middle_line + 10),
             np.arange(box.width), np.full_like(np.arange(len(box.x_density)), middle_line - 10))
    plt.title(f"X-density")
    plt.xlabel("X-axis")
    plt.ylabel("Density")
    plt.axis([0, box.width, 0, box.height])
    plt.show()


def draw_y_density(box):
    plt.plot(box.y_density,
             np.arange(box.height),
             np.full_like(np.arange(len(box.y_density)), np.average(box.y_density)),
             np.arange(box.height), "r--",
             np.full_like(np.arange(len(box.y_density)), np.max(box.y_density)),
             np.arange(box.height), "g:",
             np.full_like(np.arange(len(box.y_density)), np.median(box.y_density)),
             np.arange(box.height), "k-.")
    plt.title("Y_density")
    plt.xlabel("Density")
    plt.ylabel("Y-axis projection")
    plt.legend(["Real value", "Average value", "Max value", "Median value"])
    plt.axis([0, box.width, box.height, 0])
    plt.show()


def draw_with_gaussian_filter(box, kernel=(5, 5), border=cv.BORDER_DEFAULT):
    plt.plot(np.arange(box.width), cv.GaussianBlur(box.x_density, kernel, border))
    plt.title("Y_density")
    plt.xlabel("Density")
    plt.ylabel("Y-axis projection")
    plt.legend(["Real value", "Average value", "Max value", "Median value"])
    plt.axis([0, box.width, 0, box.height])
    plt.show()