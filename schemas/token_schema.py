from pydantic import BaseModel, EmailStr, ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    username: str
    email: EmailStr

class TokenResponse(Token):

    model_config = ConfigDict(from_attributes=True)