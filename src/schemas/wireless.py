from typing import Optional

from pydantic import ConfigDict

from schemas.joint import GenericIdentSchema, GenericIdSchema

from . import BaseSchema


class WirelessSchema(BaseSchema):
    id: int
    name: str
    vht: bool
    acs: bool
    beacon_interval: int
    rts_cts_threshold: int
    networks: list[GenericIdentSchema]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 3,
                "name": "Wireless 1",
                "vht": True,
                "acs": False,
                "beacon_interval": 30,
                "networks": [
                    {"id": 2, "name": "Guests"},
                    {"id": 3, "name": "Employees"},
                ],
            }
        },
    )


class PutWirelessSchema(BaseSchema):
    name: Optional[str] = None
    vht: Optional[bool] = None
    acs: Optional[bool] = None
    beacon_interval: Optional[int] = None
    rts_cts_threshold: Optional[int] = None
    networks: Optional[list[GenericIdSchema]] = None
