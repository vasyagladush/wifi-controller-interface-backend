from typing import List, Optional, Sequence

from pydantic import ConfigDict, Field

from schemas.joint import APIdSchema, GenericIdentSchema, GenericIdSchema

from . import BaseSchema


class NetworkSimpleSchema(BaseSchema):
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


class PutNetworkSchema(BaseSchema):
    name: Optional[str] = None
    ssid: Optional[str] = None
    country_code: Optional[str] = None
    access_points: Optional[list[GenericIdSchema]] = None
    wireless: Optional[list[GenericIdSchema]] = None
    security: Optional[list[GenericIdSchema]] = None


class NG_AP_Schema(BaseSchema):
    id: int
    device_id: int
    name: str
    ip: str


class NG_Wireless_Schema(BaseSchema):
    id: int
    name: str
    vht: bool
    acs: bool
    beacon_interval: int
    rts_cts_threshold: int


class NG_MAC_ACL_Schema(BaseSchema):
    id: int
    name: str
    macs: list[str]


class NG_Security_Schema(BaseSchema):
    id: int
    name: str
    wireless_security_type: int
    radius: str | None
    eap: bool
    mac_acl_type: int
    mac_acls: list[NG_MAC_ACL_Schema]


class NetworkGigaSchema(BaseSchema):
    id: int
    name: str
    ssid: str
    country_code: str
    password: str | None
    access_points: list[NG_AP_Schema]
    wireless: list[NG_Wireless_Schema]
    security: list[NG_Security_Schema]
