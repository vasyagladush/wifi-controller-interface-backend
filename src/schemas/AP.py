from ap_config import ConfigSchema
from pydantic import ConfigDict

from . import BaseSchema


class APSchema(BaseSchema):
    device_id: int
    name: str
    ip: str
    config: ConfigSchema
