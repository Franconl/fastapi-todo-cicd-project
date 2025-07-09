from pydantic import BaseModel
from typing import Optional, List
import uuid

class Task(BaseModel):
    id: str = None
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __init__(self, **data):
        super().__init__(**data)
        if self.id is None:
            self.id = str(uuid.uuid4())
