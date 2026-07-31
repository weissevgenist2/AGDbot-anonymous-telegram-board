from aiogram.filters import BaseFilter
from aiogram.types import Message


class NotCommand(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text is None:
            return True
        return not message.text.startswith("/")
