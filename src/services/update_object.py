from typing import Any, Awaitable, Callable

from fastapi import HTTPException

from config import DBSessionDep


async def update_item_list(
    field_to_update,
    update_data_item,
    db_getter: Callable[[Any, Any], Awaitable[Any]],
    fail_message: str,
    db_session: DBSessionDep,
):
    if update_data_item is not None:
        field_to_update = []
        for item in update_data_item:
            object = await db_getter(db_session, item.id)
            if object is None:
                await db_session.rollback()
                raise HTTPException(status_code=400, detail=fail_message)
            field_to_update.append(object)
