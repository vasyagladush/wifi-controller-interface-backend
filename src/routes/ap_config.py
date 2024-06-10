from fastapi import APIRouter, HTTPException

from config import DBSessionDep
from models import AP
from schemas.AP import APSchema
from services.AP import get_AP, get_AP_by_name

router = APIRouter()

# TODO: Add auth to all 3 of these routes, once this is confirmed to mostly work
# TODO: Implement PUT logic, only for id


@router.get("/{id}", status_code=200, response_model=APSchema)
async def get_config_id(id, db_session: DBSessionDep):
    try:
        id = int(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID")
    if id < 0:
        raise HTTPException(status_code=400, detail="Invalid ID")
    ap = await get_AP(db_session, id)
    if ap is None:
        raise HTTPException(status_code=400, detail="Invalid ID")
    return ap


# TODO: Verify this is ok
@router.get("/", status_code=200, response_model=APSchema)
async def get_config_name(name: str, db_session: DBSessionDep):
    if name is None:
        raise HTTPException(status_code=400, detail="Invalid Device Name")
    ap = await get_AP_by_name(db_session, name)
    if ap is None:
        raise HTTPException(status_code=400, detail="Invalid Device Name")
    return ap
