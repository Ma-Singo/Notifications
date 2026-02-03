from pydantic import BaseModel, Field, EmailStr, SecretStr, ConfigDict
from schemas.token_schema import TokenResponse


class User(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=50)


class UserCreateSchema(User):
    password: str = Field(min_length=6, max_length=32)


class UserResponseSchema(User):

    id: int
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)


    model_config = ConfigDict(from_attributes=True)

class UserResponseTokenSchema(UserResponseSchema):
    token: TokenResponse

    model_config = ConfigDict(from_attributes=True)


