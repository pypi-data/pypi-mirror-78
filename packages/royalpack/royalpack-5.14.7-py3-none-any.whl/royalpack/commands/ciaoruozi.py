from typing import *
import telegram
import royalnet.commands as rc
import royalnet.serf.telegram as rst


class CiaoruoziCommand(rc.Command):
    name: str = "ciaoruozi"

    description: str = "Saluta Ruozi, un leggendario essere che è tornato in Royal Games."

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        if isinstance(self.serf, rst.TelegramSerf):
            user: telegram.User = data.message.from_user
            # Se sei Ruozi, salutati da solo!
            if user.id == 112437036:
                await data.reply("👋 Ciao me!")
                return
        await data.reply("👋 Ciao Ruozi!")
