import os
import math

parent_dir='/content/drive/My Drive/Inter_IIT/GTSRB_Bosch_PS/Test_train_split_test_dir/'
'''
parent directory should conatin 3 subdirectory one for test set 
one for orginal ds and one for new ds 

1.)the first function "copying_images_from_new_ds(new_ds_path,orginal_ds_path)" will copy the
data from new dataset to the orginal dataset . it will create new class folder if the new ds
contain extra classes 
2.)find_total_num_of_files(orginal_ds_path) function  just go through datset and counts number of 
images in it 
then we will calculate the number of images that should be in the test set and train set using
the split ratio given by user 
3.)test_dict is ython diuctionary whcih stores the label and location of training data
4.)copy_user_specified_files_to_test will copy the files to the train directory
 whoses file names are in the "test_set_file_names"
5.)test_train_split should be called after the "copy user specified function" 
this function just calaculate the remioaning number og images neede to be copied 
to test set and copies it 
'''
orginal_ds_path="Ds/"
test_path="test/"
new_ds_path="New_ds/Dataset/"
#PARAMETERS  
num_class=20
split_ratio=0.2
train_set_file_names=[]#user input name of images that must be in train set 
test_set_file_names=['00011_00027.ppm','GT-00001.csv']#user input name of images that must be in test set

copying_images_from_new_ds(new_ds_path,orginal_ds_path)
test_set_num,_=find_total_num_of_files(orginal_ds_path)
test_set_curr_num=0
test_dict={}# dictionary to keep track of filename and label 

copy_user_specified_files_to_test(test_path,orginal_ds_path,parent_dir)
test_train_split(test_dir,dataset_dir,parent_dir)

def copying_images_from_new_ds(new_ds_path,orginal_ds_path):
  '''
  move images from new dataset to the orginal dataset
  create new folder for new classes if there in classes 
  in new dataset which are not in orginal one  
  

  Args :
  new_ds_path : path new dataset 
  orginal_ds_path: path to orginal dataset 

  '''




  #os walk on newds
  New_ds_path=os.path.join(parent_dir, new_ds_path)
  os.chdir(New_ds_path)
  for root, classes_newds, files in os.walk(".", topdown=False):
    pass

  #os walk on old ds 
  old_ds_path=os.path.join(parent_dir,orginal_ds_path)
  os.chdir(old_ds_path)
  for root, classes_oldds, files in os.walk(".", topdown=False):
    pass


  
  #  for di in dirs:
  #   print(di)
  print("orginal ds classes ",classes_oldds)
  print("test ds classes ",classes_newds)
  
  

  for classes in classes_newds:

    old_folder_path=os.path.join(New_ds_path,classes)
    new_folder_path=os.path.join(old_ds_path,classes)


    if classes in classes_oldds:

      #move the files 
      os.chdir(old_folder_path)
      for root, dirs, files in os.walk(".", topdown=False):
        for file in files :
          old_file_path=os.path.join(old_folder_path,file)
          new_file_path=os.path.join(new_folder_path,file)
          os.replace(old_file_path,new_file_path)

    else:
      #movie entire folder 
      os.mkdir(new_folder_path)
      os.replace(old_folder_path,new_folder_path)
      #create new dir and copy or copy the entire folder 
      #num of classes ++
      global num_class
      num_class=num_class+1

def find_total_num_of_files(path_of_dir):


  '''
  execute a os walk and find the number 
  of files in a given directory 
  can be used to count number of images in
  a dataset

  args 
  path_of_dir: path to the dataset which we want to count 
  '''
#find total number of files 
  total_num_imgs=0
  path=os.path.join(parent_dir, path_of_dir)
  os.chdir(path)
  for root, dirs, files in os.walk(".", topdown=False):
    total_num_imgs=total_num_imgs+len(files)
  print(total_num_imgs)
  #calculate test and train image number 
  train_set_num=(1-split_ratio)*total_num_imgs
  train_set_num=math.floor(train_set_num)
  print(train_set_num)
  test_set_num=split_ratio*total_num_imgs
  test_set_num=math.ceil(test_set_num)
  print(test_set_num)
  os.chdir(parent_dir)
  return test_set_num,train_set_num

def copy_user_specified_files_to_test(test_dir,dataset_dir,parent_dir):


  '''
  move images  in the list "test_set_file_names"
  to the test set and stores the location and label of 
  images in a python dictionary "test_dict"

  args:
  test_dir: path to folder of test set 
  dataset_dir :path to the dataset 
  parent_dir: path to parent directory which conatin the folder 
  of orginal ds and test ds 
  we assume that test_dir is relative path 
  we just join the parent dir with test_dir to get absolute path 
  '''
  #test_set_num,train_set_num=find_total_num_of_files(dataset_dir)
  #copy files to test folder specified by user
  
  test_dir=os.path.join(parent_dir,test_dir)
  dataset_dir=os.path.join(parent_dir,dataset_dir)
  os.chdir(dataset_dir)
  for root, dirs, filesss in os.walk(".", topdown=False):
    for dir in dirs :
      path=os.path.join(dataset_dir, dir)
      os.chdir(path)
      for root, dirss, files in os.walk(".", topdown=False):
        for file_name in files :
          if file_name in test_set_file_names:

            old_file_path=os.path.join(path,file_name)
            new_file_path=os.path.join(test_dir,file_name)

            #print(old_file_path,new_file_path)
            os.replace(old_file_path,new_file_path)
          
            test_dict.update({dir:new_file_path})
            global test_set_curr_num
            test_set_curr_num=test_set_curr_num+1
  #copy files to test folder as to complete num

def test_train_split(test_dir,dataset_dir,parent_dir):


  '''

  move images from orginal dataset to training folder and 
  stroe the location and label of the train images in 
  a python dictionary test_dict

  this function needed to be run after the copy user specified image 

  this function calaculate how many images needed to be 
  moved by substracting the number images movied by the "copy user specified image"
  function from total number of test set
  and didvide the remaining number by num of classes 
  and thus calculate the number images needed to be
  moved from each class and move the image to test set 

  args :
  test_dir: path to folder of test set 
  dataset_dir :path to the dataset 
  parent_dir: path to parent directory which conatin the folder 
              of orginal ds and test ds 
              we assume that test_dir is relative path 
              we just join the parent dir with test_dir to get absolute path 

  '''


  test_dir=os.path.join(parent_dir,test_dir)
  dataset_dir=os.path.join(parent_dir,dataset_dir)
  global test_set_num
  global test_set_curr_num
  test_set_no_img_needed=test_set_num-test_set_curr_num
  test_set_no_img_needed_per_class=int(test_set_no_img_needed/num_class)

  print("test_set_no_imgs_neede ",test_set_no_img_needed_per_class)


  if(test_set_no_img_needed_per_class>0):



    os.chdir(dataset_dir)
    for root, dirs, filesss in os.walk(".", topdown=False):
     
      for dir in dirs :
        #print("directory",dir)
       
        path=os.path.join(dataset_dir, dir)
        os.chdir(path)
        for rt, di, files in os.walk(".", topdown=False):
          num=test_set_no_img_needed_per_class
          for i in range(1,num):
            #print(i)

            file_name=files[i]
            if file_name in train_set_file_names:
              #print("file name in train set ")
              num=num+1
            else:
              old_file_path=os.path.join(path,file_name)
              #print(old_file_path,"=== odfp")
              new_file_path=os.path.join(test_dir,file_name)
              os.replace(old_file_path,new_file_path)
              test_dict.update({file_name:new_file_path})
              test_set_curr_num=test_set_curr_num+1