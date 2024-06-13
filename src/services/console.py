import aiofiles


async def send_command(
    cmd_pipe: str, output_pipe: str, cmd: str, args: list[str]
) -> str:
    for arg in args:
        cmd += f" {arg}"
    with aiofiles.open(cmd_pipe, "w") as pipe_in:
        await pipe_in.writeline(cmd)
    with aiofiles.open(output_pipe, "r") as pipe_out:
        output: str = await pipe_out.readline()
    return output
