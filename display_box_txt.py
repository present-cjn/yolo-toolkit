# -*- coding: utf-8 -*-
"""
Time:     2023/3/5 22:03
Author:   cjn
Version:  1.0.0
File:     display_box_txt.py
Describe:
"""
import argparse
import os
from utils import *
import cv2

# 下面default后可以输入默认的路径，输入后不需要命令行中添加路径
parser = argparse.ArgumentParser(description='命令行参数')
parser.add_argument('--input_img', '-ii', type=str, default='', help='图片的地址')
parser.add_argument('--input_anno', '-ia', type=str, default='', help='txt标签的地址')

args = parser.parse_args()

img_path = args.input_img
anno_path = args.input_anno
img_file = os.listdir(img_path)

for file in img_file:
    new_img_path = img_path + "/" + file
    new_anno_path = anno_path + "/" + file[:-4] + '.txt'

    img = cv2.imread(new_img_path, 1)

    boxes = []
    with open(new_anno_path, "r") as f:  # 打开文件
        for line in f.readlines():
            boxes.append(line.strip('\n'))
    new_boxes = []
    for box in boxes:
        box_list = box.split()
        label = int(box_list[0])

        [x1, y1, x2, y2] = yolobox2cvrect(box_list, img)
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)

    cv2.imshow('result', img)
    cv2.waitKey()
