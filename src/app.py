import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_responses import custom_openapi

from config import app_config, session_manager
from routes.access_points import router as AccessPointsRouter
from routes.console import router as ConsoleRouter
from routes.mac_acl import router as MacACLRouter
from routes.network import router as NetworksRouter
from routes.security import router as SecurityRouter
from routes.users import router as UsersRouter
from routes.wireless import router as WirelessRouter

# from routes.debug import router as DebugRouter

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG if app_config.DEBUG_LOGS else logging.INFO,
)


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


app = FastAPI(
    lifespan=lifespan,
    title="WiFi Controller",
    docs_url=None if app_config.ENVIRONMENT == "production" else "/docs",
)
app.openapi = custom_openapi(app)

# TODO: when we have production env set up, add FRONTEND_URL to .env and here if ENVIRONMENT == production then set allow_origin to the FRONTEND_URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=list("*"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Index"])
async def read_root():
    return {"cool": True}


app.include_router(UsersRouter, tags=["Users"], prefix="/users")
app.include_router(
    AccessPointsRouter, tags=["Access points"], prefix="/access-points"
)
app.include_router(ConsoleRouter, tags=["Console"], prefix="/console")
app.include_router(NetworksRouter, tags=["Networks"], prefix="/networks")
app.include_router(WirelessRouter, tags=["Wireless"], prefix="/wireless")
app.include_router(SecurityRouter, tags=["Security"], prefix="/security")
app.include_router(MacACLRouter, tags=["MAC ACL"], prefix="/mac-acls")
# app.include_router(DebugRouter, tags=["Debug"], prefix="/debug")
