from sqlalchemy import Sequence, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.mac_acl import MACACL
from models.security import Security


async def create_security(
    db_session: AsyncSession,
    name: str,
    wireless_security_type: int,
    radius: str,
    eap: bool,
    mac_acl_type: int,
    mac_acls: list[MACACL],
) -> Security:
    new_security = Security(
        name=name,
        wireless_security_type=wireless_security_type,
        radius=radius,
        eap=eap,
        mac_acl_type=mac_acl_type,
    )
    for acl in mac_acls:
        new_security.mac_acls.append(acl)
    db_session.add(new_security)
    await db_session.commit()
    return new_security


async def get_security(db_session: AsyncSession, id: int) -> Security | None:
    return (
        await db_session.scalars(select(Security).where(Security.id == id))
    ).first()


async def get_security_by_exact_name(db_session: AsyncSession, name: str):
    return (
        await db_session.scalars(
            select(Security)
            .filter(Security.name == name)
            .options(selectinload(Security.mac_acls))
            .order_by(Security.id)
        )
    ).first()
