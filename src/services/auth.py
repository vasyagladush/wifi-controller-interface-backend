import time
from typing import Annotated, Dict, TypedDict

import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config import app_config
from models.user import User


class AuthJWTTokenPayload(TypedDict):
    user_id: int
    expires_at: float


def construct_token_json_response(token: str):
    return {"access_token": token}


secret_key = app_config.JWT_SECRET_KEY


def construct_auth_jwt(user: User) -> Dict[str, str]:
    # Set the expiry time.
    payload: AuthJWTTokenPayload = {
        "user_id": user.id,
        "expires_at": time.time() + 2400,
    }
    return construct_token_json_response(
        jwt.encode(payload, secret_key, algorithm="HS256")  # type: ignore
    )


def decode_jwt(token: str) -> AuthJWTTokenPayload | None:
    decoded_token: AuthJWTTokenPayload = jwt.decode(
        token.encode(), secret_key, algorithms=["HS256"]
    )
    return (
        decoded_token if decoded_token["expires_at"] >= time.time() else None
    )


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) -> AuthJWTTokenPayload:  # type: ignore
        authorization: HTTPAuthorizationCredentials = await super(  # type: ignore
            JWTBearer, self
        ).__call__(
            request
        )

        if authorization:
            if not authorization.scheme == "Bearer":
                raise HTTPException(
                    status_code=401,
                    detail="Invalid authentication token type. Must be Bearer",
                )

            decoded_token = decode_jwt(authorization.credentials)

            if not decoded_token:
                raise HTTPException(
                    status_code=401, detail="Invalid token or expired token"
                )
            return decoded_token  # type: ignore
        else:
            raise HTTPException(
                status_code=401, detail="Invalid authorization token"
            )


AuthJWTTokenValidatorDep = Depends(JWTBearer())
