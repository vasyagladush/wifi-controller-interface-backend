from fastapi import APIRouter, Body, HTTPException

from config import app_config
from schemas.cmd import CmdSchema
from services.auth import AdminAccessCheckDep, AuthJWTTokenValidatorDep
from services.console import send_command

router = APIRouter(dependencies=[AdminAccessCheckDep], responses={401: {}})


@router.post("/", status_code=200)
async def cmd_input(command: CmdSchema = Body(...)):
    output = await send_command(
        app_config.CMD_PIPE_PATH,
        app_config.OUTPUT_PIPE_PATH,
        command.cmd,
        command.args,
    )
    return {"output": output}
