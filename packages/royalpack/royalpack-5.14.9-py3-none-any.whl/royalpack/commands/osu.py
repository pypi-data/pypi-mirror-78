from typing import *
import itsdangerous
import aiohttp

from royalnet.backpack import tables as rbt
import royalnet.commands as rc
import royalnet.utils as ru

from .abstract.linker import LinkerCommand
from ..tables import Osu
from ..stars.api_auth_login_osu import ApiAuthLoginOsuStar


class OsuCommand(LinkerCommand):
    name = "osu"

    description = "Connetti e sincronizza il tuo account di osu!"

    @property
    def client_id(self):
        return self.config[self.name]['client_id']

    @property
    def client_secret(self):
        return self.config[self.name]['client_secret']

    @property
    def base_url(self):
        return self.config['base_url']

    @property
    def secret_key(self):
        return self.config['secret_key']

    async def get_updatables_of_user(self, session, user: rbt.User) -> List[Osu]:
        return user.osu

    async def get_updatables(self, session) -> List[Osu]:
        return await ru.asyncify(session.query(self.alchemy.get(Osu)).all)

    async def create(self,
                     session,
                     user: rbt.User,
                     args: rc.CommandArgs,
                     data: Optional[rc.CommandData] = None) -> Optional[Osu]:
        serializer = itsdangerous.URLSafeSerializer(self.secret_key, salt="osu")
        # TODO: Ensure the chat the link is being sent in is secure!!!
        await data.reply("🔑 [b]Login necessario[/b]\n"
                         f"[url=https://osu.ppy.sh/oauth/authorize"
                         f"?client_id={self.client_id}"
                         f"&redirect_uri={self.base_url}{ApiAuthLoginOsuStar.path}"
                         f"&response_type=code"
                         f"&state={serializer.dumps(user.uid)}]"
                         f"Connetti account di osu! a {user.username}"
                         f"[/url]")
        return None

    async def update(self, session, obj: Osu, change: Callable[[str, Any], Awaitable[None]]):
        await obj.refresh_if_expired(client_id=self.client_id,
                                     client_secret=self.client_secret)
        async with aiohttp.ClientSession(headers={"Authorization": f"Bearer {obj.access_token}"}) as session:
            async with session.get("https://osu.ppy.sh/api/v2/me/osu") as response:
                m = await response.json()
                obj.avatar_url = m.get("avatar_url")
                obj.username = m["username"]
                if "statistics" in m:
                    await change("standard_pp", m["statistics"].get("pp"))
            async with session.get("https://osu.ppy.sh/api/v2/me/taiko") as response:
                m = await response.json()
                if "statistics" in m:
                    await change("taiko_pp", m["statistics"].get("pp"))
            async with session.get("https://osu.ppy.sh/api/v2/me/fruits") as response:
                m = await response.json()
                if "statistics" in m:
                    await change("catch_pp", m["statistics"].get("pp"))
            async with session.get("https://osu.ppy.sh/api/v2/me/mania") as response:
                m = await response.json()
                if "statistics" in m:
                    await change("mania_pp", m["statistics"].get("pp"))

    async def on_increase(self, session, obj: Osu, attribute: str, old: Any, new: Any) -> None:
        if attribute == "standard_pp":
            await self.notify(f"📈 [b]{obj.user}[/b] è salito a [b]{new:.0f}pp[/b] su [i]osu![/i]! Congratulazioni!")
        elif attribute == "taiko_pp":
            await self.notify(f"📈 [b]{obj.user}[/b] è salito a [b]{new:.0f}pp[/b] su [i]osu!taiko[/i]! Congratulazioni!")
        elif attribute == "catch_pp":
            await self.notify(f"📈 [b]{obj.user}[/b] è salito a [b]{new:.0f}pp[/b] su [i]osu!catch[/i]! Congratulazioni!")
        elif attribute == "mania_pp":
            await self.notify(f"📈 [b]{obj.user}[/b] è salito a [b]{new:.0f}pp[/b] su [i]osu!mania[/i]! Congratulazioni!")

    async def on_unchanged(self, session, obj: Osu, attribute: str, old: Any, new: Any) -> None:
        pass

    async def on_decrease(self, session, obj: Osu, attribute: str, old: Any, new: Any) -> None:
        if attribute == "standard_pp":
            await self.notify(f"📉 [b]{obj.user}[/b] è sceso a [b]{new:.0f}pp[/b] su [i]osu![/i].")
        elif attribute == "taiko_pp":
            await self.notify(f"📉 [b]{obj.user}[/b] è sceso a [b]{new:.0f}pp[/b] su [i]osu!taiko[/i].")
        elif attribute == "catch_pp":
            await self.notify(f"📉 [b]{obj.user}[/b] è sceso a [b]{new:.0f}pp[/b] su [i]osu!catch[/i].")
        elif attribute == "mania_pp":
            await self.notify(f"📉 [b]{obj.user}[/b] è sceso a [b]{new:.0f}pp[/b] su [i]osu!mania[/i].")

    async def on_first(self, session, obj: Osu, attribute: str, old: None, new: Any) -> None:
        if attribute == "standard_pp":
            await self.notify(f"⭐️ [b]{obj.user}[/b] ha guadagnato i suoi primi [b]{new:.0f}pp[/b] su [i]osu![/i]!")
        elif attribute == "taiko_pp":
            await self.notify(f"⭐️ [b]{obj.user}[/b] ha guadagnato i suoi primi [b]{new:.0f}pp[/b] su [i]osu!taiko[/i]!")
        elif attribute == "catch_pp":
            await self.notify(f"⭐️ [b]{obj.user}[/b] ha guadagnato i suoi primi [b]{new:.0f}pp[/b] su [i]osu!catch[/i]!")
        elif attribute == "mania_pp":
            await self.notify(f"⭐️ [b]{obj.user}[/b] ha guadagnato i suoi primi [b]{new:.0f}pp[/b] su [i]osu!mania[/i]!")

    async def on_reset(self, session, obj: Osu, attribute: str, old: Any, new: None) -> None:
        if attribute == "standard_pp":
            await self.notify(f"⬜️ [b]{obj.user}[/b] non è più classificato su [i]osu![/i].")
        elif attribute == "taiko_pp":
            await self.notify(f"⬜️ [b]{obj.user}[/b] non è più classificato su [i]osu!taiko[/i].")
        elif attribute == "catch_pp":
            await self.notify(f"⬜️ [b]{obj.user}[/b] non è più classificato su [i]osu!catch[/i].")
        elif attribute == "mania_pp":
            await self.notify(f"⬜️ [b]{obj.user}[/b] non è più classificato su [i]osu!mania[/i].")

    def describe(self, obj: Osu) -> str:
        message = [
            f"ℹ️ [url=https://osu.ppy.sh/users/{obj.osu_id}]{obj.username}[/url]",
            f"osu!: [b]{obj.standard_pp:.0f}pp[/b]",
            f"osu!taiko: [b]{obj.taiko_pp:.0f}pp[/b]",
            f"osu!catch: [b]{obj.catch_pp:.0f}pp[/b]",
            f"osu!mania: [b]{obj.mania_pp:.0f}pp[/b]",
        ]
        return "\n".join(message)
