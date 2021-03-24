import base64
import os
import pathlib


def base64_to_path(chunk):
    pass


def path_to_base64chunk(path):
    pass


def wid_to_path(wid: int):
    pass


def ln_s(src_file, dst_dir, dst_filename=None):
    pathlib.Path(dst_dir).mkdir(parents=True, exist_ok=True)
    dst_path = os.path.join(dst_dir, dst_filename) if dst_filename else dst_dir
    os.symlink(src_file, dst_path)
