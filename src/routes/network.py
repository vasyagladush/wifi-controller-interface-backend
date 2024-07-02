from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, Query

import services.access_point as AccessPointService
import services.network as NetworkService
import services.security as SecurityService
import services.update_object as HandlerService
import services.wireless as WirelessService
from config import DBSessionDep
from schemas.network import (
    NetworkGigaSchema,
    NetworkSimpleSchema,
    PutNetworkSchema,
)
from services.auth import AuthJWTTokenValidatorDep

router = APIRouter(
    dependencies=[AuthJWTTokenValidatorDep], responses={401: {}}
)


@router.put("/{id}", status_code=200)
async def change_network_config(
    id, config: PutNetworkSchema, db_session: DBSessionDep
):
    """Endpoint for changing Network's configuration. The request must be accompanied with a JSON (formatted like the result of the GET request to this endpoint) that contains only the values to be changed.

    **WARNING**: Parameter `id` **CANNOT** be changed."""

    network = await NetworkService.get_network(db_session, id)
    if network is None:
        raise HTTPException(status_code=400, detail="Invalid ID")
    update_data = dict(config)

    if update_data["name"] is not None:
        if (
            await NetworkService.get_network_by_exact_name(
                db_session, update_data["name"]
            )
            is not None
        ):
            await db_session.rollback()
            raise HTTPException(status_code=400, detail="Invalid name")
        network.name = update_data["name"]

    if update_data["ssid"] is not None:
        if update_data["ssid"] == "":
            network.ssid = sqlalchemy.sql.null()  # type: ignore
        else:
            network.ssid = update_data["ssid"]

    if update_data["country_code"] is not None:
        if len(update_data["country_code"]) != 2:
            await db_session.rollback()
            raise HTTPException(status_code=400, detail="Invalid country code")
        network.country_code = update_data["country_code"]

    await HandlerService.update_item_list(
        network.access_point,
        update_data["access_point"],
        AccessPointService.get_AP,
        "Invalid Access Point",
        db_session,
    )
    await HandlerService.update_item_list(
        network.wireless,
        update_data["wireless"],
        WirelessService.get_wireless,
        "Invalid wireless profile",
        db_session,
    )
    await HandlerService.update_item_list(
        network.security,
        update_data["security"],
        SecurityService.get_security,
        "Invalid security profile",
        db_session,
    )


@router.get("/{id}", status_code=200, response_model=NetworkGigaSchema)
async def get_network_config_by_id(id, db_session: DBSessionDep):
    """Returns JSON containg current Giga configuration of the Network with given database id."""
    try:
        id = int(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID")
    if id < 0:
        raise HTTPException(status_code=400, detail="Invalid ID")
    network = await NetworkService.get_network(db_session, id)
    if network is None:
        raise HTTPException(status_code=400, detail="Invalid ID")
    return network


@router.get("/", status_code=200, response_model=Sequence[NetworkSimpleSchema])
async def get_network_configs(db_session: DBSessionDep):
    """Returns JSON containg current (reduced) configurations of all Networks"""
    networks = await NetworkService.get_networks(db_session)
    return networks


# @router.delete("/limited/{id}", status_code=200)
# async def delete_network_only(id, db_session: DBSessionDep):
#     """Deletes Network profile with given database id."""
#     try:
#         id = int(id)
#     except ValueError:
#         raise HTTPException(status_code=400, detail="Invalid ID")
#     if id < 0:
#         raise HTTPException(status_code=400, detail="Invalid ID")
#     network = await NetworkService.get_network(db_session, id)
#     if network is None:
#         raise HTTPException(status_code=400, detail="Invalid ID")
#     await db_session.delete(network)
#     await db_session.commit()
#     return


@router.delete("/{id}", status_code=200)
async def delete_network_and_associated_items(id, db_session: DBSessionDep):
    """Deletes Network profile with given database id, **as well as the associated Security and Wireless profiles**."""
    try:
        id = int(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID")
    if id < 0:
        raise HTTPException(status_code=400, detail="Invalid ID")
    network = await NetworkService.get_network(db_session, id)
    if network is None:
        raise HTTPException(status_code=400, detail="Invalid ID")
    for wireless in network.wireless:
        await db_session.delete(wireless)
    for security in network.security:
        await db_session.delete(security)
    await db_session.delete(network)
    await db_session.commit()
    return
