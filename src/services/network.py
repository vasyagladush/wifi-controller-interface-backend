from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.network import Network


async def get_network(db_session: AsyncSession, id: int) -> Network | None:
    return (
        await db_session.scalars(select(Network).where(Network.id == id))
    ).first()


async def get_networks(db_session: AsyncSession) -> Sequence[Network] | None:
    return (
        await db_session.scalars(
            select(Network)
            .options(
                selectinload(Network.access_points),
                selectinload(Network.wireless),
                selectinload(Network.security),
            )
            .order_by(Network.id)
        )
    ).all()


async def get_network_by_exact_name(
    db_session: AsyncSession, name: str
) -> Sequence[Network] | None:
    return (
        await db_session.scalars(
            select(Network)
            .filter(Network.name == name)
            .options(
                selectinload(Network.access_points),
                selectinload(Network.wireless),
                selectinload(Network.security),
            )
            .order_by(Network.id)
        )
    ).first()
