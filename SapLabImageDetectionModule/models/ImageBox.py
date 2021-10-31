#!/usr/bin/python
# -*- coding: utf-8 -*-

from models.AbstractBox import AbstractBox


class ImageBox(AbstractBox):
    def __init__(self):
        self.original_image_box = None
        self.dilated_image_box = None
        self.laplacian_image_box = None
        self.coords = None
        self.type = None
        self.height = None
        self.width = None
        self.number_of_image_box = None
        self.x_density = None
        self.y_density = None
        self.line_boxes = None
        import scipy.signal as ss
        class ImageBox():
            """Class that represent a single small image box that contains"""

            def __init__(self, big_image: np.ndarray, box_coords: tuple, flag=True):
                up, down, left, right = box_coords
                if flag:
                    self.image = big_image[up:down + 1, left:right + 1]
                    # cv2_imshow(self.image)
                else:
                    self.image = big_image
                self.height = self.image.shape[0]
                self.width = self.image.shape[1]
                self.x_density = self._find_x_density(self.image)
                self.y_density = self._find_y_density(self.image)
                self.type_of_box = self._find_type_of_box()

            def __image_prepocessing(self):
                # grauscale
                # treshold
                # dilation?
                pass

            def _find_x_density(self, image: np.ndarray) -> np.array:
                x_density = np.zeros(self.width)
                for column in range(self.width):
                    x_density[column] = np.count_nonzero(np.transpose(image)[column])
                return x_density

            def _find_y_density(self, image: np.ndarray) -> np.array:
                y_density = np.zeros(self.height)
                for row in range(self.height):
                    y_density[row] = np.count_nonzero(self.image[row])
                return y_density

            def find_general_density(self) -> float:
                count = 0
                for line in self.image:
                    count += np.count_nonzero(line)
                return count / (self.height * self.width)

            def _find_type_of_box(self):
                baseline_height = 10  # pix
                if self.find_general_density() > 0.4:
                    return "text"
                else:
                    return "not defined"

            def find_y_direvative(self):
                def direvative_in_point(func: np.array, x: int) -> int:
                    return func[x] - func[x - 1]

                y_density_direvative = np.zeros(self.height)
                for line in range(1, self.height):
                    y_density_direvative[line] = direvative_in_point(self.y_density, line)
                y_density_direvative[0] = y_density_direvative[1]
                return y_density_direvative

            def draw_y_direvative(self):
                plt.fill_between(np.arange(self.height), self.find_y_direvative())
                plt.title("")
                plt.xlabel("Density direvative")
                plt.ylabel("Y-axis projection")
                plt.axis([0, self.width, self.height, 0])
                plt.show()

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

            def create_image_with_laplacian_filter(self, ddepth=cv.CV_16S, kernel=3):
                return cv.Laplacian(self.image, ddepth, kernel)

            # def draw_x_density_with_laplacian_filter(self, image):
            #   plt.plot(np.arange(self.width), )
            #   plt.title("Y_density")
            #   plt.xlabel("Density")
            #   plt.ylabel("Y-axis projection")
            #   plt.legend(["Real value", "Average value", "Max value", "Median value"])
            #   plt.axis([0, self.width, 0, self.height])
            #   plt.show()

            def draw_with_gaussian_filter(self, kernel=(5, 5), border=cv.BORDER_DEFAULT):
                plt.plot(np.arange(self.width), cv.GaussianBlur(self.x_density, kernel, border))
                plt.title("Y_density")
                plt.xlabel("Density")
                plt.ylabel("Y-axis projection")
                plt.legend(["Real value", "Average value", "Max value", "Median value"])
                plt.axis([0, self.width, 0, self.height])
                plt.show()

            def __str__(self):
                return f"Height={self.height}, Width={self.width}"

    def generate_dilated_image_box(self, dilation, kernel):
        pass

    def generate_laplacian_image_box(self, kernel, cv_type):
        pass

    def split_image_box_into_lines(self, ):
        pass
