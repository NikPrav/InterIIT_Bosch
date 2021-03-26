import datetime
import os
import pathlib
import shutil

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
    for item in [
        cnf.IMAGES_FOLDER,
        cnf.VALIDATION_FOLDER,
        cnf.MODELS_FOLDER,
        cnf.INF_FOLDER,
        cnf.PLOTS_FOLDER,
    ]:
        pathlib.Path(
            os.path.join(cnf.WORKSPACES_BASE_PATH, workspace_name, item)
        ).mkdir(parents=True, exist_ok=True)


def get_all_image_ids(workspace_id: int):
    workspace_name = f"workspace{workspace_id:03d}"
    workspace_path = os.path.join(cnf.WORKSPACES_BASE_PATH, workspace_name)
    images_list = [
        os.path.join(cnf.IMAGES_FOLDER, cls, f)
        for cls in os.listdir(os.path.join(workspace_path, cnf.IMAGES_FOLDER))
        for f in os.listdir(os.path.join(workspace_path, cnf.IMAGES_FOLDER, cls))
    ]
    images_list.extend(
        os.path.join(cnf.VALIDATION_FOLDER, cls, f)
        for cls in os.listdir(os.path.join(workspace_path, cnf.VALIDATION_FOLDER))
        for f in os.listdir(os.path.join(workspace_path, cnf.VALIDATION_FOLDER, cls))
    )
    return [utils.path_to_base64(image) for image in images_list]


def add_dataset_to_workspace(dataset, workspace_id):
    workspace_name = f"workspace{workspace_id:03d}"
    workspace_path = os.path.join(cnf.WORKSPACES_BASE_PATH, workspace_name)
    dataset_path = os.path.join(cnf.DATASETS_BASE_PATH, dataset)
    for cls in os.listdir(dataset_path):
        if os.path.isdir(cls):
            cls_path = os.path.join(dataset_path, cls)
            for img in cls:
                img_path = os.path.join(cls_path, img)
                dst_path = os.path.join(workspace_path, cnf.IMAGES_FOLDER, cls)
                utils.ln_s(img_path, dst_path)


def remove_dataset_from_workspace(workspace_id, dataset):
    workspace_name = f"workspace{workspace_id:03d}"
    workspace_path = os.path.join(cnf.WORKSPACES_BASE_PATH, workspace_name)
    imgs_path = os.path.join(workspace_path, cnf.IMAGES_FOLDER)
    for cls in os.listdir(imgs_path):
        if os.path.isdir(cls):
            cls_path = os.path.join(imgs_path, cls)
            for img in os.listdir(cls_path):
                if img[:4] == dataset:
                    os.remove(os.path.join(cls_path, img))


def move_to_trash(workspace_id, list_of_files):
    dict_ = {}
    workspace_name = f"workspace{workspace_id:03d}"
    base = os.path.join(cnf.WORKSPACES_BASE_PATH, workspace_name)
    for f in list_of_files:
        path = os.path.join(base, utils.base64_to_path(f))
        new_name = f"{str(datetime.datetime.now().isoformat())}_{f[:5]}"
        shutil.move(
            path,
            os.path.join(cnf.TRASH_BASE_PATH, new_name),
        )
        dict_[new_name] = (f, datetime.datetime.now().isoformat())
    return dict_
