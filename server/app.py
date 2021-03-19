import base64
from io import BytesIO

import torchvision.transforms as transforms
from flask import jsonify, request, Flask
from PIL import Image

import torchcommands

app = Flask(__name__)


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')


if __name__ == "__main__":
    app.run()
