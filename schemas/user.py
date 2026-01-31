from pydantic import BaseModel, Field, EmailStr, SecretStr, ConfigDict


class User(BaseModel):
    username: str = Field(alias="name", min_length=1, max_length=50)
    email: EmailStr = Field(max_length=50)
    password: SecretStr = Field(min_length=6, max_length=32)

class CreateUser(User):
    pass


class UserResponse(User):
    model_config = ConfigDict(from_attributes=True)

    image_file: str | None
    image_path: str
    id: int

