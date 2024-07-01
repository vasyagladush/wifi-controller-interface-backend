from sqlalchemy import Sequence, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.mac_acl import MACACL


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
