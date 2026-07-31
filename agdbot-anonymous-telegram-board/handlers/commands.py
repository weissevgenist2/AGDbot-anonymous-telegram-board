from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.types import Message

from context import AppContext

router = Router(name="commands")


@router.message(CommandStart(), F.chat.type == ChatType.PRIVATE)
async def cmd_start(message: Message, ctx: AppContext) -> None:
    await ctx.subscribers.add(message.from_user.id) # type: ignore
    await message.answer(
        "Добро пожаловать в АГД.\n\n"
        "Отправьте сообщение — оно появится в канале анонимно.\n"
        "Все новые посты из канала будут приходить сюда."
    )
