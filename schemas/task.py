from datetime import datetime
from sqlalchemy import (Column, Integer, String, DateTime, Text)

from database import Base


class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    assigned_to = Column(String, index=True)
    due_date = Column(DateTime)
    status = Column(String, default='Open')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)



