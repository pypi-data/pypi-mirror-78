from typing import *
import riotwatcher
import logging
import asyncio
import sentry_sdk
import royalnet.commands as rc
import royalnet.utils as ru
import royalnet.serf.telegram as rst
from royalnet.backpack import tables as rbt

from .abstract.linker import LinkerCommand
from ..tables import LeagueOfLegends, FiorygiTransaction
from ..types import LeagueLeague, Updatable

log = logging.getLogger(__name__)


class LeagueoflegendsCommand(LinkerCommand):
    name: str = "leagueoflegends"

    aliases = ["lol", "league"]

    description: str = "Connetti un account di League of Legends a un account Royalnet, o visualizzane le statistiche."

    syntax = "[nomeevocatore]"

    queue_names = {
        "rank_soloq": "Solo/Duo",
        "rank_flexq": "Flex",
    }

    def __init__(self, serf, config):
        super().__init__(serf, config)
        self._lolwatcher: Optional[riotwatcher.RiotWatcher] = None
        self._tftwatcher: Optional[riotwatcher.RiotWatcher] = None
        if self.enabled():
            self._lolwatcher = riotwatcher.LolWatcher(api_key=self.token())
            self._tftwatcher = riotwatcher.TftWatcher(api_key=self.token())

    def token(self):
        return self.config["leagueoflegends"]["token"]

    def region(self):
        return self.config["leagueoflegends"]["region"]

    def describe(self, obj: LeagueOfLegends) -> str:
        string = f"ℹ️ [b]{obj.summoner_name}[/b]\n" \
                 f"Lv. {obj.summoner_level}\n" \
                 f"Mastery score: {obj.mastery_score}\n" \
                 f"\n"
        if obj.rank_soloq:
            string += f"Solo: {obj.rank_soloq}\n"
        if obj.rank_flexq:
            string += f"Flex: {obj.rank_flexq}\n"
        return string

    async def get_updatables_of_user(self, session, user: rbt.User) -> List[LeagueOfLegends]:
        return await ru.asyncify(session.query(self.alchemy.get(LeagueOfLegends)).filter_by(user=user).all)

    async def get_updatables(self, session) -> List[LeagueOfLegends]:
        return await ru.asyncify(session.query(self.alchemy.get(LeagueOfLegends)).all)

    async def create(self,
                     session,
                     user: rbt.User,
                     args: rc.CommandArgs,
                     data: Optional[rc.CommandData] = None) -> Optional[LeagueOfLegends]:
        name = args.joined()

        # Connect a new League of Legends account to Royalnet
        log.debug(f"Searching for: {name}")
        summoner = self._lolwatcher.summoner.by_name(region=self.region(), summoner_name=name)
        # Ensure the account isn't already connected to something else
        leagueoflegends = await ru.asyncify(
            session.query(self.alchemy.get(LeagueOfLegends)).filter_by(summoner_id=summoner["id"]).one_or_none)
        if leagueoflegends:
            raise rc.CommandError(f"L'account {leagueoflegends} è già registrato su Royalnet.")
        # Get rank information
        log.debug(f"Getting leagues data: {name}")
        leagues = self._lolwatcher.league.by_summoner(region=self.region(),
                                                      encrypted_summoner_id=summoner["id"])
        soloq = LeagueLeague()
        flexq = LeagueLeague()
        twtrq = LeagueLeague()
        tftq = LeagueLeague()
        for league in leagues:
            if league["queueType"] == "RANKED_SOLO_5x5":
                soloq = LeagueLeague.from_dict(league)
            if league["queueType"] == "RANKED_FLEX_SR":
                flexq = LeagueLeague.from_dict(league)
            if league["queueType"] == "RANKED_FLEX_TT":
                twtrq = LeagueLeague.from_dict(league)
            if league["queueType"] == "RANKED_TFT":
                tftq = LeagueLeague.from_dict(league)
        # Get mastery score
        log.debug(f"Getting mastery data: {name}")
        mastery = self._lolwatcher.champion_mastery.scores_by_summoner(region=self.region(),
                                                                       encrypted_summoner_id=summoner["id"])
        # Create database row
        leagueoflegends = self.alchemy.get(LeagueOfLegends)(
            region=self.region(),
            user=user,
            profile_icon_id=summoner["profileIconId"],
            summoner_name=summoner["name"],
            puuid=summoner["puuid"],
            summoner_level=summoner["summonerLevel"],
            summoner_id=summoner["id"],
            account_id=summoner["accountId"],
            rank_soloq=soloq,
            rank_flexq=flexq,
            rank_twtrq=twtrq,
            rank_tftq=tftq,
            mastery_score=mastery
        )

        await FiorygiTransaction.spawn_fiorygi(
            data=data,
            session=session,
            user=user,
            qty=1,
            reason="aver collegato a Royalnet il proprio account di League of Legends"
        )

        session.add(leagueoflegends)
        return leagueoflegends

    async def update(self, session, obj: LeagueOfLegends, change: Callable[[str, Any], Awaitable[None]]):
        log.debug(f"Getting summoner data: {obj}")
        summoner = await ru.asyncify(self._lolwatcher.summoner.by_id, region=self.region(),
                                     encrypted_summoner_id=obj.summoner_id)
        await change("profile_icon_id", summoner["profileIconId"])
        await change("summoner_name", summoner["name"])
        await change("puuid", summoner["puuid"])
        await change("summoner_level", summoner["summonerLevel"])
        await change("summoner_id", summoner["id"])
        await change("account_id", summoner["accountId"])
        log.debug(f"Getting leagues data: {obj}")
        leagues = await ru.asyncify(self._lolwatcher.league.by_summoner, region=self.region(),
                                    encrypted_summoner_id=obj.summoner_id)
        soloq = LeagueLeague()
        flexq = LeagueLeague()
        for league in leagues:
            if league["queueType"] == "RANKED_SOLO_5x5":
                soloq = LeagueLeague.from_dict(league)
            if league["queueType"] == "RANKED_FLEX_SR":
                flexq = LeagueLeague.from_dict(league)
        await change("rank_soloq", soloq)
        await change("rank_flexq", flexq)
        log.debug(f"Getting mastery data: {obj}")
        mastery = await ru.asyncify(self._lolwatcher.champion_mastery.scores_by_summoner,
                                    region=self.region(),
                                    encrypted_summoner_id=obj.summoner_id)
        await change("mastery_score", mastery)

    async def on_increase(self, session, obj: LeagueOfLegends, attribute: str, old: Any, new: Any) -> None:
        if attribute in self.queue_names.keys():
            await self.notify(f"📈 [b]{obj.user}[/b] è salito a {new} su League of Legends ({self.queue_names[attribute]})! Congratulazioni!")

    async def on_unchanged(self, session, obj: LeagueOfLegends, attribute: str, old: Any, new: Any) -> None:
        pass

    async def on_decrease(self, session, obj: LeagueOfLegends, attribute: str, old: Any, new: Any) -> None:
        if attribute in self.queue_names.keys():
            await self.notify(f"📉 [b]{obj.user}[/b] è sceso a {new} su League of Legends ({self.queue_names[attribute]}).")

    async def on_first(self, session, obj: LeagueOfLegends, attribute: str, old: None, new: Any) -> None:
        if attribute in self.queue_names.keys():
            await self.notify(f"🌟 [b]{obj.user}[/b] si è classificato {new} su League of Legends ({self.queue_names[attribute]}!")

    async def on_reset(self, session, obj: LeagueOfLegends, attribute: str, old: Any, new: None) -> None:
        if attribute in self.queue_names.keys():
            await self.notify(f"⬜️ [b]{obj.user}[/b] non ha più un rank su League of Legends ({self.queue_names[attribute]}).")
