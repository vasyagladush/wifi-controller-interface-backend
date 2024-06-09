import imp
from subprocess import PIPE, Popen


def connect_to_wlc_cli(wlc_cli_path: str) -> Popen:
    try:
        return Popen(
            f"python3 {wlc_cli_path}", stdin=PIPE, stdout=PIPE, stderr=PIPE
        )
    except OSError:
        raise SystemExit


def send_command(wlc_cli_process: Popen, cmd: str, args: list[str]) -> str:
    for arg in args:
        cmd += f" {arg}"
    with open(wlc_cli_process.stdin, "w") as pipe:
        pipe.writeline(cmd)
