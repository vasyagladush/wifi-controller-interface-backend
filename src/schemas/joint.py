from pydantic import ConfigDict

from . import BaseSchema


class APIdSchema(BaseSchema):
    id: int
    name: str
    device_id: int


class NetworkIdSchema(BaseSchema):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"id": 1, "name": "Guests"}},
    )


class SecurityIdSchema(BaseSchema):
    id: int


class WirelessIdSchema(BaseSchema):
    id: int


class MacListSchema(BaseSchema):
    id: int
    macs: list[str]
