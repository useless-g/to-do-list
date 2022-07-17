from typing import List
from fastapi import APIRouter, Depends, Request, Path
from sqlalchemy.orm import Session
from starlette.responses import Response

from model import Task
from schema import NewTask, OldTask

router = APIRouter()


def get_db(request: Request):
    return request.state.db


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


@router.get('/{pk}', response_model=OldTask)
def get_task(pk: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task = db.query(Task).get(pk)
    return task if task else Response(status_code=404)  # todo: make right responses for each endpoint


@router.patch('/mark/{pk}')
def mark_as_done(pk: int = Path(..., gt=0), db: Session = Depends(get_db)):
    if db.query(Task).filter(Task.id == pk).update({Task.done: True}, synchronize_session='evaluate'):
        db.commit()
        return {'task marked as done': pk}
    else:
        return {'there are no task with this id': pk}


@router.delete('/delete_task/{pk}')
def delete_task(pk: int = Path(..., gt=0), db: Session = Depends(get_db)):
    if db.query(Task).filter(Task.id == pk).delete(synchronize_session=False):
        db.commit()
        return {'task deleted': pk}
    else:
        return {'there are no task with this id': pk}
