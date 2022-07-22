from databases import Database
from sqlalchemy import create_engine

TESTING = False
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost/to_do"
TEST_DATABASE_URL = "postgresql://postgres:123@localhost/test_to_do"

if TESTING:
    SQLALCHEMY_DATABASE_URL = TEST_DATABASE_URL

Base = Database(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)  # echo all SQL in stdout
