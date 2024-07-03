from pydantic import ConfigDict

from . import BaseSchema


class GenericIdentSchema(BaseSchema):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"id": 1, "name": "SomeName"}},
    )


class GenericIdSchema(BaseSchema):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"id": 1}},
    )


class APIdSchema(BaseSchema):
    id: int
    name: str
    device_id: int


class MacListSchema(BaseSchema):
    id: int
    name: str
    macs: list[str]
