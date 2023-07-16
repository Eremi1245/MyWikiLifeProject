from typing import List
from fastapi import APIRouter, HTTPException
from api.services.note.models import NoteCreate, NoteUpdate, Note
from api.services.note import actions



router = APIRouter(prefix="/notes")



# Создание заметки
@router.post("/", response_model = Note)
def create_note(note: NoteCreate):
    return actions.create_note(note)

# Получение всех заметок
@router.get("/",response_model = List[Note])
def get_all_notes():
    notes = actions.get_notes()
    return notes

# Получение заметки по ID
@router.get("/{note_id}",response_model=Note)
def get_note_by_id(note_id: str):
    note = actions.get_note_by_id(note_id)
    if note:
        valid_note = {}
        valid_note['id'] = note['_id']
        valid_note.update(note['_source'])
        return valid_note
    else:
        raise HTTPException(status_code=404, detail="Note not found")

# Обновление заметки
@router.put("/{note_id}",response_model=Note)
def update_note(note_id: str, note: NoteUpdate):
    return actions.update_note(note_id,note)

# Удаление заметки
@router.delete("/{note_id}",status_code=201)
def delete_note(note_id: str):
    actions.delete_note(note_id)