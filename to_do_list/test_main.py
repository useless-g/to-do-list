import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, drop_database, create_database

from .db import SQLALCHEMY_DATABASE_URL
from .main import app
from .model import metadata


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """
    Create a clean database on every test case.
    """
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    if database_exists(SQLALCHEMY_DATABASE_URL):
        drop_database(SQLALCHEMY_DATABASE_URL)
    create_database(SQLALCHEMY_DATABASE_URL)  # Create the test database.
    metadata.create_all(engine)  # Create the tables.
    yield  # Run the tests.
    drop_database(SQLALCHEMY_DATABASE_URL)  # Drop the test database.


@pytest.fixture(scope="module")
def test_app():
    with TestClient(app) as client:
        yield client  # testing happens here


def test_get_all_tasks_empty(test_app):
    response = test_app.get("/todo/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_tasks_one_task(test_app):
    test_request_payload = {
        "title": "task 1",
        "text": "task text",
        "deadline": "2022-07-22"
    }
    test_app.post('/todo/add_task', data=json.dumps(test_request_payload))
    response = test_app.get("/todo/")
    assert response.status_code == 200
    assert response.json() == [dict(**test_request_payload, id=1, done=False)]
    test_app.delete('/todo/delete_task/1')


def test_get_all_tasks_multiple_tasks(test_app):
    test_request_payload1 = {
        "title": "task 2",
        "text": "task text",
        "deadline": "2022-07-22"
    }
    test_request_payload2 = {
        "title": "task 3",
        "text": "task text",
        "deadline": "2022-08-22"
    }
    test_app.post('/todo/add_task', data=json.dumps(test_request_payload1))
    test_app.post('/todo/add_task', data=json.dumps(test_request_payload2))
    response = test_app.get("/todo/")
    assert response.status_code == 200
    assert response.json() == [dict(**test_request_payload1, id=2, done=False),
                               dict(**test_request_payload2, id=3, done=False)]
    test_app.delete('/todo/delete_task/2')
    test_app.delete('/todo/delete_task/3')


def test_load_valid_task(test_app):
    test_request_payload = {
        "title": "task 4",
        "text": "task text",
        "deadline": "2022-07-22"
    }
    response = test_app.post('/todo/add_task', data=json.dumps(test_request_payload))
    assert response.status_code == 201
    assert response.json() == test_request_payload
    test_app.delete('/todo/delete_task/4')


def test_load_valid_task_without_text(test_app):
    test_request_payload = {
        "title": "task 5",
        "deadline": "2022-07-22"
    }
    response = test_app.post('/todo/add_task', data=json.dumps(test_request_payload))
    assert response.status_code == 201
    assert response.json() == dict(**test_request_payload, text=None)
    test_app.delete('/todo/delete_task/5')


def test_load_invalid_date_task(test_app):
    test_request_payload = {
        "title": "task 422",
        "text": "task text",
        "deadline": "2022-22"
    }
    test_response_payload = {'detail': [{'loc': ['body', 'deadline'],
                                         'msg': 'invalid date format',
                                         'type': 'value_error.date'}]}
    response = test_app.post('/todo/add_task', data=json.dumps(test_request_payload))
    assert response.status_code == 422
    assert response.json() == test_response_payload


def test_load_invalid_title_task(test_app):
    test_request_payload = {
        "title": 6,
        "text": "task text",
        "deadline": "2022-07-22"
    }
    test_response_payload = {
        "title": "6",
        "text": "task text",
        "deadline": "2022-07-22"
    }
    response = test_app.post('/todo/add_task', data=json.dumps(test_request_payload))
    assert response.status_code == 201
    assert response.json() == test_response_payload
    test_app.delete('/todo/delete_task/6')


def test_load_extra_arg_task(test_app):
    test_request_payload = {
        "title": "task 7",
        "text": "task text",
        "deadline": "2022-07-22",
        "extra": "param"
    }
    test_response_payload = {
        "title": "task 7",
        "text": "task text",
        "deadline": "2022-07-22"
    }
    response = test_app.post('/todo/add_task', data=json.dumps(test_request_payload))
    assert response.status_code == 201
    assert response.json() == test_response_payload
    test_app.delete('/todo/delete_task/7')


def test_get_task(test_app):
    test_request_payload = {
        "title": "task 8",
        "text": "task text",
        "deadline": "2022-07-22"
    }
    test_app.post('/todo/add_task', data=json.dumps(test_request_payload))
    response = test_app.get('/todo/8')
    assert response.status_code == 200
    assert response.json() == dict(**test_request_payload, id=8, done=False)
    test_app.delete('/todo/delete_task/8')


def test_get_task_wrong_id(test_app):
    test_request_payload = {
        "title": "task 9",
        "text": "task text",
        "deadline": "2022-07-22"
    }
    test_app.post('/todo/add_task', data=json.dumps(test_request_payload))
    response = test_app.get('/todo/99')
    assert response.status_code == 404
    assert response.json() == {"detail": [{"loc": ["path", "pk"], "msg": "no tasks with this id"}]}
    test_app.delete('/todo/delete_task/9')


def test_get_task_not_positive_id(test_app):
    test_request_payload = {
        "title": "task 10",
        "text": "task text",
        "deadline": "2022-07-22"
    }
    test_app.post('/todo/add_task', data=json.dumps(test_request_payload))
    response = test_app.get('/todo/0')
    assert response.status_code == 422
    assert response.json() == {'detail': [{'ctx': {'limit_value': 0},
                                           'loc': ['path', 'pk'],
                                           'msg': 'ensure this value is greater than 0',
                                           'type': 'value_error.number.not_gt'}]}
    test_app.delete('/todo/delete_task/10')


def test_get_task_not_integer_id(test_app):
    test_request_payload = {
        "title": "task 11",
        "text": "task text",
        "deadline": "2022-07-22"
    }
    test_app.post('/todo/add_task', data=json.dumps(test_request_payload))
    response = test_app.get('/todo/qwerty')
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['path', 'pk'],
                                           'msg': 'value is not a valid integer',
                                           'type': 'type_error.integer'}]}
    test_app.delete('/todo/delete_task/11')


def test_mark_as_done(test_app):
    test_request_payload = {
        "title": "task 12",
        "text": "task text",
        "deadline": "2022-07-22"
    }
    test_app.post('/todo/add_task', data=json.dumps(test_request_payload))
    response = test_app.patch('/todo/mark/12')
    assert response.status_code == 200
    assert response.json() == dict(**test_request_payload, id=12, done=True)
    test_app.delete('/todo/delete_task/12')


def test_mark_as_done_wrong_id(test_app):
    test_request_payload = {
        "title": "task 13",
        "text": "task text",
        "deadline": "2022-07-22"
    }
    test_app.post('/todo/add_task', data=json.dumps(test_request_payload))
    response = test_app.patch('/todo/mark/1313')
    assert response.status_code == 404
    assert response.json() == {"detail": [{"loc": ["path", "pk"], "msg": "no tasks with this id"}]}
    test_app.delete('/todo/delete_task/13')


def test_mark_as_done_not_positive_id(test_app):
    test_request_payload = {
        "title": "task 14",
        "text": "task text",
        "deadline": "2022-07-22"
    }
    test_app.post('/todo/add_task', data=json.dumps(test_request_payload))
    response = test_app.patch('/todo/mark/-14')
    assert response.status_code == 422
    assert response.json() == {'detail': [{'ctx': {'limit_value': 0},
                                           'loc': ['path', 'pk'],
                                           'msg': 'ensure this value is greater than 0',
                                           'type': 'value_error.number.not_gt'}]}
    test_app.delete('/todo/delete_task/14')


def test_mark_as_done_not_integer_id(test_app):
    test_request_payload = {
        "title": "task 15",
        "text": "task text",
        "deadline": "2022-07-22"
    }
    test_app.post('/todo/add_task', data=json.dumps(test_request_payload))
    response = test_app.patch('/todo/mark/err')
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['path', 'pk'],
                                           'msg': 'value is not a valid integer',
                                           'type': 'type_error.integer'}]}
    test_app.delete('/todo/delete_task/15')


def test_delete_task(test_app):
    test_request_payload = {
        "title": "task 16",
        "text": "task text",
        "deadline": "2022-07-22"
    }
    test_app.post('/todo/add_task', data=json.dumps(test_request_payload))
    response = test_app.delete('/todo/delete_task/16')
    assert response.status_code == 200
    assert response.json() == {'detail': "task deleted"}


def test_delete_task_wrong_id(test_app):
    test_request_payload = {
        "title": "task 17",
        "text": "task text",
        "deadline": "2022-07-22"
    }
    test_app.post('/todo/add_task', data=json.dumps(test_request_payload))
    response = test_app.delete('/todo/delete_task/16')
    assert response.status_code == 404
    assert response.json() == {"detail": [{"loc": ["path", "pk"], "msg": "no tasks with this id"}]}
    test_app.delete('/todo/delete_task/17')


def test_delete_task_not_positive_id(test_app):
    test_request_payload = {
        "title": "task 18",
        "text": "task text",
        "deadline": "2022-07-22"
    }
    test_app.post('/todo/add_task', data=json.dumps(test_request_payload))
    response = test_app.delete('/todo/delete_task/-16')
    assert response.status_code == 422
    assert response.json() == {'detail': [{'ctx': {'limit_value': 0},
                                           'loc': ['path', 'pk'],
                                           'msg': 'ensure this value is greater than 0',
                                           'type': 'value_error.number.not_gt'}]}
    test_app.delete('/todo/delete_task/18')


def test_delete_task_not_integer_id(test_app):
    test_request_payload = {
        "title": "task 19",
        "text": "task text",
        "deadline": "2022-07-22"
    }
    test_app.post('/todo/add_task', data=json.dumps(test_request_payload))
    response = test_app.delete('/todo/delete_task/0.5')
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['path', 'pk'],
                                           'msg': 'value is not a valid integer',
                                           'type': 'type_error.integer'}]}
    test_app.delete('/todo/delete_task/19')
