from pydantic import ConfigDict

from . import BaseSchema


class CmdSchema(BaseSchema):
    cmd: str
    args: list[str]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"cmd": "show", "args": ["variables"]}},
    )
