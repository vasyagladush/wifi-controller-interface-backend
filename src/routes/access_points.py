from typing import Annotated, Optional, Sequence

from fastapi import APIRouter, Depends, HTTPException, Query

import services.access_point as AccessPointService
from config import DBSessionDep
from routes import PaginationParamsDep
from schemas.access_point import APSchema, GetAPsSchema, PutAPSchema
from schemas.pagination import PaginationParamsSchema
from services.auth import AuthJWTTokenValidatorDep

router = APIRouter(
    dependencies=[AuthJWTTokenValidatorDep], responses={401: {}}
)


# TODO: Add handling of networks changing
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
    print(update_data)
    for entry in update_data.items():
        if entry[1] != None and entry[0] != "networks":
            setattr(ap, entry[0], entry[1])
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
