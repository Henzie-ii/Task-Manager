import os
from dotenv import load_dotenv

load_dotenv()

class settings():
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: str = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30)

settings = settings()