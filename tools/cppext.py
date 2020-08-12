#! /home/chenli/Documents/tools/anaconda3/envs/pytorch/bin/python
# coding: utf-8

import os
import cv2
import ctypes
import numpy as np


class ExtLib:
    def __init__(self, so_name, so_dir):
        self.lib = np.ctypeslib.load_library(so_name, so_dir)
        self.lib.ExtStitchAndSaveImage.argtypes = [
            ctypes.POINTER(ctypes.c_char_p), ctypes.c_int, ctypes.c_int,
            ctypes.POINTER(ctypes.c_char_p), ctypes.c_int, ctypes.c_int,
            ctypes.POINTER(ctypes.c_char_p), ctypes.c_int, ctypes.c_int,
            ctypes.POINTER(ctypes.c_char_p), ctypes.c_int, ctypes.c_int,
            ctypes.c_char_p
        ]
        self.lib.ExtStitchAndSaveImage.restype = ctypes.c_bool

    def ExtStitchAndSaveImage(self, images, savepath):
        assert len(images) == 4
        image_data = [None] * 4
        image_rows = [0] * 4
        image_cols = [0] * 4
        data_type = ctypes.POINTER(ctypes.c_char_p)
        for i, image in enumerate(images):
            if image is not None:
                image_data[i] = image.ctypes.data_as(data_type)
                image_rows[i] = image.shape[0]
                image_cols[i] = image.shape[1]
        return self.lib.ExtStitchAndSaveImage(
            image_data[0], image_rows[0], image_cols[0],
            image_data[1], image_rows[1], image_cols[1],
            image_data[2], image_rows[2], image_cols[2],
            image_data[3], image_rows[3], image_cols[3],
            bytes(savepath, "utf-8"))


if __name__ == "__main__":
    pass
