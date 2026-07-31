import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config.app_config import load_app_config
from config.settings import load_settings
from context import AppContext
from handlers import setup_routers
from middlewares.mw_context import ContextMiddleware
from services.broadcaster import Broadcaster
from services.cooldown import CooldownService
from services.publisher import Publisher
from storage.held_messages import InMemoryHeldMessageStore
from storage.memory import InMemoryPostTracker, InMemorySubscriberStore

logger = logging.getLogger(__name__)


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def create_app_context(settings=None, app_config=None) -> AppContext:
    if settings is None:
        settings = load_settings()
    if app_config is None:
        app_config = load_app_config()

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    subscribers = InMemorySubscriberStore()
    post_tracker = InMemoryPostTracker()
    held_messages = InMemoryHeldMessageStore()
    publisher = Publisher(bot, settings.channel_id, post_tracker)
    broadcaster = Broadcaster(bot, settings.channel_id, subscribers, post_tracker)
    cooldown = CooldownService(app_config.cooldown_seconds)

    return AppContext(
        settings=settings,
        app_config=app_config,
        bot=bot,
        publisher=publisher,
        broadcaster=broadcaster,
        subscribers=subscribers,
        post_tracker=post_tracker,
        cooldown=cooldown,
        held_messages=held_messages,
    )


async def run_bot() -> None:
    configure_logging()
    ctx = create_app_context()
    dispatcher = Dispatcher()
    dispatcher.update.middleware(ContextMiddleware(ctx))
    dispatcher.include_router(setup_routers())

    logger.info(
        "Starting bot, channel_id=%s, cooldown_seconds=%s",
        ctx.settings.channel_id,
        ctx.app_config.cooldown_seconds,
    )
    await dispatcher.start_polling(
        ctx.bot,
        allowed_updates=dispatcher.resolve_used_update_types(),
    )


def main() -> None:
    asyncio.run(run_bot())
