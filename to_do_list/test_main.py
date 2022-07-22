from databases import Database
from starlette.applications import Starlette
from starlette.config import Config

config = Config(".env")

TESTING = config('TESTING', cast=bool, default=False)
DATABASE_URL = config('DATABASE_URL', cast=databases.DatabaseURL)
TEST_DATABASE_URL = DATABASE_URL.replace(database='test_' + DATABASE_URL.database)

# Use 'force_rollback' during testing, to ensure we do not persist database changes
# between each test case.
if TESTING:
    database = databases.Database(TEST_DATABASE_URL, force_rollback=True)
else:
    database = databases.Database(DATABASE_URL)

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost/test_to_do"
Base = Database(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)



client = TestClient(app)


def test_get_all_tasks():
    response = client.get("/todo/")
    assert response.status_code == 200
