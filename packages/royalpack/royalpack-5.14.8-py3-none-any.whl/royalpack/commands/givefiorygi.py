from typing import *
import royalnet.commands as rc
import royalnet.backpack.tables as rbt

from ..tables import FiorygiTransaction


class GivefiorygiCommand(rc.Command):
    name: str = "givefiorygi"

    description: str = "Cedi fiorygi a un altro utente."

    syntax: str = "{destinatario} {quantità} {motivo}"

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        async with data.session_acm() as session:
            author = await data.find_author(session=session, required=True)

            user_arg = args[0]
            qty_arg = args[1]

            if user_arg is None:
                raise rc.InvalidInputError("Non hai specificato un destinatario!")
            user = await rbt.User.find(alchemy=self.alchemy, session=session, identifier=user_arg)
            if user is None:
                raise rc.InvalidInputError("L'utente specificato non esiste!")
            if user.uid == author.uid:
                raise rc.InvalidInputError("Non puoi inviare fiorygi a te stesso!")

            if qty_arg is None:
                raise rc.InvalidInputError("Non hai specificato una quantità!")
            try:
                qty = int(qty_arg)
            except ValueError:
                raise rc.InvalidInputError("La quantità specificata non è un numero!")
            if qty <= 0:
                raise rc.InvalidInputError("La quantità specificata deve essere almeno 1!")

            if author.fiorygi.fiorygi < qty:
                raise rc.InvalidInputError("Non hai abbastanza fiorygi per effettuare la transazione!")

            await FiorygiTransaction.spawn_fiorygi(author, -qty, f"aver ceduto fiorygi a {user}",
                                                   data=data,
                                                   session=session)
            await FiorygiTransaction.spawn_fiorygi(user, qty, f"aver ricevuto fiorygi da {author}",
                                                   data=data,
                                                   session=session)
