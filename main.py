from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.exceptions import ValidationException, RequestValidationError
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException


from typing import Annotated

from core.config import Settings, get_settings

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")
templates = Jinja2Templates(directory="templates")


@app.get("/settings")
def hello(settings: Annotated[Settings, Depends(get_settings)]):
    return {"App Name": settings.APP_NAME}

@app.get("/", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
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

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api/"):
        return request_validation_exception_handler(request, exception)
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "exception": exception.errors(),
        }
    )
