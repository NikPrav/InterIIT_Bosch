import base64
import os
import pathlib


def base64_to_path(chunk):
    return base64.urlsafe_b64decode(chunk.encode("ascii")).decode("ascii")


def path_to_base64(path):
    return base64.urlsafe_b64encode(path.encode("ascii")).decode("ascii")


def wid_to_path(wid: int):
    pass


def ln_s(src_file, dst_dir, dst_filename=None):
    pathlib.Path(dst_dir).mkdir(parents=True, exist_ok=True)
    dst_path = os.path.join(dst_dir, dst_filename) if dst_filename else dst_dir
    os.symlink(src_file, dst_path)
