from sqlalchemy import Sequence, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.wireless import Wireless


async def get_wireless(db_session: AsyncSession, id: int) -> Wireless | None:
    return (
        await db_session.scalars(select(Wireless).where(Wireless.id == id))
    ).first()


async def get_wireless_by_exact_name(
    db_session: AsyncSession, name: str
) -> Sequence[Wireless] | None:
    return (
        await db_session.scalars(
            select(Wireless)
            .filter(Wireless.name == name)
            .options(selectinload(Wireless.networks))
            .order_by(Wireless.id)
        )
    ).first()
