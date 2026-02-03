from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from core.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.ASYNC_SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session