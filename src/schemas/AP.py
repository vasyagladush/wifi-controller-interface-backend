from pydantic import ConfigDict

from . import BaseSchema


class NetworkNameSchema(BaseSchema):
    name: str

    model_config = ConfigDict(
        from_attributes=True, json_schema_extra={"example": {"name": "Guests"}}
    )


class APSchema(BaseSchema):
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
                "device_id": 5,
                "name": "Floor 1 AP",
                "ip": "192.168.1.6",
                "networks": [
                    {"name": "Guests"},
                    {"name": "Employees"},
                ],
            }
        },
    )
