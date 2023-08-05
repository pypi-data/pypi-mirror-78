# Imports go here!
from .discord_cv import DiscordCvEvent
from .telegram_message import TelegramMessageEvent
from .pong import PongEvent

# Enter the commands of your Pack here!
available_events = [
    DiscordCvEvent,
    TelegramMessageEvent,
    PongEvent,
]

# Don't change this, it should automatically generate __all__
__all__ = [command.__name__ for command in available_events]
