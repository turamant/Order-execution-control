from pydantic import BaseModel
from datetime import datetime

class Task(BaseModel):
    id: int
    title: str
    description: str
    assigned_to: str
    due_date: datetime
    status: str = 'Open'
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class Responsible(BaseModel):
    id: int
    name: str
    email: str
    phone: str


class Status(BaseModel):
    id: int
    name: str
    description: str


class Comment(BaseModel):
    id: int
    task_id: int
    author: str
    text: str
    created_at: datetime = datetime.now()