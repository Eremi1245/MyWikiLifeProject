from pydantic import BaseModel


# Пример модели данных для заметки
class Note(BaseModel):
    id: str
    title: str
    content: str
