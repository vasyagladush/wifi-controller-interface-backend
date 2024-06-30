from pydantic import ConfigDict

from schemas.joint import APIdSchema, GenericIdentSchema

from . import BaseSchema


class NetworkSchema(BaseSchema):
    id: int
    name: str
    ssid: str
    country_code: str
    access_points: list[APIdSchema]
    wireless: list[GenericIdentSchema]
    security: list[GenericIdentSchema]

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
                    {"id": 6, "name": "Wireless 1"},
                ],
                "security": [
                    {"id": 8, "name": "Default"},
                ],
            }
        },
    )
