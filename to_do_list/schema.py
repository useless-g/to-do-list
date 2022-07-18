from datetime import datetime
from typing import List, Dict, Union

from pydantic import BaseModel, Field


class NewTask(BaseModel):
    title: str = Field(..., description='this field is for the title of the task')
    text: str = Field(..., description='this field is for the task itself')
    date: datetime = Field(..., description='this field is for the due date of the task')

    class Config:
        orm_mode = True


class OldTask(NewTask):
    id: int = Field(..., description='this field is unique identifier')
    done: bool = Field(..., description='this field shows whether the task was completed or not')


class WrongId(BaseModel):
    detail: List[Dict[str, Union[List[str], str]]]
