from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import databases


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost/to_do"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
db = databases.Database(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()
