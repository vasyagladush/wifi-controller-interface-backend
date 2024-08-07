import re

from fastapi import APIRouter, Depends, HTTPException, Query

import services.mac_acl as MacAclService
import services.security as SecurityService
import services.update_object as HandlerService
from config import DBSessionDep
from schemas.mac_acl import MacAclSchema, PutMacAclSchema
from services.auth import AdminAccessCheckDep

router = APIRouter(dependencies=[AdminAccessCheckDep], responses={401: {}})


async def mac_invalid(mac: str) -> bool:
    mac_pattern = re.compile(r"^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$")
    return not bool(mac_pattern.match(mac))


@router.post("/", status_code=200)
async def add_mac_acl(config: PutMacAclSchema, db_session: DBSessionDep):
    """Endpoint for creating MAC ACLs. The request must be accompanied with a JSON (formatted like the result of the GET request to this endpoint). Parameter `security` is optional."""
    update_data = dict(config)
    for mac in update_data["macs"]:
        if await mac_invalid(mac):
            await db_session.rollback()
            raise HTTPException(status_code=400, detail="Invalid MAC address")
    try:
        await MacAclService.create_mac_acl(
            db_session,
            update_data["name"],
            update_data["macs"],
            update_data["security"],
        )
    except ValueError:
        print("A")
        raise HTTPException(status_code=400, detail="Duplicate MAC ACL name")
    except IndexError:
        raise HTTPException(
            status_code=400, detail="Invalid Security profile ID"
        )


@router.put("/{id}", status_code=200)
async def change_mac_acl_config(
    id, config: PutMacAclSchema, db_session: DBSessionDep
):
    """Endpoint for changing MAC ACL's configuration. The request must be accompanied with a JSON (formatted like the result of the GET request to this endpoint) that contains only the values to be changed.

    **WARNING**: Parameter `id` **CANNOT** be changed."""

    mac_acl = await MacAclService.get_mac_acl(db_session, id)
    if mac_acl is None:
        raise HTTPException(status_code=400, detail="Invalid ID")
    update_data = dict(config)

    if update_data["name"] is not None:
        mac_acl_with_same_name = await MacAclService.get_mac_acl_by_exact_name(
            db_session, update_data["name"]
        )
        if mac_acl_with_same_name and mac_acl_with_same_name.id != mac_acl.id:
            await db_session.rollback()
            raise HTTPException(status_code=400, detail="Invalid name")
        mac_acl.name = update_data["name"]

    if update_data["macs"] is not None:
        for mac in update_data["macs"]:
            if await mac_invalid(mac):
                await db_session.rollback()
                raise HTTPException(
                    status_code=400, detail="Invalid MAC address"
                )
        mac_acl.macs = update_data["macs"]

    await HandlerService.update_item_list(
        mac_acl.security,
        update_data["security"],
        SecurityService.get_security,
        "Invalid security profile",
        db_session,
    )

    await db_session.commit()
    return


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


@router.delete("/{id}", status_code=200)
async def delete_mac_acl(id, db_session: DBSessionDep):
    """Deletes MAC ACL with given database id."""
    try:
        id = int(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID")
    if id < 0:
        raise HTTPException(status_code=400, detail="Invalid ID")
    mac_acl = await MacAclService.get_mac_acl(db_session, id)
    if mac_acl is None:
        raise HTTPException(status_code=400, detail="Invalid ID")
    await db_session.delete(mac_acl)
    await db_session.commit()
    return
