# -*- coding: utf-8 -*-
"""
Time:     2023/3/8 9:42
Author:   cjn
Version:  1.0.0
File:     json2txt.py
Describe: 
"""
import json
import os
import argparse


def convert(img_w, img_h, box):
    x = (box[0] + box[2]) / 2.0 - 1
    y = (box[1] + box[3]) / 2.0 - 1
    w = box[2] - box[0]
    h = box[3] - box[1]
    x = x / img_w
    w = w / img_w
    y = y / img_h
    h = h / img_h
    return (x, y, w, h)


def decode_json(json_path, json_name, txt_path):
    txt_name = json_name[0:-5] + '.txt'
    txt_file = os.path.join(txt_path, txt_name)
    f = open(txt_file, 'w')

    json_file = os.path.join(json_path, json_name)
    data = json.load(open(json_file, 'r', encoding='gb2312', errors='ignore'))

    img_w = data['imageWidth']
    img_h = data['imageHeight']

    for i in data['shapes']:

        label_name = i['label']
        if (i['shape_type'] == 'rectangle'):
            x1 = i['points'][0][0]
            y1 = i['points'][0][1]
            x2 = i['points'][1][0]
            y2 = i['points'][1][1]

            bb = (x1, y1, x2, y2)
            bbox = convert(img_w, img_h, bb)
            f.write(label_name + " " + " ".join([str(a) for a in bbox]) + '\n')
        else:
            print('ERROR: Not Rectangle!')


# 下面default后可以输入默认的路径，输入后不需要命令行中添加路径
parser = argparse.ArgumentParser(description='命令行参数')
parser.add_argument('--json_path', '-j', type=str, default='', help='json标签的地址')
parser.add_argument('--txt_path', '-t', type=str, default='', help='txt标签的地址')


if __name__ == "__main__":
    args = parser.parse_args()
    json_path = args.json_path
    txt_path = args.txt_path

    if not os.path.exists(txt_path):
        os.makedirs(txt_path)

    json_names = os.listdir(json_path)
    for json_name in json_names:
        decode_json(json_path, json_name, txt_path)

