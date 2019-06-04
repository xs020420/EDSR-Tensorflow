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




src_path = r'out\input_Youku_00200_l-0001.bmp'
dest_path = 'out\output_Youku_00200_l-0001.bmp'
image_target=cv2.imread(src_path).astype(np.float32)
output = cv2.imread(dest_path).astype(np.float32)

print(image_psnr(image_target,output))

