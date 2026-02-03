from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt

from core.config import get_settings
from models.users import UserORM
from shared.db.async_session import get_async_db



password_hash = PasswordHash.recommended()
settings = get_settings()


def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str, db: Annotated[AsyncSession, Depends(get_async_db)]):
    stmt = await db.execute(
        select(UserORM).filter(UserORM.username == username)
    )
    user = stmt.scalars().first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, email: str, expires_delta: timedelta | None = None):
    to_encode = {
        "username": username,
        "email": email,
    }
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire.isoformat()})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


