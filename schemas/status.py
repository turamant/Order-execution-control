from sqlalchemy import (Column, Integer, String, Text)

from database import Base

class StatusDB(Base):
    __tablename__ = "statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)