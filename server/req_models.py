from typing import Any, Dict, List, Optional

from pydantic import BaseModel

class WorkspaceCreate(BaseModel):
    name: str
    datasets: Optional[List[str]]


