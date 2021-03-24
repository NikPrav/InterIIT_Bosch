from typing import Any, Dict, List, Optional

from pydantic import BaseModel, confloat, conint, constr


class WorkspaceCreate(BaseModel):
    name: str
    datasets: Optional[List[str]]


class WorkspacePatch(BaseModel):
    workspace_id: int
    datasets: Optional[List[str]] = []
    imgs_to_delete: Optional[List[str]]
    model_settings: Optional[dict]


class ModelParams(BaseModel):
    workspace_id: int
    t: conint(gt=20, lt=40)  # test train split
    l: confloat(gt=0, lt=5)  # learn rate
    e: conint(gt=10, lt=2000)  # #epochs
    a: constr(
        strip_whitespace=True, to_lower=True, regex="(random|all|select)"
    ) = "select"
