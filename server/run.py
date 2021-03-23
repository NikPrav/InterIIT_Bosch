# importing app
import base64
from io import BytesIO

# import torchvision.transforms as transforms
from flask import jsonify, request
from PIL import Image

from app import app,  auth
from app.auth import *


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


# Authorsation code
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

# Setting up public, private and private-scoped endpoints
# Place holders, so change as needed
# https://auth0.com/docs/quickstart/backend/python/01-authorization#validate-access-tokens

@app.route("/api/public")
@cross_origin(headers=["Content-Type", "Authorization"])
def public():
    response = "Hello from a public endpoint! You don't need to be authenticated to see this."
    return jsonify(message=response)

# This needs authentication
@app.route("/api/private")
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def private():
    # json_response = {'Test' : 'haie','yo':'why'}
    response = "token"
    app.logger.info(f'hi2{response}')

    # app.logger.info(token)
    return jsonify(message = response)

# This needs authorization
@app.route("/api/private-scoped")
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def private_scoped():
    if requires_scope("read:current_user"):
        response = "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this."
        return jsonify(message=response)
    raise AuthError({
        "code": "Unauthorized",
        "description": "You don't have access to this resource"
    }, 403)












if __name__ == "__main__":
    app.run()
