from typing import Optional

from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, ConfigDict

from schemas import BaseSchema


class UserLoginCredentialsSchema(BaseSchema, HTTPBasicCredentials):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"username": "user.name", "password": "password"}
        }
    )


class UserLoginResponseSchema(BaseSchema):
    access_token: str


class UserSignUpSchema(BaseSchema, HTTPBasicCredentials):
    first_name: str
    last_name: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "firstName": "Name",
                "lastName": "Surname",
                "username": "user.name",
                "password": "password",
            }
        }
    )


class UserSchema(BaseSchema):
    first_name: str
    last_name: str
    username: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "firstName": "Name",
                "lastName": "Surname",
                "username": "user.name",
            }
        },
    )


class UserModSchema(BaseSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class UserPlusSchema(BaseSchema):
    id: int
    first_name: str
    last_name: str
    username: str
