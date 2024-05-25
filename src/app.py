from fastapi import FastAPI
import logging
from contextlib import asynccontextmanager
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import app_config, session_manager
from routes.users import router as UsersRouter


logging.basicConfig(
    stream=sys.stdout, level=logging.DEBUG if app_config.DEBUG_LOGS else logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if session_manager._engine is not None:
        # Close the DB connection
        await session_manager.close()

app = FastAPI(lifespan=lifespan, title="WiFi Controller")

app.add_middleware(
    CORSMiddleware,
    allow_origins=list('*'),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Index"])
async def read_root():
    return {"cool": True}

app.include_router(UsersRouter, tags=["Users"], prefix="/users")
