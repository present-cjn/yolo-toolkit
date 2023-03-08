# yolo-toolkit
一些处理yolv的小工具

## Prepare

```shell
git clone https://github.com/present-cjn/yolo-toolkit.git
cd yolo-toolkit
pip install -r requirements.txt
```

## 数据增强
旋转一定角度

需要四个路径，可以在代码中更改default值，如果不想改代码，可以在命令行输入

分别如下：

'--input_img'或'-ii'：'原始图片的地址'

'--input_anno'或'-ia'：'原始标签的地址'

'--output_img'或'-oi'：'旋转后图片的地址'

'--output_anno'或'-oa'：'旋转后标签的地址'

例：
```python
python data_aug.py --input_img D:/xuanzuan/image -ia D:/xuanzuan/label2 -oi D:/xuanzuan/out_image -oa D:/xuanzuan/out_label
```
也可以设置起始的旋转角度（默认-10到10度），如果要设置成-15到15，则输入
```python
python data_aug.py --input_img D:/xuanzuan/image -ia D:/xuanzuan/label2 -oi D:/xuanzuan/out_image -oa D:/xuanzuan/out_label --min_angle -15 --max_angle 15
```

## 图上显示txt框
需要指定图片和标签的路径，可以在代码中更改default值

然后运行
```python
python display_box_txt.py
```
如果不想改代码，可以在命令行输入路径
```python
python display_box_txt.py --input_img E:\data\images --input_anno E:\data\labels
```

# json转txt
需要指定json文件夹的路径和txt文件夹的路径，可以在代码中更改default值

然后运行
```python
python json2txt
```
如果不想改代码，可以在命令行输入路径
```python
 python display_box_txt.py --input_img D:\xuanzuan\label --input_anno D:\xuanzuan\label2    
```