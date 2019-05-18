"""
code:subpixel shuffle code explanation

use:help to understand how to conduct subpixel shuffle in matrix
"""

import tensorflow as tf
import cv2
import numpy as np
np.set_printoptions(threshold=np.inf)
g1 = tf.Graph()

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

im1 = cv2.imread("yuvH1_bmp/1.bmp")
print(im1.shape)
im2 = cv2.imread("output_im_1.bmp")
print(im2.shape)
print(5//3)
img = []
img.append((1,2))
print(type(img[0]))




