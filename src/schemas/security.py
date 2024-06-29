from pydantic import ConfigDict

from schemas.joint import MacListSchema, NetworkIdSchema

from . import BaseSchema


class SecuritySchema(BaseSchema):
    id: int
    wireless_security_type: int  # TODO: Verify correctness of this
    radius: str
    eap: bool
    mac_acl_type: int  # TODO: Verify correctness of this
    mac_acls: list[MacListSchema]
    networks: list[NetworkIdSchema]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 2,
                "wireless_security_type": 4,  # TODO: Verify correctness of this
                "radius": "192.168.1.1",
                "eap": False,
                "mac_acl_type": 1,  # TODO: Verify correctness of this
                "mac_acls": [
                    {
                        "id": 2,
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
