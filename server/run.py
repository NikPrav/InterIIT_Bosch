# importing app
import base64
from io import BytesIO

import torchvision.transforms as transforms
from flask import jsonify, request, Flask
from PIL import Image

import torchcommands

app = Flask(__name__)

@app.route("/success/")
def success():
    return "welcome"


@app.route("/pictest", methods=["POST"])
def savingpic():
    request_data = request.get_json()
    print("hi")
    app.logger.info(request_data)
    # print(request_data)
    image = request_data["image"]

    # Workaround for specific case
    image = image.split(",")[1]

    image_bytes = image.encode("ascii")
    with open("PicTest.png", "wb") as fh:
        fh.write(base64.decodebytes(image_bytes))

    # transf = request_data['transform']
    transform_dict = {
        "data_transforms": torchcommands.data_transforms,
        "data_jitter_brightness": torchcommands.data_jitter_brightness,
        "data_jitter_saturation": torchcommands.data_jitter_saturation,
        "data_jitter_contrast": torchcommands.data_jitter_contrast,
        "data_jitter_hue": torchcommands.data_jitter_hue,
        "data_rotate": torchcommands.data_rotate,
        "data_hvflip": torchcommands.data_hvflip,
        "data_hflip": torchcommands.data_hflip,
        "data_vflip": torchcommands.data_vflip,
        "data_shear": torchcommands.data_shear,
        "data_translate": torchcommands.data_translate,
        "data_center": torchcommands.data_center,
        "data_grayscale": torchcommands.data_grayscale,
    }
    tr = transform_dict[request_data["transform"]]

    # image = Image.frombytes('RGBA',  base64.decodebytes(image_bytes))
    im_bytes = base64.b64decode(image)  # im_bytes is a binary image
    im_file = BytesIO(im_bytes)  # convert image to file-like object
    img = Image.open(im_file)
    app.logger.info(img)
    img = img.convert("RGB")
    # im1 = Image.open("PicTransform.jpg")

    # save a image using extension
    x = tr(img)
    y = transforms.ToPILImage()
    x = y(x)
    # [DEBUG] Testing save image
    x.save("pic_transform.jpg")
    buffered = BytesIO()
    x.save(buffered, format="JPEG")
    tr_image = base64.b64encode(buffered.getvalue())
    tr_image = tr_image.decode("ascii")
    return jsonify(image=tr_image)


if __name__ == "__main__":
    app.run()
