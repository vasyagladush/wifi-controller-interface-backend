from fastapi import APIRouter, Body, HTTPException

import services.user as UserService
from config import DBSessionDep, hash_helper
from models.user import User
from schemas.user import (
    UserLoginCredentialsSchema,
    UserSchema,
    UserSignUpSchema,
)
from services.auth import AuthJWTTokenValidatorDep, construct_auth_jwt

router = APIRouter(tags=["users"])


@router.post("/login")
async def login(
    db_session: DBSessionDep,
    user_credentials: UserLoginCredentialsSchema = Body(...),
):
    existing_user: User | None = await UserService.get_user_by_username(
        db_session, user_credentials.username
    )

    if existing_user:
        password_valid: bool = hash_helper.verify(
            user_credentials.password, existing_user.password_hash
        )

        if password_valid:
            return construct_auth_jwt(existing_user)

        raise HTTPException(
            status_code=401, detail="Incorrect username or password"
        )

    raise HTTPException(
        status_code=401, detail="Incorrect username or password"
    )


@router.post("/", response_model=UserSchema)
async def signup(db_session: DBSessionDep, body: UserSignUpSchema = Body(...)):
    existing_user: User | None = await UserService.get_user_by_username(
        db_session, body.username
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User with the provided username already exists",
        )

    new_user: User = await UserService.create_user(db_session, body)
    return new_user


@router.get("/", response_model=UserSchema)
async def get(
    auth_token_body: AuthJWTTokenValidatorDep,
    db_session: DBSessionDep,
):
    user: User | None = await UserService.get_user(
        db_session, auth_token_body["user_id"]
    )

    if not user:
        raise HTTPException(status_code=404, detail="No user found")

    return user
