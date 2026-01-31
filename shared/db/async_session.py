from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


from core.config import Settings

engine = create_async_engine(
    Settings.ASYNC_SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session