from typing import Sequence, TypedDict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.access_point import AccessPoint
from services.pagination import (
    count_total_entities,
    get_has_next_page,
    get_total_pages,
    paginate_query,
)


class PaginatedAPsResult(TypedDict):
    docs: Sequence[AccessPoint]
    total_docs: int
    total_pages: int
    has_next_page: bool


async def get_APs(db_session: AsyncSession) -> Sequence[AccessPoint] | None:
    return (
        await db_session.scalars(
            select(AccessPoint)
            .options(selectinload(AccessPoint.networks))
            .order_by(AccessPoint.id)
        )
    ).all()


async def get_APs_by_name(
    db_session: AsyncSession, name: str
) -> Sequence[AccessPoint] | None:
    return (
        await db_session.scalars(
            select(AccessPoint)
            .filter(AccessPoint.name.ilike(f"%{name}%"))
            .options(selectinload(AccessPoint.networks))
            .order_by(AccessPoint.id)
        )
    ).all()


async def get_paginated_APs(
    db_session: AsyncSession, page: int, limit: int, name=None
) -> PaginatedAPsResult:
    query = (
        select(AccessPoint)
        .options(selectinload(AccessPoint.networks))
        .order_by(AccessPoint.id)
    )
    if name:
        query = query.filter(AccessPoint.name.ilike(f"%{name}%"))

    query = paginate_query(query, page, limit)

    access_points = (await db_session.scalars(query)).all()
    count = await count_total_entities(db_session, AccessPoint)

    total_pages = get_total_pages(limit, count)
    # TODO: count and total_pages and total_docs are not affected by the name filter. Need to fix this
    return {
        "docs": access_points,
        "total_docs": count,
        "total_pages": total_pages,
        "has_next_page": get_has_next_page(page, total_pages),
    }


async def get_AP(db_session: AsyncSession, id: int) -> AccessPoint | None:
    return (
        await db_session.scalars(
            select(AccessPoint).where(AccessPoint.id == id)
        )
    ).first()
