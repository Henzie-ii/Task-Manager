from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from .config import settings

#create async engine
engine = create_async_engine(settings.DATABASE_URL, echo=True)

#session factory
AsyncSessionLocal = async_sessionmaker(
    engine,  class_=AsyncSession, expire_on_commit=False
)

#Base class for SQLAlachemy
Base = declarative_base()

#Dependency to get A DB session in endpoints
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
