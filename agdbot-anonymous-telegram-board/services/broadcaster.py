import logging

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError

from storage.protocols import PostTracker, SubscriberStore

logger = logging.getLogger(__name__)


class Broadcaster:
    """Delivers new channel posts to all subscribed users."""

    def __init__(
        self,
        bot: Bot,
        channel_id: int,
        subscribers: SubscriberStore,
        post_tracker: PostTracker,
    ) -> None:
        self._bot = bot
        self._channel_id = channel_id
        self._subscribers = subscribers
        self._post_tracker = post_tracker

    async def broadcast_channel_post(self, channel_message_id: int) -> None:
        author_id = await self._post_tracker.pop_author(channel_message_id)
        subscribers = await self._subscribers.get_all()

        for user_id in subscribers:
            if author_id is not None and user_id == author_id:
                continue

            try:
                await self._bot.forward_message(
                    chat_id=user_id,
                    from_chat_id=self._channel_id,
                    message_id=channel_message_id,
                )
            except TelegramForbiddenError:
                logger.warning("User %s blocked the bot, removing from subscribers", user_id)
                await self._subscribers.remove(user_id)
            except Exception:
                logger.exception("Failed to deliver channel post to user %s", user_id)
