from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

#User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(BaseModel):
    password: str

class UserOut(BaseModel):
    id: int
    is_active: bool
    created_at: datetime
    class Config:
        from_attribute = True


#Task schemas

class TaskBase(BaseModel):
    title: str = Field(..., min_lenhtgh=1, max_length=100)
    description: Optional[str] = None
    complleted: bool = False

class TokenCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    compleeted: Optional[str] = None

class TaskOut(TaskBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        from_attribute = True

#Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None