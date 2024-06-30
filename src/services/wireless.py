from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.wireless import Wireless


async def get_wireless(db_session: AsyncSession, id: int) -> Wireless | None:
    return (
        await db_session.scalars(select(Wireless).where(Wireless.id == id))
    ).first()
