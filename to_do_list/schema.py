from datetime import datetime
from pydantic import BaseModel, Field


class NewTask(BaseModel):
    title: str = Field(..., description='this field is for the title of the task')
    text: str = Field(..., description='this field is for the task itself')
    date: datetime = Field(..., description='this field is for the due date of the task')

    class Config:
        orm_mode = True


class OldTask(NewTask):
    done: bool = Field(..., description='this field shows whether the task was completed or not')
