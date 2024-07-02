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