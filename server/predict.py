import numpy as np
import torch.nn.functional as F
import torch
import torch.nn as nn
from torchvision import datasets, transforms
import sys
import time
import os
from models import Net
import matplotlib.pyplot as plt
import aug


def predict(img_loc,w_loc,sv_model,device='cpu'):
	''' 
	Outputs the top 3 possible classes with their respective probabilities for a single image

	Args:
		img_loc: location of the image
		model: model to be used
		device: device to run the model on
	'''
	num_classes = len(os.listdir(os.path.join(w_loc,'images')))
	model = Net(num_classes).to(device)
	model.load_state_dict(torch.load(sv_model, map_location = 'cpu'))
	img = plt.imread(img_loc)
	img = aug.resize(img,32)
	x = img.reshape([1,img.shape[2],img.shape[0],img.shape[1]])
	x = torch.Tensor(x)
	x = x.to(device)
	y = model(x)
	y = np.exp(y[0].cpu().detach().numpy())
	clss = y.argsort()[-3:][::-1]
	prob = y[clss]
	
	temp = img_loc.split("/")[:-2]
	path = "/"
	for i in temp:
		path = os.path.join(path, i)
	
	f = os.listdir(path)
	sf = sorted(f, key=int)

	classes = {}
	l = 0
	for i in sf:
		classes[l] = int(i)
		l += 1
	# print(classes)
	data = []
	with open("class.csv", 'r') as f:
		data = [i.replace("\n", "").split(",") for i in f.readlines()]
		data = [[int(i[0]), i[1]] for i in data]
	# print(data)
	clas = {}
	for i in range(3):
		clas[data[classes[clss[i]]][1]] = prob[i]
	
	return clas

def predict_mult(loc,Net,loc_model,device,num_cls):
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


# x = predict('/home/scitech/Inter_IIT_2021/default_workspace_1/images/00000/00003_00002.ppm','/home/scitech/Inter_IIT_2021/default_workspace_1/','models/model_0_0.9679586563307494')
# print(x)