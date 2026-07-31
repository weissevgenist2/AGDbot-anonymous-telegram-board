from dataclasses import dataclass

from aiogram import Bot

from config.app_config import AppConfig
from config.settings import Settings
from services.broadcaster import Broadcaster
from services.cooldown import CooldownService
from services.publisher import Publisher
from storage.held_messages import HeldMessageStore
from storage.protocols import PostTracker, SubscriberStore


@dataclass(slots=True)
class AppContext:
    settings: Settings
    app_config: AppConfig
    bot: Bot
    publisher: Publisher
    broadcaster: Broadcaster
    subscribers: SubscriberStore
    post_tracker: PostTracker
    cooldown: CooldownService
    held_messages: HeldMessageStore

