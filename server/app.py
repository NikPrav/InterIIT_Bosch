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


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file("../web/build/index.html")


@app.route("/info", methods=["GET"])
def get_project_info():
    info = {}
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
