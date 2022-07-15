from datetime import date

from pydantic import BaseModel


class NewTask(BaseModel):
    title: str
    text: str
    date: date

    class Config:
        orm_mode = True


class OldTask(NewTask):
    done: bool
