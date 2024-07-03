import aiofiles


async def send_command(
    cmd_pipe: str, output_pipe: str, cmd: str, args: list[str]
) -> str:
    for arg in args:
        cmd += f" {arg}"
    async with aiofiles.open(cmd_pipe, "w") as pipe_in:
        await pipe_in.write(cmd)
    async with aiofiles.open(output_pipe, "r") as pipe_out:
        output: str = await pipe_out.read()
    return output


# def send_command(
#    cmd_pipe: str, output_pipe: str, cmd: str, args: list[str]
# ) -> str:
#    for arg in args:
#        cmd += f" {arg}"
#    with open(cmd_pipe, "w") as pipe_in:
#        pipe_in.write(cmd)
#    with open(output_pipe, "r") as pipe_out:
#        output: str = pipe_out.readline()
#    return output
