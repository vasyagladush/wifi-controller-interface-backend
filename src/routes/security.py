from fastapi import APIRouter, Depends, HTTPException, Query

import services.security as SecurityService
from config import DBSessionDep
from schemas.security import SecuritySchema
from services.auth import AuthJWTTokenValidatorDep

router = APIRouter(
    dependencies=[AuthJWTTokenValidatorDep], responses={401: {}}
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
