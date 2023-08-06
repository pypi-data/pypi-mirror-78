from typing import *
import dateparser
import datetime
import pickle
import telegram
import discord
from sqlalchemy import and_
import royalnet.commands as rc
import royalnet.utils as ru
import royalnet.serf.telegram as rst
import royalnet.serf.discord as rsd

from ..tables import Reminder


class ReminderCommand(rc.Command):
    name: str = "reminder"

    aliases = ["calendar"]

    description: str = "Ti ricorda di fare qualcosa dopo un po' di tempo."

    syntax: str = "[ {data} ] {messaggio}"

    def __init__(self, serf, config):
        super().__init__(serf, config)

        session = self.alchemy.Session()
        reminders = (
            session.query(self.alchemy.get(Reminder))
                   .filter(and_(
                       self.alchemy.get(Reminder).datetime >= datetime.datetime.now(),
                       self.alchemy.get(Reminder).interface_name == self.serf.interface_name))
                   .all()
        )
        for reminder in reminders:
            self.serf.tasks.add(self._remind(reminder))

    async def _remind(self, reminder):
        await ru.sleep_until(reminder.datetime)
        if isinstance(self.serf, rst.TelegramSerf):
            chat_id: int = pickle.loads(reminder.interface_data)
            client: telegram.Bot = self.serf.client
            await self.serf.api_call(client.send_message,
                                     chat_id=chat_id,
                                     text=rst.escape(f"❗️ {reminder.message}"),
                                     parse_mode="HTML",
                                     disable_web_page_preview=True)
        elif isinstance(self.serf, rsd.DiscordSerf):
            channel_id: int = pickle.loads(reminder.interface_data)
            client: discord.Client = self.serf.client
            channel = client.get_channel(channel_id)
            await channel.send(rsd.escape(f"❗️ {reminder.message}"))

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        try:
            date_str, reminder_text = args.match(r"\[\s*([^]]+)\s*]\s*([^\n]+)\s*")
        except rc.InvalidInputError:
            date_str, reminder_text = args.match(r"\s*(.+?)\s*\n\s*([^\n]+)\s*")

        try:
            date: Optional[datetime.datetime] = dateparser.parse(date_str, settings={
                "PREFER_DATES_FROM": "future"
            })
        except OverflowError:
            date = None
        if date is None:
            await data.reply("⚠️ La data che hai inserito non è valida.")
            return
        if date <= datetime.datetime.now():
            await data.reply("⚠️ La data che hai specificato è nel passato.")
            return
        await data.reply(f"✅ Promemoria impostato per [b]{date.strftime('%Y-%m-%d %H:%M:%S')}[/b]")
        if isinstance(self.serf, rst.TelegramSerf):
            interface_data = pickle.dumps(data.message.chat.id)
        elif isinstance(self.serf, rsd.DiscordSerf):
            interface_data = pickle.dumps(data.message.channel.id)
        else:
            raise rc.UnsupportedError("This command does not support the current interface.")
        async with data.session_acm() as session:
            creator = await data.find_author(session=session)
            reminder = self.alchemy.get(Reminder)(creator=creator,
                                                  interface_name=self.serf.interface_name,
                                                  interface_data=interface_data,
                                                  datetime=date,
                                                  message=reminder_text)
            self.serf.tasks.add(self._remind(reminder))
            session.add(reminder)
            await ru.asyncify(session.commit)
