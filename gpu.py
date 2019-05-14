import tensorflow as tf
import utils
import cv2
import numpy as np
np.set_printoptions(threshold=np.inf)

g1 = tf.Graph()
with g1.as_default():
    a = tf.constant([[[[1,5,9,13],[2,6,10,14]],[[3,7,11,15],[4,8,12,16]]],[[[17,21,25,29],[18,22,26,30]],[[19,23,27,31],[20,24,28,32]]]],name = "a")
    b = tf.constant([[[1,2,3],[4,5,6]],[[7,8,9],[10,11,12]]])
    #a_shape = tf.reshape(a,[3,2],name = "reshape")
with tf.Session(graph = g1) as sess:
    print(sess.run(tf.transpose(b,[2,1,0])))
    print(sess.run(utils._phase_shift(a,2)))






