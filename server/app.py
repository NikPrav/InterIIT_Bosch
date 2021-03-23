import base64
from datetime import datetime
import json
import typing as t
from functools import wraps
from io import BytesIO

# from six.moves.urllib.request import urlopen
from urllib.request import urlopen

import torchvision.transforms as transforms
from flask import Flask, _request_ctx_stack, jsonify, request
from flask_cors import cross_origin
from jose import jwt
from PIL import Image
from pydantic import ValidationError
from werkzeug.datastructures import Headers
from werkzeug.wrappers import BaseResponse
import requests

import torchcommands
from configs import cnf
from dbmodels import Dataset, Globals, Info, Workspace
from req_models import WorkspaceCreate

app = Flask(__name__)

get, post, put, patch, delete = "GET", "POST", "PUT", "PATCH", "DELETE"

w_path = "/workspaces/<int:workspace_id>"
img_path = "/workspaces/<string:workspace_id>/images/<string:image_id>"

rpc_call = lambda: {"state": "success"}

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
def get_workspaces(email):
    workspaces = Workspace.objects(user_email=email).only(
        "name",
        "datasets",
        "added_images",
        "workspace_id",
    )
    return workspaces


@app.route("/workspaces", methods=["POST"])
def create_workspace(email):
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    try:
        data = WorkspaceCreate(**json_data).dict()
        app.logger.info("%s", data)
    except ValidationError as e:
        app.logger.info("%s", e)
        return {"message": "Wrong input data provided"}, 400
    if Workspace.objects(user_email=email).count() >= 10:
        return {"message": "You have reached the limit in number of workspaces."}, 400
    num = Workspace.objects.count() + 1
    workspace = Workspace(
        **data,
        user_email=email,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        workspace_id=num,
    )
    workspace.save()
    return workspace.to_json()


@app.route("/workspaces/<int:workspace_id>", methods=["GET"])
def get_workspace(email, workspace_id: str):
    info = Workspace.objects(workspace_id=workspace_id).to_json()
    return info


@app.route("/workspaces/<int:workspace_id>", methods=["PATCH"])
def edit_workspace(email, workspace_id: str):
    info = {}
    return info


@app.route("/workspaces/<int:workspace_id>/images", methods=["GET"])
def get_images(workspace_id: str):
    info = {}
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
    info = {}
    return info


@app.route(f"{w_path}/rpc/startTrain", methods=[post])
def start_training(workspace_id: int):
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


@app.route(f"{w_path}/rpc/getSuggestions", methods=[get])
def get_suggestions(workspace_id: int):
    return rpc_call()


if __name__ == "__main__":
    app.run()
