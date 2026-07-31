from aiogram.types import Message

from context import AppContext
from service_messages.cooldown import send_cooldown_hold_message
from service_messages.keyboards import cooldown_hold_keyboard
from service_messages.texts import COOLDOWN_HOLD_TEXT
from utils.message import is_forwarded
from utils.ids import new_hold_id


async def hold_message_for_cooldown(ctx: AppContext, message: Message) -> None:
    if message.from_user is None:
        return

    hold_id = new_hold_id()
    await ctx.held_messages.create(
        hold_id=hold_id,
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        message_id=message.message_id,
        is_forwarded=is_forwarded(message),
    )

    service_message = await send_cooldown_hold_message(
        ctx.bot,
        reply_to_message=message,
        hold_id=hold_id,
    )
    await ctx.held_messages.set_service_message_id(hold_id, service_message.message_id)


async def refresh_cooldown_hold_message(ctx: AppContext, *, hold_id: str) -> None:
    held = await ctx.held_messages.get(hold_id)
    if held is None or held.service_message_id is None:
        return

    await ctx.bot.delete_message(chat_id=held.chat_id, message_id=held.service_message_id)

    service_message = await ctx.bot.send_message(
        chat_id=held.chat_id,
        text=COOLDOWN_HOLD_TEXT,
        reply_to_message_id=held.message_id,
        reply_markup=cooldown_hold_keyboard(hold_id),
    )
    await ctx.held_messages.set_service_message_id(hold_id, service_message.message_id)
