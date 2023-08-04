from datetime import datetime as dt
from pydantic import BaseModel


class LOLMatch(BaseModel):
    Week: int | None = None
    team1: str | None = None
    team2: str | None = None
    datetime: dt | None = None
    link: str | None = None

# class NoteCreate(BaseModel):
#     title: str
#     content: str

# class NoteUpdate(BaseModel):
#     title: str
#     content: str
