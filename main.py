from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError, ValidationException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.v1.routers import users
from core.config import get_settings
from shared.db.lifespan import lifespan


# FOR SYNCHRONOUS DATABASE
# from sqlalchemy.orm import Session
# from shared.db.base import Base
# from shared.db.session import get_db, engine
# Base.metadata.create_all(bind=engine)


settings = get_settings()

app = FastAPI(lifespan=lifespan)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


app.include_router(users.router, prefix="/api/users", tags=["users"])




@app.get("/")
def home_page(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "app_name": settings.APP_NAME
        }
    )

@app.exception_handler(StarletteHTTPException)
def my_exception_handler(request: Request, exception: StarletteHTTPException):
    if request.url.path.startswith("/api/"):
        return http_exception_handler(request, exception)
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "exception": exception.detail,
            "title": exception.status_code,
            "status": exception.status_code,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(ValidationException)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api/"):
        return request_validation_exception_handler(request, exception)
    return templates.TemplateResponse(request, "error.html", {"exception": exception.errors()})
