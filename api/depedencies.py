from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from api.databases import get_db
from api import crud
from api.auth import decode_access_token
from .models import User

#OAuth2 scheme: tells FASTAPI to look for token in Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)

):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail= 'could not validate credentials',
        headers={'ww-Authenticate': 'Bearer'},
    )

    token_data = decode_access_token(token)
    if token_data is None or token_data.username is None:
        raise credential_exception

    user = await crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credential_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail='inactive user')
    return current_user

