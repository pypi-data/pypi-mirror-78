import datetime
import asyncio
from typing import *
import royalnet
import royalnet.commands as rc


class PingCommand(rc.Command):
    name: str = "ping"

    description: str = "Display the status of the Herald network."

    syntax: str = ""

    _targets = ["telegram", "discord", "constellation"]

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        await data.reply("📶 Ping...")

        tasks = {}

        start = datetime.datetime.now()
        for target in self._targets:
            tasks[target] = self.loop.create_task(self.serf.call_herald_event(target, "pong"))

        await asyncio.sleep(5)

        lines = ["📶 [b]Pong![/b]", ""]

        for name, task in tasks.items():
            try:
                d = task.result()
            except (asyncio.CancelledError, asyncio.InvalidStateError):
                lines.append(f"🔴 [c]{name}[/c]")
            else:
                end = datetime.datetime.fromtimestamp(d["timestamp"])
                delta = end - start

                lines.append(f"🔵 [c]{name}[/c] ({delta.microseconds // 1000} ms)")

        await data.reply("\n".join(lines))
