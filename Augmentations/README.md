Use following examples as reference while sending inputs to the function<br/>
Accepted format of inputs to applyAugmentations in final_aug.py<br/>
  * For list of photos with list of augmentation-<br/>
    meta = {
        "Images/0/00000_00000.ppm": [
            ["add_fog", "hue", "affine_translate"],
            [, "add_rain","affine_shear", "random_contrast", "random_flip"]
        ]
    }<br/>
   * For list of photos with random augmentation-<br/>
    meta = {
        "Images/0/00000_00000.ppm": [
            ["random"]
        ]
    }<br/>
    <br/>
   * For all photos with list of augmentation-<br/>
    meta = {
        "Images/": [
            ["add_fog", "hue", "affine_translate"],
            [, "add_rain","affine_shear", "random_contrast", "random_flip"]
        ]
    }<br/>
    * For all photos with random augmentation-<br/>
    meta = {
        "Images/": [
            ["random"]
        ]
    }<br/>
    <br/>
**NOTE: Apply weather augmentation first before other augmentations**<br/><br/>

Available list of augs: ["random_contrast", "affine_shear", "affine_translate", "rotate", "hue",
                 "saturation", "random_brightness", "add_speed", "random_flip",
                 "correct_exposure", "add_snow", "add_rain", "add_fog", 
                 "add_sun_flare", "add_autumn"]<br/><br/>
Naming convention: {"random_contrast":"rc", "affine_shear":"as", "affine_translate":"at",
                       "rotate":"rt", "hue":"hu", "saturation":"st", "random_brightness":"rb",
                       "add_speed":"sp", "random_flip":"rf", "correct_exposure":"ce",
                       "add_snow":"sn", "add_rain":"rn", "add_fog":"fg", "add_sun_flare":"sf",
                       "add_autumn":"au"}
