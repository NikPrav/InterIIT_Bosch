import numpy as np
import torch.nn.functional as F
import torch
import torch.nn as nn
from torchvision import datasets, transforms
import sys
import time
import os
from models import Vanilla_Net
import matplotlib.pyplot as plt
import aug


def infer(img_loc,model,device):
	''' 
	Outputs the top 3 possible classes with their respective probabilities for a single image

	Args:
		img_loc: location of the image
		model: model to be used
		device: device to run the model on
	'''

	img = plt.imread(img_loc)
	img = aug.resize(img,32)
	x = img.reshape([1,img.shape[2],img.shape[0],img.shape[1]])
	x = torch.Tensor(x)
	x = x.to(device)
	y = model(x)
	y = np.exp(y[0].cpu().detach().numpy())
	clss = y.argsort()[-3:][::-1]
	prob = y[clss]
	return clss, prob


def infer_mult(loc,Net,loc_model,device,num_cls):
	''' 
	Outputs the top 3 possible classes with their respective probabilities for all the images

	Args:
		loc: location of the folder in which images are stored for testing
		Net: the model architecture to be used
		loc_model: location of the saved model parameters
		device: device to run the model on
		num_cls: number of classes to predict
	'''
	model = Net(num_cls).to(device)
	model.load_state_dict(torch.load(loc_model, map_location = 'cpu'))
	res = []
	i = 0
	for img_loc in os.listdir(loc):
		res.append(infer(loc+'/'+img_loc,model,device))
		print(i)
		i += 1
		if i==100:
			break
	return res