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


def draw_x_density_with_filter(self, kernel=9):
    plt.plot(np.arange(self.width),
             ss.medfilt(self.x_density, kernel),
             # np.gradient(ss.medfilt(ss.medfilt(ss.medfilt(self.x_density, 15), 15), 15)),
             np.arange(self.width),
             np.full_like(np.arange(len(self.x_density)), np.average(self.x_density)), "r--",
             np.arange(self.width),
             np.full_like(np.arange(len(self.x_density)), np.max(self.x_density)), "g:")
    plt.title("X-density with median filtering")
    plt.xlabel("X-axis")
    plt.ylabel("Density")
    plt.legend(["Real value", "Average value", "Max value"])
    # plt.text(10, np.average(self.x_density), 'percents',)
    plt.axis([0, self.width, 0, self.height])
    plt.show()


def draw_x_density(self, middle_line=10):
    plt.plot(np.arange(self.width), self.x_density,
             np.arange(self.width), np.full_like(np.arange(len(self.x_density)), middle_line),
             np.arange(self.width), np.full_like(np.arange(len(self.x_density)), middle_line + 10),
             np.arange(self.width), np.full_like(np.arange(len(self.x_density)), middle_line - 10))
    plt.title("X-density")
    plt.xlabel("X-axis")
    plt.ylabel("Density")
    plt.axis([0, self.width, 0, self.height])
    plt.show()


def draw_y_density(self):
    plt.plot(self.y_density,
             np.arange(self.height),
             np.full_like(np.arange(len(self.y_density)), np.average(self.y_density)),
             np.arange(self.height), "r--",
             np.full_like(np.arange(len(self.y_density)), np.max(self.y_density)),
             np.arange(self.height), "g:",
             np.full_like(np.arange(len(self.y_density)), np.median(self.y_density)),
             np.arange(self.height), "k-.")
    plt.title("Y_density")
    plt.xlabel("Density")
    plt.ylabel("Y-axis projection")
    plt.legend(["Real value", "Average value", "Max value", "Median value"])
    plt.axis([0, self.width, self.height, 0])
    plt.show()


def draw_with_gaussian_filter(self, kernel=(5, 5), border=cv.BORDER_DEFAULT):
    plt.plot(np.arange(self.width), cv.GaussianBlur(self.x_density, kernel, border))
    plt.title("Y_density")
    plt.xlabel("Density")
    plt.ylabel("Y-axis projection")
    plt.legend(["Real value", "Average value", "Max value", "Median value"])
    plt.axis([0, self.width, 0, self.height])
    plt.show()