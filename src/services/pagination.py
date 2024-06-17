import math
from typing import Any, Tuple, TypeVar

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=Tuple)


def paginate_query(query: Select[T], page: int, limit: int) -> Select[T]:
    return query.limit(limit).offset(
        page - 1 if page == 1 else (page - 1) * limit
    )


async def count_total_entities(
    db_session: AsyncSession, query: Select[Any]
) -> int:
    return (
        await db_session.execute(
            select(func.count()).select_from(query.alias())
        )
    ).scalar_one()


def get_total_pages(limit: int, total_count: int) -> int:
    return math.ceil(total_count / limit)


def get_has_next_page(page: int, total_pages: int) -> bool:
    return total_pages > page
