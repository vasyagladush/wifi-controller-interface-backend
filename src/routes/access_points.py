from fastapi import APIRouter, HTTPException, Query

import services.access_point as AccessPointService
from config import DBSessionDep
from schemas.access_point import APSchema
from services.auth import AuthJWTTokenValidatorDep

router = APIRouter(
    dependencies=[AuthJWTTokenValidatorDep], responses={401: {}}
)

# TODO: Implement PUT logic, only for id


@router.get("/{id}", status_code=200, response_model=APSchema)
async def get_config_id(id, db_session: DBSessionDep):
    try:
        id = int(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID")
    if id < 0:
        raise HTTPException(status_code=400, detail="Invalid ID")
    ap = await AccessPointService.get_AP(db_session, id)
    if ap is None:
        raise HTTPException(status_code=400, detail="Invalid ID")
    return ap


@router.get("/", status_code=200, response_model=APSchema)
async def get_config_name(
    db_session: DBSessionDep, name: str = Query(None, min_length=3)
):
    if name is None:
        return await AccessPointService.get_APs(db_session)
    return await AccessPointService.get_APs_by_name(db_session, name)
