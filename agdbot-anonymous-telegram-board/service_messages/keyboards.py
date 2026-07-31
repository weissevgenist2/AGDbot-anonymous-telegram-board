from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

CALLBACK_PREFIX = "cd"


def cooldown_hold_keyboard(hold_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅  Отправить заново",
                    callback_data=f"{CALLBACK_PREFIX}:send:{hold_id}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❌ Отменить",
                    callback_data=f"{CALLBACK_PREFIX}:cancel:{hold_id}",
                ),
            ],
        ]
    )
