from pydantic import BaseModel
from typing import List

class TaskData(BaseModel):
    name: str
    description: str
    employer_id: int
    unit_tests: str # TODO: не думаю, що це буде str
    complexity_id: int

class TaskIDResponse(BaseModel):
    task_ids: List[int]
    task_names: List[str]