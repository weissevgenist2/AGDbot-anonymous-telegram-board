import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery

from context import AppContext
from service_messages.keyboards import CALLBACK_PREFIX
from services.hold_flow import refresh_cooldown_hold_message
from services.post_flow import publish_user_message

logger = logging.getLogger(__name__)

router = Router(name="cooldown_callbacks")


def _extract_hold_id(callback: CallbackQuery, action: str) -> str | None:
    if callback.data is None:
        return None

    prefix = f"{CALLBACK_PREFIX}:{action}:"
    if not callback.data.startswith(prefix):
        return None
    return callback.data.removeprefix(prefix)


async def _get_owned_hold(ctx: AppContext, callback: CallbackQuery, hold_id: str):
    if callback.from_user is None:
        return None

    held = await ctx.held_messages.get(hold_id)
    if held is None or held.user_id != callback.from_user.id:
        await callback.answer("Сообщение не найдено или уже обработано.", show_alert=True)
        return None

    return held


@router.callback_query(F.data.startswith(f"{CALLBACK_PREFIX}:cancel:"))
async def cancel_held_message(callback: CallbackQuery, ctx: AppContext) -> None:
    hold_id = _extract_hold_id(callback, "cancel")
    if hold_id is None:
        await callback.answer()
        return

    held = await _get_owned_hold(ctx, callback, hold_id)
    if held is None:
        return

    await ctx.publisher.delete_user_message(chat_id=held.chat_id, message_id=held.message_id)
    if held.service_message_id is not None:
        await ctx.bot.delete_message(chat_id=held.chat_id, message_id=held.service_message_id)

    await ctx.held_messages.remove(hold_id)
    await callback.answer("Отменено")


@router.callback_query(F.data.startswith(f"{CALLBACK_PREFIX}:send:"))
async def resend_held_message(callback: CallbackQuery, ctx: AppContext) -> None:
    hold_id = _extract_hold_id(callback, "send")
    if hold_id is None:
        await callback.answer()
        return

    held = await _get_owned_hold(ctx, callback, hold_id)
    if held is None:
        return

    if ctx.cooldown.is_on_cooldown(held.user_id):
        await refresh_cooldown_hold_message(ctx, hold_id=hold_id)
        await callback.answer("Вы слишком быстро постите.", show_alert=True)
        return

    await publish_user_message(
        ctx,
        chat_id=held.chat_id,
        message_id=held.message_id,
        author_id=held.user_id,
        forwarded=held.is_forwarded,
    )

    if held.service_message_id is not None:
        await ctx.bot.delete_message(chat_id=held.chat_id, message_id=held.service_message_id)

    await ctx.held_messages.remove(hold_id)
    await callback.answer("Отправлено")
