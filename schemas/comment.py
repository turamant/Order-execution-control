from datetime import datetime
from sqlalchemy import (Column, Integer, String, DateTime, Text, ForeignKey)
from database import Base


class CommentDB(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    author = Column(String)
    text = Column(Text)
    created_at = Column(DateTime, default=datetime.now)