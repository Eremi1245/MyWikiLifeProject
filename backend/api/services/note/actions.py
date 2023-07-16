from typing import List

from fastapi import HTTPException
from database.services import ElasticsearchCRUDClient
from database.index_mappings import INDEXES
from api.services.note.models import NoteCreate,Note,NoteUpdate
from database.exceptions import IndexCRUDOperationsError
from rich import print

note_elastic_client = ElasticsearchCRUDClient(INDEXES["NOTE_INDEX"])

def get_notes()->List[Note]:
    results = note_elastic_client.get_all_documents()
    notes = []
    for res in results:
        note = {}
        note['id'] = res['_id']
        note.update(res["_source"])
        notes.append(note)
    return notes

# Вставляем заметку в Elasticsearch
def create_note(note: NoteCreate)->Note:
    note_dict = note.dict()
    new_doc = note_elastic_client.create_document(note_dict)
    return new_doc

def get_note_by_id(note_id:str)->Note:
    try:
        note = note_elastic_client.get_document_by_id(note_id)
    except IndexCRUDOperationsError:
        note = {}
    return note

def update_note(note_id:str,update_note:NoteUpdate)->Note:
    update_note = update_note.dict()
    update_note = {'doc': update_note}
    try:
        updated_document = note_elastic_client.update_document_by_id(note_id,update_note)
        doc = {}
        doc['id'] = updated_document['_id']
        doc.update(updated_document['_source'])
        return doc
    except IndexCRUDOperationsError:
        raise HTTPException(status_code=404, detail="Note not updated")


def delete_note(note_id:str):
    try:
        note_elastic_client.delete_document_by_id(note_id)
    except IndexCRUDOperationsError:
        raise HTTPException(status_code=404, detail="Note not deleted")