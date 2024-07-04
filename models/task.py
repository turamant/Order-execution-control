from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from models.status import Status
from models.responsible import Responsible

class Task(BaseModel):
    id: int
    title: str
    description: str
    responsible_id: int
    status_id: int
    due_date: datetime
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    responsible: Optional["Responsible"] = None
    status: Optional["Status"] = None





