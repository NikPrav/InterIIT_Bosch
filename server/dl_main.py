import numpy as np
import matplotlib.pyplot as plt
import os
import base64
import pathlib
from dl_functions import append_to_train, applyAugmentations, train_test_split, train_model
# from append_to_gtsrb import append_to_train
# from final_aug import applyAugmentations
# from split import train_test_split
# from train import train_model

# loc_for_worspace_creation = os.path.expanduser("~/Inter_IIT_2021")
# loc_new_dataset = os.path.expanduser("~/Inter_IIT_2021/data/new_dataset/train_")

def base64_to_path(chunk):
    return base64.urlsafe_b64decode(chunk.encode("ascii")).decode("ascii")


def path_to_base64(path):
    return base64.urlsafe_b64encode(path.encode("ascii")).decode("ascii")

# args = {
#   "name": "xyz",
#   "workspace_id": 1,  # from 1 to 999
#   "datasets": ["arts"], # use "arts", "dits","cure"
#   "added_images": {},
#   "augmentations": {
#     "aW1hZ2VzLzAwMDAwLzAwMDAwXzAwMDAwLnBwbQ==": [
#       [
#         "hue",
#         "add_fog"
#       ],
#       [
#         "add_rain"
#       ]
#     ],
#     "aW1hZ2VzLzAwMDAwLzAwMDAwXzAwMDAxLnBwbQ==":[
#       [
#         "random"
#       ]
#     ],
#   },
#   "model_settings": {
#     "test_train_split": 10,
#     "learning_rate": 0.001,
#     "epochs": 10,
#     "batch_size": 128,
#     "augmentation_setting": "all", # "select"| "random | all",
#     "opt": "rmsprop", # | adagrad | sgd | rmsprop",
#     "augs_for_all": ["add_fog", "hue"],
#   },
#   "test_preferred_images": [],
#   "train_preferred_images": [],
#   "model_results": {},
#   "user_email": "ch17btech11023@iith.ac.in",
#   "created_at": {
#     "$date": 1616577653895
#   },
#   "updated_at": {
#     "$date": 1616579262992
#   }
# }
def dl_main(args):

  loc_for_worspace_creation = os.path.expanduser("~/.btsr")
  loc_new_dataset = os.path.expanduser("~/.btsr/datasets")

  w_id = "{:03d}".format(args["workspace_id"])
  w_loc = os.path.join(loc_for_worspace_creation,"workspace"+w_id)
  if(not args["datasets"]):
    for dats in args["datasets"]:
      new_data_loc = os.path.join(loc_new_dataset,dats)
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

    

# main(args)