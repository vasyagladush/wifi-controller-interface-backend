import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException, Query

import services.mac_acl as MACACLService
import services.network as NetworkService
import services.security as SecurityService
import services.update_object as HandlerService
from config import DBSessionDep
from schemas.security import PutSecuritySchema, SecuritySchema
from services.auth import AuthJWTTokenValidatorDep

router = APIRouter(
    dependencies=[AuthJWTTokenValidatorDep], responses={401: {}}
)


@router.put("/{id}", status_code=200)
async def change_security_config(
    id, config: PutSecuritySchema, db_session: DBSessionDep
):
    """Endpoint for changing Security profile's configuration. The request must be accompanied with a JSON (formatted like the result of the GET request to this endpoint) that contains only the values to be changed.

    **WARNING**: Parameter `id` **CANNOT** be changed."""

    security = await SecurityService.get_security(db_session, id)
    if security is None:
        raise HTTPException(status_code=400, detail="Invalid ID")
    update_data = dict(config)

    if update_data["name"] is not None:
        if (
            await SecurityService.get_security_by_exact_name(
                db_session, update_data["name"]
            )
            is not None
        ):
            await db_session.rollback()
            raise HTTPException(status_code=400, detail="Invalid name")
        security.name = update_data["name"]

    if update_data["wireless_security_type"] is not None:
        if update_data["wireless_security_type"] not in {
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
        }:
            await db_session.rollback()
            raise HTTPException(
                status_code=400, detail="Invalid wireless security type"
            )
        security.wireless_security_type = update_data["wireless_security_type"]

    if update_data["radius"] is not None:
        if update_data["radius"] == "":
            security.radius = sqlalchemy.sql.null()  # type: ignore
        else:
            security.radius = update_data["radius"]

    if update_data["eap"] is not None:
        security.eap = update_data["eap"]

    if update_data["mac_acl_type"] is not None:
        if update_data["mac_acl_type"] not in {0, 1, 2}:
            await db_session.rollback()
            raise HTTPException(
                status_code=400, detail="Invalid wireless security type"
            )
        security.mac_acl_type = update_data["mac_acl_type"]

    await HandlerService.update_item_list(
        security.networks,
        update_data["networks"],
        NetworkService.get_network,
        "Invalid network",
        db_session,
    )

    await HandlerService.update_item_list(
        security.mac_acls,
        update_data["mac_acls"],
        MACACLService.get_mac_acl,
        "Invalid MAC ACL",
        db_session,
    )

    await db_session.commit()
    return


@router.get("/{id}", status_code=200, response_model=SecuritySchema)
async def get_security_config_by_id(id, db_session: DBSessionDep):
    """Returns JSON containg current configuration of the Security with given database id."""
    try:
        id = int(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID")
    if id < 0:
        raise HTTPException(status_code=400, detail="Invalid ID")
    security = await SecurityService.get_security(db_session, id)
    if security is None:
        raise HTTPException(status_code=400, detail="Invalid ID")
    return security
