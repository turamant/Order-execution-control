from pydantic import BaseModel
from datetime import datetime


class Comment(BaseModel):
    id: int
    task_id: int
    author: str
    text: str
    created_at: datetime = datetime.now()