import royalnet.utils as ru
import royalnet.constellation.api as rca


class ApiDiscordCvStar(rca.ApiStar):
    path = "/api/discord/cv/v1"

    tags = ["discord"]

    @rca.magic
    async def get(self, data: rca.ApiData) -> ru.JSON:
        """Get the members status of a single Discord guild.

        Equivalent to calling /cv in a chat."""
        response = await self.constellation.call_herald_event("discord", "discord_cv")
        return response
