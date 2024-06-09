from . import BaseSchema


class NetworkNameSchema(BaseSchema):
    name: str


class APSchema(BaseSchema):
    device_id: int
    name: str
    ip: str
    networks: list[
        NetworkNameSchema
    ]  # TODO: Verify that this how this should be done
