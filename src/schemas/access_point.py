from pydantic import ConfigDict

from . import BaseSchema


class NetworkNameSchema(BaseSchema):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"id": 1, "name": "Guests"}},
    )


class APSchema(BaseSchema):
    id: int
    device_id: int
    name: str
    ip: str
    networks: list[
        NetworkNameSchema
    ]  # TODO: Verify that this how this should be done

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "deviceId": 5,
                "name": "Floor 1 AP",
                "ip": "192.168.1.6",
                "networks": [
                    {"id": 2, "name": "Guests"},
                    {"id": 3, "name": "Employees"},
                ],
            }
        },
    )
