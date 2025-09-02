import logging.config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.config import get_config
from api.handlers import auth, resumes, improvements
from api.ioc import build_container
from dishka.integrations.fastapi import setup_dishka
from pathlib import Path

app = FastAPI(
    title=get_config().app.title,
    version=get_config().app.version,
    docs_url=get_config().app.docs_url,
    openapi_url=get_config().app.openapi_url,
)

if Path("logging.ini").exists():
    logging.config.fileConfig("logging.ini", disable_existing_loggers=False)

# Добавить CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(resumes.router)
app.include_router(improvements.router)

container = build_container()

setup_dishka(container, app)