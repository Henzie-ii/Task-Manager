from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import timedelta, timezone
from api.schemas import TokenData

#password hashing
pwd_context =  CryptContext(schemes=['bcrypt'], deperecated='auto')

#jwt settings

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE = os.getenv('ACCESS_TOKEN_EXPIRE')

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_hashed_password(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE))
    to_encode.update({'exp':expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=[ALGORITHM])

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username in None:
            return None
        return TokenData(username=username)
    except JWTError:
        return None
    