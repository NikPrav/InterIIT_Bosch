import numpy as np
import torch.nn.functional as F
import torch
import torch.nn as nn
from torchvision import datasets, transforms
import sys
import time
import pandas as pd
from __future__ import print_function
import zipfile
import os
import Net #LOAD LATEST NETWORK
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from utils import path_to_base64 #CHECK IF UTILS PATH IS CORRECT

dim = 53 #LINK NUMBER OF CLASSES



device = 'cuda'
use_gpu = True
n = 32

data_transforms = transforms.Compose([
    transforms.Resize((n, n)),
    transforms.ToTensor(),
    transforms.Normalize((0.3337, 0.3064, 0.3171), ( 0.2672, 0.2564, 0.2629))
])


model = Net(dim).to(device)
model.load_state_dict(torch.load('model_0_0.9746770025839794', map_location = 'cpu')) #LOAD LATEST MODEL


#CLASSWISE INACCURACIES
test_loader = torch.utils.data.DataLoader(
    datasets.ImageFolder('data/test_images',transform=data_transforms), #LINK TEST DATASET
    batch_size=128, shuffle=False, num_workers=1, pin_memory=use_gpu)


def test():
    model.eval()
    res = []
    for idx, (x, y) in enumerate(test_loader): 
        x = x.to(device)
        y = y.to(device)
        y_pred = model(x)
        # y_pred = y_pred
        max_index = y_pred.max(dim = -1)[1]
        max_index = max_index.cpu().detach().numpy()
        res.append(max_index)
        sys.stdout.write('\r'+str(idx)+'/'+str(len(test_loader)))
    return np.hstack(res)

df = pd.read_csv('GT-final_test.csv',delimiter = ';') #LINK GROUND TRUTH VALUES 
x2 = df['ClassId']
res = test()
print(' ')
print('Accuracy =',(np.sum(x2==res)/res.shape[0])*100,'%')
classwise = np.zeros(53)

for i in range(res.shape[0]):
  if x2[i] != res[i]:
    classwise[x2[i]] += 1

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.bar(np.arange(0, 53),classwise)
fig.savefig('class_inacc.png', bbox_inches='tight')




import captum # INSTALL CAPTUM
from captum.attr import GuidedGradCam
from matplotlib.colors import LinearSegmentedColormap
net = model
guided_gc = GuidedGradCam(net, net.conv3)



#GET CLASS OF UPLOADED IMAGE

infer_loader = torch.utils.data.DataLoader(
    datasets.ImageFolder('data/inference_images',transform=data_transforms), #SETUP INFERENCE FOLDER WITH SUBFOLDER
    batch_size=1, shuffle=False, num_workers=1, pin_memory=use_gpu)

# pred_index = -1
# for idx, (x, y) in enumerate(infer_loader): 
#     x = x.to(device)
#     y = y.to(device)
#     y_pred = model(x)
# 	# y_pred = y_pred
#     pred_index = y_pred.max(dim = -1)[1]
#     pred_index = pred_index.cpu().detach().numpy()

#GRADCAM


attrilist = []
for idx, (x, y) in enumerate(infer_loader): 
    x = x.to(device)
    y = y.to(device)
    y_pred = model(x)
    # y_pred = y_pred
    max_index = y_pred.max(dim = -1)[1]
    attrilist.append(guided_gc.attribute(x, max_index))

import cv2
from torch import tensor 
from google.colab.patches import cv2_imshow
import matplotlib.pyplot as plt


default_cmap = LinearSegmentedColormap.from_list('custom blue', 
                                                 [(0, '#ffffff'),
                                                  (0.25, '#000000'),
                                                  (1, '#000000')], N=256)


def overlay_heatmap( heatmap, image, alpha=0.5, colormap=cv2.COLORMAP_VIRIDIS):

        heatmap = cv2.applyColorMap(heatmap, colormap)
        output = cv2.addWeighted(image, alpha, heatmap, 1 - alpha, 0)
        return (heatmap, output)


for idx, (x, y) in enumerate(infer_loader):
    x = x.to(device)
    y = y.to(device)
    attri = attrilist[idx][0]
    attri = attri.permute(1,2,0)
    image = x[0].permute(1,2,0)
    original_image = image
  

    attri = attri.detach().numpy()
    attri.clip(min = 0)
    attri = (attri - np.min(attri))/ (np.max(attri) - np.min(attri))
    heatmap = cv2.applyColorMap(np.uint8(255 * attri), cv2.COLORMAP_HOT)
    heatmap = np.float32(heatmap) / 255
    cam = heatmap
    cam = cam / np.max(cam)
    cam = np.uint8(255*cam)

    f = plt.figure()
    f.add_subplot(1,2,1)
    plt.imshow(original_image.detach().numpy())
    plt.title("Original image")
    f.add_subplot(1,2,2)
    plt.imshow(cam)
    plt.title("Guided Gradcam")
    f.savefig('gradcam.png', bbox_inches='tight')


#OCCLUSION
from captum.attr import Occlusion
from captum.attr import visualization as viz
from matplotlib.colors import LinearSegmentedColormap



attrilist = []
default_cmap = LinearSegmentedColormap.from_list('custom blue', 
                                                 [(0, '#ffffff'),
                                                  (0.25, '#000000'),
                                                  (1, '#000000')], N=256)
occlusion = Occlusion(model)

for idx, (x, y) in enumerate(infer_loader): 
    x = x.to(device)
    y = y.to(device)
    y_pred = model(x)
    max_index = y_pred.max(dim = -1)[1]
    attrilist.append(occlusion.attribute(x, strides = (3, 2, 2),
                                       target=max_index,
                                       sliding_window_shapes=(3,2, 2),
                                       baselines=0))
    fig = viz.visualize_image_attr_multiple(np.transpose(attrilist[idx].squeeze().cpu().detach().numpy(), (1,2,0)),
                                      np.transpose(x.squeeze().cpu().detach().numpy(), (1,2,0)),
                                      ["original_image", "heat_map"],
                                      ["all", "absolute_value"],
                                      titles = ["Original", "Occlusion gradients"],
                                      cmap=default_cmap,
                                      show_colorbar=True, use_pyplot = False)
  
    fig[0].savefig('occlusion.png', bbox_inches='tight')


#SHAP GRADIENTS
from captum.attr import GradientShap
from captum.attr import visualization as viz
from matplotlib.colors import LinearSegmentedColormap


attrilist = []

default_cmap = LinearSegmentedColormap.from_list('custom blue', 
                                                 [(0, '#ffffff'),
                                                  (0.25, '#000000'),
                                                  (1, '#000000')], N=256)
gradient_shap = GradientShap(model)
rand_img_dist = torch.cat([x * 0, x * 1])

for idx, (x, y) in enumerate(infer_loader): 
    x = x.to(device)
    y = y.to(device)
    y_pred = model(x)
    max_index = y_pred.max(dim = -1)[1]
    attrilist.append(gradient_shap.attribute(x,
                                          n_samples=50,
                                          stdevs=0.0001,
                                          baselines=rand_img_dist,
                                          target=max_index))
    fig = viz.visualize_image_attr_multiple(np.transpose(attrilist[idx].squeeze().cpu().detach().numpy(), (1,2,0)),
                                      np.transpose(x.squeeze().cpu().detach().numpy(), (1,2,0)),
                                      ["original_image", "heat_map"],
                                      ["all", "absolute_value"],
                                      titles = ["Original", "SHAP Gradients"],
                                      cmap=default_cmap,
                                      show_colorbar=True, use_pyplot = False)
    
    fig[0].savefig('shap.png', bbox_inches='tight')

#DEEPLIFT
from captum.attr import DeepLift
from captum.attr import visualization as viz
from matplotlib.colors import LinearSegmentedColormap

def attribute_image_features(algorithm, input, y, **kwargs):
    net.zero_grad()
    tensor_attributions = algorithm.attribute(input,
                                              target=y,
                                              **kwargs
                                             )
    
    return tensor_attributions

attrilist = []


dl = DeepLift(net)


for idx, (x, y) in enumerate(infer_loader): 
    x = x.to(device)
    y = y.to(device)
    y_pred = model(x)
    max_index = y_pred.max(dim = -1)[1]
    original_image = np.transpose((x[0].cpu().detach().numpy() / 2) + 0.5, (1, 2, 0))

    attr_dl = attribute_image_features(dl,x, max_index, baselines=x * 0)
    attr_dl = np.transpose(attr_dl.squeeze(0).cpu().detach().numpy(), (1, 2, 0))
    
    fig = viz.visualize_image_attr_multiple(attr_dl,
                                      original_image,
                                      ["original_image", "blended_heat_map"],
                                      ["all", "absolute_value"],
                                      titles = ["Original", "Deeplift"],
                                      cmap=default_cmap,
                                      show_colorbar=True, use_pyplot = False)
    
    fig[0].savefig('deepl.png', bbox_inches='tight')


def plotpaths():
    filepaths = {"gradcam.png" : ["Guided Gradcam", "We use Guided Grad CAM to give the user an idea of which parts of the image contributed most to the prediction it made, whether right or wrong. In the case of a wrong prediction, the user has the option to compare the Guided Grad CAM results for both the correct and wrong classes and see what parts of the images caused the current model to classify it wrongly."] , "deepl.png" : ["DeepLift", "This is DeepLift"], "occlusion.png" : ["Occlusion", "This is Occlusion"] , "class_inacc.png" : ["Classwise Inaccuracies", "This is Classwise Inaccuracies"] , "shap.png" : ["SHAP", "This is SHAP"] }
    filepaths_final = {path_to_base64(key): val for key, val in filepaths  } 
    return plotpaths