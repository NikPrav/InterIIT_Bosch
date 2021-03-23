# This list contains the types of augmentations available 
aug_types_normal = ["random_contrast", "affine_shear", "affine_translate", "rotate", "hue",
                    "saturation", "random_brightness", "add_speed", "random_flip",
                    "correct_exposure", "lightness"]
aug_types_weather = ["add_snow", "add_rain", "add_fog",
                     "add_autumn"]
aug_types_extension = {"random_contrast":"rc", "affine_shear":"as", "affine_translate":"at",
                       "rotate":"rt", "hue":"hu", "saturation":"st", "random_brightness":"rb",
                       "add_speed":"sp", "random_flip":"rf", "correct_exposure":"ce",
                       "add_snow":"sn", "add_rain":"rn", "add_fog":"fg", "add_autumn":"au",
                      "lightness":"li"}

def applyAugmentations(metadata):
    """
    Output: None (Saves images in the same destinatino as that of input)

    Args: A dictionary which contains the path of the input as the key and the augmentations as its value 
    """
    for i in metadata:
        if(os.path.isdir(i)):
            if(metadata[i][0][0] == "random"):
                for j in os.listdir(i):
                    for im in os.listdir(i+j):
                        aug = [aug_types_weather[np.random.randint(0, len(aug_types_weather))],
                               aug_types_normal[np.random.randint(0, len(aug_types_normal))]]
                        image = cv2.resize(plt.imread(i+j+"/"+im), (45, 45))
                        name = ""
                        for k in aug:
                            image = eval(k+"(image)")
                            name += aug_types_extension[k]+"_"
                        plt.imsave(i+j+"/"+name+im, image)
            else:
                for aug in metadata[i]:
                    for j in os.listdir(i):
                        for im in os.listdir(i+j):
                            image = cv2.resize(plt.imread(i+j+"/"+im), (45, 45))
                            name = ""
                            for k in aug:
                                image = eval(k+"(image)")
                                name += aug_types_extension[k]+"_"
                            plt.imsave(i+j+"/"+name+im, image)
        else:
            if(metadata[i][0][0] == "random"):
                aug = [aug_types_weather[np.random.randint(0, len(aug_types_weather))],
                       aug_types_normal[np.random.randint(0, len(aug_types_normal))]]
                image = cv2.resize(plt.imread(i), (45, 45))
                name = ""
                for k in aug:
                    image = eval(k+"(image)")
                    name += aug_types_extension[k]+"_"
                path = ""
                for p in i.split("/")[:-1]:
                    path += p+"/"
                path += name+i.split("/")[-1]
                plt.imsave(path, image)
            else:
                for aug in metadata[i]:
                    image = cv2.resize(plt.imread(i), (45, 45))
                    name = ""
                    for k in aug:
                        image = eval(k+"(image)")
                        name += aug_types_extension[k]+"_"
                    path = ""
                    for p in i.split("/")[:-1]:
                        path += p+"/"
                    path += name+i.split("/")[-1]
                    plt.imsave(path, image)
