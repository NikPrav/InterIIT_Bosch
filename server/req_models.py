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


class ModelParams(BaseModel):
    workspace_id: int
    t: conint(gt=4, lt=60)  # test train split
    l: confloat(gt=10 ** (-7), lt=1)  # learn rate
    e: conint(gt=1, lt=2000)  # #epochs
    a: constr(
        strip_whitespace=True, to_lower=True, regex="(random|all|select)"
    ) = "select"


class ClassCreate(BaseModel):
    class_name: str
