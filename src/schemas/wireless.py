from pydantic import ConfigDict

from schemas.joint import GenericIdentSchema

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
