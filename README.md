Description
===========
RESTapi for todo-list

Stack: FastAPI, sqlalchemy, postgresql, databases, alembic, pydantic, pytest

Install (Windows)
=================
pip install virtualenv

virtualenv env

git clone https://github.com/useless-g/to-do-list/

cd /D to-do-list

pip install -r requirements.txt

uvicorn to_do_list.main:app --port 8000

Install (linux)
===============

pip install virtualenv

virtualenv env

source ./env/bin/activate

git clone https://github.com/useless-g/to-do-list/

cd to-do-list

pip install -r requirements.txt

uvicorn to_do_list.main:app --port 8000

Run
===
127.0.0.1:8000/to_do/

Swagger
=======
127.0.0.1:8000/docs

Redoc
=====
127.0.0.1:8000/redoc
