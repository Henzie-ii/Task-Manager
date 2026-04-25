from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from api.databases import get_db
from api.models import User
from api import crud, schemas
from depedencies import get_current_active_user

router = APIRouter(prefix='/tasks', tag=['tasks'])

@router.get('/', response_model=List[schemas.TaskOut])
async def read_task(
    skip: int = 0,
    limit: int = 100,
    db:AsyncSession = Depends(get_db),
    current_user:User = Depends(get_current_active_user)
):
    tasks = await crud.get_tasks(db, user_id=current_user.id, skip=skip, limit=limit)
    return tasks

@router.post('/', response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: schemas.TaskCreate,
    db:AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return crud,create_task(db, task, user_id=current_user.id)
   

@router.put('/', response_model=schemas.TaskOut)
async def update_task(
    task_id: int,
    task_update: schemas.TaskUpadte,
    db:AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user) 

):
    updated = await crud.update_task(db, task_id, task_update, current_user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db:AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
    
):
    deleted = await crud.delete_task(db, task_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Task not found')