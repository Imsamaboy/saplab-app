import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import scipy.signal as ss


# def draw_y_derivative():
#     plt.fill_between(np.arange(height), _find_y_direvative())
#     plt.title("")
#     plt.xlabel("Density direvative")
#     plt.ylabel("Y-axis projection")
#     plt.axis([0, width, height, 0])
#     plt.show()
from models.image_box import ImageBox


def draw_x_density_with_filter(image_box: ImageBox, kernel=9):
    plt.plot(np.arange(image_box.width),
             ss.medfilt(image_box.x_density, kernel),
             # np.gradient(ss.medfilt(ss.medfilt(ss.medfilt(self.x_density, 15), 15), 15)),
             np.arange(image_box.width),
             np.full_like(np.arange(len(image_box.x_density)), np.average(image_box.x_density)), "r--",
             np.arange(image_box.width),
             np.full_like(np.arange(len(image_box.x_density)), np.max(image_box.x_density)), "g:")
    plt.title("X-density with median filtering")
    plt.xlabel("X-axis")
    plt.ylabel("Density")
    plt.legend(["Real value", "Average value", "Max value"])
    # plt.text(10, np.average(self.x_density), 'percents',)
    plt.axis([0, image_box.width, 0, image_box.height])
    plt.show()


def draw_x_density(image_box: ImageBox, middle_line=10):
    plt.plot(np.arange(image_box.width), image_box.x_density,
             np.arange(image_box.width), np.full_like(np.arange(len(image_box.x_density)), middle_line),
             np.arange(image_box.width), np.full_like(np.arange(len(image_box.x_density)), middle_line + 10),
             np.arange(image_box.width), np.full_like(np.arange(len(image_box.x_density)), middle_line - 10))
    plt.title("X-density")
    plt.xlabel("X-axis")
    plt.ylabel("Density")
    plt.axis([0, image_box.width, 0, image_box.height])
    plt.show()


def draw_y_density(image_box: ImageBox):
    plt.plot(image_box.y_density,
             np.arange(image_box.height),
             np.full_like(np.arange(len(image_box.y_density)), np.average(image_box.y_density)),
             np.arange(image_box.height), "r--",
             np.full_like(np.arange(len(image_box.y_density)), np.max(image_box.y_density)),
             np.arange(image_box.height), "g:",
             np.full_like(np.arange(len(image_box.y_density)), np.median(image_box.y_density)),
             np.arange(image_box.height), "k-.")
    plt.title("Y_density")
    plt.xlabel("Density")
    plt.ylabel("Y-axis projection")
    plt.legend(["Real value", "Average value", "Max value", "Median value"])
    plt.axis([0, image_box.width, image_box.height, 0])
    plt.show()


def draw_with_gaussian_filter(image_box: ImageBox, kernel=(5, 5), border=cv.BORDER_DEFAULT):
    plt.plot(np.arange(image_box.width), cv.GaussianBlur(image_box.x_density, kernel, border))
    plt.title("Y_density")
    plt.xlabel("Density")
    plt.ylabel("Y-axis projection")
    plt.legend(["Real value", "Average value", "Max value", "Median value"])
    plt.axis([0, image_box.width, 0, image_box.height])
    plt.show()