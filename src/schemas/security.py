from typing import Optional

from pydantic import ConfigDict

from schemas.joint import GenericIdentSchema, GenericIdSchema, MacListSchema

from . import BaseSchema


class SecuritySchema(BaseSchema):
    id: int
    name: str
    wireless_security_type: int
    radius: str | None
    eap: bool
    mac_acl_type: int
    mac_acls: list[MacListSchema]
    networks: list[GenericIdentSchema]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 2,
                "name": "Default",
                "wireless_security_type": 4,
                "radius": "192.168.1.1",
                "eap": False,
                "mac_acl_type": 1,
                "mac_acls": [
                    {
                        "id": 2,
                        "name": "ACL 1",
                        "macs": ["01:01:01:01:01:01", "01:01:01:01:01:02"],
                    }
                ],
                "networks": [
                    {"id": 2, "name": "Guests"},
                    {"id": 3, "name": "Employees"},
                ],
            }
        },
    )


class PutSecuritySchema(BaseSchema):
    name: Optional[str] = None
    wireless_security_type: Optional[int] = None
    radius: Optional[str] = None
    eap: Optional[bool] = None
    mac_acl_type: Optional[int] = None
    mac_acls: Optional[list[GenericIdSchema]] = None
    networks: Optional[list[GenericIdSchema]] = None
