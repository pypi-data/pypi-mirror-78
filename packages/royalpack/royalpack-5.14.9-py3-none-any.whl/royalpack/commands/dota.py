from typing import *
import logging
import aiohttp
import royalnet.commands as rc
import royalnet.utils as ru
from royalnet.backpack import tables as rbt
from .abstract.linker import LinkerCommand

from ..tables import Steam, Dota
from ..types import DotaRank

log = logging.getLogger(__name__)


class DotaCommand(LinkerCommand):
    name: str = "dota"

    aliases = ["dota2", "doto", "doto2", "dotka", "dotka2"]

    description: str = "Visualizza le tue statistiche di Dota."

    syntax: str = ""

    def describe(self, obj: Steam) -> str:
        string = f"ℹ️ [b]{obj.persona_name}[/b]\n"
        if obj.dota.rank:
            string += f"{obj.dota.rank}\n"
        string += f"\n" \
                  f"Wins: [b]{obj.dota.wins}[/b]\n" \
                  f"Losses: [b]{obj.dota.losses}[/b]\n" \
                  f"\n"
        return string

    async def get_updatables_of_user(self, session, user: rbt.User) -> List[Dota]:
        return user.steam

    async def get_updatables(self, session) -> List[Dota]:
        return await ru.asyncify(session.query(self.alchemy.get(Steam)).all)

    async def create(self,
                     session,
                     user: rbt.User,
                     args: rc.CommandArgs,
                     data: Optional[rc.CommandData] = None) -> Optional[Dota]:
        raise rc.InvalidInputError("Dota accounts are automatically linked from Steam.")

    async def update(self, session, obj: Steam, change: Callable[[str, Any], Awaitable[None]]):
        log.debug(f"Getting player data from OpenDota...")
        async with aiohttp.ClientSession() as hcs:
            # Get profile data
            async with hcs.get(f"https://api.opendota.com/api/players/{obj.steamid.as_32}/") as response:
                if response.status != 200:
                    raise rc.ExternalError(f"OpenDota / returned {response.status}!")
                p = await response.json()
                # No such user
                if "profile" not in p:
                    log.debug(f"Not found: {obj}")
                    return
            # Get win/loss data
            async with hcs.get(f"https://api.opendota.com/api/players/{obj.steamid.as_32}/wl") as response:
                if response.status != 200:
                    raise rc.ExternalError(f"OpenDota /wl returned {response.status}!")
                wl = await response.json()
                # No such user
                if wl["win"] == 0 and wl["lose"] == 0:
                    log.debug(f"Not found: {obj}")
                    return
        # Find the Dota record, if it exists
        dota: Dota = obj.dota
        if dota is None:
            # Autocreate the Dota record
            dota = self.alchemy.get(Dota)(steam=obj)
            session.add(dota)
            session.flush()

        # Make a custom change function
        async def change(attribute: str, new: Any):
            await self._change(session=session, obj=dota, attribute=attribute, new=new)

        await change("wins", wl["win"])
        await change("losses", wl["lose"])
        if p["rank_tier"]:
            await change("rank", DotaRank(rank_tier=p["rank_tier"]))
        else:
            await change("rank", None)

    async def on_increase(self, session, obj: Dota, attribute: str, old: Any, new: Any) -> None:
        if attribute == "rank":
            await self.notify(f"📈 [b]{obj.steam.user}[/b] è salito a [b]{new}[/b] su Dota 2! Congratulazioni!")

    async def on_unchanged(self, session, obj: Dota, attribute: str, old: Any, new: Any) -> None:
        pass

    async def on_decrease(self, session, obj: Dota, attribute: str, old: Any, new: Any) -> None:
        if attribute == "rank":
            await self.notify(f"📉 [b]{obj.steam.user}[/b] è sceso a [b]{new}[/b] su Dota 2.")

    async def on_first(self, session, obj: Dota, attribute: str, old: None, new: Any) -> None:
        if attribute == "wins":
            await self.notify(f"↔️ Account {obj} connesso a {obj.steam.user}!")
        elif attribute == "rank":
            await self.notify(f"🌟 [b]{obj.steam.user}[/b] si è classificato [b]{new}[/b] su Dota 2!")

    async def on_reset(self, session, obj: Dota, attribute: str, old: Any, new: None) -> None:
        if attribute == "rank":
            await self.notify(f"⬜️ [b]{obj.steam.user}[/b] non ha più un rank su Dota 2.")
