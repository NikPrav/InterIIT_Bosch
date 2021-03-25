from typing import Any, Dict, List, Optional

from pydantic import BaseModel, confloat, conint, constr


class WorkspaceCreate(BaseModel):
    name: str
    datasets: Optional[List[str]]


class WorkspacePatch(BaseModel):
    workspace_id: int
    datasets: Optional[List[str]] = []
    imgs_to_delete: Optional[List[str]]
    datasets_to_delete: Optional[List[str]]
    datasets_to_add: Optional[List[str]]
    model_settings: Optional[dict]
    test_preferred_images: Optional[List[str]]
    train_preferred_images: Optional[List[str]]


class ModelParams(BaseModel):
    workspace_id: int
    test_train_split: conint(gt=4, lt=60)  # test train split
    learning_rate: confloat(gt=10 ** (-7), lt=1)  # learn rate
    epochs: conint(gt=1, lt=2000)  # #epochs
    batch_size: conint(ge=16, le=512, multiple_of=2)
    a: constr(
        strip_whitespace=True, to_lower=True, regex="(random|all|select)"
    ) = "random"


class ClassCreate(BaseModel):
    class_name: str
