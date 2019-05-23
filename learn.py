import os
import re
import cv2
youku_data_path = 'D:\ly\youku'
train_low_single_dir_list =[]
train_high_single_dir_list =[]
test_low_single_dir_list =[]
#找到测试集文件夹和训练集文件夹，测试集较大，所以有多个文件夹。使用正则表达式根据数字查找
for filename in os.listdir(youku_data_path):
    if filename.endswith('single'):#寻找存放单张图片的文件夹
        filepath = os.path.join(youku_data_path,filename)

        if(re.search(r'_00249_', filename) == None):#如果是训练集
            if(re.search(r'_l_', filename) != None):#如果是低清文件夹
                train_low_single_dir_list.append(filepath)
            if(re.search(r'_h_', filename) != None):
                train_high_single_dir_list.append(filepath)
        else:
            test_low_single_dir_list.append(filepath)
img = cv2.imread("1.bmp")
print(img.shape)







