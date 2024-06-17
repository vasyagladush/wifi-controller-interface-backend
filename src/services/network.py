from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.network import Network


async def get_network(db_session: AsyncSession, id: int) -> Network | None:
    return (
        await db_session.scalars(select(Network).where(Network.id == id))
    ).first()
