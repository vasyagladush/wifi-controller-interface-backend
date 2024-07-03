from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import hash_helper
from models.user import User
from schemas.user import UserSignUpSchema


async def get_user(db_session: AsyncSession, id: int) -> User | None:
    return (
        await db_session.scalars(select(User).where(User.id == id))
    ).first()


async def get_users(db_session: AsyncSession) -> Sequence[User] | None:
    return (await db_session.scalars(select(User))).all()


async def get_user_by_username(
    db_session: AsyncSession, username: str
) -> User | None:
    return (
        await db_session.scalars(select(User).where(User.username == username))
    ).first()


async def create_user(
    db_session: AsyncSession,
    user_data: UserSignUpSchema,
    commit_and_refresh: bool = True,
) -> User:
    password_hash: str = hash_helper.encrypt(user_data.password)

    new_user = User()
    new_user.username = user_data.username
    new_user.password_hash = password_hash
    new_user.first_name = user_data.first_name
    new_user.last_name = user_data.last_name

    db_session.add(new_user)

    if commit_and_refresh:
        await db_session.commit()
        await db_session.refresh(new_user)

    return new_user
