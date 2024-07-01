from fastapi import APIRouter, Depends, HTTPException, Query

import services.network as NetworkService
import services.update_object as HandlerService
import services.wireless as WirelessService
from config import DBSessionDep
from schemas.wireless import PutWirelessSchema, WirelessSchema
from services.auth import AuthJWTTokenValidatorDep

router = APIRouter(
    dependencies=[AuthJWTTokenValidatorDep], responses={401: {}}
)


@router.put("/{id}", status_code=200)
async def change_wireless_config(
    id, config: PutWirelessSchema, db_session: DBSessionDep
):
    """Endpoint for changing Wireless profile's configuration. The request must be accompanied with a JSON (formatted like the result of the GET request to this endpoint) that contains only the values to be changed.

    **WARNING**: Parameter `id` **CANNOT** be changed."""

    wireless = await WirelessService.get_wireless(db_session, id)
    if wireless is None:
        raise HTTPException(status_code=400, detail="Invalid ID")
    update_data = dict(config)

    await HandlerService.update_item_list(
        wireless.networks,
        update_data["networks"],
        NetworkService.get_network,
        "Invalid network",
        db_session,
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
