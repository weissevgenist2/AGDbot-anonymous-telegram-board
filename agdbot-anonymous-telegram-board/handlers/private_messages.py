from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.types import Message

from context import AppContext
from filters.not_command import NotCommand
from services.hold_flow import hold_message_for_cooldown
from services.post_flow import publish_from_message

router = Router(name="private")


@router.message(F.chat.type == ChatType.PRIVATE, NotCommand())
async def handle_private_message(message: Message, ctx: AppContext) -> None:
    if message.from_user is None:
        return

    await ctx.subscribers.add(message.from_user.id)

    if ctx.cooldown.is_on_cooldown(message.from_user.id):
        await hold_message_for_cooldown(ctx, message)
        return

    await publish_from_message(ctx, message)
