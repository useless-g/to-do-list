from copy import deepcopy
from typing import List, Union
from fastapi import APIRouter, Depends, Request, Path, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from model import Task
from schema import *

router = APIRouter()


def get_db(request: Request):
    return request.state.db


def wrong_id():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=[{"loc": ["path", "pk"],
                                 "msg": "no tasks with this id"}])


@router.get('/', response_model=List[OldTask])
def get_all_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


@router.post('/add_task', response_model=NewTask)
def load_new_task(item: NewTask, db: Session = Depends(get_db)):
    task = Task(**item.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get('/{pk}', response_model=Union[OldTask, WrongId])
def get_task(pk: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task = db.query(Task).get(pk)
    if task:
        return task
    wrong_id()


@router.patch('/mark/{pk}', response_model=Union[OldTask, WrongId])
def mark_as_done(pk: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task = db.query(Task).get(pk)
    if task:
        db.query(Task).filter(Task.id == pk).update({Task.done: True}, synchronize_session='evaluate')
        db.commit()
        return task
    wrong_id()


@router.delete('/delete_task/{pk}', response_model=Union[OldTask, WrongId])
def delete_task(pk: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task = deepcopy(db.query(Task).get(pk))
    if task:
        db.query(Task).filter(Task.id == pk).delete(synchronize_session=False)
        db.commit()
        return task
    wrong_id()
