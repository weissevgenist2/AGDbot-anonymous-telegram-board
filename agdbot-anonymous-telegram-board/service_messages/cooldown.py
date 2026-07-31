from aiogram import Bot
from aiogram.types import Message

from service_messages.keyboards import cooldown_hold_keyboard
from service_messages.texts import COOLDOWN_HOLD_TEXT


async def send_cooldown_hold_message(
    bot: Bot,
    *,
    reply_to_message: Message,
    hold_id: str,
) -> Message:
    return await bot.send_message(
        chat_id=reply_to_message.chat.id,
        text=COOLDOWN_HOLD_TEXT,
        reply_to_message_id=reply_to_message.message_id,
        reply_markup=cooldown_hold_keyboard(hold_id),
    )
