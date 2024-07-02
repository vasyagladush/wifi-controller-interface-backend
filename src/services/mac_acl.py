from typing import Optional

from sqlalchemy import Sequence, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.mac_acl import MACACL
from models.security import Security


async def get_mac_acl(db_session: AsyncSession, id: int) -> MACACL | None:
    return (
        await db_session.scalars(select(MACACL).where(MACACL.id == id))
    ).first()


async def get_mac_acl_by_exact_name(
    db_session: AsyncSession, name: str
) -> Sequence[MACACL] | None:
    return (
        await db_session.scalars(
            select(MACACL)
            .filter(MACACL.name == name)
            .options(selectinload(MACACL.security))
            .order_by(MACACL.id)
        )
    ).first()


async def get_security(db_session: AsyncSession, id: int) -> Security | None:
    return (
        await db_session.scalars(select(Security).where(Security.id == id))
    ).first()


async def create_mac_acl(
    db_session: AsyncSession,
    name: str,
    macs: list[str],
    security: Optional[list[Security]] = None,
):
    if await get_mac_acl_by_exact_name(db_session, name) is not None:
        raise ValueError
    mac_acl = MACACL(name=name, macs=macs)
    if security is not None:
        for sec in security:
            if await get_security(db_session, sec.id) is None:
                raise IndexError
    db_session.add(mac_acl)
    await db_session.commit()
