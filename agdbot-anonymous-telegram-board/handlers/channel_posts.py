import logging

from aiogram import Router
from aiogram.types import Message

from context import AppContext

logger = logging.getLogger(__name__)

router = Router(name="channel")


@router.channel_post()
async def handle_channel_post(message: Message, ctx: AppContext) -> None:
    """
    Обрабатывает только посты,
    которые появились в канале НЕ через PostFlow.

    Если сообщение уже было опубликовано ботом,
    Broadcaster его уже разослал.
    """

    author = await ctx.post_tracker.pop_author(message.message_id)

    if author is not None:
        return

    await ctx.broadcaster.broadcast_channel_post(
        message.message_id,
    )