from typing import Sequence

from fastapi import APIRouter, Body, Depends, HTTPException, Query

import services.access_point as AccessPointService
import services.mac_acl as MACACLService
import services.network as NetworkService
import services.security as SecurityService
import services.update_object as HandlerService
import services.wireless as WirelessService
from config import DBSessionDep, app_config
from schemas.network import (
    NetworkGigaSchema,
    NetworkSimpleSchema,
    PutNetworkSchema,
)
from services.auth import AuthJWTTokenValidatorDep

router = APIRouter(
    dependencies=[AuthJWTTokenValidatorDep], responses={401: {}}
)


@router.post("/", status_code=204)
async def create_network_config(
    db_session: DBSessionDep, config: NetworkGigaSchema = Body(...)
):
    for w in config.wireless:
        if (
            await WirelessService.get_wireless_by_exact_name(
                db_session, w.name
            )
            is not None
        ):
            raise HTTPException(400, "Wireless with that name already exists!")
    wireless = [
        await WirelessService.create_wireless(
            db_session,
            w.name,
            w.vht,
            w.acs,
            w.beacon_interval,
            w.rts_cts_threshold,
        )
        for w in config.wireless
    ]
    for s in config.security:
        if (
            await SecurityService.get_security_by_exact_name(
                db_session, s.name
            )
            is not None
        ):
            raise HTTPException(400, "Security with that name already exists!")
        for acl in s.mac_acls:
            if (
                await MACACLService.get_mac_acl_by_exact_name(
                    db_session, acl.name
                )
                is not None
            ):
                raise HTTPException(
                    400, "MAC ACL with that name already exists!"
                )
    security = [
        await SecurityService.create_security(
            db_session,
            s.name,
            s.wireless_security_type,
            s.radius,
            s.eap,
            s.mac_acl_type,
            s.mac_acls,
        )
        for s in config.security
    ]
    aps = [await AccessPointService.get_AP_by_exact_name(db_session, ap.name) for ap in config.access_points]  # type: ignore
    network = await NetworkService.create_network(
        aps,
        db_session,
        config.name,
        config.ssid,
        config.country_code,
        password=app_config.CRYPTOGRAPHY.encrypt(config.password.encode()),
        wireless=wireless,
        security=security,
    )
    return


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
        network_with_same_name = (
            await NetworkService.get_network_by_exact_name(
                db_session, update_data["name"]
            )
        )
        if network_with_same_name and network_with_same_name.id != network.id:
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

    # await HandlerService.update_item_list(
    #     network.access_point,
    #     update_data["access_point"],
    #     AccessPointService.get_AP,
    #     "Invalid Access Point",
    #     db_session,
    # )
    # await HandlerService.update_item_list(
    #     network.wireless,
    #     update_data["wireless"],
    #     WirelessService.get_wireless,
    #     "Invalid wireless profile",
    #     db_session,
    # )
    # await HandlerService.update_item_list(
    #     network.security,
    #     update_data["security"],
    #     SecurityService.get_security,
    #     "Invalid security profile",
    #     db_session,
    # )
    await db_session.commit()


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
