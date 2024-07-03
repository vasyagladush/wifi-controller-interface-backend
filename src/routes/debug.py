from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

import services.mac_acl as MacAclService
import services.user as UserService
from config import DBSessionDep
from models.mac_acl import MACACL
from models.user import User
from schemas import BaseSchema
from schemas.user import UserSchema, UserSignUpSchema

router = APIRouter(responses={401: {}})


class MacListSchema(BaseSchema):
    macs: list[str]


async def add_macacl(session: AsyncSession, name: str, macs: list[str]):
    # Define the insert query
    stmt = insert(MACACL).values(name=name, macs=macs)
    await session.execute(stmt)
    await session.commit()


@router.post("/mac-acls/{id}", status_code=200)
async def set_mac_list(id, config: MacListSchema, db_session: DBSessionDep):

    update_data = dict(config)
    await add_macacl(db_session, "A", update_data["macs"])

    return


@router.post("/signup", status_code=201, response_model=UserSchema)
async def signup(
    db_session: DBSessionDep,
    body: UserSignUpSchema = Body(...),
):
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
