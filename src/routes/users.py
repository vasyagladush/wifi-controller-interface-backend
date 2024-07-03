from typing import Annotated, Sequence

from fastapi import APIRouter, Body, HTTPException

import services.user as UserService
from config import DBSessionDep, hash_helper
from models.user import User
from schemas.user import (
    UserLoginCredentialsSchema,
    UserLoginResponseSchema,
    UserModSchema,
    UserPlusSchema,
    UserSchema,
    UserSignUpSchema,
)
from services.auth import (
    AdminAccessCheckDep,
    AuthJWTTokenPayload,
    AuthJWTTokenValidatorDep,
    construct_auth_jwt,
)

router = APIRouter()


@router.post("/login", status_code=200, response_model=UserLoginResponseSchema)
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


@router.post(
    "/",
    status_code=201,
    response_model=UserSchema,
    dependencies=[AdminAccessCheckDep],
)
async def create_user(
    db_session: DBSessionDep,
    body: UserSignUpSchema = Body(...),
):
    """Creates User with specified details"""
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


@router.get(
    "/current",
    status_code=200,
    response_model=UserPlusSchema,
    responses={401: {}},
)
async def get_current_user(
    auth_token_body: Annotated[AuthJWTTokenPayload, AuthJWTTokenValidatorDep],
    db_session: DBSessionDep,
):
    user: User | None = await UserService.get_user(
        db_session, auth_token_body["user_id"]
    )
    if not user:
        raise HTTPException(status_code=404, detail="No user found")
    return user


@router.get(
    "/all",
    status_code=200,
    response_model=Sequence[UserPlusSchema],
    responses={401: {}},
    dependencies=[AdminAccessCheckDep],
)
async def get_all_users(
    db_session: DBSessionDep,
):
    users = await UserService.get_users(db_session)
    return users


@router.delete("/{id}", status_code=204, dependencies=[AdminAccessCheckDep])
async def delete_user(
    id,
    db_session: DBSessionDep,
):
    """Deletes User with database id"""
    user_to_delete: User | None = await UserService.get_user(db_session, id)

    if user_to_delete is None:
        raise HTTPException(
            status_code=400,
            detail="User does not exist",
        )

    await db_session.delete(user_to_delete)
    await db_session.commit()
    return


@router.put("/{id}", status_code=204)
async def modify_user(
    id,
    db_session: DBSessionDep,
    auth_token_body: Annotated[AuthJWTTokenPayload, AdminAccessCheckDep],
    config: UserModSchema,
):
    """Allows modification of user. Password can be changed only by the user."""
    user: User | None = await UserService.get_user(db_session, id)

    if user is None:
        raise HTTPException(
            status_code=400,
            detail="User does not exist",
        )
    update_data = dict(config)

    if update_data["password"] is not None:
        if auth_token_body["user_id"] != id:
            await db_session.rollback()
            raise HTTPException(
                status_code=400,
                detail="Cannot change password of another user",
            )
        if len(update_data["password"]) < 8:
            await db_session.rollback()
            raise HTTPException(status_code=400, detail="Password too short")
        user.password = update_data["password"]

    if update_data["username"] is not None:
        check = await UserService.get_user_by_username(
            db_session, update_data["username"]
        )
        if check is not None and check.id != id:
            await db_session.rollback()
            raise HTTPException(
                status_code=400,
                detail="User with this username already exists",
            )
        user.name = update_data["username"]

    if update_data["first_name"] is not None:
        user.first_name = update_data["first_name"]

    if update_data["last_name"] is not None:
        user.last_name = update_data["last_name"]

    if update_data["is_admin"] is not None:
        user.is_admin = update_data["is_admin"]

    await db_session.commit()
    return
