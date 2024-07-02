from sqlalchemy import (Column, Integer, String)

from database import Base

class ResponsibleDB(Base):
    __tablename__ = "responsibles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)