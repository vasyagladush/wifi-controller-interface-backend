from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, Query

import services.access_point as AccessPointService
import services.network as NetworkService
import services.security as SecurityService
import services.update_object as HandlerService
import services.wireless as WirelessService
from config import DBSessionDep
from schemas.network import NetworkListSchema, PutNetworkSchema
from services.auth import AuthJWTTokenValidatorDep

router = APIRouter(
    dependencies=[AuthJWTTokenValidatorDep], responses={401: {}}
)

# TODO: Finish PUT


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

    # if update_data["access_points"] is not None:
    #     network.access_points = []
    #     for ap in update_data["access_points"]:
    #         ap_obj = await AccessPointService.get_AP(db_session, ap.id)
    #         if ap_obj is None:
    #             await db_session.rollback()
    #             raise HTTPException(status_code=400, detail="Invalid Access Point")
    #         network.access_points.append(ap_obj)

    # if update_data["wireless"] is not None:
    #     network.wireless = []
    #     for wireless in update_data["wireless"]:
    #         wireless_obj = await WirelessService.get_wireless(db_session, wireless.id)
    #         if wireless_obj is None:
    #             await db_session.rollback()
    #             raise HTTPException(status_code=400, detail="Invalid wireless")
    #         network.access_points.append(wireless_obj)


# @router.get("/{id}", status_code=200, response_model=NetworkSchema)
# async def get_network_config_by_id(id, db_session: DBSessionDep):
#    """Returns JSON containg current configuration of the Network with given database id."""
#    try:
#        id = int(id)
#    except ValueError:
#        raise HTTPException(status_code=400, detail="Invalid ID")
#    if id < 0:
#        raise HTTPException(status_code=400, detail="Invalid ID")
#    network = await NetworkService.get_network(db_session, id)
#    if network is None:
#        raise HTTPException(status_code=400, detail="Invalid ID")
#    return network


# @router.get("/", status_code=200, response_model=NetworkListSchema)
# async def get_network_configs(db_session: DBSessionDep):
#    """Returns JSON containg current (reduced) configurations of all Networks"""
#    networks = await NetworkService.get_networks(db_session)
#    response = NetworkListSchema(networks=networks) # type:ignore
#    return response
