from typing import Sequence

from fastapi import APIRouter, HTTPException, Query

import services.access_point as AccessPointService
from config import DBSessionDep
from schemas.access_point import APSchema
from services.auth import AuthJWTTokenValidatorDep

router = APIRouter(
    dependencies=[AuthJWTTokenValidatorDep], responses={401: {}}
)


# TODO: Implement PUT logic, only for id
@router.put("/{id}", status_code=204)  # TODO: Response model? Input model?
async def change_ap_config(id, db_session: DBSessionDep):
    """Endpoint for changing Access Point's configuration. The request must be accompanied with a JSON (formatted like the result of the GET request to this endpoint) that contains only the values to be changed.

    **WARNING**: Parameters [`id`, `deviceId`, `ip`] **CANNOT** be changed."""
    raise HTTPException(
        status_code=501, detail="Endpoint will be implemented very soon"
    )
    return "Not yet"


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


@router.get("/", status_code=200, response_model=Sequence[APSchema])
async def get_ap_configs_by_name(
    db_session: DBSessionDep, name: str = Query(None, min_length=3)
):
    """Returns a JSON list of all Access Points which have the given string as part of their name.
    Returned list can be an empty list."""
    if name is None:
        return await AccessPointService.get_APs(db_session)
    return await AccessPointService.get_APs_by_name(db_session, name)
