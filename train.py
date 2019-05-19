import data
import argparse
from model import EDSR
parser = argparse.ArgumentParser()
parser.add_argument("--dataset",default="data/General-100")
parser.add_argument("--imgsize",default=200,type=int)
parser.add_argument("--scale",default=4,type=int)#实际输入网络的图片大小为imgsize/scale
parser.add_argument("--layers",default=32,type=int)
parser.add_argument("--featuresize",default=256,type=int)
parser.add_argument("--batchsize",default=5,type=int)
parser.add_argument("--savedir",default='saved_models')
parser.add_argument("--iterations",default=1000,type=int)
args = parser.parse_args()
data.load_dataset(args.dataset,args.imgsize)
if args.imgsize % args.scale != 0:
    #print(f"Image size {args.imgsize} is not evenly divisible by scale {args.scale}")
    exit()
down_size = args.imgsize//args.scale#实际输入网络训练的大小
network = EDSR(down_size,args.layers,args.featuresize,args.scale)
network.set_data_fn(data.get_batch,(args.batchsize,args.imgsize,down_size),data.get_test_set,(args.imgsize,down_size))
network.train(args.iterations,args.savedir)
