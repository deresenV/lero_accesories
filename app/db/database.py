from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings



#debug режим
if settings.debug_type:
    engine = create_async_engine(settings.database_url, echo=True)
else:
    engine = create_async_engine(settings.database_url)

Base = declarative_base()
AsyncSessionLocal = sessionmaker(
    bind = engine,
    class_= AsyncSession,
    expire_on_commit = False
)

async def create_tables():
    """Создает все таблицы в базе данных"""
    async with engine.begin() as conn:
        import app.db.models
        await conn.run_sync(Base.metadata.create_all)