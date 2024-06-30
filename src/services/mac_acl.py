from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.mac_acl import MACACL


async def get_mac_acl(db_session: AsyncSession, id: int) -> MACACL | None:
    return (
        await db_session.scalars(select(MACACL).where(MACACL.id == id))
    ).first()
