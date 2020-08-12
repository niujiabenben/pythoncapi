#! /home/chenli/Documents/tools/anaconda3/envs/pytorch/bin/python
# coding: utf-8

# flake8: noqa
# pylint: disable=all

# ```shell
# cd .. && make && cd - && ./benchmark.py
# ```

import os
import cv2
import time
import random
import cppext
import numpy as np


def stitch_images(images, width=512, height=384, fill=(0, 0, 0)):
    """将<=9个patch合为一个.

    images: 包含最多9个cv2格式的image的list.
    width:  每一幅图像占据的宽度.
    height: 每一幅图像占据的高度.
    """

    assert len(images) <= 9
    if len(images) <= 1:
        rows, cols = 1, 1
    elif len(images) <= 2:
        rows, cols = 1, 2
    elif len(images) <= 4:
        rows, cols = 2, 2
    elif len(images) <= 6:
        rows, cols = 2, 3
    elif len(images) <= 9:
        rows, cols = 3, 3

    stitched = np.zeros((height * rows, width * cols, 3), dtype=np.uint8)
    stitched[:, :] = fill
    for i, image in enumerate(images):
        if image is None: continue

        #### 有需要的话进行保长宽比的resize
        old_height, old_width = image.shape[:2]
        if old_height > height or old_width > width:
            new_height = height
            new_width = new_height * old_width // old_height
            if new_width > width:
                new_width = width
                new_height = new_width * old_height // old_width
            image = cv2.resize(image, (new_width, new_height))

        new_height, new_width = image.shape[:2]
        start_x = (i % cols) * width + (width - new_width) // 2
        start_y = (i // cols) * height + (height - new_height) // 2
        end_x = start_x + new_width
        end_y = start_y + new_height
        stitched[start_y:end_y, start_x:end_x, :] = image
    return stitched


def stitch_images_and_save(images, savepath):
    stitched = stitch_images(images)
    dirname = os.path.dirname(savepath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    cv2.imwrite(savepath, stitched)


extlib = cppext.ExtLib("libcppext", "../build/lib")
samples = "/home/chenli/Documents/testcase/pytorchtools/testsamples/test_frames.txt"
with open(samples, "r") as srcfile:
    lines = [l.strip() for l in srcfile]
random.shuffle(lines)
lines = lines[:100]

cpp_time = py_time = 0
for sample in lines:
    paths = [os.path.join(sample, n) for n in os.listdir(sample)]
    images = [cv2.imread(path, 1) for path in paths]
    while len(images)< 4: images.append(None)
    savepath = os.path.join("../images", os.path.basename(sample)) + ".jpg"
    start_time = time.time()
    extlib.ExtStitchAndSaveImage(images, savepath)
    cpp_time += time.time() - start_time
    start_time = time.time()
    stitch_images_and_save(images, savepath)
    py_time += time.time() - start_time
print("cpp time: ", cpp_time)
print("py  time: ", py_time)
