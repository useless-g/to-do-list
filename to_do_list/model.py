from sqlalchemy import Column, Integer, String, Text, Date, Boolean, MetaData, Table

metadata = MetaData()
from .db import Base


Task = Table(
    'tasks',
    metadata,
    Column('id', Integer, primary_key=True, index=True, unique=True),
    Column('title', String, nullable=False),
    Column('text', Text, nullable=True),
    Column('deadline', Date, nullable=False),
    Column('done', Boolean, default=False),
)
