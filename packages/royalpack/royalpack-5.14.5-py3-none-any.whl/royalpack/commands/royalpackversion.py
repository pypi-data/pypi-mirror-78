from typing import *

import functools
import pkg_resources
import royalnet.commands as rc


class RoyalpackCommand(rc.Command):
    name: str = "royalpackversion"

    description: str = "Visualizza la versione attuale di Royalpack."

    syntax: str = ""

    @property
    @functools.lru_cache(1)
    def royalpack_version(self) -> str:
        return pkg_resources.get_distribution("royalpack").version

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        message = f"ℹ️ Royalpack [url=https://github.com/Steffo99/royalpack/releases/tag/{self.royalpack_version}]{self.royalpack_version}[/url]\n"
        if "69" in self.royalpack_version:
            message += "(Nice.)"
        await data.reply(message)
