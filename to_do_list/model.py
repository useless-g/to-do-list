from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean

from db import Base


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String, nullable=False)
    text = Column(Text, nullable=True)
    date = Column(DateTime, nullable=False)
    done = Column(Boolean, default=False)
