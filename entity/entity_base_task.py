from typing import List, Any

from pydantic import BaseModel

import entity


class BaseTask(BaseModel):
    field_name: str = ""
    task_name: str
    description: str = ""
    function_name: str
    chat_round_number: int
    additional_fields: List[str] = []
    opinion_field: str

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.field_name = entity.get_field_name_by_real_name(self.task_name)

    def __getitem__(self, item):
        return getattr(self, item)
