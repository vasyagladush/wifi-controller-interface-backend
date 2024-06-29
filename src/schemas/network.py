from pydantic import ConfigDict

from schemas.joint import APIdSchema, SecurityIdSchema, WirelessIdSchema

from . import BaseSchema


class NetworkSchema(BaseSchema):
    id: int
    name: str
    ssid: str
    country_code: str
    access_points: list[APIdSchema]
    wireless: list[WirelessIdSchema]
    security: list[SecurityIdSchema]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 2,
                "name": "Guests",
                "ssid": "Example Co. Guests",
                "country_code": "PL",
                "access_points": [
                    {"id": 1, "deviceId": 13, "name": "Floor 1 AP"},
                    {"id": 3, "deviceId": 34, "name": "Floor 2 AP"},
                ],
                "wireless": [
                    {"id": 6},
                ],
                "security": [
                    {"id": 8},
                ],
            }
        },
    )
