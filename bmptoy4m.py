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
import cv2
import glob


"""

终端输入： ffmpeg -f image2 -i /home/ttwang/images/image%d.jpg tt.mp4

其中/home/ttwang/images/images%d.jpg 为图片路径
图片的命名格式为image%d.jpg形式，即：image0 image1 image2 .......
tt.mp4为输出视频文件名
"""

def imgs2video(imgs_dir, save_name,):


    fps = 24
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video_writer = cv2.VideoWriter('C:/Users/lcx/python_exercise/video/1.avi', fourcc, fps, (1920, 1080))
    imgs = glob.glob(os.path.join('C:/Users/lcx/python_exercise/train_1/Youku_00000_l', '*.bmp'))
    print(len(imgs))

    for i in range(len(imgs)):
        imgname = os.path.join('C:/Users/lcx/python_exercise/train_1/Youku_00000_l',
                               'Youku_00000_l-{:04d}.bmp'.format(i))
        frame = cv2.imread(imgname)
        video_writer.write(frame)

    video_writer.release()

def generate_y4m(src_path, target_path):
    new_path = target_path

    for sample in tqdm(os.listdir(src_path)):
        sample_dir = src_path + sample
        y4mfile = new_path + sample.split('_')[0] + '_'+sample.split('_')[1]+"_h_Res.y4m"
        i = 0
        print(y4mfile,sample_dir)
        imgs2video(sample_dir,y4mfile)
        # for image in os.listdir(sample_dir):
        #     src = os.path.join(sample_dir, image)
        #     dst = os.path.join(sample_dir, str(i) + '.bmp')
        #     os.rename(src, dst)
        #     print('converting %s to %s ...' % (src, dst))
        #     i = i + 1

        # os.system("cd %s"%(sample_dir))
        # #
        # os.system("ffmpeg -r 24 -i %3d.bmp  -pix_fmt yuv420p  -vsync 0 %s -y"%(y4mfile))




# 这里我都用的绝对路径，在执行文件的建两个文件，一个放y4m的源文件train，还有一个就是放生成bmp的文件夹test1
generate_y4m(src_path='D:/ly/youku/youku_00200_00249_h_GT_single/', target_path='D:/ly/youku/outputy4m/')
