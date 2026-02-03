from contextlib import asynccontextmanager
from fastapi import FastAPI

from shared.db.async_session import engine
from shared.db.base import Base




@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()