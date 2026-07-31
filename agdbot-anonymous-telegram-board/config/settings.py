from dataclasses import dataclass
from os import getenv

@dataclass(frozen=True, slots=True)
class Settings:
    bot_token: str
    channel_id: int


def load_settings() -> Settings:

    bot_token = getenv("BOT_TOKEN")
    channel_id_raw = getenv("CHANNEL_ID")

    if not bot_token:
        raise ValueError("BOT_TOKEN is not set in .env")
    if not channel_id_raw:
        raise ValueError("CHANNEL_ID is not set in .env")

    return Settings(
        bot_token=bot_token,
        channel_id=int(channel_id_raw),
    )
