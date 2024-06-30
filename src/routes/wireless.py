from fastapi import APIRouter, Depends, HTTPException, Query

import services.wireless as WirelessService
from config import DBSessionDep
from schemas.wireless import WirelessSchema
from services.auth import AuthJWTTokenValidatorDep

router = APIRouter(
    dependencies=[AuthJWTTokenValidatorDep], responses={401: {}}
)


@router.get("/{id}", status_code=200, response_model=WirelessSchema)
async def get_wireless_config_by_id(id, db_session: DBSessionDep):
    """Returns JSON containg current configuration of the Wireless with given database id."""
    try:
        id = int(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID")
    if id < 0:
        raise HTTPException(status_code=400, detail="Invalid ID")
    wireless = await WirelessService.get_wireless(db_session, id)
    if wireless is None:
        raise HTTPException(status_code=400, detail="Invalid ID")
    return wireless
