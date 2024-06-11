from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.access_point import AccessPoint


async def get_APs(db_session: AsyncSession) -> Sequence[AccessPoint] | None:
    return (
        await db_session.scalars(
            select(AccessPoint)
            .options(selectinload(AccessPoint.networks))
            .order_by(AccessPoint.id)
        )
    ).all()


async def get_AP(db_session: AsyncSession, id: int) -> AccessPoint | None:
    return (
        await db_session.scalars(
            select(AccessPoint).where(AccessPoint.id == id)
        )
    ).first()


async def get_APs_by_name(
    db_session: AsyncSession, name: str
) -> Sequence[AccessPoint] | None:
    return (
        await db_session.scalars(
            select(AccessPoint)
            .filter(AccessPoint.name.ilike(f"%{name}%"))
            .options(selectinload(AccessPoint.networks))
            .order_by(AccessPoint.id)
        )
    ).all()
