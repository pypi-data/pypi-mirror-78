from typing import *
import datetime
import re
import dateparser
import typing
import royalnet.utils as ru
import royalnet.commands as rc
import royalnet.serf.telegram as rst

from ..tables import MMEvent
from ..utils import MMTask


class MatchmakingCommand(rc.Command):
    name: str = "matchmaking"

    description: str = "Cerca persone per una partita a qualcosa!"

    syntax: str = ""

    aliases = ["mm", "lfg"]

    def __init__(self, serf, config):
        super().__init__(serf, config)

        # Find all active MMEvents and run the tasks for them
        session = self.alchemy.Session()

        # Create a new MMEvent and run it
        if isinstance(self.serf, rst.TelegramSerf):
            MMEventT = self.alchemy.get(MMEvent)
            active_mmevents = (
                session
                .query(MMEventT)
                .filter(
                    MMEventT.interface == self.serf.interface_name,
                    MMEventT.interrupted == False
                )
                .all()
            )
            for mmevent in active_mmevents:
                task = MMTask(mmevent.mmid, command=self)
                task.start()

    @staticmethod
    def _parse_args(args) -> Tuple[Optional[datetime.datetime], str, str]:
        """Parse command arguments, either using the standard syntax or the Proto syntax."""
        try:
            timestring, title, description = args.match(r"(?:\[\s*([^]]+)\s*]\s*)?([^\n]+)\s*\n?\s*(.+)?\s*", re.DOTALL)
        except rc.InvalidInputError:
            timestring, title, description = args.match(r"(?:\s*(.+?)\s*\n\s*)?([^\n]+)\s*\n?\s*(.+)?\s*", re.DOTALL)
        if timestring is not None:
            try:
                dt: typing.Optional[datetime.datetime] = dateparser.parse(timestring, settings={
                    "PREFER_DATES_FROM": "future"
                })
            except OverflowError:
                dt = None
            if dt is None:
                raise rc.InvalidInputError("La data che hai specificato non è valida.")
            if dt <= datetime.datetime.now():
                raise rc.InvalidInputError("La data che hai specificato è nel passato.")
            if dt - datetime.datetime.now() >= datetime.timedelta(days=366):
                raise rc.InvalidInputError("Hai specificato una data tra più di un anno!\n"
                                           "Se volevi scrivere un'orario, ricordati che le ore sono separate da "
                                           "due punti (:) e non da punto semplice!")
        else:
            dt = None
        return dt, title, description

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        """Handle a matchmaking command call."""

        # Parse the arguments, either with the standard syntax or with the Proto syntax
        dt, title, description = self._parse_args(args)

        # Add the MMEvent to the database
        async with data.session_acm() as session:
            author = await data.find_author(session=session, required=True)

            mmevent: MMEvent = self.alchemy.get(MMEvent)(creator=author,
                                                         datetime=dt,
                                                         title=title,
                                                         description=description,
                                                         interface=self.serf.interface_name)
            session.add(mmevent)
            await ru.asyncify(session.commit)

            # Create and run a task for the newly created MMEvent
            task = MMTask(mmevent.mmid, command=self)
            task.start()

        await data.reply(f"🚩 Matchmaking creato!")
