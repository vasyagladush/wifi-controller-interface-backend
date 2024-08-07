from typing import Optional

from pydantic import ConfigDict

from schemas.joint import GenericIdentSchema, GenericIdSchema

from . import BaseSchema


class MacAclSchema(BaseSchema):
    id: int
    name: str
    macs: list[str]
    security: list[GenericIdentSchema]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "id": 2,
            "name": "ACL 1",
            "macs": ["01:01:01:01:01:01", "01:01:01:01:01:02"],
            "security": [
                {"id": 2, "name": "Default"},
                {"id": 3, "name": "WPA3"},
            ],
        },
    )


class PutMacAclSchema(BaseSchema):
    name: Optional[str] = None
    macs: Optional[list[str]] = None
    security: Optional[list[GenericIdSchema]] = None
