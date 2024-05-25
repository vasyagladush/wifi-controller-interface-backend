from typing import Annotated
from fastapi import Body, APIRouter, Depends, HTTPException, Header
import jwt

from services.auth.jwt_bearer import JWTBearer
from services.auth.jwt_handler import sign_jwt
from config import app_config
import services.user as UserService
from models.user import User
from schemas.user import UserSchema, UserLoginCredentialsSchema, UserSignUpSchema
from config import DBSessionDep, hash_helper

router = APIRouter(tags=["users"])

token_listener = JWTBearer()


@router.post("/login")
async def login(
    db_session: DBSessionDep, user_credentials: UserLoginCredentialsSchema = Body(...)
):
    existing_user: User | None = await UserService.get_user_by_username(
        db_session, user_credentials.username
    )

    if existing_user:
        password_valid: bool = hash_helper.verify(
            user_credentials.password, existing_user.password_hash
        )

        if password_valid:
            return sign_jwt(user_credentials.username)

        raise HTTPException(
            status_code=401, detail="Incorrect username or password")

    raise HTTPException(status_code=401, detail="Incorrect username or password")


@router.post("/", response_model=UserSchema)
async def signup(db_session: DBSessionDep, body: UserSignUpSchema = Body(...)):
    existing_user: User | None = await UserService.get_user_by_username(
        db_session, body.username
    )

    if existing_user:
        raise HTTPException(
            status_code=409, detail="User with the provided username already exists"
        )

    new_user: User = await UserService.create_user(db_session, body)
    return new_user


@router.get("/", dependencies=[Depends(token_listener)], response_model=UserSchema)
async def get(
    Authorization: Annotated[str, Header()],
    db_session: DBSessionDep,
):
    jwt_token: str = Authorization[6:].strip()

    username: str = jwt.decode(
        jwt_token, app_config.JWT_SECRET_KEY, algorithms=["HS256"]
    )["user_id"]

    # TODO: make it work with user id, not username
    user: User | None = await UserService.get_user_by_username(db_session, username)

    if not user:
        raise HTTPException(status_code=404, detail="No user found")

    return user
