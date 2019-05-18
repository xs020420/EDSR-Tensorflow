import torch
import os
print(torch.cuda.is_available())

def vediotoimage(video_path,image_path):
    img_count = 1
    crop_time = 0.0
    while crop_time <= 5.0:#转化15s的视频
        os.system('ffmpeg -i %s -f image2 -ss %s -vframes 1 %s.png'% (video_path, str(crop_time), video_path+ str(img_count)))
        img_count += 1
        print('Geting Image ' + str(img_count) + '.png' + ' from time ' + str(crop_time))
        crop_time += 1#每0.1秒截取一张照片
    print('视频转化完成！！！')

def y4mtoyuv():
    name = "Youku_00000_l"
    dir_path = r'D:\\"Program Files"\\youku'

    path = os.path.join(dir_path,name)
    print(path)
    #os.system("ffmpeg -i %s.y4m -vsync 0 %s.yuv "%(path,"001"))
    os.system("ffmpeg -i Youku_00000_h_GT.y4m  yuvH1_bmp/%d.bmp")

y4mtoyuv()