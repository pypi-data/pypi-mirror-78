from typing import *
import steam.steamid
import steam.webapi
import datetime
import royalnet.commands as rc
import royalnet.utils as ru
import logging
from royalnet.backpack import tables as rbt

from .abstract.linker import LinkerCommand

from ..tables import Steam, FiorygiTransaction
from ..types import Updatable

log = logging.getLogger(__name__)


class SteampoweredCommand(LinkerCommand):
    name: str = "steampowered"

    description: str = "Connetti e visualizza informazioni sul tuo account di Steam!"

    syntax: str = "{url_profilo}"

    def __init__(self, serf, config):
        super().__init__(serf, config)
        self._api = steam.webapi.WebAPI(self.token())

    def token(self):
        return self.config["steampowered"]["token"]

    async def get_updatables_of_user(self, session, user: rbt.User) -> List[Steam]:
        return user.steam

    async def get_updatables(self, session) -> List[Steam]:
        return await ru.asyncify(session.query(self.alchemy.get(Steam)).all)

    async def create(self,
                     session,
                     user: rbt.User,
                     args: rc.CommandArgs,
                     data: Optional[rc.CommandData] = None) -> Optional[Steam]:
        url = args.joined()
        steamid64 = await self._call(steam.steamid.steam64_from_url, url)
        if steamid64 is None:
            raise rc.InvalidInputError("Quel link non è associato ad alcun account Steam.")
        response = await self._call(self._api.ISteamUser.GetPlayerSummaries_v2, steamids=steamid64)
        r = response["response"]["players"][0]
        steam_account = self.alchemy.get(Steam)(
            user=user,
            _steamid=int(steamid64),
            persona_name=r["personaname"],
            profile_url=r["profileurl"],
            avatar=r["avatarfull"],
            primary_clan_id=r["primaryclanid"],
            account_creation_date=datetime.datetime.fromtimestamp(r["timecreated"])
        )

        await FiorygiTransaction.spawn_fiorygi(
            user=user,
            qty=1,
            reason="aver collegato a Royalnet il proprio account di Steam",

            data=data,
            session=session,
        )

        session.add(steam_account)
        return steam_account

    async def update(self, session, obj: Steam, change: Callable[[str, Any], Awaitable[None]]):
        response = await self._call(self._api.ISteamUser.GetPlayerSummaries_v2, steamids=obj.steamid.as_64)
        r = response["response"]["players"][0]
        obj.persona_name = r["personaname"]
        obj.profile_url = r["profileurl"]
        obj.avatar = r["avatar"]
        obj.primary_clan_id = r["primaryclanid"]
        obj.account_creation_date = datetime.datetime.fromtimestamp(r["timecreated"])
        response = await self._call(self._api.IPlayerService.GetSteamLevel_v1, steamid=obj.steamid.as_64)
        obj.account_level = response["response"]["player_level"]
        response = await self._call(self._api.IPlayerService.GetOwnedGames_v1,
                                    steamid=obj.steamid.as_64,
                                    include_appinfo=False,
                                    include_played_free_games=True,
                                    include_free_sub=False,
                                    appids_filter=None)
        obj.owned_games_count = response["response"]["game_count"]
        if response["response"]["game_count"] >= 0:
            obj.most_played_game_2weeks = sorted(response["response"]["games"], key=lambda g: -g.get("playtime_2weeks", 0))[0]["appid"]
            obj.most_played_game_forever = sorted(response["response"]["games"], key=lambda g: -g.get("playtime_forever", 0))[0]["appid"]

    async def on_increase(self, session, obj: Updatable, attribute: str, old: Any, new: Any) -> None:
        pass

    async def on_unchanged(self, session, obj: Updatable, attribute: str, old: Any, new: Any) -> None:
        pass

    async def on_decrease(self, session, obj: Updatable, attribute: str, old: Any, new: Any) -> None:
        pass

    async def on_first(self, session, obj: Updatable, attribute: str, old: None, new: Any) -> None:
        pass

    async def on_reset(self, session, obj: Updatable, attribute: str, old: Any, new: None) -> None:
        pass

    def describe(self, obj: Steam):
        return f"ℹ️ [url={obj.profile_url}]{obj.persona_name}[/url]\n" \
               f"[b]Level {obj.account_level}[/b]\n" \
               f"\n" \
               f"Owned games: [b]{obj.owned_games_count}[/b]\n" \
               f"Most played 2 weeks: [url=https://store.steampowered.com/app/{obj.most_played_game_2weeks}]{obj.most_played_game_2weeks}[/url]\n" \
               f"Most played forever: [url=https://store.steampowered.com/app/{obj.most_played_game_forever}]{obj.most_played_game_forever}[/url]\n" \
               f"\n" \
               f"SteamID32: [c]{obj.steamid.as_32}[/c]\n" \
               f"SteamID64: [c]{obj.steamid.as_64}[/c]\n" \
               f"SteamID2: [c]{obj.steamid.as_steam2}[/c]\n" \
               f"SteamID3: [c]{obj.steamid.as_steam3}[/c]\n" \
               f"\n" \
               f"Created on: [b]{obj.account_creation_date}[/b]\n"

    async def _call(self, method, *args, **kwargs):
        log.debug(f"Calling {method}")
        try:
            return await ru.asyncify(method, *args, **kwargs)
        except Exception as e:
            raise rc.ExternalError("\n".join(e.args).replace(self.token(), "HIDDEN"))
