from model import EDSR
import scipy.misc
import argparse
import data
import os
from tqdm import tqdm
import random

parser = argparse.ArgumentParser()
parser.add_argument("--dataset",default="data/General-100")
parser.add_argument("--imgsize",default=200,type=int)
parser.add_argument("--scale",default=4,type=int)
parser.add_argument("--layers",default=32,type=int)
parser.add_argument("--featuresize",default=256,type=int)
parser.add_argument("--batchsize",default=10,type=int)
parser.add_argument("--savedir",default="saved_models")
parser.add_argument("--iterations",default=1000,type=int)
parser.add_argument("--numimgs",default=5,type=int)
parser.add_argument("--outdir",default="out")
parser.add_argument("--image",default = "Youku_00200_l-0001.bmp")
parser.add_argument("--testdir",default = "D:\ly\youku\youku_00150_00199_l_single")

args = parser.parse_args()
# if not os.path.exists(args.outdir):
# 	os.mkdir(args.outdir)
down_size = args.imgsize//args.scale
network = EDSR(down_size,args.layers,args.featuresize,scale=args.scale)
network.resume(args.savedir)

test_single_savedir = "D:\ly\youku\youku_00200_00249_h_GT_single"#保存测试集单张图片结果的文件夹
if not os.path.exists(test_single_savedir):
	os.mkdir(test_single_savedir)

test_sample_list = os.listdir(args.testdir)#测试集文件夹
print(test_sample_list)


"""
计算验证集上的psnr
由于验证集过大，采用抽样取均值
"""
def validation_psnr():
	psnr_list = []  # 计算psnr，应该是要在训练的时候计算的，这里就简单做下线下测试
	validation_input_path = "D:\ly\youku\youku_00150_00199_l"
	validation_output_path = "D:\ly\youku\youku_00150_00199_h_GT"
	validation_sample_list = os.listdir(validation_input_path)
	sample_num = random.randint(0, len(validation_sample_list))
	sample = validation_sample_list[sample_num]
	image_list = os.listdir(validation_input_path+'/'+sample)
	for i in range(5):



	validation_sample = os.listdir()




"""
对测试集图片超分
前10%完整超分，后90%抽样超分
"""
def test_image_generate():
	for sample in tqdm(test_sample_list):
		if not os.path.exists(os.path.join(test_single_savedir, sample)):
			os.mkdir(os.path.join(test_single_savedir, sample))
		else:
			continue
		image_list = os.listdir(os.path.join(args.testdir,sample))
		for i,image in enumerate(image_list):
			if(i%25 == 0):
				x = scipy.misc.imread(os.path.join(args.testdir,sample,image))
				inputs = x
				outputs = network.predict(x)
				scipy.misc.imsave(os.path.join(test_single_savedir,sample,image),outputs)




# if args.image:
# 	x = scipy.misc.imread(args.image)
# else:
# 	print("No image argument given")
# inputs = x
# outputs = network.predict(x)
# if args.image:
# 	scipy.misc.imsave(args.outdir+"/input_"+args.image,inputs)
# 	scipy.misc.imsave(args.outdir+"/output_"+args.image,outputs)
