#!/usr/bin/python
# -*- coding: utf-8 -*
import numpy as np
from typing import List

from image_detection_module.models.Page import Page
from image_detection_module.utils import read_from_pdf


class Pages:
    def __init__(self, path):
        """
        :param path:
        """
        self.original_images = read_from_pdf(pdf_file_path=path)
        self.pages = self.create_pages(self.original_images)

    @staticmethod
    def create_pages(original_images: List[np.ndarray]) -> List[Page]:
        """
        :param original_images:
        :return:
        """
        return [Page(image) for image in original_images]

