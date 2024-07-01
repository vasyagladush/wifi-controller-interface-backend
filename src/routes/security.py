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

# TODO: Finish PUT


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
