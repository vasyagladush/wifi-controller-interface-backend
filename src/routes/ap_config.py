from fastapi import APIRouter, HTTPException

from config import DBSessionDep
from models import AP
from services.AP import get_AP

router = APIRouter()

# TODO: Implement post logic


@router.get(
    "/{id}",
    status_code=200,
)
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
    return await get_config(ap, db_session)


# TODO: Implement get by name


async def get_config(ap: AP, db_session: DBSessionDep):

    # TODO: Figure out how to get data from DB
    # TODO: Add handling of networks
    return f"OK, id: {ap.device_id}"
