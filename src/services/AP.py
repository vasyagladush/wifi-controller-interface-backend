from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.AP import AP


async def get_APs(db_session: AsyncSession) -> list[AP] | None:
    return (await db_session.scalars(select(AP).order_by(AP.id))).all()


async def get_AP(db_session: AsyncSession, id: int) -> AP | None:
    return (await db_session.scalars(select(AP).where(AP.id == id))).first()


async def get_AP_by_name(db_session: AsyncSession, name: str) -> AP | None:
    if name != None:
        return (
            await db_session.scalars(select(AP).where(AP.name == name))
        ).first()
    return None
