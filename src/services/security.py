from sqlalchemy import Sequence, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.security import Security


async def get_security(db_session: AsyncSession, id: int) -> Security | None:
    return (
        await db_session.scalars(select(Security).where(Security.id == id))
    ).first()


async def get_security_by_exact_name(
    db_session: AsyncSession, name: str
) -> Sequence[Security] | None:
    return (
        await db_session.scalars(
            select(Security)
            .filter(Security.name == name)
            .options(selectinload(Security.mac_acls))
            .order_by(Security.id)
        )
    ).first()
