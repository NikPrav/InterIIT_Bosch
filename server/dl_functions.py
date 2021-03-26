import numpy as np
import torch.nn.functional as F
import torch
import torch.nn as nn
from torchvision import datasets, transforms
import sys
import time
from models import Net
import os

# from dbmodels import Workspace

# def add_training_progress(workspace_id, dict_):
#     Workspace.objects(workspace_id=workspace_id).update_one(state=dict_)


def train(train_loader,model,optimizer,epoch,device):
    model.train()
    l = 0
    correct = 0
    for idx, (x, y) in enumerate(train_loader): 
        x = x.to(device)
        y = y.to(device)
        model.zero_grad()
        y_pred = model(x)
        # print(y_pred.shape)
        loss = F.nll_loss(y_pred,y)
        # loss = F.cross_entropy(y_pred,y)
        loss.backward()
        optimizer.step()
        l += loss.item()
        max_index = y_pred.max(dim = 1)[1]
        correct += ((max_index == y).sum()).item()
        # dict2 = {'\rEpoch: ':str(epoch),' Batch: ':str(idx+1)+'/'+str(len(train_loader)),' Training Loss: ':str(loss.item())}
        sys.stdout.write('\rEpoch: '+str(epoch)+' Batch: '+str(idx+1)+'/'+str(len(train_loader))+' Training Loss: '+str(loss.item()))
    return (l/idx), correct/len(train_loader.dataset)

def val(val_loader,model,device):
    model.eval()
    l = 0
    correct = 0
    for idx, (x, y) in enumerate(val_loader): 
        x = x.to(device)
        y = y.to(device)
        y_pred = model(x)
        loss = F.nll_loss(y_pred,y)
        # loss = F.cross_entropy(y_pred,y)
        l += loss.item()
        max_index = y_pred.max(dim = 1)[1]
        correct += ((max_index == y).sum()).item()
        # print(max_index)
        # print(y)
    return (l/idx), correct/len(val_loader.dataset)


def train_model(w_id,w_loc,num_classes,train_loc, val_loc, bs, EPOCH,opt,lr,device='cuda'):
    data_transforms = transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
        transforms.Normalize((0.3337, 0.3064, 0.3171), ( 0.2672, 0.2564, 0.2629))
    ])
    
    model = Net(num_classes).to(device)
    train_loader = torch.utils.data.DataLoader(
        datasets.ImageFolder(train_loc,
        transform=data_transforms), batch_size=bs, shuffle=True, num_workers=4, pin_memory=True)

    val_loader = torch.utils.data.DataLoader(
        datasets.ImageFolder(val_loc,transform=data_transforms),
        batch_size=bs, shuffle=True, num_workers=1, pin_memory=True)
    if opt == 'adam':
        optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    elif opt == 'adagrad':
        optimizer = torch.optim.Adagrad(model.parameters(), lr=lr)
    elif opt == 'rmsprop':
        optimizer = torch.optim.RMSprop(model.parameters(), lr=lr)
    elif opt == 'sgd':
        optimizer = torch.optim.SGD(model.parameters(), lr=lr)


    val1 = 0

    for epoch in range(EPOCH):
        time1 = time.time()
        tr_loss, tr_acc = train(train_loader,model,optimizer, epoch,device)
        time2 = time.time()
        val_loss, val_acc = val(val_loader,model,device)
        # dict1 = {'Epochs:':epoch,'Training Loss:':tr_loss,'Val Loss:':val_loss,'Training Acc:':tr_acc,'Val Acc:':val_acc,'Time :':time2-time1}
        # add_training_progress(w_id,dict1)
        print('Epochs:',epoch,'Training Loss:',tr_loss,'Val Loss:',val_loss,'Training Acc:',tr_acc,'Val Acc:',val_acc,'Time :',time2-time1)
        if(val_acc>val1):
            sv_file = os.path.join(w_loc,'models','model_'+str(epoch)+'_'+str(val_acc))
            torch.save(model.state_dict(), sv_file)
            print('Validation Accuracy increased, Model Saved')
            val1 = val_acc



import os
import math 


# dataset_dir='/content/drive/My Drive/Inter_IIT/GTSRB_Bosch_PS/Test_train_split_test_dir/Ds/'
# test_dir='/content/drive/My Drive/Inter_IIT/GTSRB_Bosch_PS/Test_train_split_test_dir/test/'
  
# num_class=5
# split_ratio=0.2
# train_set_file_names=["/content/drive/My Drive/Inter_IIT/GTSRB_Bosch_PS/Test_train_split_test_dir/Ds/00001/x.jpg","/content/drive/My Drive/Inter_IIT/GTSRB_Bosch_PS/Test_train_split_test_dir/Ds/00001/y.jpg"]
# test_set_file_path=[]#user input name of images that must be in test set

# train_test_split(dataset_dir,test_dir,test_set_file_path,num_class,split_ratio,train_set_file_names)

def train_test_split(dataset_dir,test_dir,test_set_file_path,num_class,split_ratio,train_set_file_names):
  test_dict={}
  #find total number of files 
  total_num_imgs=0
  path=dataset_dir
  
  
  os.chdir(path)
  for root, dirs, files in os.walk(".", topdown=False):
    total_num_imgs=total_num_imgs+len(files)
  #print(total_num_imgs)
  #calculate test and train image number 


  train_set_num=(1-split_ratio)*total_num_imgs
  train_set_num=math.floor(train_set_num)
  #print(train_set_num)
  test_set_num=split_ratio*total_num_imgs
  test_set_num=math.ceil(test_set_num)
  #print(test_set_num)
  #os.chdir(parent_dir)
  #return test_set_num,train_set_num


  
  test_set_curr_num=0
 #copy user specified files 
  

  for paths_of_test in test_set_file_path:
    #print("paths_of_test",paths_of_test)
    head_tail = os.path.split(paths_of_test)
    #print("head tai",head_tail)
    head_tai_0=head_tail[0]
    file_name=head_tail[1]
    dir=os.path.split(head_tai_0)[1]
    #print("dir is ",dir)
    #print("filename is ",file_name)

    #directory is the class name
     


    old_file_path=paths_of_test
    new_file_path=os.path.join(test_dir,file_name)

    os.replace(old_file_path,new_file_path)
    test_dict.update({dir:new_file_path})
    #global test_set_curr_num
    test_set_curr_num=test_set_curr_num+1


  
  test_set_no_img_needed=test_set_num-test_set_curr_num
  test_set_no_img_needed_per_class=int(test_set_no_img_needed/num_class)

  if(test_set_no_img_needed_per_class>0):

    os.chdir(dataset_dir)
    for root, dirs, filesss in os.walk(".", topdown=False):
     
      for dir in dirs :
        #print("directory",dir)
        create_folder_path=os.path.join(test_dir, dir)
        os.mkdir(create_folder_path)
       
        path=os.path.join(dataset_dir, dir)
        os.chdir(path)
        for rt, di, files in os.walk(".", topdown=False):
          num=test_set_no_img_needed_per_class
          #print("files namessss",files)
          #num=3
          for i in range(0,num):
            #print("for loop i th iteration",i)
            #print("filename not in train set",file_name)
            

            file_name=files[i]
            old_file_path=os.path.join(path,file_name)
            
            #print("filename :",file_name)
            #print("train set file name list ",train_set_file_names)



            if old_file_path in train_set_file_names:
              #print("file name in train set ",file_name)
              num=num+1
              
            else:
              #print("file----",train_set_file_names)
              
              #print("filename not in train set",file_name)
              new_file_path=os.path.join(test_dir,dir,file_name)
              os.replace(old_file_path,new_file_path)
              test_dict.update({file_name:new_file_path})
              test_set_curr_num=test_set_curr_num+1
  return test_dict




import numpy as np
import torch.nn.functional as F
import torch
import torch.nn as nn
from torchvision import datasets, transforms
import sys
import time

device = 'cuda'
# device = 'cpu'


class Net(nn.Module):
    def __init__(self,out_dim):
        super(Net,self).__init__()
        # CNN layers
        self.conv1 = nn.Conv2d(3, 100, kernel_size=5)
        self.bn1 = nn.BatchNorm2d(100)
        self.conv2 = nn.Conv2d(100, 150, kernel_size=3)
        self.bn2 = nn.BatchNorm2d(150)
        self.conv3 = nn.Conv2d(150, 250, kernel_size=3)
        self.bn3 = nn.BatchNorm2d(250)
        self.conv_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(250*2*2, 350)
        self.fc2 = nn.Linear(350, out_dim)

        self.localization = nn.Sequential(
            nn.Conv2d(3, 8, kernel_size=7),
            nn.MaxPool2d(2, stride=2),
            nn.ReLU(True),
            nn.Conv2d(8, 10, kernel_size=5),
            nn.MaxPool2d(2, stride=2),
            nn.ReLU(True)
            )

        # Regressor for the 3 * 2 affine matrix
        self.fc_loc = nn.Sequential(
            nn.Linear(10 * 4 * 4, 32),
            nn.ReLU(True),
            nn.Linear(32, 3 * 2)
            )

        # Initialize the weights/bias with identity transformation
        self.fc_loc[2].weight.data.zero_()
        self.fc_loc[2].bias.data.copy_(torch.tensor([1, 0, 0, 0, 1, 0], dtype=torch.float))


    # Spatial transformer network forward function
    def stn(self, x):
        xs = self.localization(x)
        xs = xs.view(-1, 10 * 4 * 4)
        theta = self.fc_loc(xs)
        theta = theta.view(-1, 2, 3)
        # print(theta.shape, x.shape)
        grid = F.affine_grid(theta, x.size())
        x = F.grid_sample(x, grid)
        return x

    def forward(self, x):
        # transform the input
        x = self.stn(x)

        # Perform forward pass
        x = self.bn1(F.max_pool2d(F.leaky_relu(self.conv1(x)),2))
        x = self.conv_drop(x)
        x = self.bn2(F.max_pool2d(F.leaky_relu(self.conv2(x)),2))
        x = self.conv_drop(x)
        x = self.bn3(F.max_pool2d(F.leaky_relu(self.conv3(x)),2))
        x = self.conv_drop(x)
        x = x.view(-1, 250*2*2)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)


import os
import shutil

# gtsrb_train_folder = "D:/gtsrb/moddata/train_images"
# gtsrb_test_folder = "D:/gtsrb/moddata/test_images"

# newds_train_folder = "D:/gtsrb/cure tsr/New folder/mod_train_cure"
# newds_test_folder = "D:/gtsrb/cure tsr/New folder/mod_test_cure"
# newdscsvfilename = "CURE-final_test.csv"

def append_to_train(gtsrb_train_folder,newds_train_folder):
    i=len(os.listdir(gtsrb_train_folder))
    uncommonclassdict = {}
    for classfolder in os.listdir(newds_train_folder):
        gtsrbclasspath = os.path.join(gtsrb_train_folder,classfolder)
        newdsclasspath = os.path.join(newds_train_folder,classfolder)
        if(os.path.exists(gtsrbclasspath)==False):
            uncommonclassdict[i] = int(classfolder)
            i+=1
            os.mkdir(gtsrbclasspath)
        for img in os.listdir(newdsclasspath):
            imgpath = os.path.join(newdsclasspath,img)
            os.symlink(imgpath,os.path.join(gtsrbclasspath,img))
    # print(uncommonclassdict)
    return uncommonclassdict
       
# append_to_train(gtsrb_train_folder,newds_train_folder)   
            
def append_to_test(gtsrb_test_folder,newds_test_folder,newdscsvfilename):
    # for img in os.listdir(newds_test_folder):
    #     imgpath = os.path.join(newds_test_folder,img)
    #     shutil.copy(imgpath,gtsrb_test_folder)
    newdscsvfileloc = os.path.join(gtsrb_test_folder,newdscsvfilename)
    gtsrbcsvfileloc = os.path.join(gtsrb_test_folder,"GT-final_test.csv")
    with open(newdscsvfileloc, 'r') as f1,open(gtsrbcsvfileloc, 'a') as f2:
        f1.readline()
        f2.write(f1.read())
    os.remove(newdscsvfileloc)

# append_to_test(gtsrb_test_folder,newds_test_folder,newdscsvfilename)









import numpy as np
import matplotlib.pyplot as plt
import os
import base64
import pathlib
from append_to_gtsrb import append_to_train
from final_aug import applyAugmentations
from split import train_test_split
from train import train_model

# loc_for_worspace_creation = os.path.expanduser("~/Inter_IIT_2021")
# loc_new_dataset = os.path.expanduser("~/Inter_IIT_2021/data/new_dataset/train_")

def base64_to_path(chunk):
    return base64.urlsafe_b64decode(chunk.encode("ascii")).decode("ascii")


def path_to_base64(path):
    return base64.urlsafe_b64encode(path.encode("ascii")).decode("ascii")


args = {
  "name": "xyz",
  "workspace_id": 1,  # from 1 to 999
  "datasets": ["arts"], # use "arts", "dits","cure"
  "added_images": {},
  "augmentations": {
    "aW1hZ2VzLzAwMDAwLzAwMDAwXzAwMDAwLnBwbQ==": [
      [
        "hue",
        "add_fog"
      ],
      [
        "add_rain"
      ]
    ],
    "aW1hZ2VzLzAwMDAwLzAwMDAwXzAwMDAxLnBwbQ==":[
      [
        "random"
      ]
    ],
  },
  "model_settings": {
    "test_train_split": 10,
    "learning_rate": 0.001,
    "epochs": 10,
    "batch_size": 128,
    "augmentation_setting": "all", # "select"| "random | all",
    "opt": "rmsprop", # | adagrad | sgd | rmsprop",
    "augs_for_all": ["add_fog", "hue"],
  },
  "test_preferred_images": [],
  "train_preferred_images": [],
  "model_results": {},
  "user_email": "ch17btech11023@iith.ac.in",
  "created_at": {
    "$date": 1616577653895
  },
  "updated_at": {
    "$date": 1616579262992
  }
}
def main(args):

  loc_for_worspace_creation = os.path.expanduser("~/Inter_IIT_2021")
  loc_new_dataset = os.path.expanduser("~/Inter_IIT_2021/data/temp/train_")

  w_id = "{:03d}".format(args["workspace_id"])
  w_loc = os.path.join(loc_for_worspace_creation,"workspace"+w_id)
  if(not args["datasets"]):
    for dats in args["datasets"]:
      new_data_loc = loc_new_dataset + dats
      class_dict = append_to_train(os.path.join(w_loc,'images'),new_data_loc)
  
  num_classes = len(os.listdir(os.path.join(w_loc,'images')))
  train_dir = os.path.join(w_loc,'images')
  val_dir = os.path.join(w_loc,'validation_images')
  val_dict = train_test_split(train_dir,val_dir,args["test_preferred_images"],num_classes,args["model_settings"]["test_train_split"]/100,args["train_preferred_images"])

  dict1 = {}
  if args["model_settings"]["augmentation_setting"] == "select":
    for key in args["augmentations"]:
      img_loc = os.path.join(w_loc,base64_to_path(key))
      dict1[img_loc] = args["augmentations"][key]  
  elif args["model_settings"]["augmentation_setting"] == "all":
    img_loc = os.path.join(w_loc,'images')
    dict1[img_loc] = [args["model_settings"]["augs_for_all"]]
  elif args["model_settings"]["augmentation_setting"] == "random":
    img_loc = os.path.join(w_loc,'images')
    dict1[img_loc] = [["random"]]
  d1, d2 = applyAugmentations(dict1)
  
  train_loc = os.path.join(w_loc,'images')
  val_loc = os.path.join(w_loc,'validation_images')
  bs = args["model_settings"]["batch_size"]
  EPOCH = args["model_settings"]["epochs"]
  opt = args["model_settings"]["opt"]
  lr = args["model_settings"]["learning_rate"]
  device = 'cuda'
  train_model(args["workspace_id"],w_loc,num_classes,train_loc, val_loc, bs, EPOCH,opt,lr,device)

    

main(args)