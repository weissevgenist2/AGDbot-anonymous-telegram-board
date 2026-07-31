from aiogram.types import Message

from context import AppContext
from utils.message import is_forwarded


async def publish_user_message(
    ctx: AppContext,
    *,
    chat_id: int,
    message_id: int,
    author_id: int,
    forwarded: bool,
) -> None:
    if forwarded:
        channel_message = await ctx.publisher.publish_forwarded_by_id(
            chat_id=chat_id,
            message_id=message_id,
            author_id=author_id,
        )
    else:
        channel_message = await ctx.publisher.publish_anonymously_by_id(
            chat_id=chat_id,
            message_id=message_id,
            author_id=author_id,
        )

    # Удаляем оригинал из ЛС
    await ctx.publisher.delete_user_message(
        chat_id=chat_id,
        message_id=message_id,
    )

    # Возвращаем пользователю форвард из канала
    await ctx.publisher.forward_from_channel(
        chat_id=chat_id,
        channel_message_id=channel_message.message_id,
    )

    # СРАЗУ рассылаем всем подписчикам
    await ctx.broadcaster.broadcast_channel_post(
        channel_message.message_id,
    )

    ctx.cooldown.mark_posted(author_id)


async def publish_from_message(ctx: AppContext, message: Message) -> None:
    if message.from_user is None:
        return

    await publish_user_message(
        ctx,
        chat_id=message.chat.id,
        message_id=message.message_id,
        author_id=message.from_user.id,
        forwarded=is_forwarded(message),
    )