from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, DecodeError

from core.config import get_settings
from models.users import UserORM
from shared.db.async_session import get_async_db
from schemas.token_schema import TokenPayload




password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/token")
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

    # converting date -> timestamp -> int
    to_encode.update(dict(exp=int(expire.timestamp())))
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[AsyncSession, Depends(get_async_db)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("username")
        email = payload.get("email")

        if username is None or email is None:
            raise credentials_exception

        token_data = TokenPayload(
            username=username,
            email=email,
        )

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except DecodeError as e:
        # Specific handling for the exp integer issue
        print(f"Decode error: {e}")  # For debugging
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has invalid format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise credentials_exception

    stmt = await db.execute(
        select(UserORM).filter(UserORM.username == token_data.username)
    )
    user = stmt.scalars().first()
    if user is None:
        raise credentials_exception

    return user

