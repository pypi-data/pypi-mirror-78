from typing import *
import royalnet
import royalnet.commands as rc


class HelpCommand(rc.Command):
    name: str = "help"

    description: str = "Visualizza informazioni su un comando."

    syntax: str = "{comando}"

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        if len(args) == 0:
            message = [
                "ℹ️ Comandi disponibili:"
            ]

            for command in sorted(list(set(self.serf.commands.values())), key=lambda c: c.name):
                message.append(f"- [c]{self.serf.prefix}{command.name}[/c]")

            await data.reply("\n".join(message))
        else:
            name: str = args[0].lstrip(self.serf.prefix)

            try:
                command: rc.Command = self.serf.commands[f"{self.serf.prefix}{name}"]
            except KeyError:
                raise rc.InvalidInputError("Il comando richiesto non esiste.")

            message = [
                f"ℹ️ [c]{self.serf.prefix}{command.name} {command.syntax}[/c]",
                "",
                f"{command.description}"
            ]

            await data.reply("\n".join(message))
