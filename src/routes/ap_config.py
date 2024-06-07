from fastapi import APIRouter, HTTPException

router = APIRouter()

# TODO: Implement post logic


@router.get(
    "/{id}",
    status_code=200,
)
async def get_config(id):
    try:
        id = int(id)
        if id < 0 or id > 255:
            raise HTTPException(status_code=404, detail="Invalid Device ID")
    except ValueError:
        raise HTTPException(status_code=404, detail="Invalid Device ID")

    # TODO: Figure out how to get data from DB
    # TODO: Add handling of networks

    return f"OK, id: {id}"


# TODO: Implement get by name
