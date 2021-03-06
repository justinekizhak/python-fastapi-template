import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from {{cookiecutter.project_root}}.api import api_v1
from {{cookiecutter.project_root}}.core.config import settings, set_env

from dotenv import load_dotenv

import typer
from loguru import logger

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_DOC}/openapi.json",
    debug=settings.DEBUG,
    version=settings.VERSION,
    docs_url=settings.API_SWAGGER_URL,
    redoc_url=settings.API_DOC,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_v1.api_router, prefix=settings.API_V1_STR)


@app.get("/", status_code=301)
def redirect_to_api():
    return RedirectResponse(settings.API_DOC, status_code=301)


def main():
    uvicorn.run(
        "{{cookiecutter.project_root}}.__main__:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.SERVER_RELOAD,
    )


if __name__ == "__main__":
    typer.run(main)
