from typing import List, Union
from fastapi import APIRouter, Depends, Request, Path, HTTPException, status
from .model import Task
from .schema import *
from .db import Base

router = APIRouter()


def wrong_id():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=[{"loc": ["path", "pk"],
                                 "msg": "no tasks with this id"}])


@router.get('/', response_model=List[OldTask])
async def get_all_tasks():
    query = Task.select()
    return await Base.fetch_all(query)


@router.post('/add_task', status_code=status.HTTP_201_CREATED, response_model=NewTask)
async def load_new_task(item: NewTask):
    query = Task.insert().values(**item.dict())
    await Base.execute(query)
    return item


@router.get('/{pk}', response_model=Union[OldTask, WrongId])
async def get_task(pk: int = Path(..., gt=0)):
    task = await Base.fetch_one(query=Task.select().where(Task.c.id == pk))
    if task:
        return task
    wrong_id()


@router.patch('/mark/{pk}', response_model=Union[OldTask, WrongId])
async def mark_as_done(pk: int = Path(..., gt=0)):
    task = await Base.fetch_one(query=Task.select().where(Task.c.id == pk))
    if task:
        query = Task.update().where(Task.c.id == pk).values(done=True)
        await Base.execute(query)
        response = dict(**task)
        response['done'] = True
        return response
    wrong_id()


@router.delete('/delete_task/{pk}', response_model=TaskDeleted)
async def delete_task(pk: int = Path(..., gt=0)):
    task = await Base.fetch_one(query=Task.select().where(Task.c.id == pk))
    if task:
        query = Task.delete().where(Task.c.id == pk)
        await Base.execute(query)
        return {'detail': "task deleted"}
    wrong_id()
