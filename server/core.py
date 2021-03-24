import os
import pathlib

import utils
from configs import cnf
from dbmodels import User


def add_user_if_not_exists(email: str):
    if User.objects(email=email).count() == 0:
        count = User.objects.count()
        user = User(email=email, user_id=count)
        user.save()


def create_workspace_dir(workspace_id: int):
    workspace_name = f"workspace{workspace_id:03d}"
    pathlib.Path(os.path.join(cnf.WORKSPACES_BASE_PATH, workspace_name)).mkdir(
        parents=True, exist_ok=True
    )


def add_dataset_to_workspace(dataset_path, workspace_path):
    pass


def remove_dataset_from_workspace(workspace_path, dataset_path):
    pass


def remove_image_from_workspace(path_to_img):
    pass
