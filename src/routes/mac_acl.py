from fastapi import APIRouter, Depends, HTTPException, Query

import services.mac_acl as MacAclService
from config import DBSessionDep
from schemas.mac_acl import MacAclSchema
from services.auth import AuthJWTTokenValidatorDep

router = APIRouter(
    dependencies=[AuthJWTTokenValidatorDep], responses={401: {}}
)


@router.get("/{id}", status_code=200, response_model=MacAclSchema)
async def get_mac_acl_config_by_id(id, db_session: DBSessionDep):
    """Returns JSON containg current configuration of the MAC ACL with given database id."""
    try:
        id = int(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID")
    if id < 0:
        raise HTTPException(status_code=400, detail="Invalid ID")
    mac_acl = await MacAclService.get_mac_acl(db_session, id)
    if mac_acl is None:
        raise HTTPException(status_code=400, detail="Invalid ID")
    return mac_acl
