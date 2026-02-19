from typing import Annotated, List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from datetime import timedelta

from schemas.token_schema import TokenResponse
from schemas.user_schema import UserCreateSchema, UserResponseSchema
from shared.db.async_session import get_async_db
from core.config import get_settings
from models.users import UserORM
from auth.user_token import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_user
)


router = APIRouter()

settings = get_settings()


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




@router.get("/", response_model=List[UserResponseSchema])
async def read_users(db: Annotated[AsyncSession, Depends(get_async_db)]):
    stmt = await db.execute(select(UserORM))

    users = stmt.scalars().all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
    return users

@router.get("/me", response_model=UserResponseSchema)
async def read_user_me(
    current_user: Annotated[UserORM, Depends(get_current_user)]
):
    return current_user

