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

    if update_data["name"] is not None:
        wireless_with_same_name = (
            await WirelessService.get_wireless_by_exact_name(
                db_session, update_data["name"]
            )
        )
        if (
            wireless_with_same_name
            and wireless_with_same_name.id != wireless.id
        ):
            await db_session.rollback()
            raise HTTPException(status_code=400, detail="Invalid name")
        wireless.name = update_data["name"]

    if update_data["vht"] is not None:
        wireless.vht = update_data["vht"]

    if update_data["acs"] is not None:
        wireless.acs = update_data["acs"]

    if update_data["beacon_interval"] is not None:
        if update_data["beacon_interval"] < 0:
            await db_session.rollback()
            raise HTTPException(
                status_code=400, detail="Invalid beacon interval"
            )
        wireless.beacon_interval = update_data["beacon_interval"]

    if update_data["rts_cts_threshold"] is not None:
        if (
            type(update_data["rts_cts_threshold"]) is not int
            or update_data["rts_cts_threshold"] > 65535
            or update_data["rts_cts_threshold"] < 1
        ):
            await db_session.rollback()
            raise HTTPException(
                status_code=400, detail="Invalid RTS/CTS Threshold"
            )
        wireless.rts_cts_threshold = update_data["rts_cts_threshold"]

    await HandlerService.update_item_list(
        wireless.networks,
        update_data["networks"],
        NetworkService.get_network,
        "Invalid network",
        db_session,
    )

    await db_session.commit()
    return


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


@router.delete("/{id}", status_code=200)
async def delete_wireless(id, db_session: DBSessionDep):
    """Deletes Wireless profile with given database id."""
    try:
        id = int(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID")
    if id < 0:
        raise HTTPException(status_code=400, detail="Invalid ID")
    wireless = await WirelessService.get_wireless(db_session, id)
    if wireless is None:
        raise HTTPException(status_code=400, detail="Invalid ID")
    await db_session.delete(wireless)
    await db_session.commit()
    return
