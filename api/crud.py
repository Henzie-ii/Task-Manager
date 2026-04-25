from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from api import models, schemas
from .auth import get_hashed_password

#user CRUD
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select.models.User).where(models.User.username==username)
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_pw = get_hashed_password(user.password)
    db_user = models.User(
        email = user.email,
        username = user.username,
        hashed_password = hashed_pw
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_tasks(db: AsyncSession, user_id: int, skip: int=0, limit:int=100):
    result = await db.execute(
        select(models.Task)
        .where(models.Task.owner_id==user_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def update_task(db: AsyncSession, task_id: int, task_update:schemas.TaskUpdate, user_id: int ):
    #first ensure the task belong to the user
    stmt = select(models.Task).where(models.Task.id == task_id, models.Task.owner_id == user_id )
    result  = await db.execute(stmt)
    db_task = result.scalar_one_or_none()
    if not db_task:
        return None
    #only update provided field
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)

    await db.commit()
    await db.refresh(db_task)
    return db_task

async def delete(db:AsyncSession, task_id:int, user_id:int):
    stmt = delete(models.Task).where(models.Task.id==task_id, models.Task.owner_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0