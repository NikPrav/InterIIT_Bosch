import base64
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
from werkzeug.datastructures import Headers
from werkzeug.wrappers import BaseResponse

import torchcommands
from models import Info, Globals, Workspace, Dataset

_str_bytes = t.Union[str, bytes]
_data_type = t.Union[
    _str_bytes,
    BaseResponse,
    t.Dict[str, t.Any],
    t.Callable[
        [t.Dict[str, t.Any], t.Callable[[str, t.List[t.Tuple[str, str]]], None]],
        t.Iterable[bytes],
    ],
]
_status_type = t.Union[int, _str_bytes]
_headers_type = t.Union[
    Headers,
    t.Dict[_str_bytes, _str_bytes],
    t.Iterable[t.Tuple[_str_bytes, _str_bytes]],
]

view_return_type = t.Union[
    _data_type,
    t.Tuple[_data_type],
    t.Tuple[_data_type, _status_type],
    t.Tuple[_data_type, _headers_type],
    t.Tuple[_data_type, _status_type, _headers_type],
]

app = Flask(__name__)

get, post, put, patch, delete = "GET", "POST", "PUT", "PATCH", "DELETE"

w_path = "/workspaces/<int:workspace_id>"
img_path = "/workspaces/<string:workspace_id>/images/<string:image_id>"

rpc_call = lambda: {"state": "success"}

AUTH0_DOMAIN = "YOUR_DOMAIN"
API_AUDIENCE = "YOUR_API_AUDIENCE"
ALGORITHMS = ["RS256"]

APP = Flask(__name__)

# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file("../web/build/index.html")


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header"""
    auth = request.headers.get("Authorization", None)
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
    return token


def requires_auth(f):
    """Determines if the Access Token is valid"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
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
            return f(*args, **kwargs)
        raise AuthError(
            {"code": "invalid_header", "description": "Unable to find appropriate key"},
            401,
        )

    return decorated


@app.route("/info", methods=["GET"])
def get_project_info():
    info = Info.objects.exclude("_id").to_json()
    return info


@app.route("/workspaces", methods=["GET"])
def get_workspaces():
    info = {}
    return info


@app.route("/workspaces", methods=["POST"])
def create_workspace():
    info = {}
    return info


@app.route("/workspaces/<int:workspace_id>", methods=["GET"])
def get_workspace(workspace_id: str):
    info = {}
    return info


@app.route("/workspaces/<int:workspace_id>", methods=["PATCH"])
def edit_workspace(workspace_id: str):
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
