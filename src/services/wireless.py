from sqlalchemy import Sequence, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.wireless import Wireless


async def create_wireless(
    db_session: AsyncSession,
    name: str,
    vht: bool,
    acs: bool,
    beacon_interval: int,
    rts_cts_threshold: int,
) -> Wireless:
    new_wireless = Wireless(
        name=name,
        vht=vht,
        acs=acs,
        beacon_interval=beacon_interval,
        rts_cts_threshold=rts_cts_threshold,
    )
    await db_session.add(new_wireless)
    await db_session.commit()
    return new_wireless


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
