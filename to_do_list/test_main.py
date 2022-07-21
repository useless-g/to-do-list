from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_some():
    response = client.get("/todo/")
    assert response.status_code == 200
  #   assert response.json() == [
  # {
  #   "title": "string",
  #   "text": None,
  #   "deadline": "2022-07-20",
  #   "id": 34,
  #   "done": False
  # },
  # {
  #   "title": "string",
  #   "text": None,
  #   "deadline": "2022-07-20",
  #   "id": 35,
  #   "done": False
  # },
  # {
  #   "title": "string",
  #   "text": "string",
  #   "deadline": "2022-07-20",
  #   "id": 36,
  #   "done": False
  # },
  # {
  #   "title": "string",
  #   "text": "string",
  #   "deadline": "2022-07-20",
  #   "id": 37,
  #   "done": False
  # },
  # {
  #   "title": "string",
  #   "text": "string",
  #   "deadline": "2022-07-20",
  #   "id": 38,
  #   "done": False
  # }]