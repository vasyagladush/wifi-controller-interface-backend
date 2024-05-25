from pydantic import BaseModel
from fastapi.security import HTTPBasicCredentials


class UserLoginCredentialsSchema(HTTPBasicCredentials):
    class Config:
        json_schema_extra = {
            "example": {"username": "user.name", "password": "password"}
        }


class UserSignUpSchema(HTTPBasicCredentials):
    firstname: str
    lastname: str

    class Config:
        json_schema_extra = {
            "example": {
                "firstname": "Name",
                "lastname": "Surname",
                "username": "user.name",
                "password": "password"
            }
        }


class UserSchema(BaseModel):
    firstname: str
    lastname: str
    username: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "firstname": "Name",
                "lastname": "Surname",
                "username": "user.name",
            }
        }
