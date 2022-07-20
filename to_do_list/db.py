from databases import Database
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost/to_do"
Base = Database(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)  # echo all SQL in stdout

# SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
# Base = declarative_base()
