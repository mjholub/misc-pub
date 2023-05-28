#!/usr/bin/env python3

import asyncio
import aiofiles
import os
from subprocess import PIPE, STDOUT

async def get_uu_executables(path):
    proc = await asyncio.create_subprocess_shell(f'exa -l --oneline {path} | rg uutils | awk \'{{ print $1 }}\'', stdout=PIPE, stderr=STDOUT)
    stdout, stderr = await proc.communicate()
    return stdout.decode().splitlines()

async def check_alias_exists(j):
    async with aiofiles.open(os.path.expanduser("~/.config/fish/config.fish"), mode='r') as f:
        content = await f.read()
        if f"alias {j}=" in content:
            return True
    return False

async def write_alias(j, i):
    async with aiofiles.open(os.path.expanduser("~/.config/fish/config.fish"), mode='a') as f:
        await f.write(f'alias {j}={i}\n')

async def main():
    uu_executables = []
    for dir in os.environ['PATH'].split(os.pathsep):
        if os.path.exists(dir):
            uu_executables += await get_uu_executables(dir)

    tasks = []
    for i in uu_executables:
        coreutils_executable = await asyncio.create_subprocess_shell(f'echo {i} | awk -F \'-\' \'{{ print $2 }}\'', stdout=PIPE, stderr=STDOUT)
        stdout, stderr = await coreutils_executable.communicate()
        coreutils_executables = stdout.decode().splitlines()

        for j in coreutils_executables:
            if j != "[" or j != "uutils-test" and not await check_alias_exists(j):
                tasks.append(write_alias(j, i))

    if tasks:
        await asyncio.gather(*tasks)
    else:
        print("No aliases to add")

if __name__ == '__main__':
    asyncio.run(main())
