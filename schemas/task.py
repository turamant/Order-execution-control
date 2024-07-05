from datetime import datetime
from sqlalchemy import (ForeignKey, Column, Integer, String, DateTime, Text)
from sqlalchemy.orm import relationship
from database import Base
from .responsible import ResponsibleDB
from .status import StatusDB

class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    responsible_id = Column(Integer, ForeignKey('responsibles.id'), index=True)
    status_id = Column(Integer, ForeignKey('statuses.id'), index=True)
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    responsible = relationship("ResponsibleDB", backref="tasks")
    status = relationship("StatusDB", backref="tasks")
    comments = relationship("CommentDB", back_populates="task")

