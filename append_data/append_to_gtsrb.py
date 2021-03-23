import os
import shutil

# gtsrb_train_folder = "/home/scitech/Inter_IIT_2021/Data Append/GTSRB/Final_Training/Images/"
# gtsrb_test_folder = "/home/scitech/Inter_IIT_2021/Data Append/GTSRB/Final_Test/Images/"

# newds_train_folder = "/home/scitech/Inter_IIT_2021/Data Append/new modified datasets/dits/classification train/"
# newds_test_folder = "/home/scitech/Inter_IIT_2021/Data Append/new modified datasets/dits/classification test/"
# newdscsvfilename = "dits-final_test.csv"

def append_to_train(gtsrb_train_folder,newds_train_folder):
	'''
	merges train data between new dataset and original dataset

	arguments:
		gtsrb_train_folder: location of train folder of original dataset
		newds_train_folder: location of train folder of new dataset
	'''
    for classfolder in os.listdir(newds_train_folder):
        gtsrbclasspath = os.path.join(gtsrb_train_folder,classfolder)
        newdsclasspath = os.path.join(newds_train_folder,classfolder)
        if(os.path.exists(gtsrbclasspath)==False):
            os.mkdir(gtsrbclasspath)
        for img in os.listdir(newdsclasspath):
            imgpath = os.path.join(newdsclasspath,img)
            shutil.move(imgpath,gtsrbclasspath)
       
# append_to_train(gtsrb_train_folder,newds_train_folder)   
            
def append_to_test(gtsrb_test_folder,newds_test_folder,newdscsvfilename):
	'''
	merges test data between new dataset and original dataset, along with label csv file

	arguments:
		gtsrb_test_folder: location of test folder of original dataset
		newds_test_folder: location of test folder of new dataset
		newdscsvfilename: name of csv file containing labels of new dataset
	'''
    for img in os.listdir(newds_test_folder):
        imgpath = os.path.join(newds_test_folder,img)
        shutil.move(imgpath,gtsrb_test_folder)
    newdscsvfileloc = os.path.join(gtsrb_test_folder,newdscsvfilename)
    gtsrbcsvfileloc = os.path.join(gtsrb_test_folder,"GT-final_test.csv")
    with open(newdscsvfileloc, 'r') as f1,open(gtsrbcsvfileloc, 'a') as f2:
        f1.readline()
        f2.write(f1.read())
    os.remove(newdscsvfileloc)

# append_to_test(gtsrb_test_folder,newds_test_folder,newdscsvfilename)