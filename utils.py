# -*- coding: utf-8 -*-
"""
Time:     2023/3/6 15:54
Author:   cjn
Version:  1.0.0
File:     utils.py
Describe: 
"""


def yolobox2cvrect(box, img):
    h, w = img.shape[:2]
    cx = float(box[1])
    cy = float(box[2])
    bw = float(box[3])
    bh = float(box[4])
    x1 = (cx - bw / 2) * w
    y1 = (cy - bh / 2) * h
    x2 = (cx + bw / 2) * w
    y2 = (cy + bh / 2) * h
    return [x1, y1, x2, y2]


def cvrect2yolobox(rect, img, label):
    h, w = img.shape[:2]
    x1, y1, x2, y2 = rect
    bw = (x2-x1)/w
    bh = (y2-y1)/h
    cx = x1/w + bw/2
    cy = y1/h + bh/2
    return [label, cx, cy, bw, bh]