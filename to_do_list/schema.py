from datetime import date
from typing import List, Dict, Union
from pydantic import BaseModel, Field, validator


class NewTask(BaseModel):
    title: str = Field(..., description='this field is for the title of the task')
    text: Union[str, None] = Field(default=None, description='this field is for the task itself')
    deadline: date = Field(..., description='this field is for the due date of the task')

    class Config:
        orm_mode = True


class OldTask(NewTask):
    id: int = Field(..., description='this field is unique identifier')
    done: Union[bool, None] = Field(default=False, description='this field shows whether the task was completed or not')

    @validator('done')
    def check_done(cls, done_):
        if done_ is None:
            done_ = False
        return done_


class WrongId(BaseModel):
    detail: List[Dict[str, Union[List[str], str]]]


class TaskDeleted(BaseModel):
    detail: str = "task deleted"
