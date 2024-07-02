from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.access_point import AccessPoint
from models.network import Network
from models.security import Security
from models.wireless import Wireless


async def create_network(
    aps: list[AccessPoint],
    db_session: AsyncSession,
    name: str,
    ssid: str,
    country_code: str,
    password,
    wireless: list[Wireless],
    security: list[Security],
) -> None:
    new_net = Network(
        name=name, ssid=ssid, country_code=country_code, password=password
    )
    for ap in aps:
        new_net.access_points.append(ap)
    for w in wireless:
        new_net.wireless.append(w)
    for s in security:
        new_net.security.append(s)
    db_session.add(new_net)
    await db_session.commit()


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


async def get_network_by_exact_name(db_session: AsyncSession, name: str):
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
