# -*- coding: utf-8 -*-
"""
Time:     2023/3/5 22:13
Author:   cjn
Version:  1.0.0
File:     data_aug.py
Describe:
"""
import cv2
import math
import os
import argparse
from utils import *


def getRotatedImg(angle,img_path,img_write_path):
    img = cv2.imread(img_path)
    rows, cols = img.shape[:2]
    a, b = cols / 2, rows / 2
    M = cv2.getRotationMatrix2D((a, b), angle, 1)
    rotated_img = cv2.warpAffine(img, M, (cols, rows))  # 旋转后的图像保持大小不变
    cv2.imwrite(img_write_path,rotated_img)
    return a,b, img, rotated_img


def getRotatedAnno(Pi_angle,a,b,anno_path,anno_write_path, img, rotated_img):
    boxes = []
    with open(anno_path, "r") as f:  # 打开文件
        for line in f.readlines():
            boxes.append(line.strip('\n'))
    new_boxes = []
    for box in boxes:
        box_list = box.split()
        label = int(box_list[0])

        [x1, y1, x2, y2] = yolobox2cvrect(box_list, img)
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)

        x3=x1
        y3=y2
        x4=x2
        y4=y1

        X1 = (x1 - a) * math.cos(Pi_angle) - (y1 - b) * math.sin(Pi_angle) + a
        Y1 = (x1 - a) * math.sin(Pi_angle) + (y1 - b) * math.cos(Pi_angle) + b

        X2 = (x2 - a) * math.cos(Pi_angle) - (y2 - b) * math.sin(Pi_angle) + a
        Y2 = (x2 - a) * math.sin(Pi_angle) + (y2 - b) * math.cos(Pi_angle) + b

        X3 = (x3 - a) * math.cos(Pi_angle) - (y3 - b) * math.sin(Pi_angle) + a
        Y3 = (x3 - a) * math.sin(Pi_angle) + (y3 - b) * math.cos(Pi_angle) + b

        X4 = (x4 - a) * math.cos(Pi_angle) - (y4 - b) * math.sin(Pi_angle) + a
        Y4 = (x4 - a) * math.sin(Pi_angle) + (y4 - b) * math.cos(Pi_angle) + b

        X_MIN=  min(X1,X2,X3,X4)
        X_MAX = max(X1, X2, X3, X4)
        Y_MIN = min(Y1, Y2, Y3, Y4)
        Y_MAX = max(Y1, Y2, Y3, Y4)

        new_box = cvrect2yolobox([X_MIN, Y_MIN, X_MAX, Y_MAX], img, label)
        # [x1, y1, x2, y2] = yolobox2cvrect(new_box, img)
        # cv2.rectangle(rotated_img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)

        new_box_str = str(new_box[0])+' ' + str(new_box[1])+ ' ' + str(new_box[2])+ ' ' + str(new_box[3])+' ' + str(new_box[4])
        new_boxes.append(new_box_str)

    # cv2.imshow('src', img)
    # cv2.imshow('dst', rotated_img)
    # cv2.waitKey()
    with open(anno_write_path, "w") as f:
        for line in new_boxes:
            f.write(line + '\n')

def rotate(angle,img_dir,anno_dir,img_write_dir,anno_write_dir):
    if not os.path.exists(img_write_dir):
        os.makedirs(img_write_dir)

    if not os.path.exists(anno_write_dir):
        os.makedirs(anno_write_dir)

    Pi_angle = -angle * math.pi / 180.0  # 弧度制，后面旋转坐标需要用到，注意负号！！！
    img_names=os.listdir(img_dir)
    for img_name in img_names:
        img_path=os.path.join(img_dir,img_name)
        img_write_path=os.path.join(img_write_dir,img_name[:-4]+'R'+str(angle)+'.png')
        #
        anno_path=os.path.join(anno_dir,img_name[:-4]+'.txt')
        anno_write_path = os.path.join(anno_write_dir, img_name[:-4]+'R'+str(angle)+'.txt')
        #
        a,b, img, rotated_img=getRotatedImg(angle,img_path,img_write_path)
        getRotatedAnno(Pi_angle,a,b,anno_path,anno_write_path, img, rotated_img)


parser = argparse.ArgumentParser(description='命令行参数')
parser.add_argument('--input_img', '-ii', type=str, help='原始图片的地址')
parser.add_argument('--input_anno', '-ia', type=str, help='原始标签的地址')
parser.add_argument('--output_img', '-oi', type=str, help='增强后图片的地址')
parser.add_argument('--output_anno', '-oa', type=str, help='增强后标签的地址')
parser.add_argument('--min_angle', type=int, default=-10, help='最小角度（角度制）')
parser.add_argument('--max_angle', type=int, default=10, help='最大角度（角度制）')
parser.add_argument('--angle_step', type=int, default=1, help='角度步长（角度制）')


args = parser.parse_args()
img_dir = args.input_img
anno_dir = args.input_anno
img_write_dir = args.output_img
anno_write_dir = args.output_anno

min_angle = args.min_angle
max_angle = args.max_angle
angle_step = args.angle_step

for angle in range(min_angle, max_angle, angle_step):
    if angle == 0:
        pass
    else:
        print('start rotate with angle = ' + str(angle))
        rotate(angle, img_dir, anno_dir, img_write_dir, anno_write_dir)
