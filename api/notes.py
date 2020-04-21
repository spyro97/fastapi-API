from api import crud
from typing import List
from api.models import NoteDB, NoteSchema
from fastapi import APIRouter, HTTPException, Path, BackgroundTasks

router = APIRouter()


@router.post("/", response_model=NoteDB, status_code=201)
async def create_note(background_tasks: BackgroundTasks, payload: NoteSchema):
    note_id = await crud.post(payload)

    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object

# Mandar una tarea que se realice en el fondo
@router.post("/background", status_code=201)
async def create_note(background_tasks: BackgroundTasks, payload: NoteSchema):
    note_id = background_tasks.add_task(await crud.post(payload))

    return {'message':'tarea enviada al fondo'}

@router.get("/{id}/", response_model=NoteDB)
async def read_note(id: int = Path(..., gt=0),):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.get("/", response_model=List[NoteDB])
async def read_all_notes():
    return await crud.get_all()

@router.put("/{id}/", response_model=NoteDB)
async def update_note(id: int, payload: NoteSchema):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note_id = await crud.put(id, payload)

    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object

@router.delete("/{id}/", response_model=NoteDB)
async def delete_note(id: int = Path(..., gt=0)):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    await crud.delete(id)

    return note