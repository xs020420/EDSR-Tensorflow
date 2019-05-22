import os
import re
youku_data_path = 'D:\ly\youku'
train_single_dir_list =[]
test_single_dir_list =[]

#找到以single结尾的文件夹，存放有所有单张图片的数据集
for filename in os.listdir(youku_data_path):
    if filename.endswith('single'):
        print(os.path.join(youku_data_path,filename))

        if(re.search(r'00249', filename) == None):
            train_single_dir_list.append(os.path.join(youku_data_path,filename))
        elif:

            else:
            test_single_dir_list.append(os.path.join(youku_data_path,filename))


#找到测试集文件夹和训练集文件夹，测试集较大，所以有多个文件夹。使用正则表达式根据数字查找


