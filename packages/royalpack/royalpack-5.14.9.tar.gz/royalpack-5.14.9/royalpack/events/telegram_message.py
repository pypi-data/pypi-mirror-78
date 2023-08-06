import logging
import telegram
from typing import *
from royalnet.serf.telegram.telegramserf import TelegramSerf, escape
import royalnet.commands as rc


log = logging.getLogger(__name__)


class TelegramMessageEvent(rc.HeraldEvent):
    name = "telegram_message"

    async def run(self, chat_id, text, **kwargs) -> dict:
        if not isinstance(self.parent, TelegramSerf):
            raise rc.UnsupportedError()

        # noinspection PyTypeChecker
        serf: TelegramSerf = self.parent

        log.debug("Forwarding message from Herald to Telegram.")
        await serf.api_call(serf.client.send_message,
                            chat_id=chat_id,
                            text=escape(text),
                            parse_mode="HTML",
                            disable_web_page_preview=True)

        return {}
