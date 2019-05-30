import numpy as np
import cv2
"""
几个加权系数0.3,0.59,0.11是根据人的亮度感知系统调节出来的参数，
是个广泛使用的标准化参数,用于bgr图像转灰度值图像
"""
def bgr2gray(image_bgr):
    row = image_bgr.shape[0]
    col = image_bgr.shape[1]
    image_gray = np.zeros((row,col))
    for r in range(row):
        for l in range(col):
            image_gray[r, l] = 0.11 * image_bgr[r, l, 0] + 0.59 * image_bgr[r, l, 1] + 0.3 * image_bgr[r, l, 2]
    return image_gray


"""
使用差异度hash计算图像相似度
返回16位的hash编码
"""
def dhash(grayscale_image):

    rows = grayscale_image.shape[0]
    cols = grayscale_image.shape[1]
    difference = []
    for row in range(rows):
        for col in range(cols-1):
            difference.append(grayscale_image[row,col]>grayscale_image[row,col+1])
    #print(difference)
    decimal_value = 0
    hash_string = ""
    for index, value in enumerate(difference):
        if value:  # value为0, 不用计算, 程序优化
            decimal_value += value * (2 ** (index % 8))
        if index % 8 == 7:  # 每8位的结束
            hash_string += str(hex(decimal_value)[2:].rjust(2, "0"))  # 不足2位以0填充。0xf=>0x0f
            decimal_value = 0
    #print(hash_string)
    return hash_string


"""
输入两个16位的hash编码，
计算其汉明距离,
"""
def hanming_distance(dhash_1,dhash_2):
    difference = (int(dhash_1, 16)) ^ (int(dhash_2, 16))
    return bin(difference).count("1")