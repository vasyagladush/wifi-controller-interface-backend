from typing import Optional

from pydantic import ConfigDict

from schemas.joint import GenericIdentSchema

from . import BaseSchema, PaginatedSchema


class APSchema(BaseSchema):
    id: int
    device_id: int
    name: str
    ip: str
    networks: list[GenericIdentSchema]

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


class GetAPsSchema(PaginatedSchema[APSchema]):
    pass


class NetworkSetSchema(BaseSchema):
    id: int


class PutAPSchema(BaseSchema):
    name: Optional[str] = None
    networks: Optional[list[NetworkSetSchema]] = None
