from pydantic import ConfigDict

from . import BaseSchema


class ConfigSchema(BaseSchema):
    ssid: str
    country_code: str
    security_type: str
