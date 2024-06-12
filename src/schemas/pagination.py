from . import BaseSchema


class PaginationParamsSchema(BaseSchema):
    page: int
    limit: int
