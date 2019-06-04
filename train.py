import data
import argparse
from model import EDSR
parser = argparse.ArgumentParser()
parser.add_argument("--dataset",default="data/General-100")
parser.add_argument("--imgsize",default=200,type=int)
parser.add_argument("--scale",default=4,type=int)#实际输入网络的图片大小为imgsize/scale
<<<<<<< HEAD
parser.add_argument("--layers",default=16,type=int)
parser.add_argument("--featuresize",default=64,type=int)
parser.add_argument("--batchsize",default=4,type=int)
=======
parser.add_argument("--layers",default=32,type=int)
parser.add_argument("--featuresize",default=256,type=int)
parser.add_argument("--batchsize",default=16,type=int)
>>>>>>> be1f4ebbf16b0ed6d9d5dcf1b7685ddbe126b99d
parser.add_argument("--savedir",default='saved_models')
parser.add_argument("--iterations",default=6000,type=int)
args = parser.parse_args()
data.load_dataset(args.imgsize,args.imgsize//args.scale)

if args.imgsize % args.scale != 0:
    #print(f"Image size {args.imgsize} is not evenly divisible by scale {args.scale}")
    exit()
down_size = args.imgsize//args.scale#实际输入网络训练的大小
network = EDSR(down_size,args.layers,args.featuresize,args.scale)

network.set_train_data_fn(data.get_batch,(args.batchsize,args.imgsize//args.scale,'train'))
network.set_val_data_fn(data.get_batch,(args.batchsize,args.imgsize//args.scale,'val'))

network.train(args.iterations,args.savedir)
