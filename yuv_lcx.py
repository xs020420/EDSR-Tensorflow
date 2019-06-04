import PIL.Image as Image
import pylab
#import imageio
#这段代码执行一次就好，下载ffmpeg工具完把这一行注释掉
#imageio.plugins.ffmpeg.download()
import skimage
import numpy as np
import os
from subprocess import call#python 子进程模块
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt


def extract_frames(src_path, target_path):
    new_path = target_path

    for video_name in tqdm(os.listdir(src_path)):
        # video_name = "Youku_00000_l.y4m"
        filename = src_path + video_name
        cur_new_path = new_path + video_name.split('.')[0] + '/'
        if not os.path.exists(cur_new_path):
            os.mkdir(cur_new_path)

        dest = cur_new_path + video_name.split('.')[0] + '-%04d.bmp'
        call(["ffmpeg", "-i", filename,"-r","25", dest],shell=True)  #一帧提取
        #call(["ffmpeg", "-i", filename, "-vf", "select=not(mod(n\,25))", "-vsync", "vfr", dest], shell=True)  # 25帧提取


# 这里我都用的绝对路径，在执行文件的建两个文件，一个放y4m的源文件train，还有一个就是放生成bmp的文件夹test1
<<<<<<< HEAD
extract_frames(src_path='F:/youku/youku_00150_00199_h_GT/', target_path='D:/Program Files/youku/youku_00150_00199_h_GT_single/')
=======
extract_frames(src_path='D:/ly/youku/youku_00150_00199_l/', target_path='D:/ly/youku/youku_00150_00199_l_single/')
>>>>>>> be1f4ebbf16b0ed6d9d5dcf1b7685ddbe126b99d
