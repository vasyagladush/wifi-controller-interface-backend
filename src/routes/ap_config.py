from fastapi import APIRouter, HTTPException

from config import DBSessionDep
from models import AP
from schemas.AP import APSchema
from services.AP import get_AP, get_AP_by_name

router = APIRouter()

# TODO: Implement post logic


@router.get("/{id}", status_code=200, response_model=APSchema)
async def get_config_id(id, db_session: DBSessionDep):
    try:
        id = int(id)
        if id < 0 or id > 255:
            raise HTTPException(status_code=400, detail="Invalid Device ID")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Device ID")

    ap = await get_AP(db_session, id)
    if ap is None:
        raise HTTPException(status_code=400, detail="Invalid Device ID")
    return ap


# TODO: Implement router for config?name={name}
async def get_config_name(name, db_session: DBSessionDep):
    ap = await get_AP_by_name(db_session, name)
    if ap is None:
        raise HTTPException(status_code=400, detail="Invalid Device Name")
    return ap
