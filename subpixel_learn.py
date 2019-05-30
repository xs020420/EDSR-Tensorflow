"""
code:subpixel shuffle code explanation

use:help to understand how to conduct subpixel shuffle in matrix
"""

import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(threshold=np.inf)


def _phase_shift(I, r):
    with tf.Session(graph=g1) as sess:
        bsize, a, b, c = I.get_shape().as_list() #get_shape返回一个元祖
        bsize = tf.shape(I)[0] # Handling Dimension(None) type for undefined batch dim
        X = tf.reshape(I, (bsize, a, b, r, r))
        print("reshape:",sess.run(X))
        X = tf.transpose(X, (0, 1, 2, 4, 3))  # bsize, a, b, 1, 1
        print("transpose:",sess.run(X))
        X = tf.split(X, a, 1)  # a, [bsize, b, r, r]#split后产生两个array
        print("split:",sess.run(X))
        X = tf.concat([tf.squeeze(x, axis=1) for x in X],2)  # bsize, b, a*r, r
        print("concat:",sess.run(X))
        X = tf.split(X, b, 1)  # b, [bsize, a*r, r]
        print("split:",sess.run(X))
        X = tf.concat([tf.squeeze(x, axis=1) for x in X],2)  # bsize, a*r, b*r
        print("concat:",sess.run(X))
        result =tf.reshape(X, (bsize, a*r, b*r, 1))
        print("result", sess.run(result))
        return result

def subpixel_test():
    with g1.as_default():
        a = tf.constant([[[[1,5,9,13],[2,6,10,14]],[[3,7,11,15],[4,8,12,16]]],[[[17,21,25,29],[18,22,26,30]],[[19,23,27,31],[20,24,28,32]]]],name = "a")
        b = tf.constant([[[1,2,3],[4,5,6]],])

    with tf.Session(graph=g1) as sess:
        print(sess.run(tf.transpose(b,[2,0,1])))
        print(sess.run(tf.squeeze(b, axis=0)))
    print((_phase_shift(a,2)))

def log10(x):
  numerator = tf.log(x)
  denominator = tf.log(tf.constant(10, dtype=numerator.dtype))
  return numerator / denominator

def image_psnr(image_target,image_output):
    g1 = tf.Graph()
    with g1.as_default():

        if(image_target.shape != image_output.shape):
            print("same shape of ndarray is required")

        image_height = image_target.shape[0]
        image_width = image_target.shape[1]
        output_channels = image_target.shape[2]

        target = tf.placeholder(tf.float32, [image_height, image_width, output_channels])
        output = tf.placeholder(tf.float32, [image_height, image_width, output_channels])

        print(target[0].shape)

        mse = tf.reduce_mean(tf.squared_difference(target, output))
        PSNR = tf.constant(255 ** 2, dtype=tf.float32) / mse
        PSNR_db = tf.constant(10, dtype=tf.float32) *log10(PSNR)
    with tf.Session(graph=g1) as sess:
        print(sess.run(PSNR_db,feed_dict ={target : image_target,output: image_output}))



#几个加权系数0.3,0.59,0.11是根据人的亮度感知系统调节出来的参数，是个广泛使用的标准化参数,用于
def bgr2gray(image_bgr):
    row = image_bgr.shape[0]
    col = image_bgr.shape[1]
    image_gray = np.zeros((row,col))
    for r in range(row):
        for l in range(col):
            image_gray[r, l] = 0.11 * image_bgr[r, l, 0] + 0.59 * image_bgr[r, l, 1] + 0.3 * image_bgr[r, l, 2]
    return image_gray

#使用差异度hash计算图像相似度
def dhash(grayscale_image,resized_height = 9,resized_width = 8):
    # pixels = list(grayscale_image.getdata())
    # difference = []
    # for row in range(resized_height):
    #     row_start_index = row * resized_width
    #     for col in range(resized_width - 1):
    #         left_pixel_index = row_start_index + col
    #         difference.append(pixels[left_pixel_index] > pixels[left_pixel_index + 1])
    rows = grayscale_image.shape[0]
    cols = grayscale_image.shape[1]
    difference = []
    for row in range(rows):
        for col in range(cols-1):
            difference.append(grayscale_image[row,col]>grayscale_image[row,col+1])
    print(difference)
    decimal_value = 0
    hash_string = ""
    for index, value in enumerate(difference):
        if value:  # value为0, 不用计算, 程序优化
            decimal_value += value * (2 ** (index % 8))
        if index % 8 == 7:  # 每8位的结束
            hash_string += str(hex(decimal_value)[2:].rjust(2, "0"))  # 不足2位以0填充。0xf=>0x0f
            decimal_value = 0
    print(hash_string)
    return hash_string

def hanming_distance(dhash_1,dhash_2):
    difference = (int(dhash_1, 16)) ^ (int(dhash_2, 16))
    return bin(difference).count("1")

src_path = r'out\target_1.bmp'
dest_path = 'out\output_1.bmp'
image_target=cv2.imread(src_path).astype(np.float32)
output = cv2.imread(dest_path).astype(np.float32)
other = cv2.imread("correct0.png").astype(np.float32)



tmp_output  = cv2.resize(output,(9,8))
tmp_target  = cv2.resize(image_target,(9,8))
tmp_other = cv2.resize(other,(9,8))


tmp_gray_target = bgr2gray(tmp_target)
tmp_gray_output = bgr2gray(tmp_output)
tmp_gray_other = bgr2gray(tmp_other)

dis_similar = hanming_distance(dhash(tmp_gray_target),dhash(tmp_gray_output))
dis_difference = hanming_distance(dhash(tmp_gray_target),dhash(tmp_gray_other))
print(dis_similar,dis_difference)
#使用hash方法来初步检索出图片库中的相似帧
rgb = image_target[...,::-1].astype(np.int32)
plt.imshow(rgb[...,::-1].astype(np.int32))

plt.show()