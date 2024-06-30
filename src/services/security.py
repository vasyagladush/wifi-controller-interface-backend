from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.security import Security


async def get_security(db_session: AsyncSession, id: int) -> Security | None:
    return (
        await db_session.scalars(select(Security).where(Security.id == id))
    ).first()
