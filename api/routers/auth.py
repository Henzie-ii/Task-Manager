from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from api import auth, crud, schemas
from api.databases import get_db

router = APIRouter(prefix='/Auth', tags=['authenticated'])

@router.post('/register', response_model=schemas.UserOut)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    #check if user exist
    existing = await crud.get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400,  detail='username already registered')
    return await crud.create_user(db, user)

@router.post('/login', response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession=Depends(get_db)):
    user =  await crud.get_user_by_username(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = 'incorrect username or password'
        )
    access_token = auth.create_access_token(data={'sub':user.username})
    return {'access token': access_token, 'token_type':'bearer'}
