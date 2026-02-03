from typing import Annotated, List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import timedelta

from schemas.token_schema import TokenPayload, TokenResponse
from schemas.user_schema import UserCreateSchema, UserResponseSchema, UserResponseTokenSchema
from shared.db.async_session import get_async_db
from core.config import get_settings
from models.users import UserORM
from auth.user_token import (
    authenticate_user,
    create_access_token,
    get_password_hash
)


router = APIRouter()

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/v1/create", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def async_create_user(
    payload: UserCreateSchema,
    db: Annotated[AsyncSession, Depends(get_async_db)]
):
    stmt = await db.execute(
        select(UserORM)
        .where(UserORM.username == payload.username)
    )
    user = stmt.scalars().first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    user = UserORM(
            username=payload.username,
            email=payload.email,
            hashed_password=get_password_hash(payload.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.post("/token", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login_for_access_token(
        db: Annotated[AsyncSession, Depends(get_async_db)],
        form_data: OAuth2PasswordRequestForm = Depends(),

):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise credentials_exception
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user.username,
        user.email,
        expires_delta=access_token_expires,
    )
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )

@router.get("/me", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
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
    except InvalidTokenError:
        raise credentials_exception

    stmt = await db.execute(
        select(UserORM).filter(UserORM.username == token_data.username)
    )
    user = stmt.scalars().first()
    if user is None:
        raise credentials_exception

    return user


@router.get("/", response_model=List[UserResponseSchema])
async def read_users(db: Annotated[AsyncSession, Depends(get_async_db)]):
    stmt = await db.execute(select(UserORM))

    users = stmt.scalars().all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
    return users


