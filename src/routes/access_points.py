from sqlite3 import IntegrityError
from typing import Annotated, Optional, Sequence

from fastapi import APIRouter, Depends, HTTPException, Query

import services.access_point as AccessPointService
import services.network as NetworkService
from config import DBSessionDep
from routes import PaginationParamsDep
from schemas.access_point import APSchema, GetAPsSchema, PutAPSchema
from schemas.pagination import PaginationParamsSchema
from services.auth import AuthJWTTokenValidatorDep

router = APIRouter(
    dependencies=[AuthJWTTokenValidatorDep], responses={401: {}}
)


@router.put("/{id}", status_code=204)
async def change_ap_config(
    id, config: PutAPSchema, db_session: DBSessionDep
) -> None:
    """Endpoint for changing Access Point's configuration. The request must be accompanied with a JSON (formatted like the result of the GET request to this endpoint) that contains only the values to be changed.

    **WARNING**: Parameters [`id`, `deviceId`, `ip`] **CANNOT** be changed."""
    ap = await AccessPointService.get_AP(db_session, id)
    if ap is None:
        raise HTTPException(status_code=400, detail="Invalid ID")
    update_data = dict(config)
    if update_data["networks"] is not None:
        ap.networks = []
        for net in update_data["networks"]:
            net_obj = await NetworkService.get_network(db_session, net.id)
            if net_obj is None:
                await db_session.rollback()
                raise HTTPException(status_code=400, detail="Invalid network")
            ap.networks.append(net_obj)
    if update_data["name"] is not None:
        ap_with_same_name = await AccessPointService.get_AP_by_exact_name(
            db_session, update_data["name"]
        )
        if ap_with_same_name and ap_with_same_name.id != ap.id:
            await db_session.rollback()
            raise HTTPException(status_code=400, detail="Invalid name")
        ap.name = update_data["name"]
    await db_session.commit()
    return


@router.get("/{id}", status_code=200, response_model=APSchema)
async def get_ap_config_by_id(id, db_session: DBSessionDep):
    """Returns JSON containg current configuration of the Access Point with given database id."""
    try:
        id = int(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID")
    if id < 0:
        raise HTTPException(status_code=400, detail="Invalid ID")
    ap = await AccessPointService.get_AP(db_session, id)
    if ap is None:
        raise HTTPException(status_code=400, detail="Invalid ID")
    return ap


@router.get("/", status_code=200, response_model=GetAPsSchema)
async def get_ap_configs(
    db_session: DBSessionDep,
    pagination: Annotated[
        PaginationParamsSchema, Depends(PaginationParamsDep)
    ],
    name: Optional[str] = Query(None, min_length=3),
):
    """Returns a paginated JSON result of all Access Points which have the given string as part of their name.
    Returned list can be an empty list."""
    return await AccessPointService.get_paginated_APs(
        db_session, pagination.page, pagination.limit, name
    )
