import os
import re
import cv2
import data
import pickle
from tqdm import tqdm
import random




#装饰器函数
# def physical_pra(sex):
#     def physical(be_func):
#         print('enter deco_pro')
#         def func2():
#             if(sex == 'man'):
#                 print("strong")
#             if(sex == 'woman'):
#                 print("weak")
#
#             return be_func()
#         return func2
#     return physical
#
# @physical_pra(sex='man')
# def man():
#     print("man work hard")
# @physical_pra(sex='woman')
# def woman():
#     print("woman work hard")

def physical(be_func):

    def func2():
        print("human being")

        return be_func()
    return func2

@physical
def man():
    print("man work hard")
@physical
def woman():
    print("woman work hard")



