import scipy.misc
import random
import numpy as np
import os
import math
import re
from tqdm import tqdm
import pickle
import hash
import cv2

input_set = []
target_set = []
train_set =[]

batch_index = 0
hash_threshold =15
youku_data_path = 'D:\ly\youku'
train_low_single_dir_list = []
train_high_single_dir_list = []
test_low_single_dir_list = []


"""
Get image path according
to a block dir
For example:inputdata/block1/sample_dir/image_path

"""
def get_image_list(dir_list):
	image_list = []
	for block_dir in dir_list:  # block_dir:D:\ly\youku\youku_00000_00049_l_single
		for sample_dir in os.listdir(block_dir):  # sample_dir:Youku_00000_l
			for image_path in os.listdir(os.path.join(block_dir, sample_dir)):  # Youku_00000_l-0001.bmp
				image_list.append(os.path.join(block_dir, sample_dir,image_path))
	print(len(image_list))
	return image_list


"""
Get image block list
and make input and target list
and
return input_list and target_list
"""
def load_dataset(high_size,low_size):
	# 找到测试集文件夹和训练集文件夹，测试集较大，所以有多个文件夹。使用正则表达式根据数字查找
	for filename in os.listdir(youku_data_path):
		if filename.endswith('single'):  # 寻找存放单张图片的文件夹
			filepath = os.path.join(youku_data_path, filename)

			if (re.search(r'_00249_', filename) == None):  # 如果是训练集
				if (re.search(r'_l_', filename) != None):  # 如果是低清文件夹
					train_low_single_dir_list.append(filepath)
				if (re.search(r'_h_', filename) != None):
					train_high_single_dir_list.append(filepath)
			else:
				test_low_single_dir_list.append(filepath)

	# 读取input和target文件目录，并存入列表
	print(train_low_single_dir_list)
	print(train_high_single_dir_list)
	print(test_low_single_dir_list)

	input_list = get_image_list(train_low_single_dir_list)
	target_list = get_image_list(train_high_single_dir_list)

	global input_set#在函数内部改变外部全局变量时候，要先用global申明
	global target_set
	global train_set

	try:
		list_file = open('input_set.pickle', 'rb')
		input_set = pickle.load(list_file)
		list_file = open('target_set.pickle', 'rb')
		target_set = pickle.load(list_file)
		list_file = open('train_set.pickle', 'rb')
		train_set = pickle.load(list_file)
	except:
		# 先进行hash编码，去除相似帧。由于相似帧大多连续，只和上一帧图进行比较。
		print("dhash encoding")

		input_afterhash_list = []
		target_afterhash_list = []

		image_index=[]
		distance = []
		str_last = ""

		for i,img in tqdm(enumerate(input_list)):  # image_path_list
			tmp = cv2.imread(img)
			tmp = cv2.resize(tmp,(9,8))
			str_current = hash.dhash(hash.bgr2gray(tmp))
			if(i==0):
				str_last =str_current
				input_afterhash_list.append(img)
				image_index.append(i)
			else:
				dis = hash.hanming_distance(str_last,str_current)
				if(dis <= hash_threshold):
					pass
				else:
					input_afterhash_list.append(img)
					image_index.append(i)
				str_last = str_current
				distance.append(dis)

		#将经过dhash后，未分块的list保存下来
		list_file = open('input_afterhash_list.pickle', 'wb')
		pickle.dump(input_afterhash_list, list_file)
		list_file.close()

		list_file = open('distance.pickle', 'wb')
		pickle.dump(distance, list_file)
		list_file.close()

		#根据image_index对高清图进行筛选
		for i,img in tqdm(enumerate(target_list)):  # image_path_list
			if i in image_index:
				target_afterhash_list.append(img)
			else:
				pass

		list_file = open('target_afterhash_list.pickle', 'wb')
		pickle.dump(target_afterhash_list, list_file)
		list_file.close()

		#以下是分块代码，分好块后，以（image_path,块名）的元祖存入列表。
		for img in tqdm(input_afterhash_list):#image_path_list
			try:
				tmp= scipy.misc.imread(img)
				x,y,z = tmp.shape
				coords_x = x / low_size
				coords_y = y/low_size
				coords = [ (q,r) for q in range(math.floor(coords_x)) for r in range(math.floor(coords_y)) ]#等价于两个嵌套for循环
				for coord in coords:
					input_set.append((img,coord))#添加元祖
			except:
				print("oops")

		for img in tqdm(target_afterhash_list):#image_path_list
			try:
				tmp= scipy.misc.imread(img)
				x,y,z = tmp.shape
				coords_x = x / high_size
				coords_y = y/high_size
				coords = [ (q,r) for q in range(math.floor(coords_x)) for r in range(math.floor(coords_y)) ]#等价于两个嵌套for循环
				for coord in coords:
					target_set.append((img,coord))#添加元祖
			except:
				print("oops")

		#使用元祖列表保存input和target对

		for i in range(len(input_set)):
			tmp = (input_set[i],target_set[i])
			train_set.append(tmp)

		list_file = open('train_set.pickle','wb')
		pickle.dump(train_set,list_file)
		list_file.close()

		list_file = open('input_set.pickle','wb')
		pickle.dump(input_set,list_file)
		list_file.close()

		list_file = open('target_set.pickle','wb')
		pickle.dump(target_set,list_file)
		list_file.close()
	return

"""
Get test set from the loaded dataset

size (optional): if this argument is chosen,
each element of the test set will be cropped
to the first (size x size) pixels in the image.

returns the test set of your data
"""

def get_image(imgtuple,size,scale):#获取分块后的图片，scale为低清图片到高清素片的放大倍数
	assert scale in [1,2, 3, 4]
	img = scipy.misc.imread(imgtuple[0])
	x,y = imgtuple[1]
	img = img[x*size*scale:(x+1)*size*scale,y*size*scale:(y+1)*size*scale]
	return img
	

"""
Get a batch of images from the training
set of images.

batch_size: size of the batch
original_size: size for target images
shrunk_size: size for shrunk images

returns x,y where:
	-x is the input set of shape [-1,shrunk_size,shrunk_size,channels]
	-y is the target set of shape [-1,original_size,original_size,channels]
"""
def get_batch(batch_size,original_size):#制作训练图片对（input和target），使用了分块
	global batch_index
	"""img_indices = random.sample(range(len(train_set)),batch_size)
	for i in range(len(img_indices)):
		index = img_indices[i]
		img = scipy.misc.imread(train_set[index])
		if img.shape:
			img = crop_center(img,original_size,original_size)
			x_img = scipy.misc.imresize(img,(shrunk_size,shrunk_size))
			x.append(x_img)
			y.append(img)"""
	max_counter = len(target_set)/batch_size
	counter = batch_index % max_counter
	#每进行新的epoch，shuffle一次数据集
	if(counter == 0):
		random.shuffle(train_set)

	window = [x for x in range(int(counter*batch_size),int((counter+1)*batch_size))]#range(a,b)左闭右开,[0,1,2,3,4]
	imgs_input = [train_set[q][0] for q in window]#target 中为输入输出对，元素为元祖的列表
	imgs_target= [train_set[q][1] for q in window]
	x = [get_image(q,original_size,scale = 1) for q in imgs_input]#scipy.misc.imread(q[0])[q[1][0]*original_size:(q[1][0]+1)*original_size,q[1][1]*original_size:(q[1][1]+1)*original_size].resize(shrunk_size,shrunk_size) for q in imgs]
	y = [get_image(q,original_size,scale = 4) for q in imgs_target]#scipy.misc.imread(q[0])[q[1][0]*original_size:(q[1][0]+1)*original_size,q[1][1]*original_size:(q[1][1]+1)*original_size] for q in imgs]
	batch_index = (batch_index+1)%max_counter
	return x,y

"""
Simple method to crop center of image

img: image to crop
cropx: width of crop
cropy: height of crop
returns cropped image
"""
def crop_center(img,cropx,cropy):
	y,x,_ = img.shape
	startx = random.sample(range(x-cropx-1),1)[0]#x//2-(cropx//2)
	starty = random.sample(range(y-cropy-1),1)[0]#y//2-(cropy//2)
	return img[starty:starty+cropy,startx:startx+cropx]







