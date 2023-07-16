from datetime import datetime
from pydantic import BaseModel


class Note(BaseModel):
    id: str
    title: str
    content: str | None = None
    created_at: datetime| None = None
    updated_at: datetime| None = None
    user_id: str| None


class NoteCreate(BaseModel):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: str
    content: str