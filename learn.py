import os
import re
import cv2
import data
import pickle

list_file = open("input_set.pickle",'rb')
list = pickle.load(list_file)

print(len(list))



