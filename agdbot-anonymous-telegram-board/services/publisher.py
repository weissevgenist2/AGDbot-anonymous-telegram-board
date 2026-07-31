import logging

from aiogram import Bot
from aiogram.types import Message

from storage.protocols import PostTracker

logger = logging.getLogger(__name__)


class Publisher:
    """Publishes user messages to the anonymous board channel."""

    def __init__(self, bot: Bot, channel_id: int, post_tracker: PostTracker) -> None:
        self._bot = bot
        self._channel_id = channel_id
        self._post_tracker = post_tracker

    async def publish_anonymously(
        self,
        message: Message,
        *,
        author_id: int,
    ) -> Message:
        return await self.publish_anonymously_by_id(
            chat_id=message.chat.id,
            message_id=message.message_id,
            author_id=author_id,
        )

    async def publish_anonymously_by_id(
        self,
        *,
        chat_id: int,
        message_id: int,
        author_id: int,
    ) -> Message:
        channel_message = await self._bot.copy_message(
            chat_id=self._channel_id,
            from_chat_id=chat_id,
            message_id=message_id,
        )
        await self._post_tracker.mark_author_post(channel_message.message_id, author_id)

        logger.info(
            "Published anonymous message %s from chat %s to channel as %s",
            message_id,
            chat_id,
            channel_message.message_id,
        )
        return channel_message

    async def publish_forwarded(
        self,
        message: Message,
        *,
        author_id: int,
    ) -> Message:
        return await self.publish_forwarded_by_id(
            chat_id=message.chat.id,
            message_id=message.message_id,
            author_id=author_id,
        )

    async def publish_forwarded_by_id(
        self,
        *,
        chat_id: int,
        message_id: int,
        author_id: int,
    ) -> Message:
        channel_message = await self._bot.forward_message(
            chat_id=self._channel_id,
            from_chat_id=chat_id,
            message_id=message_id,
        )
        await self._post_tracker.mark_author_post(channel_message.message_id, author_id)

        logger.info(
            "Forwarded message %s from chat %s to channel as %s",
            message_id,
            chat_id,
            channel_message.message_id,
        )
        return channel_message

    async def replace_with_channel_forward(
        self,
        user_message: Message,
        channel_message: Message,
    ) -> Message:
        await user_message.delete()
        return await self.forward_from_channel(
            chat_id=user_message.chat.id,
            channel_message_id=channel_message.message_id,
        )

    async def forward_from_channel(self, *, chat_id: int, channel_message_id: int) -> Message:
        return await self._bot.forward_message(
            chat_id=chat_id,
            from_chat_id=self._channel_id,
            message_id=channel_message_id,
        )

    async def delete_user_message(self, *, chat_id: int, message_id: int) -> None:
        await self._bot.delete_message(chat_id=chat_id, message_id=message_id)
