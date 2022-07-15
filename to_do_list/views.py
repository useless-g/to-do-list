from typing import List

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from model import Task
from schema import NewTask, OldTask

router = APIRouter()


def get_db(request: Request):
    return request.state.db


@router.get('/{id}')
def get_task(id: int):
    pass


@router.get('/', response_model=List[OldTask])
def get_all(db: Session = Depends(get_db)):
    return db.query(Task).all()


@router.post('/new')
def load_task(item: NewTask, db: Session = Depends(get_db)):
    task = Task(**item.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return {'task created': task}
