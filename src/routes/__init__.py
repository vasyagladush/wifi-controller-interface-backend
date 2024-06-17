from fastapi import Query

from schemas.pagination import PaginationParamsSchema


def PaginationParamsDep(
    page: int = Query(ge=1, required=False, default=1),
    limit: int = Query(ge=1, le=100, required=False, default=20),
):
    return PaginationParamsSchema(page=page, limit=limit)
