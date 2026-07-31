from dataclasses import dataclass
from os import getenv

@dataclass(frozen=True, slots=True)
class AppConfig:
    cooldown_seconds: float


def load_app_config() -> AppConfig:
    cooldown_seconds = int(getenv("COOLDOWN_SECONDS", "1"))
    if cooldown_seconds <= 0:
        raise ValueError("cooldown_seconds must be greater than 0")

    return AppConfig(cooldown_seconds=float(cooldown_seconds))
