from contextlib import asynccontextmanager
from typing import Annotated, Any, AsyncIterator
from typing import Optional
from fastapi import Depends
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from passlib.context import CryptContext


class AppConfig(BaseSettings):
    PYTHONPATH: str = "./src"
    DATABASE_URL: str = "sqlite:///./database.sqlite"
    JWT_SECRET_KEY: Optional[str] = None
    DEBUG_LOGS: bool = False
    ECHO_SQL: bool = False

    class Config:
        env_file = ".env"
        from_attributes = True


app_config = AppConfig()

# Heavily inspired by https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(
            host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


session_manager = DatabaseSessionManager(
    app_config.DATABASE_URL, {"echo": app_config.ECHO_SQL})


async def get_db_session():
    async with session_manager.session() as session:
        yield session

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


hash_helper = CryptContext(schemes=["bcrypt"])
