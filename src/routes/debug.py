from fastapi import APIRouter, HTTPException
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

import services.mac_acl as MacAclService
from config import DBSessionDep
from models.mac_acl import MACACL
from schemas import BaseSchema

router = APIRouter(responses={401: {}})


class MacListSchema(BaseSchema):
    macs: list[str]


async def add_macacl(session: AsyncSession, name: str, macs: list[str]):
    # Define the insert query
    stmt = insert(MACACL).values(name=name, macs=macs)
    await session.execute(stmt)
    await session.commit()


@router.post("/{id}", status_code=200)
async def set_mac_list(id, config: MacListSchema, db_session: DBSessionDep):

    update_data = dict(config)
    await add_macacl(db_session, "A", update_data["macs"])

    return
