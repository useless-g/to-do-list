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
sudo apt update

sudo apt install postgresql postgresql-contrib

sudo systemctl start postgresql.service

sudo -i -u postgres

\password postgres

123

123

\q

exit

sudo apt install python3-virtualenv

sudo apt install python3.8-venv

python3 -m venv ./env

source ./env/bin/activate

git clone https://github.com/useless-g/to-do-list/

cd to-do-list/

sudo apt install pip

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
