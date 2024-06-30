from fastapi import APIRouter, Depends, HTTPException, Query

import services.network as NetworkService
from config import DBSessionDep
from schemas.network import NetworkSchema
from services.auth import AuthJWTTokenValidatorDep

router = APIRouter(
    dependencies=[AuthJWTTokenValidatorDep], responses={401: {}}
)


@router.get("/{id}", status_code=200, response_model=NetworkSchema)
async def get_network_config_by_id(id, db_session: DBSessionDep):
    """Returns JSON containg current configuration of the Network with given database id."""
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
