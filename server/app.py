import base64
import contextlib
import csv
import json
import os
import pathlib
import shutil
import typing as t
from datetime import datetime
from functools import wraps
from io import BytesIO
from urllib.request import urlopen

import requests
import torchvision.transforms as transforms
from auth0.v3.authentication import Users
from flasgger import Swagger
from flask import Flask, _request_ctx_stack, jsonify, request, send_from_directory
from flask_cors import cross_origin
from jose import jwt
from PIL import Image
from pydantic import ValidationError
from werkzeug.datastructures import Headers
from werkzeug.utils import secure_filename
from werkzeug.wrappers import BaseResponse

import torchcommands
import utils
from configs import cnf
from core import (
    add_dataset_to_workspace,
    create_workspace_dir,
    get_all_image_ids,
    move_to_trash,
    remove_dataset_from_workspace,
)
from dbmodels import Class, Dataset, Globals, Info, User, Workspace
from req_models import ClassCreate, ModelParams, WorkspaceCreate, WorkspacePatch

# from dl_main import dl_main

app = Flask(__name__)

get, post, put, patch, delete = "GET", "POST", "PUT", "PATCH", "DELETE"

w_path = "/workspaces/<int:workspace_id>"
img_path = "/workspaces/<int:workspace_id>/images/<string:image_id>"

rpc_call = lambda: {"state": "success"}

app = Flask(__name__)

swagger = Swagger(app)

AUTH0_DOMAIN = "dev-kqx4v2yr.jp.auth0.com"
API_AUDIENCE = "https://dev-kqx4v2yr.jp.auth0.com/api/v2/"
ALGORITHMS = ["RS256"]


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Verifies Access Tokes against your JWKS
# Format error response and append status code
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header"""
    auth = request.headers.get("Authorization", None)
    email = request.headers.get("email", None)
    if not auth:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected",
            },
            401,
        )

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must start with" " Bearer",
            },
            401,
        )
    elif len(parts) == 1:
        raise AuthError(
            {"code": "invalid_header", "description": "Token not found"}, 401
        )
    elif len(parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must be" " Bearer token",
            },
            401,
        )

    token = parts[1]
    return token, auth, email


def requires_auth(f):
    """Determines if the Access Token is valid"""

    @wraps(f)
    def decorated(*args, **kwargs):

        token, auth, email = get_token_auth_header()
        jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)

        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://" + AUTH0_DOMAIN + "/",
                )

            except jwt.ExpiredSignatureError:
                raise AuthError(
                    {"code": "token_expired", "description": "token is expired"}, 401
                )
            except jwt.JWTClaimsError:
                raise AuthError(
                    {
                        "code": "invalid_claims",
                        "description": "incorrect claims,"
                        "please check the audience and issuer",
                    },
                    401,
                )
            except Exception:
                raise AuthError(
                    {
                        "code": "invalid_header",
                        "description": "Unable to parse authentication" " token.",
                    },
                    401,
                )

            _request_ctx_stack.top.current_user = payload
            return f(email, *args, **kwargs)
        raise AuthError(
            {"code": "invalid_header", "description": "Unable to find appropriate key"},
            401,
        )

    return decorated


# Looking for a particular scope in the Access Token
def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
        token_scopes = unverified_claims["scope"].split()
        for token_scope in token_scopes:
            if token_scope == required_scope:
                return True
    return False


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file("../web/build/index.html")


@app.route("/pictest", methods=["POST"])
def savingpic():
    request_data = request.get_json()
    print("hi")
    app.logger.info(request_data)
    # print(request_data)
    image = request_data["image"]
    image = image.split(",")[1]

    image_bytes = image.encode("ascii")
    with open("PicTest.png", "wb") as fh:
        fh.write(base64.decodebytes(image_bytes))

    # # transf = request_data['transform']
    # transform_dict = {
    #     "data_transforms": torchcommands.data_transforms,
    #     "data_jitter_brightness": torchcommands.data_jitter_brightness,
    #     "data_jitter_saturation": torchcommands.data_jitter_saturation,
    #     "data_jitter_contrast": torchcommands.data_jitter_contrast,
    #     "data_jitter_hue": torchcommands.data_jitter_hue,
    #     "data_rotate": torchcommands.data_rotate,
    #     "data_hvflip": torchcommands.data_hvflip,
    #     "data_hflip": torchcommands.data_hflip,
    #     "data_vflip": torchcommands.data_vflip,
    #     "data_shear": torchcommands.data_shear,
    #     "data_translate": torchcommands.data_translate,
    #     "data_center": torchcommands.data_center,
    #     "data_grayscale": torchcommands.data_grayscale,
    # }
    # tr = transform_dict[request_data["transform"]]

    # # image = Image.frombytes('RGBA',  base64.decodebytes(image_bytes))
    # im_bytes = base64.b64decode(image)  # im_bytes is a binary image
    # im_file = BytesIO(im_bytes)  # convert image to file-like object
    # img = Image.open(im_file)
    # app.logger.info(img)
    # img = img.convert("RGB")
    # # im1 = Image.open("PicTransform.jpg")

    # # save a image using extension
    # x = tr(img)
    # y = transforms.ToPILImage()
    # x = y(x)
    # # [DEBUG] Testing save image
    # x.save("pic_transform.jpg")
    # buffered = BytesIO()
    # x.save(buffered, format="JPEG")
    # tr_image = base64.b64encode(buffered.getvalue())
    # tr_image = tr_image.decode("ascii")
    return jsonify(image=image)


@app.route("/info", methods=["GET"])
@cross_origin(headers=["Content-Type", "Authorization"])
def get_project_info():
    """
    Endpoint returning info needed to setup app.
    ---
    responses:
      200:
        description: Info including uneditable workspaces
    """
    info = Info.objects.exclude("_id").to_json()
    return info, 200


@app.route("/register", methods=[post])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def add_user_if_not_exists(email):
    """
    Create user if not exists.
    ---
    responses:
      201:
        description: User was created.
      208:
        description: User already exists.
    """
    if not User.objects(email=email):
        num = User.objects.count()
        user = User(user_id=num + 1, email=email)
        user.save()
        return user.to_json(), 201
        workspace = Workspace(
            **data,
            user_email=email,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            workspace_id=num,
        )
    return {"message": "User already exists."}, 208


@app.route("/workspaces", methods=["GET"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def get_workspaces(email):
    """
    Get info about user's workspaces.
    ---
    responses:
      200:
        description: Returning info about workspaces.
    """
    workspaces = (
        Workspace.objects(user_email=email)
        .only(
            "name",
            "datasets",
            "added_images",
            "workspace_id",
        )
        .exclude("_id")
        .to_json()
    )
    return workspaces, 200


@app.route("/workspaces", methods=["POST"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def create_workspace(email):
    """
    Create new workspace.
    ---
    responses:
      201:
        description: Created workspace.
      418:
        description: Reached limit of workspaces.
    """
    app.logger.error("%s", email)
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    try:
        data = WorkspaceCreate(**json_data).dict()
        app.logger.info("%s", data)
        user_id = User.objects.get(email=email).user_id
        if Workspace.objects(user_email=email).count() >= 10:
            return {
                "message": "You have reached the limit in number of workspaces."
            }, 418
        s = set(range(user_id * 10 + 1, user_id * 10 + 11)) - {
            w.workspace_id for w in Workspace.objects(user_email=email)
        }
        num, *_ = sorted(list(s))
        workspace = Workspace(
            **data,
            user_email=email,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            workspace_id=num,
        )
        create_workspace_dir(num)
        workspace.save()
        return workspace.to_json()
    except ValidationError as e:
        app.logger.info("%s", e)
        return {"message": "Wrong input data provided"}, 400


@app.route("/workspaces/<int:workspace_id>", methods=["GET"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def get_workspace(email, workspace_id: str):
    """
    Get info about specific workspace.
    ---
    parameters:
      - name: workspace_id
        in: path
        type: int
        required: true
    responses:
      200:
        description: Returning info about workspaces.
    """
    info = Workspace.objects(workspace_id=workspace_id).exclude("_id")[0].to_json()
    return info, 200


@app.route("/workspaces/<int:workspace_id>", methods=["PATCH"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def edit_workspace(email, workspace_id: int):
    """
    Edit workspace.
    ---
    parameters:
      - name: workspace_id
        in: path
        type: int
        required: true
      - name: datasets
        in: body
        schema:
          type: array
          items:
            type: string
      - name: model_settings
        in: body
        schema:
          type: object
      - name: images_to_delete
        in: body
        schema:
          type: array
          items:
            type: string
    responses:
      200:
        description: Edited workspace.
    """
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    try:
        data = WorkspacePatch(**json_data, workspace_id=workspace_id).dict()
        imgs_to_delete = data.pop("imgs_to_delete")
        if imgs_to_delete:
            move_to_trash(workspace_id, imgs_to_delete)
        existing_datasets = set(
            Workspace.objects(workspace_id=workspace_id)[0].datasets
        )
        datasets = existing_datasets
        if data["datasets_to_delete"]:
            datasets -= set(data.pop("datasets_to_delete"))
        if data["datasets_to_add"]:
            datasets += set(data.pop("datasets_to_add"))
        data["datasets"] = list(datasets)
        for dataset in datasets - existing_datasets:
            add_dataset_to_workspace(dataset)
        for dataset in existing_datasets - datasets:
            remove_dataset_from_workspace(dataset)
        Workspace.objects(workspace_id=workspace_id).update_one(**data)
        return Workspace.objects(workspace_id=workspace_id).to_json()
    except ValidationError as e:
        app.logger.error("%s", e)
        return {"message": f"{e}"}, 400


@app.route("/workspaces/<int:workspace_id>", methods=[delete])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def delete_workspace(email, workspace_id: int):
    workspace_name = f"workspace{workspace_id:03d}"
    Workspace.objects(workspace_id=workspace_id).delete()
    shutil.rmtree(os.path.join(cnf.WORKSPACES_BASE_PATH, workspace_name))
    return {"message": "success"}


@app.route("/workspaces/<int:workspace_id>/classes", methods=[get])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def get_classes(email, workspace_id):
    workspace_name = f"workspace{workspace_id:03d}"
    workspace_path = os.path.join(cnf.WORKSPACES_BASE_PATH, workspace_name)
    with open(os.path.join(workspace_path, cnf.CLASSES_FILE), "r") as f:
        reader = csv.reader(f)
        data = list(reader)
        dict_ = dict(zip([x, y] for [x, y] in data))
    return dict_


@app.route("/workspaces/<int:workspace_id>/classes", methods=[post])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def add_class(email, workspace_id):
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    try:
        data = ClassCreate(**json_data).dict()
        if data["classname"]:
            workspace_name = f"workspace{workspace_id:03d}"
            workspace_path = os.path.join(cnf.WORKSPACES_BASE_PATH, workspace_name)
            imgs_path = os.path.join(workspace_path, cnf.IMAGES_FOLDER)
            num = max(int(sorted(os.listdir(imgs_path))[:-1]), 80) + 1
            class_folder_name = f"{num:05d}"
            with open(os.path.join(workspace_path, cnf.CLASSES_FILE), "a") as f:
                writer = csv.writer(f)
                writer.writerow([num, class_folder_name])
            pathlib.Path(
                os.path.join(workspace_path, class_folder_name).mkdir(
                    parents=True, exist_ok=True
                )
            )
    except ValidationError as e:
        app.logger.error("%s", e)
        return {"message": f"{e}"}, 400
    return {}


@app.route("/workspaces/<int:workspace_id>/classes/<int:class_id>", methods=[delete])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def delete_class_from_workspace(email, workspace_id, class_id):
    workspace_name = f"workspace{workspace_id:03d}"
    workspace_path = os.path.join(cnf.WORKSPACES_BASE_PATH, workspace_name)
    class_folder_name = f"{class_id:05d}"
    with contextlib.suppress(FileNotFoundError):
        os.remove(os.path.join(workspace_path, cnf.IMAGES_FOLDER, class_folder_name))
    with contextlib.suppress(FileNotFoundError):
        os.remove(
            os.path.join(workspace_path, cnf.VALIDATION_FOLDER, class_folder_name)
        )


@app.route("/workspaces/<int:workspace_id>/images", methods=["GET"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def get_images(email, workspace_id: str):
    """
    Get image details.
    ---
    Parameters:
      - name: workspace_id
        in: path
        type: int
        required: true
    responses:
      200:
        description: Get routes of all images in workspace.
    """
    info = {"image_ids": get_all_image_ids(workspace_id)}
    return info, 200


@app.route("/workspaces/<int:workspace_id>/images", methods=[post])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def add_image_metadata(email, workspace_id: str):
    """
    Post image metadata.
    ---
    Parameters:
      - name: workspace_id
        in: path
        type: int
        required: true
    responses:
      201:
        description: Metadata has been added.
    """
    json_data = request.get_json()
    image = json_data["image"]
    class_id = json_data["id"]
    image_bytes = image.encode("ascii")
    workspace_name = f"workspace{workspace_id:03d}"
    workspace_path = os.path.join(cnf.WORKSPACES_BASE_PATH, workspace_name)
    cls_name = f"{class_id:05d}"
    cls_path = os.path.join(workspace_path, cls_name)
    n = len([x for x in os.listdir(cls_path) if x[:4] == "user"]) + 1
    with open(f"user_{n:03d}", "wb") as fh:
        fh.write(base64.decodebytes(image_bytes))
    info = {}
    return info, 201


@app.route("/workspaces/<int:workspace_id>/images/<string:image_id>", methods=[post])
@cross_origin(headers=["Content-Type", "Authorization"])
def add_image(workspace_id: str, image_id: str):
    """
    Post image.
    ---
    Parameters:
      - name: workspace_id
        in: path
        type: int
        required: true
    responses:
      201:
        description: Image has been added.
    """
    if "file" not in request.files:
        return {"message": "No input data provided"}, 400
    f = request.files["file"]
    if f:
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    info = {}
    return info, 201


@app.route("/workspaces/<int:workspace_id>/images/<string:image_id>", methods=[get])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def get_image(email, workspace_id: str, image_id: str):
    """
    Get image.
    ---
    Parameters:
      - name: workspace_id
        in: path
        type: int
        required: true
      - name: image_id
        in: path
        type: int
        required: true
    responses:
      200:
        description: Sending image.
    """
    workspace_name = f"workspace{workspace_id:03d}"
    image_path = os.path.join(workspace_name, utils.base64_to_path(image_id))
    return send_from_directory(cnf.WORKSPACES_BASE_PATH, image_path), 200


@app.route("/workspaces/<int:workspace_id>/images/<string:image_id>", methods=[delete])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def delete_image(email, workspace_id, image_id):
    move_to_trash(workspace_id, [image_id])
    return {}


@app.route(f"{w_path}/rpc/setModelParams", methods=[post])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def set_model_params(email, workspace_id: int):
    """
    Set params for models.
    ---
    Parameters:
      - name: workspace_id
        in: path
        type: int
        required: true
      - name: l
        description: learning rate
        in: body
        type: int
        required: true
      - name: t
        description: Test train split as percentage of test.
        in: body
        type: int
      - name: e
        description: Number of epochs
        in: body
        type: int
      - name: a
        description: Augmentation type
        enum: [random, all, selected]
        in: body
        type: string
      - name: f
        in: query
        type: string
    responses:
      200:
        description: Updated params.
    """
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    try:
        params = ModelParams(workspace_id=workspace_id, **json_data).dict()
        params.pop("workspace_id")
        Workspace.objects(workspace_id=workspace_id).update_one(
            model_settings=params, updated_at=datetime.utcnow()
        )
        return Workspace.objects.get(workspace_id=workspace_id).model_settings
    except ValidationError as e:
        app.logger.error("%s", e)
        return {"message": f"{e}"}, 400


@app.route(f"{w_path}/rpc/setAugmentation", methods=[post])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def set_augmentation(email, workspace_id):
    json_data = request.get_json()
    if not json_data:
        return {}
    augs = Workspace.objects.get(workspace_id=workspace_id).augmentations
    augs = {**augs, **json_data}
    Workspace.objects(workspace_id=workspace_id).update_one(
        augmentations=augs, updated_at=datetime.utcnow()
    )
    return augs


@app.route(f"{w_path}/rpc/startTrain", methods=[post])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def start_training(email, workspace_id: int):
    workspace = json.loads(Workspace.objects.get(workspace_id=workspace_id).to_json())
    print(workspace)
    return dl_main(workspace)


@app.route(f"{w_path}/rpc/getTrainInfo", methods=[get])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def get_training_info(email, workspace_id: int):
    return Workspace.objects.get(workspace_id=workspace_id).state


@app.route(f"{w_path}/rpc/stopTrain", methods=[post])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def stop_training(email, workspace_id: int):
    return rpc_call()


@app.route(f"{w_path}/rpc/getModelInfo", methods=[get])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def get_model_info(email, workspace_id: int):
    return rpc_call()


@app.route(f"{w_path}/rpc/infer", methods=[post])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def infer(email, workspace_id: int):
    return rpc_call()


@app.route(f"{w_path}/rpc/feedback", methods=[post])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def feedback(email, workspace_id: int):
    return rpc_call()


@app.route(f"{w_path}/rpc/getSuggestions", methods=[get])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def get_suggestions(email, workspace_id: int):
    return rpc_call()


@app.route("/test")
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def test(email):
    return {"message": email}


if __name__ == "__main__":
    app.run()
