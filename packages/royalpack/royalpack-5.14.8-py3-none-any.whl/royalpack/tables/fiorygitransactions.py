from typing import *
import datetime

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr
import royalnet.utils as ru

from .fiorygi import Fiorygi

if TYPE_CHECKING:
    from royalnet.commands import CommandData


class FiorygiTransaction:
    __tablename__ = "fiorygitransactions"

    @declared_attr
    def id(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def change(self):
        return Column(Integer, nullable=False)

    @declared_attr
    def user_id(self):
        return Column(Integer, ForeignKey("fiorygi.user_id"), nullable=False)

    @declared_attr
    def wallet(self):
        return relationship("Fiorygi", backref=backref("transactions"))

    @property
    def user(self):
        return self.wallet.user

    @declared_attr
    def reason(self):
        return Column(String, nullable=False, default="")

    @declared_attr
    def timestamp(self):
        return Column(DateTime)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.change:+} to {self.user.username} for {self.reason}>"

    @classmethod
    async def spawn_fiorygi(cls, user, qty: int, reason: str, *, data: "CommandData", session):
        FiorygiT = data.alchemy.get(cls)
        FiorygiTransactionT = data.alchemy.get(FiorygiTransaction)

        if user.fiorygi is None:
            session.add(
                FiorygiT(
                    user_id=user.uid,
                    fiorygi=0
                )
            )
            await ru.asyncify(session.commit)

        session.add(
            FiorygiTransactionT(
                user_id=user.uid,
                change=qty,
                reason=reason,
                timestamp=datetime.datetime.now()
            )
        )

        user.fiorygi.fiorygi += qty
        await ru.asyncify(session.commit)

        if len(user.telegram) > 0:
            user_str = user.telegram[0].mention()
        else:
            user_str = user.username

        if qty > 0:
            msg = f"💰 [b]{user_str}[/b] ha ottenuto [b]{qty}[/b] fioryg{'i' if qty != 1 else ''} per [i]{reason}[/i]!"
        elif qty == 0:
            msg = f"❓ [b]{user_str}[/b] ha mantenuto i suoi fiorygi attuali per [i]{reason}[/i].\nWait, cosa?"
        else:
            msg = f"💸 [b]{user_str}[/b] ha perso [b]{-qty}[/b] fioryg{'i' if qty != -1 else ''} per [i]{reason}[/i]."

        await data.command.serf.call_herald_event(
            "telegram", "telegram_message",
            chat_id=data.command.config["Telegram"]["main_group_id"],
            text=msg)
