import base64
import json
import os
import typing as t
from datetime import datetime
from functools import wraps
from io import BytesIO
from urllib.request import urlopen

import requests
import torchcommands
import torchvision.transforms as transforms
import utils
from configs import cnf
from core import (add_dataset_to_workspace, create_workspace_dir,
                  get_all_image_ids, move_to_trash,
                  remove_dataset_from_workspace)
from dbmodels import Dataset, Globals, Info, User, Workspace
from flask import (Flask, _request_ctx_stack, jsonify, request,
                   send_from_directory)
from flask_cors import cross_origin
from jose import jwt
from PIL import Image
from pydantic import ValidationError
from req_models import ModelParams, WorkspaceCreate, WorkspacePatch
from werkzeug.datastructures import Headers
from werkzeug.wrappers import BaseResponse

app = Flask(__name__)

get, post, put, patch, delete = "GET", "POST", "PUT", "PATCH", "DELETE"

w_path = "/workspaces/<int:workspace_id>"
img_path = "/workspaces/<int:workspace_id>/images/<string:image_id>"

rpc_call = lambda: {"state": "success"}
email = "ch17btech11023@iith.ac.in"

app = Flask(__name__)

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
    ustub = request.headers.get("User_sub", None)
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
    return token, auth, ustub


def requires_auth(f):
    """Determines if the Access Token is valid"""

    @wraps(f)
    def decorated(*args, **kwargs):

        token, auth, ustub = get_token_auth_header()
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
                # headers = {"Authorization": auth}
                # response = requests.get(
                #     f"https://dev-kqx4v2yr.jp.auth0.com/api/v2/users/{ustub}",
                #     headers=headers,
                # )
                # response_json = response.json()
                # email = response_json.get("email")
                email = "ch17btech11023@iith.ac.in"

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


@app.route("/info", methods=["GET"])
def get_project_info():
    info = Info.objects.exclude("_id").to_json()
    return info


@app.route("/workspaces", methods=["GET"])
def get_workspaces():
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
    return workspaces


@app.route("/workspaces", methods=["POST"])
def create_workspace():
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
            }, 400
        s = set(range(user_id * 10 + 1, user_id * 10 + 11)) - {
            w.workspace_id for w in Workspace.objects(user_email=email)
        }
        print(s)
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
def get_workspace(workspace_id: str):
    info = Workspace.objects(workspace_id=workspace_id).exclude("_id")[0].to_json()
    return info


@app.route("/workspaces/<int:workspace_id>", methods=["PATCH"])
def edit_workspace(workspace_id: int):
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
        merged_datasets = list({*existing_datasets, *data["datasets"]})
        data["datasets"] = merged_datasets
        Workspace.objects(workspace_id=workspace_id).update_one(**data)
        return Workspace.objects(workspace_id=workspace_id).to_json()
    except ValidationError as e:
        app.logger.error("%s", e)
        return {"message": f"{e}"}, 400


@app.route("/workspaces/<int:workspace_id>/images", methods=["GET"])
def get_images(workspace_id: str):
    info = {"image_ids": get_all_image_ids(workspace_id)}
    return info


@app.route("/workspaces/<int:workspace_id>/images", methods=[post])
def add_image_metadata(workspace_id: str):
    info = {}
    return info


@app.route("/workspaces/<int:workspace_id>/images/<string:image_id>", methods=[put])
def add_image(workspace_id: str, image_id: str):
    info = {}
    return info


@app.route("/workspaces/<int:workspace_id>/images/<string:image_id>", methods=[get])
def get_image(workspace_id: str, image_id: str):
    workspace_name = f"workspace{workspace_id:03d}"
    image_path = os.path.join(workspace_name, utils.base64_to_path(image_id))
    return send_from_directory(cnf.WORKSPACES_BASE_PATH, image_path)


@app.route(f"{w_path}/rpc/setModelParams", methods=[post])
def set_model_params(workspace_id: int):
    all_args = dict(request.args)
    try:
        params = ModelParams(workspace_id=workspace_id, **all_args).dict()
        params.pop("workspace_id")
        Workspace.objects(workspace_id=workspace_id).update_one(
            model_settings=params, updated_at=datetime.utcnow()
        )
        return Workspace.objects.get(workspace_id=workspace_id).model_settings
    except ValidationError as e:
        app.logger.error("%s", e)
        return {"message": f"{e}"}, 400


@app.route(f"{w_path}/rpc/setAugmentation", methods=[post])
def set_augmentation(workspace_id):
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
def start_training(workspace_id: int):
    workspace = json.loads(Workspace.objects.get(workspace_id=workspace_id).to_json())
    print(workspace)
    return rpc_call()


@app.route(f"{w_path}/rpc/getTrainInfo", methods=[get])
def get_training_info(workspace_id: int):
    return rpc_call()


@app.route(f"{w_path}/rpc/stopTrain", methods=[post])
def stop_training(workspace_id: int):
    return rpc_call()


@app.route(f"{w_path}/rpc/getModelInfo", methods=[get])
def get_model_info(workspace_id: int):
    return rpc_call()


@app.route(f"{w_path}/rpc/infer", methods=[post])
def infer(workspace_id: int):
    return rpc_call()


@app.route(f"{w_path}/rpc/feedback", methods=[post])
def feedback(workspace_id: int):
    return rpc_call()


@app.route(f"{w_path}/rpc/getSuggestions", methods=[get])
def get_suggestions(workspace_id: int):
    return rpc_call()


if __name__ == "__main__":
    app.run()
