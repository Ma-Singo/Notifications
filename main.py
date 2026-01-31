from fastapi import FastAPI, Depends


from typing import Annotated

from core.config import settings

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello World!", "secret_key": settings.ACCESS_TOKEN_EXPIRE_MINUTES}

